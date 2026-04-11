"""Add documents and document_chunks tables

Revision ID: d9a0f9f1b2c7
Revises: c2f2a0a1c4d1
Create Date: 2026-04-11
"""

# 导入类型标注。
from typing import Sequence, Union

# 导入 Alembic 操作对象。
from alembic import op
# 导入 SQLAlchemy。
import sqlalchemy as sa


# 迁移版本号（必须存在，否则 Alembic 会报你看到的错误）。
revision: str = "d9a0f9f1b2c7"
# 上一个迁移版本号。
down_revision: Union[str, None] = "c2f2a0a1c4d1"
# 分支标签（当前不用）。
branch_labels: Union[str, Sequence[str], None] = None
# 依赖迁移（当前不用）。
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建 documents 表。
    op.create_table(
        "documents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("document_id", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # 文档业务 ID 唯一索引。
    op.create_index(op.f("ix_documents_document_id"), "documents", ["document_id"], unique=True)
    # 来源普通索引。
    op.create_index(op.f("ix_documents_source"), "documents", ["source"], unique=False)

    # 创建 document_chunks 表。
    op.create_table(
        "document_chunks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("document_pk", sa.UUID(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["document_pk"], ["documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # 外键索引。
    op.create_index(op.f("ix_document_chunks_document_pk"), "document_chunks", ["document_pk"], unique=False)


def downgrade() -> None:
    # 回滚时先删子表索引/子表。
    op.drop_index(op.f("ix_document_chunks_document_pk"), table_name="document_chunks")
    op.drop_table("document_chunks")

    # 再删父表索引/父表。
    op.drop_index(op.f("ix_documents_source"), table_name="documents")
    op.drop_index(op.f("ix_documents_document_id"), table_name="documents")
    op.drop_table("documents")
