from enum import Enum

GAMEOBJECT_TYPES = {
    "banana": 0,
    "coin": 1,
    "cauldron": 2
}

ACTIONS = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3
}

def pretty_print(game_map):
    print("**** GAME MAP ****")
    for row in game_map:
        print('\t -- '.join([str(x) for x in row]))
    print("******************")

def get_delta_between_points(pt1, pt2):
    return get_dx_dy_between_points(pt1, pt2)

def get_dx_dy_between_points(pt1, pt2):
    dy, dx = 0, 0
    
    if pt1[0] - pt2[0] > 0:
        dy = 1
    elif pt1[0] - pt2[0] < 0:
        dy = -1
    elif pt1[1] - pt2[1] > 0:
        dx = 1
    elif pt1[1] - pt2[1] < 0:
        dx = -1
    else:
        raise ValueError
    
    return dy, dx

def get_action_for_delta(dx, dy):
    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == 1:
        return 'down'
    elif dy == -1:
        return 'up'
    raise ValueError("dx, dy must be -1 or 1")

class GameStatus(Enum):
    IN_PROGRESS = 0
    TIMEOUT = 1
    GAMEOBJECT_COLLECTED = 2
    ALL_GAMEOBJECTS_COLLECTED = 3


class GamePlayer:
    pass


class GameState:
    def __init__(self, bots, map_, turn):
        self.bots = bots
        self.map = map_
        self.turn = turn

class GameObject:
    def __init__(self, pos, obj_type):
        self.position = pos
        self.obj_type = obj_type

    def __repr__(self):
        return f"GameObject:{{{self.position[0]}, {self.position[1]}| {self.obj_type}}}"
    
    def get_name(self):
        return f"f{self.obj_type+1}"


class Bot:
    def __init__(self, player=None, i=-1):
        self.player = player
        self.i = i
        if player is not None:
            self.i = player.i
            self.name = player.name
            self.group = player.group
            self.image_name = player.image_name
        self.collected_objects = [0, 0, 0]
        self.prev_collected_objects = [0, 0, 0]
        
    @classmethod
    def copy_Bot(cls, orig):
        bot = cls(None)
        bot.name = orig.name
        bot.group = orig.group
        bot.i = orig.i
        bot.image_name = orig.image_name
        bot.collected_objects = orig.collected_objects[:]
        bot.prev_collected_objects = orig.prev_collected_objects[:]
        bot.position = orig.position
        bot.category_tops = orig.category_tops
        return bot
    
    def __repr__(self):
        return f"Bot:{{{self.position[0]}, {self.position[1]} | {self.get_name()} | {self.collected_objects}}}"

    def get_name(self):
        return f"b{self.image_name}"

    def pos(self):
        return (self.position[0], self.position[1])

    def set_pos(self, pos):
        self.position = pos
    
    def add_object(self, obj):
        self.prev_collected_objects = self.collected_objects[:]
        self.collected_objects[obj] += 1
    
    def step(self, game_map, turn):
        return self.player.step(game_map, turn, tuple(self.position))
