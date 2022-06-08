import MapCreater
import copy



def Dijkstra(StartSite, EndSite):
    if StartSite == EndSite:
        return 0, 0
    if StartSite not in MapCreater.SiteDic:
        print("起始点不存在")
        return -1, -1
    if EndSite not in MapCreater.SiteDic:
        print("终止点不存在")
        return -1, -1

    StartSiteIndex = MapCreater.SiteDic[StartSite]
    EndSiteIndex = MapCreater.SiteDic[EndSite]

    DijkstraArr = copy.deepcopy(MapCreater.HeadSiteArr)



    RouteMap = [[float("inf") for col in range(500)] for row in range(500)]  # 存储最短路径，之后倒序查找可以回溯到起始点
    valuequeue = [] #权值队列，存储pair(index, value)

    BusIdMap = [[[] for col in range(500)] for row in range(500)]   #保存车站路径，之后倒序查找可以回溯到起始点

    for i, site in enumerate(DijkstraArr[StartSiteIndex]):
        if site < 10000:
            pair = [i, site, StartSiteIndex]
            valuequeue.append(pair)
            DijkstraArr[i][StartSiteIndex] = float("inf")   #无向边，从正向走过去就不要走回来了
        else:
            continue    #如果不连通（权值是无穷大）则跳过

    #初步找到了所有和StartSite相连的点，建立邻接路径矩阵，每次保存最短路径，之后可以倒序输出。
    while(len(valuequeue) > 0):#非空，先将队列排序，按照value递增排序，每次弹出队列头。
        sorted(valuequeue, key=lambda t: t[1])  #按照value对valuequeue中的pair进行排序
        [tindex, tvalue, tparent] = valuequeue.pop(0)    #释放队列头，即权值最小的节点
        RouteMap[tparent][tindex] = tvalue   #这一条路径已经确定，记录下来
        BusIdMap[tparent][tindex].extend(MapCreater.BusIdArr[tparent][tindex])  #保存路线站点

        if tindex == EndSiteIndex:  #这样就找到了
            return tvalue, RouteMap, BusIdMap
        else:   #这样就还没找到
            temparr = []    #暂时保存新扩展的节点
            for i, tsite in enumerate(DijkstraArr[tindex]):
                if tsite < 10000:
                    tpair = [i, tsite + tvalue, tindex]   #因为是在tindex对应的节点上扩展的，所以权值应该是tindex的权值+本身的权值
                    temparr.append(tpair)
                    DijkstraArr[i][tindex] = float("inf")
            while(len(temparr) > 0):    #用新扩展的节点更新dijkstra邻接矩阵路径代价
                [newindex, newvalue, newparent] = temparr.pop()
                for one in valuequeue:
                    if newindex == one[0]:  #如果扩展到了已经存在的节点，就更新值
                        if one[1] > newvalue:
                            one[1] = newvalue
                        break
                else:       #如果是新扩展的，就添加进入队列中
                    valuequeue.append([newindex, newvalue, newparent])
    else:
        print("没有路径")
        return -2, -2



def find_route(route, busidmap, StartSite, EndSite):
    if StartSite == EndSite:
        return [EndSite], [""]
    if StartSite not in MapCreater.SiteDic:
        print("起始点不存在")
        return -1
    if EndSite not in MapCreater.SiteDic:
        print("终止点不存在")
        return -1

    StartSiteIndex = MapCreater.SiteDic[StartSite]
    EndSiteIndex = MapCreater.SiteDic[EndSite]
    row = EndSiteIndex  #倒叙查找
    RouteArr = [EndSite]
    BusIdArr = []
    while row != StartSiteIndex:    #倒叙查找到了头
        for col in range(500):
            if route[col][row] < 10000:
                RouteArr.append(MapCreater.Index_Site_Dic[col])
                BusIdArr.append(busidmap[col][row])
                row = col
                break
            else:
                continue

    RouteArr.reverse()
    BusIdArr.reverse()

    return RouteArr, BusIdArr


if __name__ == "__main__":
    MapCreater.init_data()
    Cost, Route, BusIdMap = Dijkstra("老山公交场站", "成府路口南")
    if Cost >= 0:
        RouteArr, BusIdArr = find_route(Route, BusIdMap, "老山公交场站", "成府路口南")
        print(RouteArr)
        print(BusIdArr)
    else:
        pass

    #print(Cost)
    #print(Route)