# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RecipeItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    thumbnail = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    summary = scrapy.Field()
    info_size = scrapy.Field()
    info_time = scrapy.Field()
    info_difficulty = scrapy.Field()
    ingredients_main = scrapy.Field()
    ingredients_sub = scrapy.Field()
    video_url = scrapy.Field()
    steps = scrapy.Field()
    tip = scrapy.Field()
    tags = scrapy.Field()
    pass

class StepItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()