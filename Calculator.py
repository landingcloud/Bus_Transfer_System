import MapCreater
import OneRoadMapCreater
import copy
import random
import operator
import InputCtrl

def MinTransferDijkstra(StartSite, EndSite):
    if StartSite == EndSite:
        return 0, [], []
    if StartSite not in OneRoadMapCreater.SiteDic:
        print("起始点不存在")
        return -1, [], []
    if EndSite not in OneRoadMapCreater.SiteDic:
        print("终止点不存在")
        return -1, [], []

    StartSiteIndex = OneRoadMapCreater.SiteDic[StartSite]
    EndSiteIndex = OneRoadMapCreater.SiteDic[EndSite]

    DijkstraArr = copy.deepcopy(OneRoadMapCreater.HeadSiteArr)

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
            BusIdMap[tparent][tindex].extend(OneRoadMapCreater.BusIdArr[tparent][tindex])  #保存路线站点
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

def MinDistanceDijkstra(StartSite, EndSite):
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

def mintransferselect(RouteArr, BusIdArr):  #在若干条路径中提取最少换乘路径。   当最短路径获取后，再次获取其中最少换乘的路径。
    mincount = float('inf') #保存最小值
    goodindexes = []    #BusIdArr和RouteArr中符合标准的元素的下标   即mincount最小的元素的下标

    # BusIdArr是三维数组，第一维保存不同的路径，第二维保存某一条路径对应的站点，第三维保存两个站点之间的公交线路
    #例：[['2路', '5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路']]
    #   [['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路'], ['5路']]
    for i in range(len(BusIdArr)):
        same = set(BusIdArr[i][0])  #前后两个节点间的并集
        counter = 0 #换乘次数
        for each in BusIdArr[i]:
            if len((same & set(each))) > 0: #并集非空，说明不用换乘
                same = same & set(each)
                each.clear()    #更新站点为交集站点
                each.extend(same)

            else:
                counter += 1
                same.clear()
                same = set(each)

        if counter <= mincount:#是当前最小的
            if counter < mincount:  #发现之前的都太大了，清空重来
                goodindexes.clear()
            mincount = counter  #更新min
            goodindexes.append(i)#存入

    #保留最短
    RouteArr2 = []
    BusIdArr2 = []
    for i in goodindexes:
        RouteArr2.append(RouteArr[i])
        BusIdArr2.append(BusIdArr[i])

    #去重，有重复的
    tlen = len(RouteArr2)
    ti = 0
    while ti < tlen:
        tj = ti + 1
        while tj < tlen:
            if len(RouteArr2[ti]) != len(RouteArr2[tj]):    #长度不相等直接不用比了
                tj += 1
                continue
            if len(set(RouteArr2[ti]) & set(RouteArr2[tj])) != len(RouteArr2[ti]): #交集不相等，说明不同
                tj += 1
                continue
            else:   #说明相等
                if len(BusIdArr2[ti]) != len(BusIdArr2[ti]):
                    tj += 1
                    continue
                #BusIdArr2[ti]是二维列表，第一维是一条路线的公交线路，第二维保存了节点间的公交线路，有可能两个节点之间不止一个公交线。
                #例如：BusIdArr2[ti] == [["1站", "2站"], ["2站"], ["2站"]]
                for p in range(len(BusIdArr2[ti])):
                    if len(set(BusIdArr2[ti][p]) & set(BusIdArr2[tj][p])) != len(set(BusIdArr2[ti][p])):
                        tj += 1
                        break
                else:
                    RouteArr2 = RouteArr2[0: tj] + RouteArr2[tj + 1:]
                    BusIdArr2 = BusIdArr2[0: tj] + BusIdArr2[tj + 1:]
                    tlen -= 1   #由于删了一个，就让总长度减一。    ti是固定的，tj是浮动的，所以应该优先删除tj。
        ti += 1 #ti顺延一位
                #旧的，思路正确但是实现不正确
                #这里因为BusIdArr2[ti]是二维列表，无法变为set，只能手动写一下
                # if len(set(BusIdArr2[ti]) & set(BusIdArr2[tj])) != len(BusIdArr2[ti]):#这次真的不等了，删掉tj
                #     RouteArr2 = RouteArr2[0: tj] + RouteArr2[tj + 1:]
                #     BusIdArr2 = BusIdArr2[0: tj] + BusIdArr2[tj + 1:]


    return RouteArr2, BusIdArr2



