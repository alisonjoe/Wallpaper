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
        author_value = response.xpath('/html/body/header/div/a/p/text()[2]').get()
        # 删除最前面的空格
        author_value = author_value.lstrip()
        self.author_value = author_value.split("：")[-1]
        # 选择 <header> 元素
        header_element = response.css('header.index-kv')
        # 从 style 属性中提取 background 属性的值
        style_value = header_element.xpath('./@style').get()
        # 提取背景图片的 URL
        background_url = self.extract_background_url(style_value)
        self.logger.info("Background URL: %s", background_url)
        self.image_url = background_url

        yield Request(url=pic_url, callback=self.parse_detail)

    def extract_background_url(self, style_value):
        # 从 style 属性中提取 background 属性的值
        # 示例中假设 background 属性总是在第一个分号之前
        background_index = style_value.find('background')
        semicolon_index = style_value.find(';')
        background_value = style_value[background_index:semicolon_index]

        # 提取 URL
        print("background_value: ", background_value)
        url_start_index = background_value.find('url(')
        url_end_index = background_value.find(')')
        background_url = background_value[url_start_index + 4:url_end_index]

        return background_url

    def parse_detail(self, response):
        title_values = response.xpath('//meta[@property="og:title"]/@content').getall()
        title_value = title_values[0]
        desc_values = response.xpath('//meta[@property="og:description"]/@content').getall()
        desc_value = desc_values[0]
        image_value = self.image_url
        tag_value = "natgeomedia"
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
        else:
            print(f"{triviaId} is not exists")


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



