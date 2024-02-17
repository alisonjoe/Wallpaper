# Scrapy settings for wallpaper_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from fake_useragent import UserAgent

LOG_FILE = 'scrapy.log'
# 配置日志级别，可以选择 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
LOG_LEVEL = 'DEBUG'
# 配置日志格式
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 配置日志时间格式
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

BOT_NAME = "wallpaper_scrapy"

SPIDER_MODULES = ["wallpaper_scrapy.spiders"]
NEWSPIDER_MODULE = "wallpaper_scrapy.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = UserAgent().random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SPLASH_URL = 'http://192.168.1.105:8050'


# 用来支持cache_args（可选）
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}


# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'wallpaper_scrapy.markdownmiddlewares.MarkdownMiddleware': 888,  # Adjust the priority as needed
    'wallpaper_scrapy.hugomiddlewares.HugoMiddleware': 889, 


    #设置不参与scrapy的自动重试的动作
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware':None
}

# 设置去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'wallpaper_scrapy.pipelines.WallpaperImgDownloadPipeline': 300
}

WALLPAPER_BASE="/app/Wallpaper"
IMAGES_STORE="/app/Wallpaper/static"
BLOG_STORE="/app/Wallpaper/content/blog"
#WALLPAPER_BASE="/Users/alison/WorkSpace/Wallpaper/"
#IMAGES_STORE="/Users/alison/WorkSpace/Wallpaper/static"
#BLOG_STORE="/Users/alison/WorkSpace/Wallpaper/content/blog"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

HTTPERROR_ALLOWED_CODES = [403]
