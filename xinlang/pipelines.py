# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys


class XinlangPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
        # sonUrls = item['sonUrls']
        #
        # #文件名为子链接url中间部分，并将/替换为_,保存为.txt格式
        # filename = sonUrls[7:-6].replace('/','_')
        filename = item['head']
        filename += '.txt'
        fp = open(item['subFilename'] + '/'+filename, 'w', encoding='utf8')
        print(item['content'])
        fp.write(item['content'])
        fp.close()
        return item

