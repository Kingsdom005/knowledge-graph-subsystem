# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItcastItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()

class Site2Item(scrapy.Item):
    # 如标题、时代、介绍等；文物对应的详情页面的URL；文物图片（原图，爬取请注意检查，部分网站可能需要手动解析原图地址）；原图下载链接。

    id = scrapy.Field()                         # 文物ID
    title = scrapy.Field()                      # 文物标题
    dated = scrapy.Field()                      # 文物时代
    artist = scrapy.Field()                     # 文物创作者
    role = scrapy.Field()                       # 文物类型
    department = scrapy.Field()                 # 文物归属部门
    medium = scrapy.Field()                     # 材质
    country = scrapy.Field()                    # 国家归属

    onview = scrapy.Field()                     # 新增，是否正在展示(web_img是否有效)

    description = scrapy.Field()                # 文物介绍
    comments = scrapy.Field()                   # 作品评价

    web_url = scrapy.Field()                    # web端原始链接
    img_url = scrapy.Field()                    # 文物图片地址

    submit_time = scrapy.Field()                # 记录爬取时间，日志记录
