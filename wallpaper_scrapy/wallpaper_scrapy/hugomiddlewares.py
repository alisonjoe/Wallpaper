import os
import subprocess
from scrapy import signals
from scrapy.utils.project import get_project_settings


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
        subprocess.run(["rm", "-rf", "docs"], cwd=working_directory)
        subprocess.run(["hugo", "--gc", "-d", "docs"], cwd=working_directory)
        subprocess.run(["git", "add", "."], cwd=working_directory)
        subprocess.run(["git", "commit", "-m", "auto add wallpaper"], cwd=working_directory)
        subprocess.run(["git", "push", "origin"], cwd=working_directory)





# 添加文件到暂存区
def git_add(file_path):
    subprocess.run(["git", "add", file_path])

# 提交暂存区的更改
def git_commit(message):
    subprocess.run(["git", "commit", "-m", message])

# 推送更改到远程仓库
def git_push():
    subprocess.run(["git", "push"])
