# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import pymongo
import pymysql


class MongoPipeline:
    """

    """

    def __init__(self, mongo_uri, mongo_db):
        """

        :param mongo_uri:
        :param mongo_db:
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """

        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.client.close()


class MysqlPipeline:
    """

    """

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        """

        :param crawler:
        :return:
        """
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.db.close()

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        yield item


class ImagePipeline(ImagesPipeline):
    """

    """

    def file_path(self, request, response=None, info=None):
        """

        :param request:
        :param response:
        :param info:
        :return:
        """
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        """

        :param results:
        :param item:
        :param info:
        :return:
        """
        images_path = [x['path'] for ok, x in results if ok]
        if not images_path:
            raise DropItem('Image Download Failed')
        return item

    def get_media_requests(self, item, info):
        """

        :param item:
        :param info:
        :return:
        """
        yield Request(item['image_url'])
