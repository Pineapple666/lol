# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LolItem(Item):
    """

    """
    collection=table='skins'
    hero_name = Field()
    skin_name = Field()
    image_url = Field()
