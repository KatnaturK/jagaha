# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JagahaItem(scrapy.Item):
    platform = scrapy.Field()
    city = scrapy.Field()
    txn_type = scrapy.Field()
    property_type = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    google_place_id = scrapy.Field()
    building_name = scrapy.Field()
    area = scrapy.Field()
    selling_price = scrapy.Field()
    monthly_rent = scrapy.Field()
    location = scrapy.Field()
    data_id = scrapy.Field()
    desc = scrapy.Field()
    furnished = scrapy.Field()
    immediate_possession = scrapy.Field()
    age = scrapy.Field()
    locality = scrapy.Field()
    data_time = scrapy.Field()
