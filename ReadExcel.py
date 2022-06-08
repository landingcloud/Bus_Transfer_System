#import openpyxl
from SiteMapClass import*
SiteArr = ["东", "西", "南", "北", "西", "西北", "北"]

HeadSiteArr = []

def find_site_in_arr(site):
    if len(HeadSiteArr) == 0:
        return -1
    for index, headsite in enumerate(HeadSiteArr):
        print(headsite.m_name)
        if headsite.m_name == site:
            if index == len(HeadSiteArr) - 1:
                return -2
            else:
                return index
    return -1


def read_headsitearr(SiteArr):
    global HeadSiteArr
    preindex = -1   #前一个headnode在数组HeadSiteArr中的下标
    for site in SiteArr:    #读入一个节点
        is_exist = find_site_in_arr(site)   #判断是否已经存在
        if is_exist == -1:
            headsite = HeadNode(site, None)
            HeadSiteArr.append(headsite)
            if preindex >= 0:   #如果不是第一次读入的，那么上一个读入的一定和本次读入的连结
                #上一个节点的边连结到这个节点
                arc = HeadSiteArr[preindex].m_first_arc
                if arc == None: #如果上一个头结点的边节点没有节点（实际上只有初始化时没有），就连接新的
                    HeadSiteArr[preindex].m_first_arc = ArcNode(len(HeadSiteArr) - 1, None)
                else:
                    while arc.m_next_arc != None:   #移动到最后
                        arc = arc.m_next_arc
                    arc.m_next_arc = ArcNode(len(HeadSiteArr) - 1, None)

                #这个节点的边连接到上一个节点（因为所有边都是无向边）
                headsite.m_first_arc = ArcNode(preindex, None)


            else:   #如果是第一次读入，直接读入即可就不用更新上一个节点的边了
                pass
            preindex = HeadSiteArr.index(headsite)

        elif is_exist >= 0:
            headsite = HeadNode(site, ArcNode(preindex, None))
            HeadSiteArr.append(headsite)
            arc = HeadSiteArr[preindex].m_first_arc
            while(arc.m_next_arc != None):
                arc = arc.m_next_arc
            arc.m_next_arc = ArcNode(is_exist, None)

        else:
            continue

if __name__ == "__main__":
    read_headsitearr(SiteArr)