def mindistanceselect(RouteArr, BusIdArr):  #在若干条路径中提取最短距离路径。   当最少换乘路径获取后，再次获取其中最短距离的路径。
    #大体思路
    #通过BusIdArr来计算距离，挑选出距离最短的若干路线。此时注意环形线路问题。
    #去重

    mincount = float("inf") #最短路线
    #goodindex = []  #选出的下标
    goodtempRouteArr = []
    goodtempBusIdArr = []
    for i in range(len(BusIdArr)):  #每一种路线情况
        tlen = 0
        tempRouteArr = [[RouteArr[i][0]]]   #函数remakesite不会返回Start节点，所以整个tempRouteArr的第一个节点是空的，需要补上
        tempBusIdArr = [[]]                 #这个补上有点特殊，因为BusIdArr[i][0]是一条公交线路
        for j in range(len(BusIdArr[i])):   #一条路线中的每个节点对应的公交线路   eg：[['2路', '5路'], ['5路']]
            ttlen ,ttempRouteArr, ttempBusIdArr = remakesite(BusIdArr[i][j], RouteArr[i][j], RouteArr[i][j + 1])
            tlen += ttlen
            #开始拼接，有时候可能2条路径后又有3条路径，根据乘法原则，会产生2*3=6条路径
            #再中转一下QAQQAQ我尽量让自己看得懂
            tttempRouteArr = []
            for troutearr in tempRouteArr:
                for ttroutearr in ttempRouteArr:
                    tttempRouteArr.append(copy.deepcopy(troutearr + ttroutearr))
            tempRouteArr.clear()
            tempRouteArr = tttempRouteArr

            tttempBusIdArr = []
            for tbusidarr in tempBusIdArr:
                for ttbusidarr in ttempBusIdArr:
                    if len(tbusidarr) == 0: #这就是上面补上第一个公交线路
                        ttbusidarr.insert(0, ttbusidarr[0])
                    tttempBusIdArr.append(copy.deepcopy(tbusidarr + ttbusidarr))


            tempBusIdArr.clear()
            tempBusIdArr = tttempBusIdArr



        if tlen <= mincount:
            if tlen < mincount:
                goodtempRouteArr.clear()
                goodtempBusIdArr.clear()
            mincount = tlen
            goodtempRouteArr.extend(tempRouteArr)
            goodtempBusIdArr.extend(tempBusIdArr)

    #去重
    RouteArr2 = goodtempRouteArr
    BusIdArr2 = goodtempBusIdArr

    tlen = len(RouteArr2)
    ti = 0
    while ti < tlen:
        tj = ti + 1
        while tj < tlen:
            if len(RouteArr2[ti]) != len(RouteArr2[tj]):  # 长度不相等直接不用比了
                tj += 1
                continue
            if len(set(RouteArr2[ti]) & set(RouteArr2[tj])) != len(RouteArr2[ti]):  # 交集不相等，说明不同
                tj += 1
                continue
            else:  # 说明相等
                if len(BusIdArr2[ti]) != len(BusIdArr2[ti]):
                    tj += 1
                    continue
                # BusIdArr2[ti]是二维列表，第一维是一条路线的公交线路，第二维保存了节点间的公交线路，有可能两个节点之间不止一个公交线。
                # 例如：BusIdArr2[ti] == [["1站", "2站"], ["2站"], ["2站"]]
                for p in range(len(BusIdArr2[ti])):
                    if len(set(BusIdArr2[ti][p]) & set(BusIdArr2[tj][p])) != len(set(BusIdArr2[ti][p])):
                        tj += 1
                        break
                else:
                    RouteArr2 = RouteArr2[0: tj] + RouteArr2[tj + 1:]
                    BusIdArr2 = BusIdArr2[0: tj] + BusIdArr2[tj + 1:]
                    tlen -= 1  # 由于删了一个，就让总长度减一。    ti是固定的，tj是浮动的，所以应该优先删除tj。
        ti += 1  # ti顺延一位

    return RouteArr2, BusIdArr2

