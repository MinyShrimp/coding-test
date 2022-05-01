# RPG EXTREME
# INPUT
# 7 8
## . : 빈공간
## # : 벽
## B : 아이템 - W(무기) A(방어구) O(장신구)
## & : 몬스터 - y, x, name, atk, def, hp, exp
## ^ : 가시 함정 ( 체력 -5 )
## M : 보스몬스터 - y, x, name, atk, def, hp, exp
# .&....&.
# ..B.&..&
# B...&...
# .B@.B#..
# .&....M.
# .B...B..
# ..B^^&..
# RRRUULLULUDDDLDRDRDRRRURRULUULLU
# 3 5 One 4 2 10 3
# 2 5 Two 10 2 8 3
# 1 2 Three 20 2 14 7
# 5 2 Four 16 2 16 5
# 7 6 Five 16 5 16 12
# 5 7 Boss 2 9 20 2
# 1 7 EO 20 1 1 4
# 2 8 ET 10 5 4 10
# 4 5 W 4
# 2 3 O CO
# 3 1 A 10
# 4 2 A 2
# 6 2 O DX
# 7 3 O HU
# 6 6 W 3

## START 2022-05-01 17:58
## PAUSE 18:38 ~ 19:00
## END   2022-05-

TYPE = {
    "." : "NONE",
    "#" : "WALL",
    "&" : "MONSTER",
    "M" : "BOSS",
    "B" : "ITEM",
    "^" : "TRAP",
    "@" : "PLAYER"
}

class Object:
    def __init__(self, y, x, type) -> None:
        self.y, self.x, self.type = y, x, TYPE[type]
    
    def __str__(self) -> str:
        return f"{self.type} {self.x} {self.y}"

class Player(Object):
    def __init__(self, y, x, type) -> None:
        super().__init__( y, x, type )
        self.lv, self.hp, self.max_hp, self.cur_exp, self.max_exp = 1, 20, 20, 0, 5
        self.n_att, self.w_att, self.n_def, self.w_def = 2, 0, 2, 0
        self.accessories = []
    
    def is_can_level_up(self) -> bool:
        return self.cur_exp >= self.max_exp
    
    def level_up(self) -> None:
        if not self.is_can_level_up():
            return 

        self.lv += 1
        self.cur_exp, self.max_exp = 0, self.lv * 5
        self.max_hp += 5
        self.hp = self.max_hp
        self.n_att, self.n_def = self.n_att + 2, self.n_def + 2
    
    def set_exp(self, exp) -> None:
        self.cur_exp += exp
        self.level_up()
    
    def set_wep(self, w) -> None:
        self.w_att = w if w > self.w_att else self.w_att
    
    def set_def(self, d) -> None:
        self.w_def = d if d > self.w_def else self.w_def
    
    def plus_hp(self, hp) -> None:
        self.hp = min( hp + self.hp, self.max_hp )
    
    def get_att(self) -> int:
        return self.w_att + self.n_att
    
    def get_def(self) -> int:
        return self.w_def + self.n_def
    
    def get_move_position(self, dir) -> None:
        if dir == "L":
            return self.y, self.x - 1
        elif dir == "R":
            return self.y, self.x + 1
        elif dir == "U":
            return self.y - 1, self.x
        elif dir == "D":
            return self.y + 1, self.x

    def move(self, dir, map) -> None:
        move_pos = self.get_move_position(dir)
    
    def get_accessories(self, o) -> None:
        if len(self.accessories) > 4:
            return
        self.accessories.append(o)
    
    # def __str__(self) -> str:
    #     return f"{self.type} {self.x} {self.y}"

class Monster(Object):
    def __init__(self, y, x, type, _name, _att, _def, _hp, _exp) -> None:
        super().__init__(y, x, type)
        self.name, self.n_att, self.n_def, self.hp, self.exp = _name, _att, _def, _hp, _exp

class Game:
    def __init__(self, N):
        self.map = []
        for y in range(N):
            _tmp = []
            for x, v in enumerate( list(input()) ):
                if v == '@':
                    self.player = Player(y, x, v)
                    _tmp.append(self.player)
                elif v == "&" or v == "B":
                    _tmp.append(Monster(y, x, v, "", 0, 0, 0, 0)) 
                else:
                    _tmp.append(Object(y, x, v))
            self.map.append(_tmp)
    
    def set_cmd(self, _cmd):
        self.cmds = _cmd

if __name__ == "__main__":
    N, M = input().split(' ')
    N, M = int(N), int(M)
    _game = Game(N)
    print( [ str(o) for o in _game.map[0] ] )
    _cmd = list( input() )
