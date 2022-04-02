
dist = [[0,2,3,1],[2,0,1,1],[3,1,0,2],[1,1,2,0]]
dist2 = [[0,5,2,4,1],[5,0,3,9,6],[2,3,0,6,3],[4,9,6,0,3],[1,6,3,3,0]]

def solution(dist):
    result = []
    dot_count = len(dist)
    for item in dist:
        _tmp = {}
        for _i, _v in enumerate( item ):
            _tmp[_i] = _v
        _tmp = sorted(_tmp.items(), key=lambda x: x[1])

        _count = 0
        for i in range(len(_tmp) - 1):
            _pos = [ _tmp[i][0], _tmp[i+1][0] ]
            _value = [ _tmp[i][1], _tmp[i+1][1] ]
            if dist[_pos[0]][_pos[1]] == _value[1] - _value[0]:
                _count += 1
                
        if _count == dot_count - 1:
            result.append( [ _[0] for _ in _tmp ] )
    
    return result

print(solution(dist))
print(solution(dist2))