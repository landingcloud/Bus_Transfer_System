#按照同一条公交线路，创建邻接矩阵
#同一条公交线路的所有节点认为互相连通，并且边代价都为1
import ExcelReader
SiteDic = {} #站点名：站点index
Index_Site_Dic = {} #站点index：站点名
BusIdArr = [[[] for col in range(500)] for row in range(500)]   #站点对应公交线
HeadSiteArr = [[float("inf") for col in range(500)] for row in range(500)]
def read_HeadSiteArr(sitearr):
    global HeadSiteArr
    global SiteDic
    global BusIdArr
    i = 0 #节点总数

    #is_though = 0 #判断连通，换公交就不连通
    nowbussid = ''

    #oneroadsite = []#一条路上的所有站点
    oneroadsiteindex = []#一条路上的所有站点对应的下标，先保存下来，减少运行时间消耗
    for site in sitearr:
        if '*' in site:
            #将之前的所有连通节点串起来
            for orsite_start in oneroadsiteindex:   #二重循环，将节点两两连接
                for orsite_end in oneroadsiteindex:
                    HeadSiteArr[orsite_start][orsite_end] = 1   #节点连接，边代价1
                    BusIdArr[orsite_start][orsite_end].append(nowbussid)    #保存路线
                HeadSiteArr[orsite_start][orsite_start] = float("inf")  #认为自己和自己不连接

            #更新连通情况
            #is_though = 0
            nowbussid = site[1:]    #保存当前公交名称
            oneroadsiteindex.clear()    #清空连通路线
            continue
        else:
            #oneroadsite.append(site)    #保存这一条路的所有节点
            if site not in SiteDic: #如果这个节点是新的，给新节点一个新的index
                SiteDic[site] = i
                Index_Site_Dic[i] = site
                i += 1
            oneroadsiteindex.append(SiteDic[site])#保存对应下标
            #is_though = 1   #同一条线路，置为连通

    else:
        # 将之前的所有连通节点串起来
        for orsite_start in oneroadsiteindex:  # 二重循环，将节点两两连接
            for orsite_end in oneroadsiteindex:
                HeadSiteArr[orsite_start][orsite_end] = 1  # 节点连接，边代价1
                BusIdArr[orsite_start][orsite_end].append(nowbussid)  # 保存路线
            HeadSiteArr[orsite_start][orsite_start] = float("inf")  # 认为自己和自己不连接

def init_data():
    read_HeadSiteArr(ExcelReader.load_excel("./公交.xlsx"))

def print_Site():
    for site in SiteDic:
        print(site)

