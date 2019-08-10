# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.ireadweek.com']
    start_urls = ['http://www.ireadweek.com/']

    def parse(self, response):
        pass
