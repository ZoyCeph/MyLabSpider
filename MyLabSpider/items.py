# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()   
    #pass
    author=scrapy.Field()
    content=scrapy.Field()
    source=scrapy.Field()
    like=scrapy.Field()
    transfer=scrapy.Field()
    comment=scrapy.Field()
    
class CommentItem(scrapy.Item):
    author=scrapy.Field()
    reply=scrapy.Field()
    content=scrapy.Field()
    like=scrapy.Field()
    source=scrapy.Field()
    collection_name=scrapy.Field()