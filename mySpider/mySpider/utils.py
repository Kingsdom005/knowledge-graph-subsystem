import requests
import json

def req_site17(query="china",frm=10,size=10):

    headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Content-Type':'application/json',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'no-cache',
            "cookie":'ASP.NET_SessionId=3pjxvpvrvmfjc2qudwgqpdt2; _ga=GA1.3.422491723.1682224801; _gid=GA1.3.596914618.1682224801; _sp_id.f671=3567acc7-2e3d-4cf4-b963-e0db7e3f1f03.1682224801.1.1682224804.1682224801.69cb8fe4-b7cb-4699-bd89-773cf42891b7; rp_www.roots.gov.sg=e563f1531a9cbd01052296cec33193a5; AWSALB=EoWBvT4qXqx8kuEtuEgGij8jAoILdc9gZLpLR+drw84zK4Rik5w1qY4VAxCX42eGy2MwO6vLyVr/xkkA1oBEr+B1YWi36gGjBbsk0mQXpWXO/CgymKihjVJJ3nDQ; _ga_YEJDFPG313=GS1.1.1682240724.2.0.1682240724.60.0.0; _ga_8SHNNF4FWD=GS1.1.1682240724.2.0.1682240724.0.0.0'
        }

    #空的对象，body参数
    data = {
        "id": "12",
        "topicsQuery":
        {
            "not":[
                {"field":"source", "value": "CSV"}
            ]
        },
        "query":query,
        "from":frm,
        "size":size,
        "searchMode":"NEW"
    }
    data = json.dumps(data)
    url = 'https://www.roots.gov.sg/get-search-results'
    response = requests.post(url=url,data=data,headers=headers)
    # res = response.request.headers
    # print(res)
    # print(response.text)

    return response.text

