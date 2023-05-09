import json, os
import time

import scrapy
from scrapy import FormRequest,Request

from ..items import Site2Item
from ..utils import req_site17

class Site17Spider(scrapy.Spider):
    name = "site17"
    allowed_domains = ["www.roots.gov.sg"]
    # count
    ERROR_COUNT = 0
    PASS_COUNT = 0
    SUCCESS_COUNT = 0
    TOTAL_COUNT = 0
    # run time
    start_time = 0
    end_time = 0
    # file handle
    f = None

    def parse(self, response, *args, **kwargs):
        # items
        items = []
        # data range max 10 700 10
        for i in range(10,700,10):
            documents = json.loads(req_site17(frm=i))
            success_local_count = 0
            error_local_count = 0
            for data in documents["documents"]:
                # print("\n\n\ndata=",data,"\n\n\n\n")
                item = Site2Item()
                try:
                    item["id"] = data["id"]
                    item["title"] = data["title"]
                    try:
                        item["dated"] = data["metadata"]["date_period"]
                    except Exception as e:
                        item["dated"] = "unknown"
                    try:
                        item["artist"] = data["metadata"]["creator"]
                    except Exception as e:
                        item["artist"] = "unknown"
                    try:
                        item["role"] = data["metadata"]["nlb_type"]
                    except Exception as e:
                        item["role"] = "unknown"
                    try:
                        item["department"] = data["metadata"]["collection_of"]
                    except Exception as e:
                        item["department"] = "unknown"
                    try:
                        item["medium"] = data["metadata"]["material"][0]
                    except Exception as e:
                        item['medium'] = "unknown"
                    item["country"] = "china"

                    item["description"] = data["content"]
                    try:
                        item["comments"] = data["metadata"]["credit_line"]
                    except Exception as e:
                        item["comments"] = "unknown"
                    item["web_url"] = data["path"]
                    item["img_url"] = data["metadata"]["image_url"]

                    item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    success_local_count += 1
                except Exception as e:
                    print("MSG AS %s"%e)
                    error_local_count += 1
                    continue
                yield item
                items.append(item)
            self.f.write("Crawl {}: with {} success and {} error.".format(response.url, success_local_count, error_local_count) + " [" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "]\n")
            self.SUCCESS_COUNT += success_local_count
            self.ERROR_COUNT += error_local_count
            self.TOTAL_COUNT += success_local_count + error_local_count
        # end request
        # record time
        self.end_time = time.time()
        # runtime using round function
        run_time = round(self.end_time - self.start_time)
        # calculate hour minute second
        hour = run_time // 3600
        minute = (run_time - 3600 * hour) // 60
        second = run_time - 3600 * hour - 60 * minute
        # output to file
        self.f.write('\nTotal program running time (hour:minute:second) is %d:%02d:%02d\n' % (hour, minute, second))
        info = "\n\n##########################################\n\n" \
               "Error-{} Pass-{} Success-{} Total-{}\n\n" \
               "##########################################\n".format(self.ERROR_COUNT, self.PASS_COUNT,
                                                                     self.SUCCESS_COUNT, self.TOTAL_COUNT)
        self.f.write(info)

        return items

    def start_requests(self):
        self.start_time = time.time()
        # check path
        self.check_path()
        self.clear_file()
        # write log
        self.f = open('save/site17_log.txt',"w", encoding="utf-8")
        url = 'https://www.roots.gov.sg/get-search-results'
        yield FormRequest(
            url=url,
            method='POST',  # GET or POST
            # self.set_data(),  # 表单提交的数据
            formdata={
                "id": "",
                "topicsQuery":{
                    "not": [
                        {"field": "source", "value": "CSV"}
                    ]
                },
                "query": "china",
                "from": "10",
                "size": "10",
                "searchMode": "NEW"
            },
        )

    def check_path(self):
        if not os.path.exists("./save"):
            os.makedirs("./save")
    def clear_file(self):
        choice = input("clear file 17.json and 17.csv? (Yes/No): ")
        if not ("Yes" in choice or "yes" in choice):
            return False
        # choose clear file
        clear_files = ['17.json','17.csv']
        # clear file
        for fileName in clear_files:
            with open("save/{}".format(fileName),"w") as ff:
                ff.close()
        return True