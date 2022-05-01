# RPG EXTREME
## START 2022-05-01 17:58
## PAUSE 18:38 ~ 19:00
## END   2022-05-01 22:28

TYPE = {
    "." : "NONE",
    "#" : "WALL",
    "&" : "MONSTER",
    "M" : "BOSS",
    "B" : "ITEM",
    "^" : "TRAP",
    "@" : "PLAYER"
}

REVERSE_TYPE = {
    "NONE"    : ".",
    "WALL"    : "#",
    "MONSTER" : "&",
    "BOSS"    : "M",
    "ITEM"    : "B",
    "TRAP"    : "^",
    "PLAYER"  : "@"
}

result = 'Press any key to continue.'

class Object:
    def __init__(self, y, x, type):
        self.y, self.x, self.type = y, x, TYPE[type]
    
    def __str__(self):
        return f"{self.x} {self.y} {self.type}"

class PlayerDeadError(Exception): pass
class PlayerRebirthError(Exception): pass
class BossKillError(Exception): pass

class Player(Object):
    def __init__(self, y, x, type):
        super().__init__( y, x, type )
        self.start_y, self.start_x = y, x
        self.lv, self.hp, self.max_hp, self.cur_exp, self.max_exp = 1, 20, 20, 0, 5
        self.n_att, self.w_att, self.n_def, self.w_def, self.is_dead = 2, 0, 2, 0, False
        self.accessories = []
    
    def is_can_level_up(self):
        return self.cur_exp >= self.max_exp
    
    def level_up(self):
        self.lv += 1
        self.cur_exp, self.max_exp = 0, self.lv * 5
        self.max_hp += 5
        self.hp = self.max_hp
        self.n_att, self.n_def = self.n_att + 2, self.n_def + 2
    
    def set_wep(self, w):
        # self.w_att = w if w > self.w_att else self.w_att
        self.w_att = w
    
    def set_def(self, d):
        # self.w_def = d if d > self.w_def else self.w_def
        self.w_def = d
    
    def set_accessories(self, o):
        if len(self.accessories) >= 4:
            return
        self.accessories.append(o)
    
    def plus_exp(self, exp):
        if 'HR' in self.accessories:
            self.plus_hp(3)

        self.cur_exp += int(exp * 1.2) if 'EX' in self.accessories else exp
        if self.is_can_level_up():
            self.level_up()
    
    def plus_hp(self, hp):
        self.hp = min( hp + self.hp, self.max_hp )
    
    def vaild_dead(self, monster = None):
        global result
        self.is_dead = self.hp <= 0
        if self.is_dead:
            if 'RE' in self.accessories:
                self.accessories.remove('RE')
                self.hp = self.max_hp
                self.is_dead = False
                self.move( self.start_y, self.start_x )

                if monster != None:
                    monster.hp = monster.max_hp
                
                raise PlayerRebirthError
            else:
                self.hp = 0
                if monster == None:
                    result = "YOU HAVE BEEN KILLED BY SPIKE TRAP.."
                else:
                    result = f"YOU HAVE BEEN KILLED BY {monster.name}.."
                raise PlayerDeadError
    
    def get_att(self):
        return self.w_att + self.n_att
    
    def get_def(self):
        return self.w_def + self.n_def
    
    def get_move_position(self, dir):
        if dir == "L":
            return self.y, self.x - 1
        elif dir == "R":
            return self.y, self.x + 1
        elif dir == "U":
            return self.y - 1, self.x
        elif dir == "D":
            return self.y + 1, self.x
    
    def set_item(self, i):
        if i.type2 == 'W':
            self.set_wep(i.effect)
        elif i.type2 == 'A':
            self.set_def(i.effect)
        elif i.type2 == 'O':
            self.set_accessories(i.effect)
    
    def move(self, y, x):
        self.y, self.x = y, x

    def down_trap(self):
        self.plus_hp( -1 if 'DX' in self.accessories else -5 )
        self.vaild_dead()
    
    def __str__(self):
        return f"LV : {self.lv}\nHP : {self.hp}/{self.max_hp}\nATT : {self.n_att}+{self.w_att}\nDEF : {self.n_def}+{self.w_def}\nEXP : {self.cur_exp}/{self.max_exp}"

class Monster(Object):
    def __init__(self, y, x, type):
        super().__init__(y, x, type)
        self.name, self.n_att, self.n_def, self.hp, self.max_hp, self.exp = "", 0, 0, 0, 0, 0
        
    def set_ability(self, name, n_att, n_def, hp, exp):
        self.name, self.n_att, self.n_def, self.hp, self.max_hp, self.exp = name, n_att, n_def, hp, hp, exp
    
    def __str__(self):
        return f"{super().__str__()} {self.name} {self.n_att} {self.n_def} {self.hp} {self.exp}"

