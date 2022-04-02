
results = []
def graf(n, edges):
    _tmp = { }
    for _ in range(n):
        _tmp[_] = []

    for edge in edges:
        _tmp[edge[0]].append(edge[1])
        _tmp[edge[1]].append(edge[0])
    
    return _tmp

def next(g, a, depth, pref, limit, goal):
    if depth > limit:
        return 0

    if a == goal:
        results.append(pref)
        return 0

    for _ in g[a]:
        if _ in pref:
            continue

        _tmp = pref[:]
        _tmp.append(_)
        next(g, _, depth + 1, _tmp, limit, goal)
    
def solution(n, edges, k, a, b):
    g = graf(n, edges)
    #print(g) 

    next(g, a, 0, [a], k, b)
    #print(results)
    _tmp = []
    for result in results:
        _tmp += result
    
    count = 0
    for diff in list( set([ _ for _ in range(n) ]) - set(_tmp) ):
        g[diff] = []
        for i in range(len(g)):
            if diff in g[i]:
                g[i].remove(diff)
    for item in g.values():
        count += len(item)
    
    #print(count)

    return int( count / 2 )

edges = [[0,1],[1,2],[2,3],[4,0],[5,1],[6,1],[7,2],[7,3],[4,5],[5,6],[6,7]]	
n, k, a, b = 8, 4, 0, 3
solution(n, edges, k, a, b)