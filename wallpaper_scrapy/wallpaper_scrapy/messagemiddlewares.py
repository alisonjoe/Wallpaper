# FILEPATH
from scrapy import signals
from wechat_work import WechatWork


class WeworkMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.files_downloaded, signal=signals.item_scraped)
        return middleware

    def __init__(self):
        corpid = 'xxxx'
        appid = 'xxxx'
        corpsecret = 'xxx'
        self.w = WechatWork(corpid=corpid,
                            appid=appid,
                            corpsecret=corpsecret)

    def files_downloaded(self, item, response, spider):
        print('files_downloaded called send message')
        # 在每次下载完成后触发
        self.process_item(item, spider)

    def process_item(self, item, spider):
        self.w.send_text(f"壁纸 {item['platform']} - {item['title']} 下载成功, https://alisonjoe.github.io/", ['@all'])
        return item
