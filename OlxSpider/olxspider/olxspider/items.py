# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxspiderItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    name = scrapy.Field()
    sku = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    pass

# ScrapingList Residential & Yield Estate for sale
class ListResidentialItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()