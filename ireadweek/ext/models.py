# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/ruohan", max_overflow=5)
Base = declarative_base()

# 文章分类表
class articleCate(Base):
    __tablename__ = 'tp_article_cate'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer)
    name = Column(String(100))
    add_time = Column(DateTime)
    status = Column(Integer)

# 文章表
class article(Base):
    __tablename__ = 'tp_article'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    cate_id = Column(Integer)
    image = Column(String(200))
    desc = Column(Text)
    content = Column(Text)
    hits = Column(Integer)
    author = Column(String(30))
    grade = Column(String(20))
    book_detail_url = Column(String(250))
    origin_book_id = Column(Integer)
    download_url = Column(String(250))
    add_time = Column(DateTime)
    update_time = Column(DateTime)
    is_recommend = Column(Integer)
    is_index = Column(Integer)
    status = Column(Integer)

Base.metadata.create_all(engine)
#创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()
