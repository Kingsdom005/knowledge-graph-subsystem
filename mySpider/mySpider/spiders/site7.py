import time
import scrapy
from scrapy import FormRequest, Request
import json
from ..items import Site2Item
class Site7Spider(scrapy.Spider):
    name = "site7"
    allowed_domains = ["www.vam.ac.uk","collections.vam.ac.uk/"]
    # start_urls = ["http://www.vam.ac.uk/"]
    # https://collections.vam.ac.uk/item/id
    # https://api.vam.ac.uk/v2/objects/search?page=n&page_size=15

    def parse(self, response, *args, **kwargs):
        print("\n进入parse layer\n")
        datas = json.loads(response.body)
        # print(datas,"\n\n")
        for data in datas['records']:
            next_url = "https://api.vam.ac.uk/v2/object/%s"%(data["systemNumber"])
            if data["_primaryPlace"] == "China":
                yield Request(url=next_url, callback=self.parse_second,meta={"dated":data['_primaryDate'],"place":data['_primaryPlace']}, dont_filter=True) # 必须添加dont_filter防止忽略url
            else:
                print("Ignore place %s"%(data["_primaryPlace"]))

    def start_requests(self):
        for i in range(666): # 请求前100页数据
            url = "https://api.vam.ac.uk/v2/objects/search?page=%s&page_size=15"%(str(i))
            yield Request(url)

    def parse_second(self, response):
        print("\nsecond layer parse,with meta",response.meta,"\n")
        data = json.loads(response.body)
        # print("\ndata=",data,"\n")
        item = Site2Item()
        item["id"] = data['record']["systemNumber"]
        item["title"] = data['record']["titles"][0]['title'] # 取第一个标题
        item["dated"] = response.meta["dated"]

        artist = ""
        for i in data['record']["artistMakerPerson"]:
            artist += i['name']['text'] + ";"
        item["artist"] = artist
        # item["artist"] = data['record']["artistMakerPerson"][0]['name']['text']  # bug 多个作者

        item["role"] = data['record']["objectType"] #类型
        item["department"] = data["meta"]['images']['_images_meta'][0]['copyright']

        material = ""
        for i in data['record']["materials"]:
            material += i['text'] + ";"
        item["medium"] = material
        # item["medium"] = data['record']["materials"][0]['text']  # bug
        item["country"] = response.meta['place']

        item["description"] = data['record']["summaryDescription"]
        item["comments"] = data['record']["materialsAndTechniques"]

        item["web_url"] = "https://collections.vam.ac.uk/item/%s" % (data['record']["systemNumber"])
        item["img_url"] = data['meta']['images']['_primary_thumbnail']

        item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        yield item
