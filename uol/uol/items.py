# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from uol.utils import formatted_text


class UolItem(scrapy.Item):
    title = scrapy.Field(serializer=formatted_text)
    author = scrapy.Field(serializer=formatted_text)
    category = scrapy.Field(serializer=formatted_text)
    location = scrapy.Field(serializer=formatted_text)
    datetime = scrapy.Field()
    comments_count = scrapy.Field(serializer=int)
    url = scrapy.Field(serializer=str)
