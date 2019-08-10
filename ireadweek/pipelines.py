# -*- coding: utf-8 -*-


from ireadweek.settings import logger
import json, time
from ireadweek.items import bookList, bookDetail

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

    def close_spider(self,spider):
        self.file1.close()
        self.file2.close()
        