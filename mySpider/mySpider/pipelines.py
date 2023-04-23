# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyspiderPipeline:

    # 爬虫打开后
    def spider_open(self, spider):
        print("爬虫打开")
        pass

    # 爬虫关闭后
    def spider_close(self, spider):
        print("爬虫关闭")
        pass

    def process_item(self, item, spider):
        return item
