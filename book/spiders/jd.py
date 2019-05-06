# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from urllib.parse import urljoin
import json
import re

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item = {}
            item['first_title'] = dt.xpath('./a/text()').extract_first()
            # item['first_href'] = dt.xpath('./a/@href').extract_first()
            # item['first_href'] = urljoin(response.url,item['first_href'])
            dd_list = dt.xpath('./following-sibling::dd[1]')
            for dd in dd_list:
                item['second_title'] = dd.xpath('./em/a/text()').extract_first()
                item['second_href'] = dd.xpath('./em/a/@href').extract_first()
                item['second_href'] = urljoin(response.url,item['second_href'])

                yield scrapy.Request(
                    item['second_href'],
                    callback=self.parse_list,
                    meta={"item":deepcopy(item)}
                )

    #第二分类的图书列表
    def parse_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            item["book_name"] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            item["book_author"] = li.xpath('.//span[@class="p-bi-name"]//a/text()').extract()
            item["book_public"] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            item["book_href"] = li.xpath('//div[@class="p-name"]/a/@href').extract_first()
            item["book_href"] = urljoin(response.url,item["book_href"])
            book_number = li.xpath('./div[@class="gl-i-wrap j-sku-item"]/@data-sku').extract_first()
            price_href = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(book_number)
            yield scrapy.Request(
                price_href,
                callback=self.parse_detail,
                meta={"item":deepcopy(item)}
            )
        #翻页
        next_url = re.findall('<a class=\"pn-next\" href=\"(.*?)\">下一页',response.body.decode())[0]
        next_url = urljoin(response.url,next_url)
        yield scrapy.Request(
            next_url,
            callback=self.parse_list
        )
    #价格在js文件中，需要找到对应的json文件。
    def parse_detail(self,response):
        item = response.meta["item"]
        item["price"] = json.loads(response.body.decode('utf8'))[0]['p']
        yield item






