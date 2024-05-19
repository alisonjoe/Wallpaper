import os
import time
import asyncio
from scrapy import signals
from datetime import datetime, timezone, timedelta
from scrapy.utils.project import get_project_settings
import baidu_translate as fanyi
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from wallpaper_scrapy.aitagmiddlewares import AitagMiddlewares


class MarkdownMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.files_downloaded, signal=signals.item_scraped)
        return middleware


    def files_downloaded(self, item, response, spider):
        # 在每次下载完成后触发
        d = Deferred()
        reactor.callFromThread(self.create_md, item, spider, d)
        d.addCallback(self.on_md_created)
        d.addErrback(self.on_error)


    def create_md(self, item, spider, d):
        try:
            aitag = AitagMiddlewares(
                'xxxxx',
                'xxxxx',
                'xxxxx',
                'xxxxx',
            )

            tags = aitag.extract_key_phrases(item['desc'])
            print(tags)
            current_time = datetime.now(timezone(timedelta(hours=8)))  # 东八区时区
            # 格式化时间为指定格式
            formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
            settings = get_project_settings()
            md_filename = os.path.join(settings.get('BLOG_STORE'), f"{item['trivia_id']}.md")
            title = yield fanyi.translate_text({item['title']}, to=fanyi.Lang.ZH)
            desc = yield fanyi.translate_text({item['desc']}, to=fanyi.Lang.ZH)
            markdown_content = f"""---
author: "AlisonLai"
title: {title}
date: {formatted_time}
description: ""
tags: ["{item['tag']}"]
copyright: {item['copyright']}
thumbnail: /{item['platform']}/{item['trivia_id']}.jpg
---
图文来源自：{item['platform']}.  copyright: {item['copyright']}

{desc}

![{item['trivia_id']}](/{item['platform']}/{item['trivia_id']}.jpg)"""
            print(md_filename)
            with open(md_filename, 'w') as f:
                f.write(markdown_content)
            d.callback(md_filename)
        except Exception as e:
            print(e)
            raise e 


    def on_md_created(self, result):
        print(f"Markdown file created: {result}")

    def on_error(self, failure):
        print(f"An error occurred: {failure.getErrorMessage()}")