def remakesite(Roads, Start, End):
    '''一条公交线路，给定起点和终点，复原出最短通路
    Roads: list [string, string,...]
    Start: string
    End: string
    return: value, list，list 最短长度, 复原后的节点线路, 相匹配的公交线路。注意，可能不止1条
    '''
    minlen = float('inf')
    goodSites = []  #good可能不止一条！！！！！
    goodRoads = []
    for road in Roads:
        sites = OneRoadMapCreater.RoadSiteDic[road]
        tempSites = []
        tempRoads = []
        counter = -1 #计数，Start和End间隔了几个节点，当没有检测到Start或End时为-1，检测到后置为0，之后开始计数
        if (Start not in sites) or (End not in sites):  #如果这条公交线路没有经过Start或End
            continue
        if sites[0] == sites[-1]:   #环形线路
            for site in sites:
                if counter == -1 and (site == Start or site == End):
                    counter = 0
                    if site == End: #反向
                        tempSites.append(site)
                        tempRoads.append(road)
                    continue    #计算需要，可以手动计算一下
                elif counter >= 0:
                    counter += 1
                    tempSites.append(site)  #暂存当前路线
                    tempRoads.append(road)
                    if site == Start or site == End:    #循环线路，循环取最小
                        reverse_counter = len(sites) - 1 - counter  #手动计算一下，假设Start和End为1和4     1 2 3 4 5 1     距离是6 - 1 - 3
                        if counter <= reverse_counter:  #如果不用求补
                            if site == End: #正向
                                break
                            else:   #反向，即先访问的End，将tempSites倒过来
                                del(tempSites[-1])
                                del(tempRoads[-1])
                                tempSites.reverse()
                                tempRoads.reverse()
                                break
                        else:   #需要求补
                            counter = reverse_counter
                            tempSites.clear()   #求补的话之前正向的结果都删掉
                            tempRoads.clear()
                            if site == End: #正向
                                tt = sites[0:sites.index(Start)]    #不要Start
                                tt += sites[sites.index(End): len(sites) - 1]   #不能要最后一个，因为循环队列的开头和结尾一样
                                tt.reverse()
                                tempSites.extend(tt)
                                tempRoads.extend([road for tc in range(counter - 1)])
                                break
                            else:   #反向
                                tt = sites[sites.index(Start) + 1, len(sites) - 1]  #不要Start
                                tt += sites[0: sites.index(End) + 1]
                                tempSites.extend(tt)
                                tempRoads.extend([road for tc in range(counter - 1)])
                                break
        else:   #不是环形线路，重复上面代码，去掉求补即可
            for site in sites:
                if counter == -1 and (site == Start or site == End):
                    counter = 0
                    if site == End: #反向保存
                        tempSites.append(site)
                        tempRoads.append(road)
                    continue
                elif counter >= 0:
                    counter += 1
                    tempSites.append(site)  # 暂存当前路线
                    tempRoads.append(road)
                    if site == Start or site == End:
                        if site == End: #正向
                            break
                        else:   #反向
                            del(tempSites[-1])
                            del(tempRoads[-1])
                            tempSites.reverse()
                            tempRoads.reverse()
                            break
        #接下来选最小
        if counter <= minlen:
            if 0 or counter < minlen:
                minlen = counter
                goodSites.clear()
                goodRoads.clear()
            goodSites.append(tempSites)
            goodRoads.append(tempRoads)
    return minlen, goodSites, goodRoads


def getfinall(start, end, Routes, BusIdMaps, mode):
    pairs = [[], []]
    for i in range(len(Routes)):
        RouteArr, BusIdArr = find_route(Routes[i], BusIdMaps[i], start, end)
        if len(BusIdArr) == 0:
            return
        pairs[0].append(RouteArr)
        pairs[1].append(BusIdArr)

    RouteArr2 = None
    BusIdArr2 = None
    if mode == 1:   #最短路径
        RouteArr2, BusIdArr2 = mintransferselect(pairs[0], pairs[1])
    else:
        RouteArr2, BusIdArr2 = mindistanceselect(pairs[0], pairs[1])

    for i in range(len(RouteArr2)):
        print(RouteArr2[i])
        print(BusIdArr2[i])


#逐渐废弃
def print_info(start, end, Routes, BusIdMaps):
    pairs = [[], []]
    for i in range(len(Routes)):
        RouteArr, BusIdArr = find_route(Routes[i], BusIdMaps[i], start, end)
        if len(BusIdArr) == 0:
            return


        pairs[0].append(RouteArr)
        pairs[1].append(BusIdArr)

    #去重，但是有bug，这个tj的操作应该有问题，“相对正确”的操作见上
    tlen = len(pairs[0])
    ti = 0
    # while ti < tlen:
    #     tj = ti + 1
    #     while tj < tlen:
    #         if pairs[0][ti] == pairs[0][tj]:
    #             pairs[0][:] = pairs[0][0:tj] + pairs[0][tj + 1:]
    #             pairs[1][:] = pairs[1][0:tj] + pairs[1][tj + 1:]
    #             tlen -= 1
    #             tj -= 1
    #         tj += 1
    #     ti += 1

    for i in range(len(pairs[0])):
        print(pairs[0][i])
        print(pairs[1][i])

if __name__ == "__main__":
    OneRoadMapCreater.init_data()
    MapCreater.init_data()
    cmd = 1
    print("*****欢迎进入公交换乘系统*****")
    while cmd > 0:
        cmd = InputCtrl.Input_Ctrl()
        if isinstance(cmd, int):
            if cmd == 1:
                pass
            if cmd == 2:
                OneRoadMapCreater.print_Site()
        else:
            cmd = cmd.split()
            mode = cmd[1]
            start, end = cmd[2:]
            if "transfer" in mode:
                Cost, Routes, BusIdMaps = MinTransferDijkstra(start, end)
                #print_info(start, end, Routes, BusIdMaps)
                getfinall(start, end, Routes, BusIdMaps, 0)
            elif "distance" in mode:
                Cost, Routes, BusIdMaps = MinDistanceDijkstra(start, end)
                #print_info(start, end, Routes, BusIdMaps)
                getfinall(start, end, Routes, BusIdMaps, 1)
            cmd = 1
