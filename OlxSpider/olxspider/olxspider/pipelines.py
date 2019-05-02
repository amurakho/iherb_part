# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.misc import md5sum

class MyImagesPipeline(ImagesPipeline):

    def set_filename(self, response):
        if response.meta['number'] == 0:
            return '{0}/{1}.jpg'.format(response.meta['category'], response.meta['sku'])
        else:
            return '{0}/{1}@{2}.jpg'.format(response.meta['category'], response.meta['sku'], response.meta['number'])
        pass


    def get_media_requests(self, item, info):
        for idx, image_url in enumerate(item['image_urls']):
            yield scrapy.Request(image_url, meta={'sku': item["sku"],
                                                  'number': idx,
                                                'category': item["category"]})

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if response.meta['number'] == 0:
                path = 'full/{0}/{1}.jpg'.format(response.meta['category'], response.meta['sku'])
            else:
                path = 'full/{0}/{1}@{2}.jpg'.format(response.meta['category'], response.meta['sku'], response.meta['number']) # **Here Changed**
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height},
                headers={'Content-Type': 'image/jpeg'})
        return checksum