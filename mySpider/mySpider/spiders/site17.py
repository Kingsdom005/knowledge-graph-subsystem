import json
import time

import scrapy
from scrapy import FormRequest,Request

from ..items import Site2Item
from ..utils import req_site17

class Site17Spider(scrapy.Spider):
    name = "site17"
    allowed_domains = ["www.roots.gov.sg"]

    def parse(self, response, *args, **kwargs):
        # 配置 headers
        items = []
        for i in range(10,700,10):
            documents = json.loads(req_site17(frm=i))
            for data in documents["documents"]:
                print("\n\n\ndata=",data,"\n\n\n\n")
                item = Site2Item()
                try:
                    item["id"] = data["id"]
                    item["title"] = data["title"]
                    item["dated"] = data["metadata"]["date_period"]
                    item["artist"] = data["metadata"]["creator"]
                    item["role"] = data["metadata"]["nlb_type"]
                    item["department"] = data["metadata"]["collection_of"]
                    item["medium"] = data["metadata"]["material"][0]

                    item["country"] = "china"

                    item["description"] = data["content"]
                    item["comments"] = data["metadata"]["credit_line"]

                    item["web_url"] = data["path"]
                    item["img_url"] = data["metadata"]["image_url"]

                    item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                except Exception as e:
                    print("MSG AS %s"%e)
                    continue
                yield item
                items.append(item)

        return items

    def start_requests(self):
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
            }
        )