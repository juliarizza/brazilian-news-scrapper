# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import csv

from scrapy.exceptions import DropItem

from uol.items import UolItem


class TitlePipeline(object):
    def process_item(self, item, spider):
        if not item.get('title'):
            raise DropItem('Missing title for %s' % item)
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.processed_urls = set()

    def process_item(self, item, spider):
        if item['url'] in self.processed_urls:
            raise DropItem('Duplicate item found: %s' % item)
        return item


class CSVPipeline(object):
    def open_spider(self, spider):
        write_headers = not os.path.exists('data.csv')
        self.file = open('data.csv', 'a+')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=UolItem.fields)

        if write_headers:
            self.csv_writer.writeheader()
            write_headers = False

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(dict(item))
        return item