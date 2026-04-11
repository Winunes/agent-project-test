# 检索服务（MVP：混合检索版）
# 目标：
# 1) 向量检索（pgvector）作为主通道
# 2) FTS 作为辅助通道
# 3) ILIKE 作为中文兜底
# 4) 最后用 RRF 融合，返回统一结果

# 哈希：用于构造稳定向量
import hashlib
# 数学：用于向量归一化
import math
# 正则：用于轻量分词/清洗
import re

# SQLAlchemy 查询函数
from sqlalchemy import desc, func, or_, select, text
# SQLAlchemy 异步会话
from sqlalchemy.ext.asyncio import AsyncSession

# ORM 模型
from app.models import DocumentChunk


# 工具函数：去重并保持原顺序
def _dedupe_keep_order(values: list[str]) -> list[str]:
    # 已见集合
    seen: set[str] = set()
    # 输出列表
    out: list[str] = []

    # 逐个处理
    for v in values:
        # 去空白
        x = (v or "").strip()
        # 跳过空值
        if not x:
            continue
        # 未出现则加入
        if x not in seen:
            seen.add(x)
            out.append(x)

    # 返回结果
    return out


# 轻量分词（与 ingest.py 保持一致）
def _tokenize_for_embedding(text_value: str) -> list[str]:
    # 标准化小写
    t = (text_value or "").strip().lower()
    # 空值直接返回
    if not t:
        return []

    # token 容器
    tokens: list[str] = []

    # 英文/数字连续串
    for w in re.findall(r"[a-z0-9]+", t):
        if w:
            tokens.append(w)

    # 中文按单字切（MVP 简化）
    for ch in t:
        if "\u4e00" <= ch <= "\u9fff":
            tokens.append(ch)

    # 返回 token
    return tokens


# 构造查询向量（与 ingest.py 保持一致，维度 1024）
def _build_embedding(text_value: str, dim: int = 1024) -> list[float]:
    # 初始化 0 向量
    vec = [0.0] * dim
    # 分词
    tokens = _tokenize_for_embedding(text_value)

    # 无 token 则直接返回
    if not tokens:
        return vec

    # 哈希桶计数
    for token in tokens:
        # 计算稳定哈希
        h = hashlib.md5(token.encode("utf-8")).hexdigest()
        # 映射桶位
        idx = int(h, 16) % dim
        # 计数 +1
        vec[idx] += 1.0

    # L2 归一化
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]

    # 返回向量
    return vec


# 转为 pgvector 字面量字符串
def _to_pgvector_literal(vec: list[float]) -> str:
    # 固定小数位，避免字符串过长
    return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"


# 提取 ILIKE 关键词（中文友好）
def _extract_terms(query: str) -> list[str]:
    # 清洗 query
    q = (query or "").strip()
    # 空查询返回空
    if not q:
        return []

    # 常见尾巴短语（会降低命中）
    suffixes = ["是什么", "是啥", "什么意思", "有哪些", "怎么做", "怎么", "如何", "请问"]

    # 候选词先放原句
    candidates: list[str] = [q]

    # 去尾巴版本（如：退款规则是什么 -> 退款规则）
    for suf in suffixes:
        if q.endswith(suf):
            trimmed = q[: -len(suf)].strip(" ，。！？?!.")
            if len(trimmed) >= 2:
                candidates.append(trimmed)

    # 轻量按标点切分
    cleaned = re.sub(r"[，。！？、,.;；:：()\[\]{}\"'`]+", " ", q)
    for part in cleaned.split():
        p = part.strip()
        if len(p) >= 2:
            candidates.append(p)

    # 去重并返回
    return _dedupe_keep_order(candidates)


# 向量检索
async def _search_by_vector(
    db: AsyncSession,
    query: str,
    limit: int,
) -> list[dict]:
    # 构造查询向量
    query_vec = _build_embedding(query, dim=1024)
    # 转 pgvector 字面量
    embedding_literal = _to_pgvector_literal(query_vec)

    # 原生 SQL：按余弦距离排序，取最相近
    stmt = text(
        """
        SELECT
            id,
            document_pk,
            chunk_text,
            (1 - (embedding <=> CAST(:embedding AS vector))) AS score
        FROM document_chunks
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
        """
    )

    # 执行查询
    result = await db.execute(
        stmt,
        {
            "embedding": embedding_literal,
            "limit": limit,
        },
    )

    # 读取映射结果
    rows = result.mappings().all()

    # 标准化输出
    return [
        {
            "chunk_id": str(row["id"]),
            "content": row["chunk_text"],
            "score": float(row["score"]) if row["score"] is not None else 0.0,
            "metadata": {
                "document_pk": str(row["document_pk"]),
                "match_type": "vector",
            },
        }
        for row in rows
    ]


