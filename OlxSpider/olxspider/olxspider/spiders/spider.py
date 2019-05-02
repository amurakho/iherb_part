import scrapy
from datetime import datetime
from ..items import ImageItem, OlxspiderItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class OlxSpiderCategoryState(CrawlSpider):

    name = 'olxcategory'

    #allowed_domains = 'olx.ua'

    start_urls = [
        'https://www.iherb.com/c/algae?p=1'
    ]

#https://www.iherb.com/pr/Sunfood-Broken-Cell-Wall-Chlorella-Tablets-250-mg-456-Tablets-4-oz-113-g/59420
    rules = (
        # Rule for pagination
        Rule(LinkExtractor(restrict_xpaths='//*[contains(concat( " ", @class, " " ), concat( " ", "pagination", " " ))]'), callback='parse_start', follow=True),
        # rule for parse page
        Rule(LinkExtractor(
            restrict_xpaths='//*[contains(concat( " ", @class, " " ), concat( " ", "product-image", " " ))]'),
             callback='parse_page', follow=True),
    )

    def parse_start(self, response):
        pass

    def parse_page(self, response):

        item = OlxspiderItem()

        item['name'] = response.xpath('//*[(@id = "name")]/text()').get()

        description = response.xpath('//div[@itemprop="description"]//li/text()').getall()
        description.append(response.xpath('//div[@itemprop="description"]//p/text()').get())

        item['description'] = '\n'.join(description)

        block = response.xpath('//*[(@id="product-specs-list")]').css('li')

        item['sku'] = block.xpath('//span[@itemprop="sku"]/text()').get()

        img_container =response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "thumbnail-container", " " ))]').xpath('img/@src').getall()

        item['category'] = response.css('a~ a+ .last::text').get()

        item['image_urls'] = []

        for link in img_container:
            item['image_urls'].append(link)

        return item