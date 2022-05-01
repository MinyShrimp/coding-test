
engs = {
    "A": [ 0, -26], "B": [ 1, -25],
    "C": [ 2, -24], "D": [ 3, -23],
    "E": [ 4, -22], "F": [ 5, -21],
    "G": [ 6, -20], "H": [ 7, -19],
    "I": [ 8, -18], "J": [ 9, -17],
    "K": [10, -16], "L": [11, -15],
    "M": [12, -14], "N": [13, -13],
    "O": [14, -12], "P": [15, -11],
    "Q": [16, -10], "R": [17,  -9],
    "S": [18,  -8], "T": [19,  -7],
    "U": [20,  -6], "V": [21,  -5],
    "W": [22,  -4], "X": [23,  -3],
    "Y": [24,  -2], "Z": [25,  -1],
}

def solution(name: list):
    name_index   = [ engs[n] for n in name ]
    tmp_index    = [ engs["A"] for n in name ]
    result_index = [ [0, False] for n in name ]
    answer = 0

    for i, v in enumerate( zip( name_index, tmp_index ) ):
        _min = 100
        for a in v[1]:
            for b in v[0]:
                _tmp = a - b if a - b > 0 else b - a
                _min = min(_min, _tmp)
        result_index[i][0] = _min
        answer += _min

    now_index, cursor, result_index[0][1] = 0, 0, True
    plus, minus = now_index + 1, now_index - 1
    if result_index[plus][0] >= result_index[minus][0]:
        now_index = plus
        cursor += 1
    else:
        now_index = minus
        cursor += 1
    
    print(result_index)

    return answer

print(solution("JEREON"))