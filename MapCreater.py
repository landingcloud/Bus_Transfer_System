import ExcelReader
SiteArr = ["*", "东", "西", "*", "南", "北", "西", "西北", "北"]
SiteDic = {}    #保存 站点名字 : 站点对应index
Index_Site_Dic = {} #保存 站点对应index : 站点名字
BusIdArr = [[[] for col in range(500)] for row in range(500)]   #保存每一个站点对应的公交路
HeadSiteArr = [[float('inf') for col in range(500)] for row in range(500)]
def read_HeadSitArr(sitearr):
    global HeadSiteArr
    global SiteDic
    global BusIdArr
    i = 0   #一共多少个站点
    index = 0
    is_though = 0   #判断连通，有时候换了一条公交线路会变得不连通
    nowbussid = ''
    for site in sitearr:
        if '*' in site: #说明换公交线
            is_though = 0
            nowbussid = site[1:]
            continue
        else:
            pass

        if site not in SiteDic:
            SiteDic[site] = i
            Index_Site_Dic[i] = site
            if is_though == 1:
                HeadSiteArr[i][index] = 1   #将本节点和上一个节点连接
                HeadSiteArr[index][i] = 1   #将上一个节点和本节点连接
                BusIdArr[i][index].append(nowbussid)
                BusIdArr[index][i].append(nowbussid)
            index = i   #更新上一个节点index
            i += 1  #节点总数增加1
            is_though = 1   #默认每一个都与下一个连通
        else:
            nowindex = SiteDic[site]
            if is_though == 1:
                HeadSiteArr[nowindex][index] = 1
                HeadSiteArr[index][nowindex] = 1
                BusIdArr[nowindex][index].append(nowbussid)
                BusIdArr[index][nowindex].append(nowbussid)
            index = nowindex
            is_though = 1
    HeadSiteArr[0][0] = float("inf")

def init_data():
    read_HeadSitArr(ExcelReader.load_excel("./公交.xlsx"))

def print_Site():
    for site in SiteDic:
        print(site)

if __name__ == "__main__":
    #read_HeadSitArr(SiteArr)
    read_HeadSitArr(ExcelReader.load_excel("./公交.xlsx"))
    print(SiteDic)
    print(HeadSiteArr)
