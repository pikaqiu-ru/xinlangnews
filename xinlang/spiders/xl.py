# -*- coding: utf-8 -*-
import scrapy
from ..items import XinlangItem
import os


class XlSpider(scrapy.Spider):
    name = 'xl'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # items = []
        #所有大类的url和标题
        parentUrls = response.xpath('//div[@class="clearfix"]/h3/a/@href').extract()
        parentTitle = response.xpath('//div[@class="clearfix"]/h3/a/text()').extract()

        #所有小类的url和标题
        subUrls = response.xpath('//div[@class="clearfix"]/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@class="clearfix"]/ul/li/a/text()').extract()

        #爬取所有大类
        for i in range(0, len(parentTitle)):
            #指定大类目录的路径和目录名
            parentFilename = './Data1/' + parentTitle[i]

            #如果目录不存在，则创建路径
            if not os.path.exists(parentFilename):
                os.makedirs(parentFilename)

            items = []
            #爬取所有小类
            for j in range(0, len(subUrls)):
                item = XinlangItem()

                #保存大类的urls
                item['parentUrls'] = parentUrls[i]

                #检查小类的url是否以同类别大类url开头，如果是返回True（sports.com.cn和sports.sina.com.cn/nba）
                if_belong = subUrls[j].startswith(parentUrls[i])

                #如果属于本大类，将储存目录放在本大类目录下
                if(if_belong):
                    subFilename = parentFilename + '/' + subTitle[j]
                    #如果目录不存在，则创建目录
                    if (not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    #存储小类filename字段数据
                    item['subUrls'] = subUrls[j]
                    item['subFilename'] = subFilename
                    # print(f"子类链接为{subUrls[j]}")
                    items.append(item)
            for it in items:
                yield scrapy.Request(url=it['subUrls'], meta={'meta_1': it}, callback=self.second_parse)

    def second_parse(self, response):
        #提取每次response的metal数据
        meta_1 = response.meta['meta_1']

        #取出小类里所有子链接
        sonUrls = response.xpath('//a/@href').extract()

        items = []
        print(f"小类的连接数目是{len(sonUrls)}")
        for i in range(0, len(sonUrls)):
            #检查每个链接是否以大类url开头，以.shtml结尾，如果返回Ture
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            #如果属于本大类，获取字段值放在同一个item下便于传输
            if (if_belong):
                item = XinlangItem()
                item['parentUrls'] = meta_1['parentUrls']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                # print(f"子之类链接为{item['sonUrls']}")
                items.append(item)
        for ie in items:
            yield scrapy.Request(url=ie['sonUrls'], meta={'meta_2': ie}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ''
        print(f'当前连接的地址是{response.url}')
        content_list = response.xpath('//div[@id="artibody"]//text()').extract()
        if len(content_list) == 0:
            content_list = response.xpath('//div[@id="article"]//text()').extract()
        print(f'长度为{len(content_list)}')

        #将p标签里的文本内容合并到一起
        for content_one in content_list:
            content += content_one
        print(content)
        head = response.xpath('//h1[@id="artibodyTitle"]//text()').extract()[0]

        if len(head) == 0:
            head = response.xpath('//h1[@class="main-title"]/text()').extract()[0]
        item['head'] = head
        item['content'] = content
        yield item

