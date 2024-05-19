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
    name = 'bing_api'
    host = 'https://cn.bing.com'
    bing_template = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp&FORM=BEHPTB&uhd=1&setmkt=%s&setlang=en"
    mkts = ["en-US","zh-CN","ja-JP","en-IN","pt-BR", "fr-FR", "de-DE", "en-CA", "en-GB", "it-IT", "es-ES", "fr-CA"]

    start_urls = []
    for mkt in mkts:
        start_urls.append(bing_template % mkt)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        url = response.url
        # urlparse 解析url中的mkt参数, url中的mkt参数格式为 setmkt=xx-XX
        parsed = urlparse(url)
        query = parsed.query
        query_dict = parse_qs(query)
        mkt = query_dict.get('setmkt', [''])[0]

        jsonStr = json.loads(response.text)
        imageJson = jsonStr['images'][0]
        urlbase = imageJson.get('urlbase', '')
        # urlbase =  '/th?id=OHR.DominicaWhales_EN-IN1231273818'
        # urlbase 用 . 和 _ 作为分隔符，获取 DominicaWhales
        split_pattern = r'[._]'
        s = re.split(split_pattern, urlbase)
        triviaId = s[1]
        wallpaper_url = f"https://cn.bing.com{urlbase}_UHD.jpg"
        desc = imageJson.get('desc', 'have no desc')
        copyrightStr = imageJson.get('copyrightonly', '')
        tag = imageJson.get('title', '')
        title = imageJson.get('copyright', '')

        # 判断数据库中是否有 triviaId 数据
        db_pool = DBConnectionPool()
        count = db_pool.is_exists(triviaId)
        if count == 1:
            print(f"{urlbase} is exists")
            return


        item_data = {
            'platform': 'bing',
            'mkt': mkt,
            'title': title,
            'tag': tag,
            'desc': desc,
            'copyright': copyrightStr,
            'image_urls': [wallpaper_url],
            'trivia_id': triviaId
        }

        yield item_data
