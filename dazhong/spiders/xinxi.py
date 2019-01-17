# -*- coding: '# -*- coding',
import scrapy

from selenium.webdriver.chrome.options import Options
import time
import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
# 导入驱动接口
from selenium import webdriver

from dazhong import settings
from dazhong.items import DazhongItem

class XinxiSpider(scrapy.Spider):
    name = 'xinxi'
    allowed_domains = ['dianping.com']
    # start_urls = ['http://dianping.com/']

    def start_requests(self):
        url ='https://account.dianping.com/login?'
        yield scrapy.Request(url, callback=self.parse )

    def parse(self, response):
        url = 'https://www.dianping.com/beijing/ch10/g110p{}?'
        for i in range(1, 4):
            dian_url = url.format(i)
            yield scrapy.Request(dian_url, callback=self.dian_parse)

    #每一页的所有店
    def dian_parse(self, response):
        print('-dian_parse- 所有店-->')
        dian_id = response.xpath("//a[@data-click-name='shop_img_click']/@data-shopid").extract()
        for id in dian_id:
            url ='http://www.dianping.com/shop/{}/review_all'
            print(url)
            fulurl = url.format(id)
            yield scrapy.Request(fulurl, callback=self.ji_parse)

    #获取每个店里面点击获取所有评论
    def ji_parse(self,response):
        print("#" * 50)
        print(response.url)
        print("#" * 50)
        item = DazhongItem()
        #店名称
        dian_name =response.xpath("//a[@class='shop-name']/text()").extract_first()
        item['dian_name']=dian_name
        print(dian_name)
        #星数几颗星
        # star_num = response.xpath("//div[@class='rank-info']/span[1]/@class")
        #人均消费
        ren_jun= response.xpath("//span[@class='price']/strong/text()").extract_first()
        item['ren_jun']=ren_jun
        #地址
        attress=response.xpath("//p[@class='address']/a/text()").extract_first()
        item['address']=attress
        #电话
        phone=response.xpath("//p[@class='phone']/em/text()").extract_first()
        item['phone']=phone
        #好评
        hao_ping=response.xpath("//label[@class='filter-item filter-good']/span//text()").extract_first()
        item['hao_ping']=hao_ping
        #评论
        pin_lun = response.xpath("//div[@class='review-words']").extract()
        item['pin_lun']=pin_lun
        yield item






