import json
import logging
from scrapy import signals
import requests
from ireadweek.settings import logger


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
    
    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False
    
    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        proxy = self.get_random_proxy()
        # logger.info('myprint:' + proxy)
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            logger.info('使用代理 ' + proxy) # 使用代理 123.200.14.238:8080
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )