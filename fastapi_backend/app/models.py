"""ORM 模型定义：描述数据库表结构与表之间关系。"""

# fastapi-users 提供的“UUID 主键用户表”基类。
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
# DeclarativeBase 是 SQLAlchemy 2.x 的声明式基类。
from sqlalchemy.orm import DeclarativeBase
# Column/类型/外键用于声明字段。
from sqlalchemy import Column, String, Integer, ForeignKey
# relationship 用于声明 ORM 层的一对多/多对一关系。
from sqlalchemy.orm import relationship
# PostgreSQL UUID 字段类型。
from sqlalchemy.dialects.postgresql import UUID
# uuid4 用于生成默认主键值。
from uuid import uuid4


# 所有模型统一继承的基类（承载 metadata）。
class Base(DeclarativeBase):
    # 这里不定义字段，仅作为声明式模型根基类。
    pass


# 用户模型：在 fastapi-users 的默认用户字段基础上扩展关系字段。
class User(SQLAlchemyBaseUserTableUUID, Base):
    # 与 Item 的一对多关系：一个用户可以有多个 Item。
    # back_populates="user" 对应 Item.user。
    # cascade="all, delete-orphan" 表示删除用户时级联删除其 Item。
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")


# 业务模型：用户的条目数据（示例领域对象）。
class Item(Base):
    # 数据库表名。
    __tablename__ = "items"

    # 主键：UUID，默认自动生成。
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # 条目名称，必填。
    name = Column(String, nullable=False)
    # 条目描述，可空。
    description = Column(String, nullable=True)
    # 数量，可空（模板允许不填）。
    quantity = Column(Integer, nullable=True)
    # 所属用户 ID，外键关联 user.id，必填。
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # 多对一关系：每个 Item 归属于一个 User。
    user = relationship("User", back_populates="items")
