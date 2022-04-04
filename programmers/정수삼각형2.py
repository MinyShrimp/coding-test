
def isOutOfRange( tri, col, row ):
    return \
        ( col < 0 or len(tri) <= col) or \
        ( row < 0 or len(tri[col]) <= row )

class Node:
    def __init__(self, tri, value, col, row):
        self.value   = value
        self.sum     = -1
        self.p1      = None if isOutOfRange(tri, col - 1, row - 1) else [col - 1, row - 1]
        self.p2      = None if isOutOfRange(tri, col - 1, row)     else [col - 1, row]
        # self.isEnter = False
    
    def __str__(self) -> str:
        return "value: {}\tsum: {}\tp1: {}\tp2: {}".format(self.value, self.sum, self.p1, self.p2)

def setTree(tri):
    for col_i, col_v in enumerate( tri ):
        for row_i, row_v in enumerate( col_v ):
            tri[col_i][row_i] = Node( tri, row_v, col_i, row_i )
    tri[0][0].sum = tri[0][0].value

def getNode( tri, pos ):
    return None if pos == None else tri[pos[0]][pos[1]]

def getSum( tri, node ):
    if node.sum != -1:
        return node.sum

    p1 = getNode( tri, node.p1 )
    p2 = getNode( tri, node.p2 )

    if p1 == None and p2 != None:
        if p2.sum != -1:
            node.sum = node.value + p2.sum
        else:
            getSum( tri, p2 )
            node.sum = node.value + p2.sum

    elif p1 != None and p2 == None:
        if p1.sum != -1:
            node.sum = node.value + p1.sum
        else:
            getSum( tri, p1 )
            node.sum = node.value + p1.sum

    elif p1 != None and p2 != None:
        if p1.sum == -1:
            getSum( tri, p1 )
            node.sum = node.value + p1.sum
        if p2.sum == -1:
            getSum( tri, p2 )
            node.sum = node.value + p2.sum
        if p1.sum != -1 and p2.sum != -1:
            node.sum = node.value + max( p1.sum, p2.sum )
    
    print(node, "\t|", p1, "\t|", p2)


def search( tri ):
    _max = -1
    print("="*200)
    for row in range( len(tri[-1]) ):
        node = tri[-1][row]
        getSum( tri, node )

        _max = max( _max, node.sum )
        print("="*200)
    
    return _max

def solution(triangle):
    setTree(triangle)
    return search(triangle)
    
# print( solution([[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]) )
print( solution([[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [4, 5, 2, 6, 5], [1,2,3,4,5,6]]) )