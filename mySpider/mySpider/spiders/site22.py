import scrapy
import time
from scrapy import FormRequest, Request
from ..items import Site2Item

class Site22Spider(scrapy.Spider):
    name = "site22"
    allowed_domains = ["www.nezu-muse.or.jp"]
    start_urls = ["https://www.nezu-muse.or.jp/en/sp/collection"]

    ERROR_COUNT = 0
    PASS_COUNT = 0
    SUCCESS_COUNT = 0
    TOTAL_COUNT = 0
    f=None
    sum=108

    def parse(self, response, *args, **kwargs):
        ul=response.xpath('//*[@id="container"]/section/article/ul')
        li_list=ul.xpath('//*[@id="container"]/section/article/ul/li')
        for li in li_list:
            if li:
                href = li.xpath('./div[1]/a/@href').extract()[0]
                img_url = li.xpath('./div[1]/a/img/@src').extract()[0]
                img_url="https://www.nezu-muse.or.jp%s"%str(img_url)
                web_url = "https://www.nezu-muse.or.jp/en/sp/collection/%s" % href
                country=li.xpath('./div[2]/p[2]//text()').extract()[0]
                id = href[-5:]
                yield Request(url=web_url, callback=self.parse_second, meta={"img_url": img_url, "id": id,"country":country},
                              dont_filter=True)
    def parse_second(self,response):
        item=Site2Item()
        div = response.xpath('//*[@id="container"]/section/article')
        title = div.xpath('./div[1]/div/p').xpath('string(.)').extract()[0]
        res = div.xpath('./div[2]/ul/li[5]/text()').extract()
        res1=div.xpath('./div[2]/ul/li[4]/text()').extract()
        artist="unknown"
        medium="unknown"
        if not res1:
            medium="unknown"
        elif not res:
            medium = div.xpath('./div[2]/ul/li[2]//text()')[0].extract()
            if medium==response.meta["country"]:
                medium="unknown"
        else:
            artist = div.xpath('./div[2]/ul/li[1]//text()')[0].extract()
            medium = div.xpath('./div[2]/ul/li[3]//text()')[0].extract()
        description = div.xpath('./div[2]/div/p').xpath('string(.)').extract()[0]
        try:
            item["id"] = response.meta["id"]
            item["title"] = title
            item["dated"] = "unknown"
            item["artist"] = artist
            item["role"] = "unknown"
            item["department"] = "Nezu Museum"
            item["medium"] = medium
            item["country"] = response.meta["country"]
            item["description"] = description
            item["comments"] = "unknown"
            item["web_url"] = response.url
            item["img_url"] = response.meta["img_url"]
            item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if ("china" in item["country"]) or ("China" in item["country"]):
                self.SUCCESS_COUNT+=1
                self.TOTAL_COUNT+=1
                self.set_log(msg="Crawl {}: Success.".format(response.url))
                yield item  # 将item提交给管道
            else:
                self.PASS_COUNT += 1
                self.TOTAL_COUNT += 1
                self.set_log(msg="Crawl {}: Pass. Ignore place {}".format(response.url, item["country"]))
        except Exception as e:
            self.ERROR_COUNT+=1
            self.TOTAL_COUNT+=1
            self.set_log(msg="Crawl {}: Error. Error msg as {}".format(response.url, e))
            return
        # print(self.TOTAL_COUNT)
        # print(self.SUCCESS_COUNT)

    def start_requests(self):
        with open("save/22.json", "w", encoding="utf-8") as ff:
            ff.close()
        base_url = "https://www.nezu-muse.or.jp/en/sp/collection/list.php?category="
        self.f = open("save/site22_log.txt", "w", encoding="utf-8")
        for i in range(1,10):
            url = base_url + str(i)
            yield Request(url)

    def set_log(self, msg):
        # write file
        self.f.write(msg+" ["+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"]\n")
        #print(self.TOTAL_COUNT)
        # output to screen
        if self.TOTAL_COUNT == 108:
            # output to screen
            info = "\n\n#######################################\n\n" \
                  "Error-{} Pass-{} Success-{} Total-{}\n\n" \
                  "#######################################\n".format(self.ERROR_COUNT, self.PASS_COUNT, self.SUCCESS_COUNT, self.TOTAL_COUNT)
            print(info)
            # close file
            self.f.write(info)
            self.f.close()

