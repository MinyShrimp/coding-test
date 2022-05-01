

def solution(n: int, lost: list, reserve: list):
    lost, reserve = sorted(lost), sorted(reserve)
    _reserve = [ r for r in reserve ]

    for r in _reserve:
        if r in lost:
            reserve.remove(r)
            lost.remove(r)
    
    for r in reserve:
        minus, plus = r - 1, r + 1
        if minus > 0:
            if minus in lost:
                lost.remove( minus )
                continue
        if plus <= n:
            if plus in lost:
                lost.remove( plus )
                continue

    return n - len(lost)

print(solution(5, [2,4], [3,1]))