
class FPNode(object):
    '''定义树节点'''
    def __init__(self,tree,item, count=1):
        self._tree=tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    #获取self节点出现的树  
    @property
    def tree(self):
        return self._tree

    #获取或者修改item
    def item():

        def fget(self):
            return self._item

        def fset(self,value):       
            self._item=value
        return locals()
    item=property(**item())
     
    #获取或者修改count
    def count():

        def fget(self):
            return self._count

        def fset(self,value):
            if isinstance(value,int):
                self._count=value
        return locals()
    count=property(**count())
    
    #获取或者修改parent
    def parent():
        
        def fget(self):
            return self._parent
        
        def fset(self,value):
            if value is not None and not isinstance(value,FPNode):
                raise TypeError('父亲节点必须是FPNode类型的')
            if value and value.tree is not self.tree:
                raise ValueError("不能拥有来自另一棵树的父母")
            self._parent=value
        return locals()
        #以字典的形式 返回所有局部变量的 名称与值{self._parent:value}
    parent= property(**parent())
    #加了星号（**）的变量名会存放所有未命名的变量参数

    ##获取或者修改 neighbor
    def neighbor():
        
        def fget(self):
            return self._neighbor
        
        def fset(self, value):
            if value is not None and not isinstance(value, FPNode):
                raise TypeError("节点必须具有FPNode作为邻居。")
            if value and value.tree is not self.tree:
                raise ValueError("不能有另一棵树的邻居。")
            self._neighbor = value
        return locals()
    neighbor = property(**neighbor())

    #返回self节点的每个子节点的节点，并且存放在list中
    @property
    def children(self):
        return list(self._children.values())
    
    #如果self节点是树的根，则返回true，否则返回false
    #根节点的特征：根为空，计数也为空
    @property
    def root(self):
        return self._item is None and self._count is None

    #如果self节点是叶子节点，则返回true，否则返回false
    #叶子节点的特征：没有孩子
    def leaf(self):
        return len(self._children)==0
    
    #增加与self节点项目相关的计数
    def increment(self):
        if self._count is None:
            raise ValueError('根节点没有计数')
        self._count+=1
    # 
    #将给定的FPNode->“child”添加为此节点的子节点   
    def add(self, child):
       
        if not isinstance(child, FPNode):
            raise TypeError("只能添加其他FPNode作为子项")

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    #检查此节点是否包含给定项的子节点
    #如果是，则返回该节点
    #否则，返回None
    def search(self,item):
        try:
            return self._children[item]
        except KeyError:
            return None

    #判断item是否包含在self节点的_children中
    def __contains__(self,item):
        return item in self._children

        
    #移除某一个孩子节点
    def remove(self,child):
        try:
            if self._children[child.item] is child:
                del self._children[child.item]
                child.parent=None
                self._tree._remove(child)
                for sub_child in child.children:
                    try:
                        #合并节点，计数增加
                        self._children[sub_child.item]._count+=sub_child.count
                        sub_child.parent=None
                    except KeyError:
                        self.add(sub_child)
                child._children={}
            else:
                raise ValueError(child,'不是这个节点的孩子')
        except KeyError:
            print('孩子中没有该节点！')
    
    


    #检查
    def inspect(self):
        for child in self.children:
            print(child.item)
            print(child.count)
            print(child.parent)
            
            
        
    
    
