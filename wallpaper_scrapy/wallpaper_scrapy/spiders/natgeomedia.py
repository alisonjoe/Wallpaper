import scrapy
import re
import json
from urllib.parse import urlparse, parse_qs
from wallpaper_scrapy.mariadb import DBConnectionPool
from typing import Any, Iterable
from scrapy.http import Request, Response
from wallpaper_scrapy.items import BingScrapyItem
from fake_useragent import UserAgent
from scrapy_splash import SplashRequest


class WallpaperBingAPISpider(scrapy.Spider):
    name = 'natgeomedia'
    host = 'https://www.natgeomedia.com'

    start_urls = ['https://www.natgeomedia.com/']
    def start_requests(self):
        print("start_requests")
        for url in self.start_urls:
            print(url)
            yield Request(url=url, callback=self.parse_home)


    def parse_home(self, response):
        path = '/html/body/header/div/a/@href'
        pic_url = response.xpath(path).extract_first()
        author_values = response.xpath('/html/body/header/div/a/p/text()[2]').get()
        self.author_value = author_values.split("：")[-1]

        yield Request(url=pic_url, callback=self.parse_detail)


    def parse_detail(self, response):
        title_values = response.xpath('//meta[@property="og:title"]/@content').getall()
        title_value = title_values[0]
        desc_values = response.xpath('//meta[@property="og:description"]/@content').getall()
        desc_value = desc_values[0]
        image_values = response.xpath('//meta[@property="og:image"]/@content').getall()
        image_value = image_values[0]
        tag_values = response.xpath('//meta[@name="keywords"]/@content').getall()
        tag_value = tag_values[0]
        triviaId = self.author_value + "_" + image_value.split("/")[-1].split(".")[0]
        triviaId = triviaId.replace(" ", "_")

        print(f"title: {title_value}")
        print(f"content: {desc_value}")
        print(f"image_url: {image_value}")
        print("tag: ", tag_value)
        print("author: ", self.author_value)
        print("triviaId: ", triviaId)

        # 判断数据库中是否有 triviaId 数据
        db_pool = DBConnectionPool()
        count = db_pool.is_exists(triviaId)
        if count == 1:
            print(f"{triviaId} is exists")
            return


        item_data = {
            'platform': 'netgeomedia',
            'mkt': 'zh-CN',
            'title': title_value,
            'tag': tag_value,
            'desc': desc_value,
            'copyright': self.author_value,
            'image_urls': [image_value],
            'trivia_id': triviaId
        }

        yield item_data



