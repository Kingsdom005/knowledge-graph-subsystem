import json, time
import scrapy
from scrapy import FormRequest, Request

from ..items import Site2Item


class Site12Spider(scrapy.Spider):
    name = "site12"
    allowed_domains = ["www.nga.gov"]

    ERROR_COUNT = 0
    PASS_COUNT = 0
    SUCCESS_COUNT = 0
    TOTAL_COUNT = 0
    f = None

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
        success_local_count = 0
        pass_local_count = 0
        # print("\n\n", len(data), data, "\n\n")
        for i in range(len(data)): # 0下标可能不是数据
            # print(data[i])
            try:
                item["id"] = data[i]["id"]
                item["title"] = data[i]["title"]
                item["dated"] = data[i]["displaydate"]
                # item["artist"] = data["artist"]
                artist = ""
                for j in data[i]['artists']:
                    artist += j['name'] + ";"
                item["artist"] = artist

                item["role"] = data[i]["classification"]
                item["department"] = "National Gallery of Art"  # 美国国家博物馆 data["department"]
                item["medium"] = data[i]["medium"]

                item["country"] = "china"  # 描述的中国作品 data["country"]
                item["description"] = data[i]["creditline"]
                item["comments"] = ""  # data["text"]

                item["onview"] = data[i]['onview']

                item["web_url"] = "https://collections.artsmia.org/art/{}".format(str(data[i]["id"]))
                item["img_url"] = data[i]["imagepath"]

                item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                self.SUCCESS_COUNT+=1
                self.TOTAL_COUNT+=1

                success_local_count += 1
                # self.set_log(msg="Crawl {}: Success.".format(response.url))
                yield item
            except Exception as e:
                pass_local_count += 1
                self.PASS_COUNT+=1
                self.TOTAL_COUNT += 1
        self.set_log(msg="Crawl {}: with {} success and {} pass.".format(response.url, success_local_count, pass_local_count))
        # self.set_log(msg="Crawl {}: Error. Error msg as {}".format(response.url, e))


    def start_requests(self):

        with open("save/12.json","w") as ff:
            ff.close()

        itemCount = 860 # max 860
        pageSize = 30
        maxPage = (int)(itemCount/pageSize) + 1 # 28+1
        self.f = open("save/site12_log.txt", "w", encoding="utf-8")
        for i in range(1,maxPage):
            url = "https://www.nga.gov/global-site-search-page/jcr:content/parmain/facetcomponent/parList/global_sitesearch_result.pageSize__%s.pageNumber__%s.json?searchterm=china&_=1682083002327"%(str(pageSize),str(i))
            yield Request(url)

    def set_log(self, msg):
        # write file
        self.f.write(msg+" ["+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"]\n")
        #print(self.TOTAL_COUNT)
        # output to screen
        if self.TOTAL_COUNT == 840:
            # output to screen
            info = "\n\n##########################################\n\n" \
                  "Error-{} Pass-{} Success-{} Total-{}\n\n" \
                  "##########################################\n".format(self.ERROR_COUNT, self.PASS_COUNT, self.SUCCESS_COUNT, self.TOTAL_COUNT)
            print(info)
            # close file
            self.f.write(info)
            self.f.close()
