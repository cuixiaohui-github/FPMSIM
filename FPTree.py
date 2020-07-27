from collections import namedtuple
import FPNode

class FPTree(object):
    
    Route = namedtuple('namedtuple','head tail')

    #初始化
    def __init__(self):
        
        self._root=FPNode.FPNode(self,None,None)
        self._routes={}   #将项目映射到“邻居”路径的头部和尾部的字典，
                          #该路径将命中包含该项目的每个节点。

    #获取树的根节点
    @property
    def root(self):
        return self._root
   
            
    #调整树结构
    def adjust_fptree(self,data_list,all_big_table):
        for line in data_list:
            line=list(filter(lambda v: v in all_big_table,line))
            line.sort(key=lambda x: all_big_table[x],reverse=True)
            self.adj_add(line)
            
    #调整时，向树中添加事务
    def adj_add(self,line):
        point=self.root
        for item in line:
            next_point=point.search(item)
            '''此树已经存在该节点，计数不增加'''
            if next_point and item in self.order_dict:
                pass
            elif next_point:
                next_point.increment()
            else:
                '''创建一个新节点，并添加为self的孩子节点'''
                next_point=FPNode.FPNode(self,item)
                point.add(next_point)
                 # 更新包含此项的节点的routes以包括我们的新节点
                self._update_route(next_point)
            point=next_point
                       
    
    #向树中添加事务  一行一个事务
    def add (self,line):
        point=self.root

        for item in line:
            next_point=point.search(item)
            if next_point:
                '''此树已经存在当前事务的节点，支持度加1'''
                next_point.increment()
            else:
                '''创建一个新节点，并添加为self的孩子节点'''
                next_point=FPNode.FPNode(self,item)
                point.add(next_point)
                 # 更新包含此项的节点的routes以包括我们的新节点
                self._update_route(next_point)
            point=next_point

    #更新路径(item的所有项节点)
    def _update_route(self,point):
        '''将节点添加到Route中'''
        assert self is point.tree
        
        try:
            route=self._routes[point.item]
            route[1].neighbor=point  #route[1] is the tail
            self._routes[point.item]=self.Route(route[0],point)            
        except:
            #没有这个项，开始一条新路径
            self._routes[point.item]=self.Route(point,point)
            #例如{'a':namedtuple(head='节点a',tail='节点a')}

    ##
    def items(self):
        '''为树中表示的每个项生成一个二元组，(例如：I1,I2,I3...)
           元组的第一个元素是项本身，第二个元素是一个生成器
           它将生成 树中属于该项的节点
        '''
        for item in self._routes.keys():  #iterkeys()返回一个迭代器
            yield (item ,self.nodes(item))
        
    # 生成包含给定项的节点序列
    def nodes(self,item):
        try:
            node=self._routes[item][0]
        except KeyError:
            return
        #用yield获取每个节点
        while node:
            yield node
            node=node.neighbor
            
    def prefix_paths(self, item):
        """生成以给定项结束的前缀路径"""

        def collect_path(node):
            path = []
            while node and not node.root:
                if path == []:
                    path.append([node.item,node.count])
                else:
                    path.append(node.item)
                node = node.parent
            
            return path

        return (collect_path(node) for node in self.nodes(item))

    #删除树中的节点
    def _remove (self,node):
        head, tail =self._routes[node.item]
        if node is head:
            if node is tail or not node.neighbor:
                #唯一的一个节点
                del self._routes[node.item]
            else:
                self._routes[node.item]=self.Route(node.neighbor,tail)
        else:
            for n in self.nodes(node.item):
                if n.neighbor is node:
                    n.neighbor=node.neighbor
                    if node is tail:
                        self._routes[node.item]=self.Route(head,n)
                        break
                    
                      
        
    #检查
    def inspect(self): 
        print('Tree:')
        print('根节点为：',self.root)
        print('根节点的item：',self.root.item)
        print('根节点的count：',self.root.count)
        ##项路径
        print ('Routes:')
        for item, nodes in self.items():
            print ('  %r' %item)
            for node in nodes:
                print ('    %r'% node)
                print('支持度计数为：',node.count)
                print( '是叶子节点：',node.leaf())
                print('孩子节点：',node.children)
        '''
        ##前缀路径
        for item, nodes in self.items():
            print(item,'prefix_paths:')
            for path in self.prefix_paths(item):
                print('    ',path)
        '''
     
