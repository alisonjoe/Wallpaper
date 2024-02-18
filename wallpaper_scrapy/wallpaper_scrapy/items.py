# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BingScrapyItem(scrapy.Item):
    platform = scrapy.Field()
    desc = scrapy.Field()
    tag = scrapy.Field()
    copyright = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    md_path = scrapy.Field()
    trivia_id = scrapy.Field()
    mkt = scrapy.Field()
