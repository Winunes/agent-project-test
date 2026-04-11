"""给 document_chunks 增加 pgvector embedding 列和向量索引（MVP）"""

# Alembic 迁移工具
from alembic import op

# revision identifiers, used by Alembic.
revision = "e3c1a9d4f8a1"
down_revision = "d9a0f9f1b2c7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) 启用 pgvector 扩展（如果已启用则跳过）
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # 2) 在 document_chunks 表增加 embedding 向量列（维度先固定 1024，后续可按模型调整）
    op.execute(
        "ALTER TABLE document_chunks "
        "ADD COLUMN IF NOT EXISTS embedding vector(1024)"
    )

    # 3) 建立 ivfflat 索引（余弦相似度）
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_document_chunks_embedding_ivfflat "
        "ON document_chunks USING ivfflat (embedding vector_cosine_ops) "
        "WITH (lists = 100)"
    )


def downgrade() -> None:
    # 回滚时先删索引
    op.execute("DROP INDEX IF EXISTS ix_document_chunks_embedding_ivfflat")

    # 再删 embedding 列
    op.execute(
        "ALTER TABLE document_chunks "
        "DROP COLUMN IF EXISTS embedding"
    )

    # 扩展一般不强制删除，避免影响其他表
