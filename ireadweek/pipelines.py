# -*- coding: utf-8 -*-


from ireadweek.settings import logger
import json, time
from ireadweek.items import bookCateList, bookList, bookDetail
from ireadweek.ext.models import session, articleCate, article

class booksPipeline(object):
    def open_spider(self, spider):
        self.file1 = open('booklist.log', 'w', encoding='utf-8')
        self.file2 = open('bookDetail.log', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        add_time = time.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(item, bookList):
            # 写入文本
            context = json.dumps(dict(item),ensure_ascii=False) + '\n'
            self.file1.write(context)
        if isinstance(item, bookDetail):
            # 写入文本
            context = json.dumps(dict(item),ensure_ascii=False) + '\n'
            self.file2.write(context)
        return item

    def close_spider(self,spider):
        self.file1.close()
        self.file2.close()

class mysqlPipeline(object):
    def process_item(self, item, spider):
        # 写入分类表
        if isinstance(item, bookCateList):
            add_time = time.strftime('%Y-%m-%d %H:%M:%S')
            obj = articleCate(id=item['id'], pid=0, name=item['name'], add_time=add_time, status=1)
            session.add(obj)
            session.commit()
        # 文章列表
        if isinstance(item, bookList):
            add_time = time.strftime('%Y-%m-%d %H:%M:%S')
            obj = article(title=item['book_name'], cate_id=item['cate_id'], author=item['author'], grade=item['grade'], book_detail_url=item['book_detail_url'], origin_book_id=item['origin_book_id'], add_time=add_time, status=1)
            session.add(obj)
            session.commit()
        # 文章详情
        if isinstance(item, bookDetail):
            origin_book_id = item['origin_book_id']
            book = session.query(article).filter(article.origin_book_id == origin_book_id).first()
            book.image = item['book_image']
            book.desc = item['desc']
            book.download_url = item['download_url']
            session.commit()
        return item
        