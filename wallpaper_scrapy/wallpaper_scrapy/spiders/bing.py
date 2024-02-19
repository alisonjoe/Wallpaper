import scrapy
import re
import json
from typing import Any, Iterable
from scrapy.http import Request, Response
from wallpaper_scrapy.items import BingScrapyItem
from fake_useragent import UserAgent
from scrapy_splash import SplashRequest
from wallpaper_scrapy.mariadb import DBConnectionPool


class WallpaperBingSpider(scrapy.Spider):
    name = 'bing'
    host = 'https://cn.bing.com'
    start_urls = [
        'https://cn.bing.com/?FORM=BEHPTB',
        'https://cn.bing.com/?FORM=BEHPTB&ensearch=1'
    ]


    def start_requests(self):
        for url in self.start_urls:
            #yield SplashRequest(url=url, callback=self.parse, args={'wait': 6, 'timeout':60})
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        context_xpath='/html/body/script/text()'
        desc = response.xpath(context_xpath).getall()
        # print(type(desc))
        # 从 JavaScript 代码中提取 _model 对象的内容
        javascript_code = ''.join(desc)
        pattern = re.compile(r'_model\s*=\s*({.*?});', re.DOTALL)
        match = pattern.search(javascript_code)
        if match:
            # 匹配到了 _model 对象的内容
            model_data = match.group(1)
    
            # 解析 JSON 数据
            model_json = json.loads(model_data)
    
            # 获取 MediaContents 部分的内容
            media_contents = model_json.get('MediaContents', [])

            #print(type(media_contents))
            # [{'ImageContent': {'Description': '普拉格斯湖坐落在雄伟的多洛米蒂山脉中，是阿尔卑斯山的一颗明珠，也被称为布莱耶斯湖。湖水清澈见底，倒映着多洛米蒂山壮丽伟岸的白云岩，四周环绕着郁郁葱葱的森林。湖边有一条风景优美的小径，在气候温和的时节吸引着众多游客前来远足和散步。夏季，这里是乘船休闲的好去处；冬季，湖光山色成了一幅浓郁的瑰画散发着魅力。普拉格斯湖把自然美景、历史与文化完美融合，矗立一旁的圣维特小教堂见证了它的过去。这个“拥有世上最美的高山景观”的迷人地方将为你带来难忘的体验。', 'Image': {'Url': '/th?id=OHR.LakeDolomites_ZH-CN2317113886_1920x1080.webp', 'Wallpaper': '/th?id=OHR.LakeDolomites_ZH-CN2317113886_1920x1200.jpg&rf=LaDigue_1920x1200.jpg', 'Downloadable': True}, 'Headline': '自然奇景', 'Title': '多洛米蒂山的布莱耶斯湖，南蒂罗尔，意大利', 'Copyright': '© Marco Bottigelli/Getty Images', 'SocialGood': None, 'MapLink': {'Url': '', 'Link': ''}, 'QuickFact': {'MainText': '湖水清澈碧绿，闻名遐迩。', 'LinkUrl': '', 'LinkText': ''}, 'TriviaUrl': '/search?q=Bing+homepage+quiz&filters=WQOskey:"HPQuiz_20240217_LakeDolomites"&FORM=HPQUIZ', 'BackstageUrl': '/search?q=%e5%b8%83%e8%8e%b1%e8%80%b6%e6%96%af%e6%b9%96&form=hpcapt&filters=HpDate:"20240216_1600"', 'TriviaId': 'HPQuiz_20240217_LakeDolomites'}, 'AudioContent': None, 'VideoContent': None, 'Ssd': '20240216_1600', 'FullDateString': '2月 17, 2024'}]
            # 打印 MediaContents 部分
            for item in media_contents:
                #print(type(item))
                self.description = item.get('ImageContent', '').get('Description', '')
                self.tag = item.get('ImageContent', '').get('Headline', '')
                self.copyright = item.get('ImageContent', '').get('Copyright', '')
                self.title = item.get('ImageContent', '').get('Title', '')
                triviaId = item.get('ImageContent', '').get('TriviaId', '').split("_")
                #HPQuiz_20240218_DominicaWhales
                self.triviaId = triviaId[2]
                image_url = 'https://bing.com' + item.get('ImageContent', '').get('Image', '').get('Wallpaper', '')
                # 删掉rf=xxx
                new_url = re.sub(r"&rf=[^&]+", "", image_url)
                self.image_urls = [new_url.replace("_1920x1200.jpg", "_UHD.jpg")]

        else:
            print("No match found.")

        # 判断数据库中是否有 triviaId 数据
        db_pool = DBConnectionPool()
        count = db_pool.is_exists(triviaId)
        if count == 1:
            print(f"{triviaId} is exists")
            return

        item_data = {
            'platform': 'bing',
            'title': self.title,
            'tag': self.tag,
            'mkt':'bing-cn',
            'desc': self.description,
            'copyright': self.copyright,
            'image_urls': self.image_urls,
            'trivia_id': self.triviaId
        }
        print(item_data)

        yield item_data