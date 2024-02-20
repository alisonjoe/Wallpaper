import os
import time
from scrapy import signals
from datetime import datetime, timezone, timedelta
from scrapy.utils.project import get_project_settings


class MarkdownMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.files_downloaded, signal=signals.item_scraped)
        return middleware

    def files_downloaded(self, item, response, spider):
        # 在每次下载完成后触发
        self.create_md(item, spider)


    def create_md(self, item, spider):

        # 获取当前时间
        current_time = datetime.now(timezone(timedelta(hours=8)))  # 东八区时区
        # 格式化时间为指定格式
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        settings = get_project_settings()
        md_filename = os.path.join(settings.get('BLOG_STORE'), f"{item['trivia_id']}.md")
        markdown_content = f"""---
author: "AlisonLai"
title: "{item['title']}"
date: {formatted_time}
description: ""
tags: ["{item['tag']}"]
copyright: {item['copyright']}
thumbnail: /{item['platform']}/{item['trivia_id']}.jpg
---
图文来源自：{item['platform']}.  copyright: {item['copyright']}

{item['desc']}

![{item['trivia_id']}](/{item['platform']}/{item['trivia_id']}.jpg)"""
        print(md_filename)
        with open(md_filename, 'w') as f:
            f.write(markdown_content)
