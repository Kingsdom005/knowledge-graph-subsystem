import json, time
import scrapy
from scrapy import FormRequest, Request

from ..items import Site2Item


class Site12Spider(scrapy.Spider):
    name = "site12"
    allowed_domains = ["www.nga.gov"]
    # start_urls = ["https://www.nga.gov/exhibitions/2023/going-through-hell-divine-dante.html"] #"https://www.nga.gov/",

    # img = https://media.nga.gov/iiif/bc6196b4-e6c8-476a-9e37-754e1394eb43/full/!400,/0/default.jpg
    # https://media.nga.gov/iiif/1ff7cdea-f23a-4158-bb9a-ede300b87574/full/full/0/default.jpg?attachment_filename=hunting_scene_with_a_pond_1970.17.102.jpg
    # https://media.nga.gov/iiif/c771e519-15ae-4f89-a8f6-b382dc655d70/full/full/0/default.jpg?attachment_filename=christ_on_the_road_to_emmaus_1966.13.6.jpg
    # https://www.nga.gov/collection/art-object-page.43715.html
    # https://www.nga.gov/collection/art-object-page.43716.html

    def parse(self, response, *args, **kwargs):
        print("\n正在访问:", response.url, "获取到%d字节信息" % (len(response.body)), "\n")
        data = json.loads(response.body)
        # print("\n\n",len(data['results']),"\n\n")
        data = data['results']
        items = []
        item = Site2Item()
        # print("\n\n", len(data), data, "\n\n")
        for i in range(1, len(data)): # 0下标不是数据
            print(data[i])
            if not data[i]["id"]:
                continue
            item["id"] = data[i]["id"]
            item["title"] = data[i]["title"]
            item["dated"] = data[i]["displaydate"]
            # item["artist"] = data["artist"]
            artist = ""
            for j in data[i]['artists']:
                artist += j['name'] + ";"
            item["artist"] = artist

            item["role"] = data[i]["classification"]
            item["department"] = "National Gallery of Art" # 美国国家博物馆 data["department"]
            item["medium"] = data[i]["medium"]

            item["country"] = "china"  # 描述的中国作品 data["country"]
            item["description"] = data[i]["creditline"]
            item["comments"] = "" # data["text"]

            item["onview"] = data[i]['onview']

            item["web_url"] = "https://collections.artsmia.org/art/{}".format(str(data[i]["id"]))
            item["img_url"] = data[i]["imagepath"]

            item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            yield item


    def start_requests(self):
        itemCount = 860
        pageSize = 30
        maxPage = (int)(itemCount/pageSize) + 1

        for i in range(1,maxPage):

            url = "https://www.nga.gov/global-site-search-page/jcr:content/parmain/facetcomponent/parList/global_sitesearch_result.pageSize__%s.pageNumber__%s.json?searchterm=china&_=1682083002327"%(str(pageSize),str(i))
            yield Request(url)

