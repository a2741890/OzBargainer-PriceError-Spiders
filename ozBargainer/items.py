# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OzbargainerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    node = scrapy.Field()
    title = scrapy.Field()
    post = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    pass
