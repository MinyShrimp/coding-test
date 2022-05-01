
def isOutOfRange( tri, col, row ):
    return \
        ( col < 0 or len(tri) <= col) or \
        ( row < 0 or len(tri[col]) <= row )

def setTree(tri):
    for col_i, col_v in enumerate( tri ):
        for row_i, row_v in enumerate( col_v ):
            tri[col_i][row_i] = {
                "value": row_v, "sum": -1,
                "p1": None if isOutOfRange(tri, col_i - 1, row_i - 1) else [col_i - 1, row_i - 1],
                "p2": None if isOutOfRange(tri, col_i - 1, row_i)     else [col_i - 1, row_i],
                "pos": [ col_i, row_i ]
            }
    tri[0][0]["sum"] = tri[0][0]["value"]

def getNode( tri, pos ):
    return None if pos == None else tri[pos[0]][pos[1]]

def getSum( tri, node ):
    if node["sum"] != -1:
        return node["sum"]

    p1 = getNode( tri, node["p1"] )
    p2 = getNode( tri, node["p2"] )

    if p1 == None and p2 != None:
        if p2["sum"] != -1:
            node["sum"] = node["value"] + p2["sum"]
        else:
            getSum( tri, p2 )
            node["sum"] = node["value"] + p2["sum"]

    elif p1 != None and p2 == None:
        if p1["sum"] != -1:
            node["sum"] = node["value"] + p1["sum"]
        else:
            getSum( tri, p1 )
            node["sum"] = node["value"] + p1["sum"]

    elif p1 != None and p2 != None:
        if p1["sum"] == -1:
            getSum( tri, p1 )
            node["sum"] = node["value"] + p1["sum"]
        if p2["sum"] == -1:
            getSum( tri, p2 )
            node["sum"] = node["value"] + p2["sum"]
        if p1["sum"] != -1 and p2["sum"] != -1:
            node["sum"] = node["value"] + max( p1["sum"], p2["sum"] )
    
    #print(node, "\t|", p1, "\t|", p2)

def search( tri ):
    _max = -1
    #print("="*200)
    for row in range( len(tri[-1]) ):
        node = tri[-1][row]
        getSum( tri, node )

        _max = max( _max, node["sum"] )
        #print("="*200)
    
    return _max

def search2( tri ):
    _max = -1
    for row in range( len(tri[-1]) ):
        node = tri[-1][row]
        prevs = []
        while True:
            p1 = getNode( tri, node["p1"] )
            p2 = getNode( tri, node["p2"] )

            if p1 == None and p2 != None:
                if p2["sum"] != -1:
                    node["sum"] = node["value"] + p2["sum"]
                    if len(prevs) == 0: break
                    node = prevs.pop()
                else:
                    prevs.append( node )
                    node = p2
            elif p1 != None and p2 == None:
                if p1["sum"] != -1:
                    node["sum"] = node["value"] + p1["sum"]
                    if len(prevs) == 0: break
                    node = prevs.pop()
                else:
                    prevs.append( node )
                    node = p1
            elif p1 != None and p2 != None:
                if p1["sum"] == -1:
                    prevs.append( node )
                    node = p1
                if p2["sum"] == -1:
                    prevs.append( node )
                    node = p2
                if p1["sum"] != -1 and p2["sum"] != -1:
                    node["sum"] = node["value"] + max( p1["sum"], p2["sum"] )
                    if len(prevs) == 0: break
                    node = prevs.pop()
            
        #     print(node, "\t|", p1, "\t|", p2)
        # print("="*200)

        _max = max( _max, node["sum"] )
    return _max

def solution(triangle):
    setTree(triangle)
    return search(triangle)
    
print( solution([[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]) )
# print( solution([[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [4, 5, 2, 6, 5]]) )