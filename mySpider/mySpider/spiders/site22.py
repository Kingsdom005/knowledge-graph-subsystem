import scrapy
import time
from scrapy import FormRequest, Request
from ..items import Site2Item

class Site22Spider(scrapy.Spider):
    name = "site22"
    allowed_domains = ["www.nezu-muse.or.jp"]
    start_urls = ["https://www.nezu-muse.or.jp/en/sp/collection"]

    def parse(self, response):
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

        item= Site2Item()
        div = response.xpath('//*[@id="container"]/section/article')
        title = div.xpath('./div[1]/div/p//text()')[0].extract()
        res = div.xpath('./div[2]/ul/li[5]/text()').extract()
        res1=div.xpath('./div[2]/ul/li[4]/text()').extract()
        artist=""
        medium=""
        if not res1:
            medium=""
        elif not res:
            medium = div.xpath('./div[2]/ul/li[2]//text()')[0].extract()
        else:
            artist = div.xpath('./div[2]/ul/li[1]//text()')[0].extract()
            medium = div.xpath('./div[2]/ul/li[3]//text()')[0].extract()
        description = div.xpath('./div[2]/div/p/text()')[0].extract()
        item["id"] = response.meta["id"]
        item["title"] = title
        item["dated"]=""
        item["artist"] = artist
        item["role"]=""
        item["department"]="Nezu Museum"
        item["medium"] = medium
        item["country"] = response.meta["country"]
        item["description"] = description
        item["comments"]=""
        item["web_url"]=response.url
        item["img_url"]=response.meta["img_url"]
        item["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if ("china" in item["country"]) or ("China" in item["country"]):
            yield item  # 将item提交给管道
        else:
            print("Ignore place %s" % (item["country"]))
    def start_requests(self):
        base_url = "https://www.nezu-muse.or.jp/en/sp/collection/list.php?category="
        for i in range(1,10):
            url = base_url + str(i)
            yield Request(url)

