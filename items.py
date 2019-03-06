# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RecipeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    thumbnail = scrapy.Field()
    image_url = scrapy.Field()
    image = scrapy.Field()
    summary = scrapy.Field()
    info_size = scrapy.Field()
    info_time = scrapy.Field()
    info_difficulty = scrapy.Field()
    ingredients_main = scrapy.Field()
    ingredients_sub = scrapy.Field()
    video_url = scrapy.Field()
    steps_text = scrapy.Field()
    steps_image_url = scrapy.Field()
    steps_image = scrapy.Field()
    tip = scrapy.Field()
    tags = scrapy.Field()
    pass
