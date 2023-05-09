import re
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service

def antiInsectBrowser():
    option = webdriver.ChromeOptions()
    option.page_load_strategy = 'none' # normal,eager,none
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)

    # s = Service(executable_path=ChromeDriverManager().install())
    # browser = webdriver.Chrome(service=s, options=option)

    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    return browser

print(ChromeDriverManager().install())

driver = antiInsectBrowser() #webdriver.Chrome(ChromeDriverManager().install())
ress=driver.get("https://www.roots.gov.sg/search?query=china&page=2")

print(ress)
time.sleep(1)
datas = driver.page_source

next_links = re.compile('a.*href="(https://www.roots.gov.sg/Collection-Landing/listing/\d{7})">').findall(datas)
print(next_links)
i = 0
for link in next_links:
    driver.get(link)
    time.sleep(3)
    datas = driver.page_source
    # with open("./html/2.html", "wb") as f:
    #     f.write(driver.page_source.encode("gbk", "ignore"))
    res_arr = re.compile('<div .*?class="dd">(.*?)</div>').findall(datas)
    # print("res_arr=", res_arr, "\n")
    res = list(map(lambda x: re.compile('<a.*>(.*?)</a>').findall(x)[0] if x.find("<a") != -1 else x, res_arr))[:9] # 9为属性个数
    print("res=",res,"\n")
    # test count
    if i >= 5 :
        break
    i += 1


print("end")
driver.quit()
# driver.close()