import os.path
import time
import re
import scrapy
from scrapy import FormRequest, Request
import json
from ..items import Site2Item

class Site2Spider(scrapy.Spider):
    name = "site2"
    allowed_domains = ["collections.artsmia.org","new.artsmia.org","iiif.dx.artsmia.org"]
    # count
    ERROR_COUNT = 0
    PASS_COUNT = 0
    SUCCESS_COUNT = 0
    TOTAL_COUNT = 0
    # data range
    start_id = 0
    end_id = 6666 # max approx 6666
    # run time
    start_time = 0
    end_time = 0
    # file handle
    f = None


    # start_urls = (
    # https://artstories.artsmia.org/#/o/1854
    # https://iiif.dx.artsmia.org/1854.jpg/info.json
    # https://search.artsmia.org/id/1854
    # https://6.api.artsmia.org/1854.jpg
    # )

    def parse(self, response, *args, **kwargs):

        print("\n正在访问:", response.url, "获取到%d字节信息"%(len(response.body)) ,"\n")
        # data in the format of json
        data = json.loads(response.body)
        # create model example
        item = Site2Item()
        try:
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
            # filter
            if data["country"] == "China" or data["country"] == "china":
                self.SUCCESS_COUNT += 1
                self.TOTAL_COUNT += 1
                self.set_log(msg="Crawl {}: Success.".format(response.url))
                yield item
            else:
                self.PASS_COUNT += 1
                self.TOTAL_COUNT += 1
                # print("Ignore place %s" % (data["country"]))
                self.set_log(msg="Crawl {}: Pass. Ignore place {}" .format(response.url, data["country"]))

        except Exception as e:
            # error log
            self.ERROR_COUNT += 1
            self.TOTAL_COUNT += 1
            # print("Error msg as %s"%e)
            self.set_log(msg="Crawl {}: Error. Error msg as {}".format(response.url, e))
            return

    def start_requests(self):
        # log time
        self.start_time = time.time()
        # check path
        self.check_path()
        self.clear_file()
        # log file stream
        self.f = open("save/site2_log.txt","w",encoding="utf-8")
        # start crawl
        base_url = "https://search.artsmia.org/id/"
        for i in range(self.start_id,self.end_id): # 2000
            url = base_url + str(i)
            header = {
                "Cookie":'_gcl_au=1.1.1872783380.1680790619; _ga_T0BL8ZBKC1=GS1.1.1681305320.10.1.1681307464.0.0.0; _ga=GA1.1.634546262.1680790619',
                "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
            }
            yield Request(url=url, headers=header)

    def set_log(self, msg):
        # write file
        self.f.write(msg + " [" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]\n")
        # output to screen
        if self.TOTAL_COUNT == self.end_id - self.start_id:
            # log runtime hour:minute:seconds
            self.end_time = time.time()
            # runtime using round function
            run_time = round(self.end_time - self.start_time)
            # calculate hour minute second
            hour = run_time // 3600
            minute = (run_time - 3600 * hour) // 60
            second = run_time - 3600 * hour - 60 * minute
            # output to file
            self.f.write('\nTotal program running time (hour:minute:second) is %d:%02d:%02d\n'%(hour, minute, second))
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
        choice = input("clear file 2.json and 2.csv? (Yes/No): ")
        if not ("Yes" in choice or "yes" in choice):
            return False
        # choose clear file
        clear_files = ['2.json','2.csv']
        # clear file
        for fileName in clear_files:
            with open("save/{}".format(fileName),"w") as ff:
                ff.close()
        return True