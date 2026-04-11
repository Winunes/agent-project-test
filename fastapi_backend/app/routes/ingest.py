# 文档入库路由（MVP：加入向量写入）
# 这一版做三件事：
# 1) 文档写入 documents
# 2) 切块写入 document_chunks
# 3) 为每个 chunk 生成 embedding 并写入 pgvector 列

# 标准库：哈希（做稳定向量特征）
import hashlib
# 标准库：数学函数（做向量归一化）
import math
# 标准库：正则（做简单分词）
import re

# FastAPI 路由和依赖
from fastapi import APIRouter, Depends, HTTPException
# Pydantic 请求体模型
from pydantic import BaseModel, Field
# SQLAlchemy 查询/删除/原生 SQL
from sqlalchemy import delete, select, text
# SQLAlchemy 异步会话
from sqlalchemy.ext.asyncio import AsyncSession

# 数据库 session 依赖
from app.database import get_async_session
# ORM 模型
from app.models import Document, DocumentChunk

# 路由对象
router = APIRouter(tags=["ingest"])


# 单个文档入库结构
class IngestDocument(BaseModel):
    # 文档业务 ID（外部系统主键）
    document_id: str = Field(..., description="文档ID")
    # 文档来源（faq/sop/help 等）
    source: str = Field(..., description="文档来源")
    # 文档标题
    title: str = Field(..., description="文档标题")
    # 文档正文
    content: str = Field(..., description="文档正文文本")


# 批量入库请求结构
class IngestRequest(BaseModel):
    # 文档列表
    documents: list[IngestDocument]


# 文本规范化：去掉多余空白
def normalize_text(text: str) -> str:
    # split + join 能把连续空白压缩成一个空格
    return " ".join(text.strip().split())


# 简单切块：按固定字符长度切分
def simple_chunk(text: str, max_chars: int = 500) -> list[str]:
    # 空文本直接返回空
    if not text:
        return []
    # 准备切块结果
    chunks: list[str] = []
    # 起始下标
    start = 0
    # 循环切分
    while start < len(text):
        # 结束下标
        end = start + max_chars
        # 追加一个块
        chunks.append(text[start:end])
        # 前进到下一段
        start = end
    # 返回切块
    return chunks


# 简单分词（MVP 本地版本，不依赖外部 embedding 服务）
def tokenize_for_embedding(text_value: str) -> list[str]:
    # 去前后空白
    t = (text_value or "").strip().lower()
    # 空文本直接空 tokens
    if not t:
        return []

    # token 列表
    tokens: list[str] = []

    # 1) 英文/数字连续串作为 token
    for w in re.findall(r"[a-z0-9]+", t):
        if w:
            tokens.append(w)

    # 2) 中文按“单字”切（MVP 简化，先保证可用）
    for ch in t:
        if "\u4e00" <= ch <= "\u9fff":
            tokens.append(ch)

    # 返回 token
    return tokens


# 构造固定维度向量（哈希袋模型）
def build_embedding(text_value: str, dim: int = 1024) -> list[float]:
    # 初始化全 0 向量
    vec = [0.0] * dim
    # 分词
    tokens = tokenize_for_embedding(text_value)

    # 没有 token 就返回零向量
    if not tokens:
        return vec

    # 累加 token 频次到哈希桶
    for token in tokens:
        # 用 md5 保证同样 token 映射稳定
        h = hashlib.md5(token.encode("utf-8")).hexdigest()
        # 映射到 [0, dim)
        idx = int(h, 16) % dim
        # 计数 +1
        vec[idx] += 1.0

    # L2 归一化，便于余弦相似度
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]

    # 返回向量
    return vec


# 把 Python 向量转成 pgvector 文本格式："[0.1,0.2,...]"
def to_pgvector_literal(vec: list[float]) -> str:
    # 统一保留 6 位小数，控制长度和可读性
    return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"


# 入库接口
@router.post("/documents")
async def ingest_documents(
    # 请求体
    payload: IngestRequest,
    # 异步数据库会话
    db: AsyncSession = Depends(get_async_session),
):
    # 统计：文档数
    total_docs = 0
    # 统计：切块数
    total_chunks = 0
    # 返回详情
    items: list[dict] = []

    try:
        # 逐文档处理
        for doc in payload.documents:
            # 文档数 +1
            total_docs += 1

            # 文本清洗
            cleaned = normalize_text(doc.content)
            # 切块
            chunks = simple_chunk(cleaned, max_chars=500)
            # 统计块数
            total_chunks += len(chunks)

            # 查是否已存在同 document_id
            existing_stmt = select(Document).where(Document.document_id == doc.document_id)
            existing_result = await db.execute(existing_stmt)
            existing_doc = existing_result.scalars().first()

            # 已存在：覆盖更新
            if existing_doc is not None:
                # 先删旧 chunks（避免脏数据）
                await db.execute(
                    delete(DocumentChunk).where(DocumentChunk.document_pk == existing_doc.id)
                )
                # 更新文档主信息
                existing_doc.source = doc.source
                existing_doc.title = doc.title
                existing_doc.content = cleaned
                # 复用对象
                doc_row = existing_doc
            else:
                # 不存在：新建文档
                doc_row = Document(
                    document_id=doc.document_id,
                    source=doc.source,
                    title=doc.title,
                    content=cleaned,
                )
                # 放入会话
                db.add(doc_row)
                # flush 让 doc_row.id 立即可用
                await db.flush()

            # 写入 chunks + embedding
            for idx, chunk_text in enumerate(chunks):
                # 新建 chunk 记录
                chunk_row = DocumentChunk(
                    document_pk=doc_row.id,
                    chunk_index=idx,
                    chunk_text=chunk_text,
                )
                # 加入会话
                db.add(chunk_row)
                # flush 拿到 chunk_row.id（后面 UPDATE embedding 要用）
                await db.flush()

                # 生成向量（MVP 本地哈希向量）
                embedding = build_embedding(chunk_text, dim=1024)
                # 转 pgvector 字面量
                embedding_literal = to_pgvector_literal(embedding)

                # 用原生 SQL 更新 embedding 列（因为 ORM 里暂未声明 Vector 类型）
                await db.execute(
                    text(
                        "UPDATE document_chunks "
                        "SET embedding = CAST(:embedding AS vector) "
                        "WHERE id = :chunk_id"
                    ),
                    {
                        "embedding": embedding_literal,
                        "chunk_id": chunk_row.id,
                    },
                )

            # 收集本次文档结果
            items.append(
                {
                    "document_id": doc.document_id,
                    "source": doc.source,
                    "title": doc.title,
                    "chunk_count": len(chunks),
                    "preview_chunk": chunks[0] if chunks else "",
                }
            )

        # 提交事务
        await db.commit()

    except Exception as exc:
        # 异常回滚
        await db.rollback()
        # 返回 500
        raise HTTPException(status_code=500, detail=f"Ingest failed: {exc}") from exc

    # 返回入库结果
    return {
        "status": "ok",
        "total_docs": total_docs,
        "total_chunks": total_chunks,
        "items": items,
        "embedding_dim": 1024,
        "note": "MVP ingest done: documents + chunks + embedding",
    }
