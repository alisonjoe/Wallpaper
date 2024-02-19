import pymysql
from enum import Enum
from dbutils.pooled_db import PooledDB



class DBConnectionPool:
    _instance = None

    def __init__(self):
        self.connection = self.pool.connection()


    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DBConnectionPool, cls).__new__(cls)
            cls._instance.pool = cls.create_connection_pool()
        return cls._instance

    @staticmethod
    def create_connection_pool():
        # 这里使用 dbutils.pooled_db 中的 PooledDB 来创建连接池
        return PooledDB(
            creator=pymysql,  # 使用 pymysql 作为连接库
            maxconnections=10,  # 最大连接数
            mincached=2,  # 最小空闲连接数
            maxcached=5,  # 最大空闲连接数
            maxshared=3,  # 最大共享连接数
            blocking=True,  # 连接池满时是否阻塞
            maxusage=None,  # 单个连接最大使用次数，None 表示无限制
            setsession=[],  # 每次连接时执行的 SQL 语句
            ping=0,  # 检查连接是否有效
            host='192.168.1.105',
            port=33006,  # 你的自定义端口号
            user='root',
            password='*****',
            database='scrapy_manga',
            charset='utf8mb4'
        )



    def is_exists(self, triviaId):
        """
        判断wallpaper_url是否存在
        :param trivia_id : 壁纸ID
        :return: 存在返回1，不存在返回0
        """
        with self.connection.cursor() as cursor:
            sql = """
            SELECT EXISTS(SELECT * FROM wallpaper WHERE trivia_id = %s)
            """
            cursor.execute(sql, (triviaId))
            total_urls = cursor.fetchone()[0]
        return total_urls


    def insert_wallpaper(self, triviaId, wallpaper_url, mkt, platform):
        """
        插入壁纸信息
        :param wallpaper_url: 壁纸URL
        :param mkt: 市场
        :param platform: 平台
        :return:
        """
        with self.connection.cursor() as cursor:
            sql = """
            INSERT INTO wallpaper(trivia_id, wallpaper_url, mkt, platform) VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (triviaId, wallpaper_url, mkt, platform))
        self.connection.commit()
