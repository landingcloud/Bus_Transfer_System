import MapCreater
import copy
import random
import operator
import InputCtrl

def Dijkstra(StartSite, EndSite):
    if StartSite == EndSite:
        return 0, [], []
    if StartSite not in MapCreater.SiteDic:
        print("起始点不存在")
        return -1, [], []
    if EndSite not in MapCreater.SiteDic:
        print("终止点不存在")
        return -1, [], []

    StartSiteIndex = MapCreater.SiteDic[StartSite]
    EndSiteIndex = MapCreater.SiteDic[EndSite]

    DijkstraArr = copy.deepcopy(MapCreater.HeadSiteArr)

    minlen = float("inf")
    BusIdMaps = []
    RouteMaps = []
    is_continue = 10
    while is_continue:
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
            #valuequeue中最小值可能不止一个，随机返回一个最小值
            minline = []
            min_in_minline = valuequeue[0][1]   #valuequeue头上的一定是最小的
            for tmin in valuequeue:
                if tmin[1] == min_in_minline:
                    minline.append(tmin)
                else:
                    break
            random.shuffle(minline)

            [tindex, tvalue, tparent] = valuequeue.pop(valuequeue.index(minline.pop(0)))    #释放队列头，即权值最小的节点
            RouteMap[tparent][tindex] = tvalue   #这一条路径已经确定，记录下来
            BusIdMap[tparent][tindex].extend(MapCreater.BusIdArr[tparent][tindex])  #保存路线站点
            #DijkstraArr[tparent][tindex] = float("inf")

            if tindex == EndSiteIndex:  #这样就找到了
                #return tvalue, RouteMap, BusIdMap
                if minlen >= tvalue:
                    minlen = tvalue
                    # for eachroute in RouteMaps:
                    #     if doublelist_equal(eachroute, RouteMap):
                    #         break
                    # else:
                    RouteMaps.append(RouteMap)
                    BusIdMaps.append(BusIdMap)
                    is_continue -= 1
                    break
                else:
                    is_continue = 0
                    return minlen, RouteMaps, BusIdMaps

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
            #print("没有路径")
            print(minlen)
            return minlen, RouteMaps, BusIdMaps
    return minlen, RouteMaps, BusIdMaps

def doublelist_equal(dlist1, dlist2):
    for di in range(500):
        for dj in range(500):
            if dlist1[di][dj] != dlist2[di][dj]:
                return 0
    return 1

def find_route(route, busidmap, StartSite, EndSite):
    if StartSite == EndSite:
        return [EndSite], [""]
    if StartSite not in MapCreater.SiteDic:
        print("起始点不存在")
        return [], []
    if EndSite not in MapCreater.SiteDic:
        print("终止点不存在")
        return [], []

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

def print_info(start, end, Routes, BusIdMaps):
    pairs = [[], []]
    for i in range(len(Routes)):
        RouteArr, BusIdArr = find_route(Routes[i], BusIdMaps[i], start, end)
        if len(BusIdArr) == 0:
            return


        pairs[0].append(RouteArr)
        pairs[1].append(BusIdArr)


    tlen = len(pairs[0])
    ti = 0
    while ti < tlen:
        tj = ti + 1
        while tj < tlen:
            if pairs[0][ti] == pairs[0][tj]:
                pairs[0][:] = pairs[0][0:tj] + pairs[0][tj + 1:]
                pairs[1][:] = pairs[1][0:tj] + pairs[1][tj + 1:]
                tlen -= 1
                tj -= 1
            tj += 1
        ti += 1

    for i in range(len(pairs[0])):
        print(pairs[0][i])
        print(pairs[1][i])

if __name__ == "__main__":
    MapCreater.init_data()
    cmd = 1
    print("*****欢迎进入公交换乘系统*****")
    while cmd > 0:
        cmd = InputCtrl.Input_Ctrl()
        if isinstance(cmd, int):
            if cmd == 1:
                pass
            if cmd == 2:
                MapCreater.print_Site()
        else:
            cmd = cmd.split()
            start, end = cmd[1:]
            Cost, Routes, BusIdMaps = Dijkstra(start, end)
            print_info(start, end, Routes, BusIdMaps)
            cmd = 1
