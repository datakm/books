# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from ireadweek.settings import logger
from ireadweek.items import bookList, bookDetail
import re,time,random

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.ireadweek.com']
    # start_urls = ['http://www.ireadweek.com/index.php?g=portal&m=list&a=index&id=67&p=1'] # 分类: 逻辑学
    start_urls = ['http://www.ireadweek.com/index.php?m=list&a=index&id=2'] # 分类：凡人修仙
    def parse(self, response):
        '''
        # 循环分类列表，采集一个分类，返回当前分类id和当前对应的文章列表并写入数据库，同时返回后续文章request列表，文章request详情写入数据库。
        '''
        request_url = response.url
        cate_id = re.search('.*?id=(.*?)$', request_url, re.S).group(1)
        html = response.text
        doc = pq(html)
        book_list = doc('.hanghang-list').children('a').items()
        TEST_FLAG = True # 开启测试，减少时间爬取最少数据
        for book in book_list:
            book_item = bookList()
            book_item['book_name'] = book.find('.hanghang-list-name').text()
            book_item['grade'] = book.find('.hanghang-list-num').text()
            book_item['author'] = book.find('.hanghang-list-zuozhe').text()
            book_item['cate_id'] = cate_id
            book_item['page'] = doc.find('.hanghang-page').find('.current').text()
            book_item['book_detail_url'] = book.attr('href')
            yield book_item
            
            # 爬取书籍详情页
            sleep_time = random.uniform(0.1,0.9)
            logger.info('爬取书籍详情页，睡眠'+str(sleep_time)+'秒')
            time.sleep(sleep_time)
            book_detail_url = response.urljoin(book.attr('href'))
            yield scrapy.Request(url=book_detail_url, callback=self.parse_book_detail, meta={'cate_id':cate_id})
            if TEST_FLAG:
                break # 只爬取一个分类下的一本书和对应的详情页

        if not TEST_FLAG:
            # 后续request，下一页
            sleep_time = random.uniform(0.1,0.9)
            logger.info('爬取下一页，睡眠'+str(sleep_time)+'秒')
            time.sleep(sleep_time)
            # next_page = doc.find('.hanghang-page').find('li:last').prev().children('a').attr('href')
            next_page = doc.find('.hanghang-page').find('.current').parent('li').next('li a').attr('href')
            if next_page:
                next_page = response.urljoin(next_page)
                logger.info('next_page')
                logger.info(next_page)
                yield scrapy.Request(url=next_page, callback=self.parse, meta={})
        
        # 爬取下一个分类
        cate_name = ''
        if 'cate_name' in response.meta.keys():
            cate_name = response.meta['cate_name']
        if not cate_name:
            cate_name = ''
        sleep_time = random.uniform(0.1,0.9)
        logger.info('爬取下一个分类，分类名称：'+ cate_name +'，睡眠'+str(sleep_time)+'秒')
        time.sleep(sleep_time)
        cate_list = doc('.hanghang-shupu-content a:gt(0)').items()
        for item in cate_list:
            next_cate_url = item.attr('href')
            next_cate_url = response.urljoin(next_cate_url)
            cate_name = item.text()
            yield scrapy.Request(url=next_cate_url, callback=self.parse, meta={'cate_name':cate_name})
            
    def parse_book_detail(self, response):
        html = response.text
        doc = pq(html)
        item = bookDetail()
        item['book_name'] = doc.find('.hanghang-shu-content-font').children('p').eq(0).text()
        item['book_image'] = doc.find('.hanghang-shu-content-img').children('img').attr('src')
        item['author'] = doc.find('.hanghang-shu-content-font').children('p').eq(1).text()
        item['cate_name'] = doc.find('.hanghang-shu-content-font').children('p').eq(2).text()
        item['grade'] = doc.find('.hanghang-shu-content-font').children('p').eq(3).text()
        item['desc'] = doc.find('.hanghang-shu-content-font').children('p').eq(4).nextAll('p').text()
        item['download_url'] = doc.find('.hanghang-shu-content-btns').parent('a').attr('href')
        yield item
            