# FTS 检索
async def _search_by_fts(
    db: AsyncSession,
    query: str,
    limit: int,
) -> list[dict]:
    # 去空白
    q = (query or "").strip()
    # 空查询直接空
    if not q:
        return []

    # 构造 tsquery
    ts_query = func.websearch_to_tsquery("simple", q)
    # 构造 tsvector
    ts_vector = func.to_tsvector("simple", DocumentChunk.chunk_text)
    # 相关性分数
    rank = func.ts_rank_cd(ts_vector, ts_query)

    # 语句：命中 + 按 rank 排序
    stmt = (
        select(DocumentChunk, rank.label("rank"))
        .where(ts_vector.op("@@")(ts_query))
        .order_by(desc("rank"), DocumentChunk.created_at.desc())
        .limit(limit)
    )

    # 执行
    result = await db.execute(stmt)
    rows = result.all()

    # 标准化
    return [
        {
            "chunk_id": str(chunk_row.id),
            "content": chunk_row.chunk_text,
            "score": float(score) if score is not None else 0.0,
            "metadata": {
                "document_pk": str(chunk_row.document_pk),
                "match_type": "fts",
            },
        }
        for chunk_row, score in rows
    ]


# ILIKE 兜底检索
async def _search_by_ilike(
    db: AsyncSession,
    query: str,
    limit: int,
) -> list[dict]:
    # 提取关键词
    terms = _extract_terms(query)
    # 无关键词直接空
    if not terms:
        return []

    # 构造 OR 条件
    conditions = [DocumentChunk.chunk_text.ilike(f"%{t}%") for t in terms]

    # 查询语句
    stmt = (
        select(DocumentChunk)
        .where(or_(*conditions))
        .order_by(DocumentChunk.created_at.desc())
        .limit(limit)
    )

    # 执行查询
    result = await db.execute(stmt)
    rows = result.scalars().all()

    # 标准化
    return [
        {
            "chunk_id": str(row.id),
            "content": row.chunk_text,
            "score": 0.3,
            "metadata": {
                "document_pk": str(row.document_pk),
                "match_type": "ilike",
                "terms": terms,
            },
        }
        for row in rows
    ]


# RRF 融合：把多路结果合并成一个排序
def _rrf_fuse(
    vector_rows: list[dict],
    fts_rows: list[dict],
    ilike_rows: list[dict],
    limit: int,
    k: int = 60,
) -> list[dict]:
    # 合并容器：key=chunk_id
    merged: dict[str, dict] = {}

    # 定义三路数据
    channels = [
        ("vector", vector_rows),
        ("fts", fts_rows),
        ("ilike", ilike_rows),
    ]

    # 遍历每一路
    for source_name, rows in channels:
        # 排名从 1 开始
        for rank, item in enumerate(rows, start=1):
            # 当前 chunk_id
            cid = item["chunk_id"]

            # 首次出现：创建基础记录
            if cid not in merged:
                merged[cid] = {
                    "chunk_id": cid,
                    "content": item.get("content", ""),
                    "score": 0.0,  # 这里是融合分，不是原始分
                    "metadata": {
                        **(item.get("metadata") or {}),
                        "sources": [],
                        "match_type": "hybrid_rrf",
                    },
                }

            # 记录来源通道
            if source_name not in merged[cid]["metadata"]["sources"]:
                merged[cid]["metadata"]["sources"].append(source_name)

            # RRF 加分：1 / (k + rank)
            merged[cid]["score"] += 1.0 / (k + rank)

    # 按融合分降序
    ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)

    # 截断到 limit
    return ranked[:limit]


# 对外统一入口：混合检索
async def search_chunks_by_keyword(
    db: AsyncSession,
    query: str,
    limit: int = 5,
) -> list[dict]:
    # 清洗 query
    q = (query or "").strip()
    # 空 query 返回空
    if not q:
        return []

    # 1) 向量检索
    vector_rows = await _search_by_vector(db=db, query=q, limit=limit)

    # 2) FTS 检索
    fts_rows = await _search_by_fts(db=db, query=q, limit=limit)

    # 3) 如果两路都空，启用 ILIKE 兜底；否则可选不启用
    ilike_rows: list[dict] = []
    if not vector_rows and not fts_rows:
        ilike_rows = await _search_by_ilike(db=db, query=q, limit=limit)

    # 4) 融合输出
    fused = _rrf_fuse(
        vector_rows=vector_rows,
        fts_rows=fts_rows,
        ilike_rows=ilike_rows,
        limit=limit,
    )

    # 返回结果
    return fused
