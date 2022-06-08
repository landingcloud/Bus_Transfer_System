import MapCreater
import copy



def Dijkstra(StartSite, EndSite):
    if StartSite == EndSite:
        return 0
    if StartSite not in MapCreater.SiteDic:
        print("起始点不存在")
        return -1
    if EndSite not in MapCreater.SiteDic:
        print("终止点不存在")
        return -1

    StartSiteIndex = MapCreater.SiteDic[StartSite]
    EndSiteIndex = MapCreater.SiteDic[EndSite]

    DijkstraArr = copy.deepcopy(MapCreater.HeadSiteArr)
    RouteMap = [[float("inf") for col in range(500)] for row in range(500)]  # 存储最短路径，之后倒序查找可以回溯到起始点
    valuequeue = [] #权值队列，存储pair(index, value)

    for i, site in enumerate(DijkstraArr[StartSiteIndex]):
        if site < 10000:
            pair = [i, site]
            valuequeue.append(pair)
            DijkstraArr[i][StartSiteIndex] = float("inf")   #无向边，从正向走过去就不要走回来了
        else:
            continue    #如果不连通（权值是无穷大）则跳过

    #初步找到了所有和StartSite相连的点，建立邻接路径矩阵，每次保存最短路径，之后可以倒序输出。
    while(len(valuequeue) > 0):#非空，先将队列排序，按照value递增排序，每次弹出队列头。
        sorted(valuequeue, key=lambda t: t[1])  #按照value对valuequeue中的pair进行排序
        [tindex, tvalue] = valuequeue.pop(0)    #释放队列头，即权值最小的节点

        if tindex == EndSiteIndex:  #这样就找到了
            return tvalue
        else:   #这样就还没找到
            temparr = []    #暂时保存新扩展的节点
            for i, tsite in enumerate(DijkstraArr[tindex]):
                if tsite < 10000:
                    tpair = [i, tsite + tvalue]   #因为是在tindex对应的节点上扩展的，所以权值应该是tindex的权值+本身的权值
                    temparr.append(tpair)
                    DijkstraArr[i][tindex] = float("inf")
            while(len(temparr) > 0):
                [newindex, newvalue] = temparr.pop()
                for one in valuequeue:
                    if newindex == one[0]:  #如果扩展到了已经存在的节点，就更新值
                        if one[1] > newvalue:
                            one[1] = newvalue
                        break
                else:       #如果是新扩展的，就添加进入队列中
                    valuequeue.append([newindex, newvalue])
    else:
        print("没有路径")
        return -2
        '''万不得已还是不要看这一段了QAQ
        #接下来遍历DijkstraArr[tindex]，里面保存了一系列权值，寻找除了inf最大的
        prenode = 0 #遍历过程中前一个节点，等到遍历到inf回退到这个
        prevalue = 0    #遍历到最后除inf最大的value，因为由这个节点扩展的节点的value都是prevalue + 自身的value
        for nownode in DijkstraArr[tindex]
        '''


if __name__ == "__main__":
    MapCreater.init_data()
    print(Dijkstra("新源里", "学知园"))