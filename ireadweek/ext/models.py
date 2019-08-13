# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/book", max_overflow=5)
Base = declarative_base()

# 文章分类表
class articleCate(Base):
    __tablename__ = 'news_category'
    id = Column(Integer, primary_key=True)
    fid = Column(Integer, default=0)
    title = Column(String(100))
    add_time = Column(DateTime)
    order =Column(Integer)
    # status = Column(Integer)


# 文章表
class article(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    fid = Column(Integer) # 分类id
    title = Column(String(100))
    author = Column(String(30))
    origin_image_path = Column(String(200))
    image = Column(String(200))
    hits = Column(Integer)
    grade = Column(String(20))
    book_detail_url = Column(String(250))
    origin_book_id = Column(Integer)
    download_url = Column(String(250))
    view =Column(Integer)
    desc = Column(Text)
    content = Column(Text)
    order =Column(Integer)
    recomm =Column(Integer)
    add_time = Column(DateTime)
    update_time = Column(DateTime)

Base.metadata.create_all(engine)
#创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()


# row = session.query(article).filter_by(origin_book_id=13491).first()
# print(row.book_detail_url)