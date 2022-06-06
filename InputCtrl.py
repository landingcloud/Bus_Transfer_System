def version_info():
    print("公交换乘系统")
    print("作者：侯新源")
    print("班级：物联201")
    print("学号：42024106")
    print("本软件通过改进迪杰斯特拉算法和广度优先搜索算法实现多条最短路径的搜索以及路径的保存、站点信息的保存")
    print("内置部分北京公交路线以及站点，可以通过输入起始点和终止点获取二者之间的最短路径")

def help_info():
    print("公交换乘系统")
    print("--help获取帮助")
    print("--version获取程序简介")
    print("--Site获取所有站点")
    print("--find -transfer/-distance 起始点 终止点 :查找最短路径")
    print("--Q退出程序")

def Input_Ctrl():
    inp = input("请输入指令：")
    if inp == "--version":
        version_info()
        return 1
    elif inp == "--help":
        help_info()
        return 1
    elif inp == "--Site":
        return 2
    elif "--find" in inp:
        return inp
    elif inp == "--Q":
        return -1
    else:
        print("指令不存在，输入--help获取帮助！")
        return 1


