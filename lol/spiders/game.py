# -*- coding: utf-8 -*-
from lol.items import LolItem
from scrapy import Request, Spider
import json


class GameSpider(Spider):
    name = 'game'
    allowed_domains = ['game.gtimg.cn']
    start_urls = ['https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js']

    def parse(self, response):
        """

        :param response:
        :return:
        """
        if 'skins' in json.loads(response.text):
            for skin in json.loads(response.text)['skins']:
                item = LolItem()
                item['hero_name'] = skin['heroName']
                item['skin_name'] = skin['name']
                if skin['mainImg']!='':
                    item['image_url'] = skin['mainImg']
                    yield item
        else:
            base_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero'
            for hero in json.loads(response.text)['hero']:
                hero_id = hero['heroId']
                yield Request(url=f'{base_url}/{hero_id}.js', callback=self.parse)