class Item(Object):
    def __init__(self, y, x, type):
        super().__init__(y, x, type)
        self.type2, self.effect = "", ""
    
    def set_ability(self, type2, effect):
        self.type2, self.effect = type2, int(effect) if type2 != "O" else effect
    
    def __str__(self):
        return f"{super().__str__()} {self.type2} {self.effect}"

class Game:
    def __init__(self, N, M):
        self.map = []
        self.monster_count = 0
        self.item_count = 0
        self.now_turn = 0
        self.row, self.col = M, N

        ## MAP
        for y in range(N):
            _tmp = []
            for x, v in enumerate( list(input()) ):
                if v == '@':
                    self.player = Player(y, x, v)
                    _tmp.append(Object(y, x, "."))
                elif v == "&" or v == "M":
                    self.monster_count += 1
                    _tmp.append(Monster(y, x, v)) 
                elif v == "B":
                    self.item_count += 1
                    _tmp.append(Item(y, x, v))
                else:
                    _tmp.append(Object(y, x, v))
            self.map.append(_tmp)
        
        ## CMD
        self.cmds = list(input())
        
        ## MONSTER
        for _ in range(self.monster_count):
            y, x, name, n_atk, n_def, hp, exp = input().split(' ')
            self.map[int(y) - 1][int(x) - 1].set_ability(name, int(n_atk), int(n_def), int(hp), int(exp))
        
        ## ITEM
        for _ in range(self.item_count):
            y, x, type2, effect = input().split(' ')
            self.map[int(y) - 1][int(x) - 1].set_ability(type2, effect)

    def fight(self, monster):
        first_turn = True
        while True:
            if monster.type == "BOSS" and first_turn and 'HU' in self.player.accessories:
                self.player.hp = self.player.max_hp
        
            demage = max( 1, self.player.get_att() - monster.n_def )
            if first_turn:
                if 'CO' in self.player.accessories:
                    if 'DX' in self.player.accessories:
                        demage = max( 1, self.player.get_att() * 3 - monster.n_def )
                    else:
                        demage = max( 1, self.player.get_att() * 2 - monster.n_def )
            monster.hp = monster.hp - demage

            if monster.hp <= 0:
                self.player.plus_exp( monster.exp )
                if monster.type == "BOSS":
                    self.player.move( monster.y, monster.x )
                    raise BossKillError
                return True

            if not( monster.type == "BOSS" and first_turn and 'HU' in self.player.accessories ):
                demage = max( 1, monster.n_att - self.player.get_def() )
                self.player.plus_hp( demage * -1 )
                self.player.vaild_dead(monster)

            first_turn = False

    def interaction(self, y, x):
        _type = self.map[y][x].type

        if _type == "MONSTER" or _type == "BOSS":
            self.fight( self.map[y][x] )
            self.map[y][x] = Object(y, x, '.')
        elif _type == "WALL":
            if self.map[self.player.y][self.player.x].type == "TRAP":
                self.player.down_trap()
            return False
        elif _type == "ITEM":
            self.player.set_item( self.map[y][x] )
            self.map[y][x] = Object(y, x, '.')
        elif _type == "TRAP":
            self.player.down_trap()
        
        self.player.move(y, x)
        return True
    
    def turn(self):
        global result
        for cmd in self.cmds:
            try:
                self.now_turn += 1

                move_y, move_x = self.player.get_move_position(cmd)
                if move_x < 0 or move_x >= self.row or move_y < 0 or move_y >= self.col:
                    if self.map[self.player.y][self.player.x].type == "TRAP":
                        self.player.down_trap()
                    continue

                self.interaction(move_y, move_x)
            except PlayerRebirthError:
                pass
            except PlayerDeadError:
                return
            except BossKillError:
                result = "YOU WIN!"
                return
    
    def __str__(self):
        _result = ""
        for y, objects in enumerate(self.map):
            for x, obj in enumerate(objects):
                if y == self.player.y and x == self.player.x and not self.player.is_dead:
                    _result += "@"
                else:
                    _result += REVERSE_TYPE[obj.type]
            _result += '\n'
        
        _result += f"Passed Turns : {self.now_turn}\n"
        _result += str( self.player )
        return _result

N, M = input().split(' ')
N, M = int(N), int(M)
_game = Game(N, M)
_game.turn()

_str = str(_game) + '\n' + result
print(_str)