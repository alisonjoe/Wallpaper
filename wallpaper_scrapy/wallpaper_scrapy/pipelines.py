# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from fake_useragent import UserAgent

class WallpaperImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'referer': 'https://www.baidu.com',
        'user-agent': UserAgent().random,
    }

    def file_path(self, request, response=None, info=None):
        # 获取文件夹名称和图片编号
        folder_name = '%s' % (request.meta['platform'])
        # 构造自定义的文件路径
        return os.path.join(folder_name, '%s.jpg' % (request.meta['trivia_id']))

    def get_media_requests(self, item, info):
        image_urls = item.get('image_urls', [])
        print("===========================1=")
        print(image_urls)
        print("===========================2=")
        if not isinstance(image_urls, (list, tuple)):
            # 如果 image_urls 不是列表或元组，可以根据实际情况进行处理
            image_urls = [image_urls]

        valid_urls = [url for url in item.get('image_urls', []) if url.startswith('http')]
        print("===========================4=")
        print(valid_urls)
        print(item.get('image_urls', ['no']))
        print("===========================5=")
        #return [Request(url='https://bing.com/th?id=OHR.LakeDolomites_EN-CN3403215959_UHD.jpg', meta={'platform': item['platform'], 'trivia_id': item['trivia_id']})]
        return [Request(url, meta={'platform': item['platform'], 'trivia_id': item['trivia_id']})
                for url in valid_urls]

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

