import time
import re
import scrapy
from scrapy import FormRequest, Request
import json
from ..items import Site2Item

class Site2Spider(scrapy.Spider):
    name = "site2"
    allowed_domains = ["collections.artsmia.org","new.artsmia.org","iiif.dx.artsmia.org"]
    # start_urls = (
    #https://artstories.artsmia.org/#/o/1854
    #https://iiif.dx.artsmia.org/1854.jpg/info.json
    #https://search.artsmia.org/id/1854
    #https://6.api.artsmia.org/1854.jpg
    # )

    def parse(self, response, *args, **kwargs):

        print("\n正在访问:", response.url, "获取到%d字节信息"%(len(response.body)) ,"\n")

        data = json.loads(response.body)
        # print(data)
        id = re.compile("id/(\d*)").findall(response.url)[0]

        items = []
        item = Site2Item()

        item["id"] = data["id"]
        item["title"] = data["title"]
        item["dated"] = data["dated"]
        item["artist"] = data["artist"]
        item["role"] = data["role"]
        item["department"] = data["department"]
        item["medium"] = data["medium"]

        item["country"] = data["country"]

        item["description"] = data["description"]
        item["comments"] = data["text"]

        item["web_url"] = "https://collections.artsmia.org/art/%s" % (data["id"])
        item["img_url"] = "https://6.api.artsmia.org/%s.jpg"%(data["id"])

        item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        if data["country"] == "China" or data["country"] == "china":
            yield item
        else:
            print("Ignore place %s" % (data["country"]))

    def start_requests(self):
        base_url = "https://search.artsmia.org/id/"
        for i in range(2000):
            url = base_url + str(i)
            yield Request(url)




