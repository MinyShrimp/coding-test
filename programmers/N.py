
from pprint import pprint
import math

# k, kk, kkk, kkkk, ... 이 맞는지와 k의 갯수
def isPerpectNumber(N, k):
    count, total_count = 0, 0
    
    while True:
        n = N % 10
        N = int( N / 10 )

        total_count += 1
        if n == k:
            count += 1
        if N == 0:
            break
    
    return { "result": total_count == count, "count": count }

# 정수인지 확인
def isIntenger( N ):
    return N - int(N) == 0

# getData
def getData(now, key, datas):
    _min   = 999999

    if( now in datas.keys() ):
        _min = min(_min, datas[now])

    # n, n^2, n^3, n^4, ...
    if key != 1:
        indice = math.log( now, key )
        if( isIntenger( indice ) ): 
            _min = min( _min, int(indice) )

    # n, n * 2, n * 3, n * 4, ...
    value = now / key
    if( isIntenger( value ) ): 
        _min = min( _min, int(value) )

    # N = ( N - 1 ) + 1 = ( N - 2 ) + 2 = ...
    for i in range(1, int(now / 2) + 1):
        _min = min( _min, datas[i] + datas[now - i] )
    return _min

# main 함수
def my_solution(key, number):
    datas = {}

    # case 1) i < n
    #  => 1 = n / n, 2 = (n + n) / n, 3 = (n + n + n) / n, ...
    for i in range(1, key):
        datas[i] = i + 1
    
    # case 2) n, nn, nnn, nnnn, nnnnn
    datas[key] = 1
    datas[key + key * 10] = 2
    datas[key + key * 10 + key * 100] = 3
    datas[key + key * 10 + key * 100 + key * 1000] = 4
    datas[key + key * 10 + key * 100 + key * 1000 + key * 10000] = 5

    # case 3) n - 1 => 3
    datas[key - 1] = 3

    # case 4) (n + n) * (n + n) => 4
    datas[(key + key) * (key + key)] = 4
    
    # case 5) i > n
    for i in range(key + 1, number + 1):
        datas[i] = getData( i, key, datas )

    # pprint(datas, indent=4) 

    result = datas[number]
    return result if result <= 8 else -1

# print(my_solution( 5, 111 ))

###################################################################################################
# 문제 풀이 방법
# 주어진 N을 1번 사용할 때부터 최대 8번 사용할 때까지 반복해서 사칙연산을 한다.
# 1번 사용할 때는 그냥 N
# 2번 사용할 때, ex: N=5, 5*5, 5+5, 5-5, 5/5 가 되므로
# 2번일 때는 1번 (op) 1번 : op -> +, -, *, /
# 3번일 때는 1번 (op) 2번, 2번 (op) 1번 ** 반대도 해주어야 빼기와 나누기가 계산됨
# 4번일 때는 1번 (op) 3번, 2번 (op) 2번, 3번 (op) 1번
# N일 때는 1 (op) N-1, 2 (op) N-2, 3 (op) N-3,... N-1 (op) 1 까지 계산해 준다.
# 매번 계산 할 때마다 결과를 set()에 넣어 주어 중복값을 없앤다.

# 1번에 계산된 값을 2번에서 사용하고 2번에 계산된 값을 3에서 사용하는 방법으로 계산
# 큰 값을 잘게 나누어 계산 하고 그 결과를 재사용할 수 있으며, 계산되는 값들이 겹치므로 DP에 해당.

#-----------------------------------------------------------------
# 저장된 값들에 대한 사칙연산 함수
# 3번 단계에서 X는 1번으로 계산된 결과, Y는 2번에 계산된 결과가 될 수 있음

def calculate_n(X, Y):
    n_set = set()
    for x in X:
        for y in Y:
            n_set.add(x+y)
            n_set.add(x-y)
            n_set.add(x*y)
            if y != 0:
                n_set.add(x//y)
    return n_set

def solution(N, number):
    answer = -1
    result = { 1: { N } }
    if number == N: return 1

    for n in range( 2, 9 ):
        _set = { int( str(N) * n ) }
        for i in range( 1, n ):
            _set.update( calculate_n( result[i], result[n - i] ) )

        if number in _set:
            answer = n
            break

        result[n] = _set
    
    return answer