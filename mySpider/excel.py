import os.path

import xlsxwriter as xw
import requests

# get data from my server and parse it into a triplet form
def parse_ternary(choice):
    # get json from server
    url = "https://sncdeveloper.cn/2-7-12-17-22_new.json"
    res = requests.get(url=url)
    # print(res.json()['m2'])
    data = []
    # use choice to get different key - value
    if choice == 2:
        data = res.json()['m2']
    elif choice == 7:
        data = res.json()['m7']
    elif choice == 12:
        data = res.json()['m12']
    elif choice == 17:
        data = res.json()['m17']
    elif choice == 22:
        data = res.json()['m22']
    # print(len(data))

    # triples format: title - properties except title - specific data
    # attributes include: id, dated, artist, role, department, medium, (country filtered), description, comments, web_url, img_url, (submit_time used for log)
    # initialization of fields
    id_triples = []
    dated_triples = []
    artist_triples = []
    role_triples = []
    department_triples = []
    medium_triples = []
    description_triples = []
    comments_triples = []
    web_url_triples = []
    img_url_triples = []

    # parse into triples
    for item in data:
        id_triples.append([item['title'], "id", item['id']])
        dated_triples.append([item['title'], "dated", item['dated']])
        artist_triples.append([item['title'], "artist", item['artist']])
        role_triples.append([item['title'], "role", item['role']])
        department_triples.append([item['title'],"department",item['department']])
        medium_triples.append([item['title'], 'medium', item['medium']])
        description_triples.append([item['title'], "description", item['description']])
        comments_triples.append([item['title'], "comments", item['comments']])
        web_url_triples.append([item['title'], "web_url", item['web_url']])
        img_url_triples.append([item['title'], "img_url", item['img_url']])

    # print(id_triples, dated_triples, artist_triples, role_triples, department_triples, medium_triples, description_triples, comments_triples, web_url_triples, img_url_triples)

    return id_triples, dated_triples, artist_triples, role_triples, department_triples, medium_triples, description_triples, comments_triples, web_url_triples, img_url_triples

def xw_toExcel(data, fileName, title):  # xlsxwriter库储存数据到excel
    # title format: title = ['col1', 'col2', 'col3']  used for setting table header
    # create work sheet
    workbook = xw.Workbook(fileName)
    # create sub-table
    worksheet1 = workbook.add_worksheet("sheet1")
    # activate sub-table
    worksheet1.activate()
    # write headers starting from cell 'A1'
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    # write data starting from the second row
    i = 2
    for j in range(len(data)):
        row = 'A' + str(i)
        try:
            worksheet1.write_row(row, data[j])
        except Exception as e:
            pass
        i += 1
    # close table
    workbook.close()

def checkPath():
    if not os.path.exists("./triples"):
        os.makedirs("./triples")
    subpaths = ['f2','f7','f12','f17','f22']
    for path in subpaths:
        if not os.path.exists("./triples/{}".format(path)):
            os.makedirs("./triples/{}".format(path))

if __name__ == "__main__":

    # id_triples, dated_triples, artist_triples, role_triples, department_triples, medium_triples, description_triples, comments_triples, web_url_triples, img_url_triples = parse_ternary()
    # print(id_triples, dated_triples, artist_triples, role_triples, department_triples, medium_triples,
    #       description_triples, comments_triples, web_url_triples, img_url_triples)

    # check path
    checkPath()
    # data initialization
    choices = [2, 7, 12, 17, 22]
    fields = ['id', 'dated', 'artist', 'role', 'department', 'medium', 'description', 'comments', 'web_url', 'img_url']
    file_names = ['id', 'dated', 'artist', 'role', 'department', 'medium', 'description', 'comments', 'web_url','img_url']

    # double loop to write data into tables
    for choice in choices:
        data = list(parse_ternary(choice=choice))
        for i in range(len(data)):
            xw_toExcel(data=data[i], fileName="triples/f{}/".format(str(choice))+file_names[i]+".xlsx", title=['name', 'relation', fields[i]])
