# -*- coding: utf-8 -*-

BOT_NAME = 'ireadweek'

SPIDER_MODULES = ['ireadweek.spiders']
NEWSPIDER_MODULE = 'ireadweek.spiders'

ROBOTSTXT_OBEY = False

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0"

import logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('C:/Users/hqs/Desktop/script/python/spider/bak/test.log', mode='w', encoding='utf-8'))
logger.setLevel(logging.CRITICAL)  # 输出所有大于INFO级别的log

ITEM_PIPELINES = {
   # 'ireadweek.pipelines.booksPipeline': 300,
   'ireadweek.pipelines.mysqlPipeline': 301,
   'ireadweek.pipelines.imagePipeline': 302,
}

PROXY_URL = 'http://localhost:5555/random'

# DOWNLOADER_MIDDLEWARES = {
#     'ireadweek.middlewares.ProxyMiddleware': 555,
# }

IMAGES_STORE = 'D:/home/phpstudy2019install/PHPTutorial/WWW/book/Uploads/News/2019-08-13/'