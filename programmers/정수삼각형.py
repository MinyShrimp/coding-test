
def isOutOfRange( tri, col, row ):
    return \
        ( col < 0 or len(tri) <= col) or \
        ( row < 0 or len(tri[col]) <= row )

_max = -1
class Node:
    def __init__(self, tri, value, col, row, root_sum):
        global _max
        self.value   = value
        self.sum     = root_sum + value
        _max = max( self.sum, _max )

        self.left    = None if isOutOfRange(tri, col + 1, row)     else Node( tri, tri[col + 1][row],     col + 1, row,     self.sum ) # [col + 1, row]
        self.right   = None if isOutOfRange(tri, col + 1, row + 1) else Node( tri, tri[col + 1][row + 1], col + 1, row + 1, self.sum ) # [col + 1, row + 1]
    
    def __str__(self) -> str:
        return "value: {} / sum: {} / left: {} / right: {}".format(self.value, self.sum, self.left, self.right)
    
# def getTree(tri):
#     return Node( tri, tri[0][0], 0, 0, 0 )

# def DFT(tree, pos, sum):
#     global _max
#     node = tree[pos[0]][pos[1]]

#     sum += node.value
#     if node.left == None or node.right == None:
#         _max = max( _max, sum )
    
#     if node.left != None:
#         DFT( tree, node.left,  sum )
#     if node.right != None:
#         DFT( tree, node.right, sum )
    
def solution(triangle):
    Node( triangle, triangle[0][0], 0, 0, 0 )
    
    return _max

print( solution([[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5], [9, 2, 7, 5, 4, 3]]) )
# print( solution([[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [4, 5, 2, 6, 5]]) )