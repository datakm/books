# -*- coding: utf-8 -*-
import scrapy

# 书籍列表
class bookList(scrapy.Item):
    book_name = scrapy.Field()
    grade = scrapy.Field()
    author = scrapy.Field()
    cate_id = scrapy.Field()
    page = scrapy.Field()
    book_detail_url = scrapy.Field()

# 书籍详情
class bookDetail(scrapy.Item):
    book_name = scrapy.Field()
    book_image = scrapy.Field()
    author = scrapy.Field()
    cate_name = scrapy.Field()
    grade = scrapy.Field()
    desc = scrapy.Field() # 简介
    download_url = scrapy.Field() # 下载地址