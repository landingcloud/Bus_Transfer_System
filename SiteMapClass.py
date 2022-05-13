

class HeadNode:
    '''公交节点'''
    def __init__(self, _name, _first_arc):
        m_name = _name
        m_first_arc = _first_arc

class ArcNode:
    '''链接的下一个节点位置，下一个边，边代价'''
    def __init__(self, _adjvex, _next_arc, _info=1):
        m_adjvex = _adjvex
        m_next_arc = _next_arc
        m_info = _info

