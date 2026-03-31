from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from settings import DB_URI

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


engine = create_async_engine(
    DB_URI,
    #将输出所有的sql日志
    echo = True,
    #连接池大小
    pool_size=10,
    #最大空闲连接数
    max_overflow = 20,
    #连接池空闲时间
    pool_timeout = 10,
    #连接池回收时间(默认是-1, 代表永不回收)
    pool_recycle=3600,
    #连接前是否检查
    pool_pre_ping=True,
)

#创建会话工厂



AsyncSessionFactory = sessionmaker(
    #Engine 或者其子类对象
    bind=engine,
    #Session类的代替
    class_ = AsyncSession,
    #是否在查找之前执行flush操作
    autoflush=True,
    #是否在执行commit操作后Session就过期
    expire_on_commit=False
)


#定义Base类


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
       #ix: index, 索引
       "ix": "ix_%(column_0_label)s",
       #uq: unique, 唯一约束
       "uq": "uq_%(table_name)s_%(column_0_name)s",
       #ck: check, 检查约束
       "ck": "ck_%(table_name)s_%(constraint_name)s",
       #fk: foreign key, 外键约束
       "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
       #pk: primary key, 主键
       "pk": "pk_%(table_name)s"
})

from .import user

