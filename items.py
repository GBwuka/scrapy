# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongguancunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    # model = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    cpu_model = scrapy.Field()
    cpu_frequency = scrapy.Field()
    gpu_model = scrapy.Field()
    ram = scrapy.Field()
    android_sdk = scrapy.Field()
    market_time = scrapy.Field()
    resolution = scrapy.Field()
    fingerprint = scrapy.Field()
