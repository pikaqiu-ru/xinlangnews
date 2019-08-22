# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys


class XinlangItem(scrapy.Item):
    #大类标题和url
    # parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    #小类标题和子url
    # subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    #小类目录存储路径
    subFilename = scrapy.Field()

    #小类下的子连接
    sonUrls = scrapy.Field()

    #文章标题和内容
    head = scrapy.Field()
    content = scrapy.Field()