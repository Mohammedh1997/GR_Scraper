# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GrBooksItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    shelf_count = scrapy.Field()
    rate_score = scrapy.Field()
    rate_quant = scrapy.Field()
