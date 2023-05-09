import time
import scrapy
from scrapy import FormRequest, Request
import json
from ..items import Site2Item
import os
class Site7Spider(scrapy.Spider):
    name = "site7"
    allowed_domains = ["www.vam.ac.uk","collections.vam.ac.uk/"]
    # start_urls = ["http://www.vam.ac.uk/"]
    # https://collections.vam.ac.uk/item/id
    # https://api.vam.ac.uk/v2/objects/search?page=n&page_size=15

    # count
    ERROR_COUNT = 0
    PASS_COUNT = 0
    SUCCESS_COUNT = 0
    TOTAL_COUNT = 0
    # data page range
    start_page = 1
    end_page = 66 # max page approx 66
    # run time
    start_time = 0
    end_time = 0
    # file handle
    f = None

    def parse(self, response, *args, **kwargs):
        print("\n进入parse layer\n")
        datas = json.loads(response.body)
        # print(datas,"\n\n")
        for data in datas['records']:
            next_url = "https://api.vam.ac.uk/v2/object/%s"%(data["systemNumber"])
            yield Request(url=next_url, callback=self.parse_second,meta={"dated":data['_primaryDate'],"place":data['_primaryPlace']}, dont_filter=True) # 必须添加dont_filter防止忽略url

    def start_requests(self):
        # time record
        self.start_time = time.time()
        # init output file
        self.check_path()
        self.clear_file()
        # file stream
        self.f = open("save/site7_log.txt", "w", encoding="utf-8")
        for i in range(self.start_page,self.end_page+1): # 请求前100页数据 max 666
            # q=china make sure chinese creation
            url = "https://api.vam.ac.uk/v2/objects/search?q=china&page=%s&page_size=15"%(str(i))
            yield Request(url)

    def parse_second(self, response):
        print("\nsecond layer parse,with meta",response.meta,"\n")
        data = json.loads(response.body)
        # print("\ndata=",data,"\n")
        item = Site2Item()
        try:
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

            self.SUCCESS_COUNT += 1
            self.TOTAL_COUNT += 1
            self.set_log(msg="Crawl {}: Success.".format(response.url))
            yield item
        except Exception as e:
            self.ERROR_COUNT += 1
            self.TOTAL_COUNT += 1
            self.set_log(msg="Crawl {}: Error. Error msg as {}".format(response.url, e))
            # print("ERROR MSG as {}".format(e))


    def set_log(self, msg):
        # write file
        self.f.write(msg + " [" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]\n")
        # self.f.write("Total:{}\n".format(self.TOTAL_COUNT))
        # output to screen
        if self.TOTAL_COUNT == (self.end_page - self.start_page) * 15:
            # record time
            self.end_time = time.time()
            # log runtime hour:minute:seconds
            self.end_time = time.time()
            # runtime using round function
            run_time = round(self.end_time - self.start_time)
            # calculate hour minute second
            hour = run_time // 3600
            minute = (run_time - 3600 * hour) // 60
            second = run_time - 3600 * hour - 60 * minute
            # output to file
            self.f.write('\nTotal program running time (hour:minute:second) is %d:%02d:%02d\n' % (hour, minute, second))
            # output to screen
            info = "\n########################################\n\n" \
                  "Error-{} Pass-{} Success-{} Total-{}\n\n" \
                  "########################################\n".format(self.ERROR_COUNT, self.PASS_COUNT, self.SUCCESS_COUNT, self.TOTAL_COUNT)
            print(info)
            # close file
            self.f.write(info)
            self.f.close()

    def check_path(self):
        if not os.path.exists("./save"):
            os.makedirs("./save")
    def clear_file(self):
        choice = input("clear file 7.json and 7.csv? (Yes/No): ")
        if not ("Yes" in choice or "yes" in choice):
            return False
        # choose clear file
        clear_files = ['7.json','7.csv']
        # clear file
        for fileName in clear_files:
            with open("save/{}".format(fileName),"w") as ff:
                ff.close()
        return True