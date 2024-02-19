import os
import pymysql
import subprocess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from wallpaper_scrapy.mariadb import DBConnectionPool
from jinja2 import Template


class HugoMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.files_downloaded, signal=signals.item_scraped)
        return middleware

    def files_downloaded(self, item, response, spider):
        # 在每次下载完成后触发
        self.hugo_gen_html(item, spider)

    def hugo_gen_html(self, item, spider):
        settings = get_project_settings()
        working_directory = settings.get('WALLPAPER_BASE')

        self.hugo_gen_toml(item, working_directory)
        self.hugo_gen(working_directory)
        msg = f"auto add {item['platform']} {item['title']}"
        self.push_github(msg, working_directory)
        if item['trivia_id'] == "":
            return
        try:
            db_pool = DBConnectionPool()
            db_pool.insert_wallpaper(item['trivia_id'], item['image_urls'],
                                     item['mkt'], item['platform'])
        except pymysql.Error as e:
            # 打印异常信息或者记录日志
            spider.logger.error(f"Error: {e}")

    def hugo_gen_toml(self, item, cwd_path):
        # 读取 TOML 模板文件
        with open(f"{cwd_path}/tpl/hugo.tpl", "r") as f:
            template_str = f.read()

        # 创建 Jinja2 模板对象
        template = Template(template_str)

        # 定义填充模板所需的数据
        data = {
            "last_title": f"{item['title']}",
            "last_desc": f"{item['desc']}",
            "last_wallpaper": f"/{item['platform']}/{item['trivia_id']}.jpg",
        }

        # 填充模板并生成 TOML 内容
        toml_content = template.render(**data)

        # 将生成的 TOML 内容写入文件
        with open(f"{cwd_path}/hugo.toml", "w") as f:
            f.write(toml_content)

    def hugo_gen(self, cwd_path):
        subprocess.run(["rm", "-rf", "docs"], cwd=cwd_path)
        subprocess.run(["hugo", "--gc", "-d", "docs"], cwd=cwd_path)

    def push_github(self, msg, cwd_path):
        subprocess.run(["git", "add", "."], cwd=cwd_path)
        subprocess.run(["git", "commit", "-m", msg], cwd=cwd_path)
        subprocess.run(["git", "push", "origin"], cwd=cwd_path)
