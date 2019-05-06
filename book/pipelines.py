# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    def process_item(self, item, spider):
        #保存趴下来的结果，此处不再提
        print(item)
        return item
