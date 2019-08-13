# -*- coding: utf-8 -*-


from ireadweek.settings import logger
import json, time, re
from ireadweek.items import bookCateList, bookList, bookDetail
from ireadweek.ext.models import session, articleCate, article
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

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
    def __init__(self, image_store):
        self.image_store = image_store

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            image_store=crawler.settings.get('IMAGES_STORE'),
        )

    def process_item(self, item, spider):
        # 写入分类表
        if isinstance(item, bookCateList):
            row = session.query(articleCate).filter_by(id=item['id']).first()
            if not getattr(row, 'id', None):
                add_time = time.strftime('%Y-%m-%d %H:%M:%S')
                obj = articleCate(id=item['id'], pid=0, name=item['name'], add_time=add_time, status=1)
                session.add(obj)
                session.commit()
        # 文章列表
        if isinstance(item, bookList):
            add_time = time.strftime('%Y-%m-%d %H:%M:%S')
            row = session.query(article).filter_by(origin_book_id=item['origin_book_id']).first()
            if not getattr(row, 'origin_book_id', None):
                obj = article(title=item['book_name'], cate_id=item['cate_id'], author=item['author'], grade=item['grade'], book_detail_url=item['book_detail_url'], origin_book_id=item['origin_book_id'], add_time=add_time, status=1)
                session.add(obj)
                session.commit()
        # 文章详情
        if isinstance(item, bookDetail):
            origin_book_id = item['origin_book_id']
            book = session.query(article).filter(article.origin_book_id == origin_book_id).first()
            book.origin_image_path = item['book_image']
            path = re.search('/.*?(20190813.*?/)$', self.image_store).group(1)
            book.image = path + item['book_image'].split('/')[-1]
            book.desc = item['desc']
            book.content = item['desc']
            book.download_url = item['download_url']
            session.commit()
        return item

class imagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        logger.info('ImagePipelinetest1')
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        logger.info('ImagePipelinetest2')
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Dowloaded Failed')
        return item

    def get_media_requests(self, item, info):
        logger.info('ImagePipelinetest3')
        logger.info('image_url='+item['book_image'])
        yield Request(item['book_image'])
