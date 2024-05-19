import scrapy
import re
import json
from typing import Any, Iterable
from scrapy.http import Request, Response
from wallpaper_scrapy.items import BingScrapyItem
from fake_useragent import UserAgent
from scrapy_splash import SplashRequest


class WallpaperNasaSpider(scrapy.Spider):
    name = 'nasa'
    host = 'https://apod.nasa.gov'
    start_urls = [
        'https://apod.nasa.gov/apod/astropix.html'
    ]


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        pic_xpath = '/html/body/center[1]/p[2]/a/@href'
        pic_url = response.xpath(pic_xpath).extract_first()
        self.image_urls = [f"https://apod.nasa.gov/apod/{pic_url}"]
        title_xpath = '/html/body/center[2]/b[1]/text()'
        self.title = response.xpath(title_xpath).extract_first()
        copyright_xpath = '/html/body/center[2]/a[1]/text()'
        self.copyright = response.xpath(copyright_xpath).extract_first()
        desc_xpath = '/html/body/p[1]/text()'
        desc = response.xpath(desc_xpath).extract()
        desc = ''.join(desc)
        self.desc = desc.replace("\n", "")
        self.tag = 'nasa'
        trivia_xpath = '/html/body/center[2]/a[2]/text()'
        triviaId = response.xpath(trivia_xpath).extract_first()
        self.triviaId = triviaId.replace(" ", "_")

        item_data = {
            'platform': 'nasa',
            'title': self.title,
            'tag': self.tag,
            'desc': self.desc,
            'copyright': self.copyright,
            'image_urls': self.image_urls,
            'trivia_id': self.triviaId
        }
        print(item_data)

        yield item_data