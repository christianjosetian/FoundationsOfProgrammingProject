
import random

from consts import *

 

def up_is_ok(game_map, cur_pos, step):

    row, col = cur_pos[0] - step, cur_pos[1]

    if row >= 0 and game_map[row][col] and type(game_map[row][col][0]) is GameObject:

        return True

    else:

        return False

 

def down_is_ok(game_map, cur_pos, step, map_size):

    row, col = cur_pos[0] + step, cur_pos[1]

    if row < map_size and game_map[row][col] and type(game_map[row][col][0]) is GameObject:

        return True

    else:

        return False

 

def left_is_ok(game_map, cur_pos, step):

    row, col = cur_pos[0], cur_pos[1] - step

    if col >= 0 and game_map[row][col] and type(game_map[row][col][0]) is GameObject:

        return True

    else:

        return False

 

def right_is_ok(game_map, cur_pos, step, map_size):

    row, col = cur_pos[0], cur_pos[1] + step

    if col < map_size and game_map[row][col] and type(game_map[row][col][0]) is GameObject:

        return True

    else:

        return False

   

def insert_bot_to_list(bot_list, bot):

    '''(list, Bot) -> NoneType

    Insert given bot to bot_list such that bot_list is in order of Bot.i ([bot0,bot1,...]).

    '''

    k = 0

    while k < len(bot_list) and bot.i > bot_list[k].i:

        k += 1

    bot_list.insert(k, bot)

 

def get_all_bots_and_objects_on_map(game_map):

    ''' (list) -> list, list, list, list

    Returns a list of Bots ([bot0,bot1,...] in order of Bot.i), a list of GameObjects ([GameObject_i,GameObject_j,...]) on the map,

    a list of the remaining GameObjects ([remaining0,remaining1,remaining2]), and

    a list of the collected GameObjects ([collected0,collected1,collected2]) in each category .

    '''

    bot_list = []

    obj_list = []

    remaining_objects = [0] * len(GAMEOBJECT_TYPES)

    collected_objects = [0] * len(GAMEOBJECT_TYPES)

    map_size = len(game_map)

    for i in range(map_size):

        for j in range(map_size):

            item = game_map[i][j]  # item is either an empty list, or a list with one GameObject, or a list with one or more Bots

            if len(item) == 0: # item is an empty list

                continue

            if type(item[0]) is GameObject: # item is a list with one GameObject

                obj_list.append(item[0])

                # accumulate the remaining objects in each category

                remaining_objects[item[0].obj_type] += 1

            else: # item is a list with one or more Bots

                for bot in item:

                    # insert bot to bot_list so bot_list is in order of Bot.i

                    insert_bot_to_list(bot_list, bot)

                    # accumulate the collected objects in each categories

                    for cat in range(len(GAMEOBJECT_TYPES)): # banana, coin, cauldron

                        collected_objects[cat] += bot.collected_objects[cat]

   

    return bot_list, obj_list, remaining_objects, collected_objects

   

def top1_and_top2(bot_list, cat):

    '''(list, int) -> int, int

    return the top 1 and top 2 object numbers bots collected in given category.

    <bot_list=[bot0,bot1,...] in order of Bot.i> <cat=0,1,2>

    '''

    cat_col = []

    for bot in bot_list:

        cat_col.append(bot.collected_objects[cat])

           

    cat_col_len = len(cat_col)

       

    if cat_col_len > 1:

        cat_col.sort()

        return cat_col[-1], cat_col[-2]

    elif cat_col_len == 1:

        return cat_col[0], cat_col[0]

    else:

        return 0, 0

 

def distance(pos1, pos2):

    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

       

def insert_to_dis_list(dis_list, dis, action, cat):

    i = 0

    while i < len(dis_list) and dis > dis_list[i][0]:

        i += 1

    dis_list.insert(i, [dis, action, cat])

 

class Player(GamePlayer):

    def __init__(self):

        self.name = "Modesty"

        self.group = '17D'

        self.myBot = None

        self.bot_list = [] # <[bot0,bot1,...] in order of Bot.i>

        self.obj_list = [] # <[GameObject_i,GameObject_j,...]>

        self.remaining_objects = [] # <[remaining0,remaining1,remaining2]> in each category

        self.collected_objects = [] # <[collected0,collected1,collected2]> in each category

    def get_my_bot(self, game_map, cur_pos):

        '''(list, tuple) -> Bot

        Returns the Bot object for this player.

        '''

        i, j = cur_pos

        bots = game_map[i][j]

        assert len(bots) != 0

        for bot in bots:

            if bot.i == self.i:

                return bot

 

    def object_is_needed(self, cat):

        # get the top 1 and top 2 object numbers bots collected in this category

        top1, top2 = top1_and_top2(self.bot_list, cat)

           

        # object of this category is not needed if top2 player has no chance to catch up myBot

        if top2 + self.remaining_objects[cat] < self.myBot.collected_objects[cat]:

            return False

           

        # the number of objects myBot need to catch up top1 player in this category

        catch = top1 - self.myBot.collected_objects[cat]

           

        # object of this category is not needed if there is not enough objects left for myBot to catch the top1 player

        if catch > self.remaining_objects[cat]:

            return False

           

        return True

   

    def object_to_bots_shortest_distance(self, obj_pos):

        dis = []

        for bot in self.bot_list:

            if bot.i != self.myBot.i:

                dis.append(distance(obj_pos, bot.position))

        dis.sort()

        return dis[0]

       

    def step(self, game_map, turn, cur_pos):

        self.myBot = self.get_my_bot(game_map, cur_pos)

        self.bot_list, self.obj_list, self.remaining_objects, self.collected_objects = get_all_bots_and_objects_on_map(game_map)

 

        map_size = len(game_map)

        row, col = cur_pos[0], cur_pos[1]

        max_step = max(row, col, map_size-1-row, map_size-1-col)

       

        for step in range(1, max_step+1):

            dis_list = []

           

            if up_is_ok(game_map, cur_pos, step):

               

                up_cat = game_map[row-step][col][0].obj_type

               

                if self.object_is_needed(up_cat):

                    up_dis = self.object_to_bots_shortest_distance((row-step, col))

                    dis_list.append([up_dis, 'up', up_cat])

 

 

            if down_is_ok(game_map, cur_pos, step, map_size):

               

                down_cat = game_map[row+step][col][0].obj_type

               

                if self.object_is_needed(down_cat):

               

                    down_dis = self.object_to_bots_shortest_distance((row+step, col))

                    insert_to_dis_list(dis_list, down_dis, 'down', down_cat)

 

 

            if left_is_ok(game_map, cur_pos, step):

               

                left_cat = game_map[row][col-step][0].obj_type

               

                if self.object_is_needed(left_cat):

                   

                    left_dis = self.object_to_bots_shortest_distance((row, col-step))

                    insert_to_dis_list(dis_list, left_dis, 'left', left_cat)

 

           

            if right_is_ok(game_map, cur_pos, step, map_size):

               

                right_cat = game_map[row][col+step][0].obj_type

               

                if self.object_is_needed(right_cat):

                   

                    right_dis = self.object_to_bots_shortest_distance((row, col+step))

                    insert_to_dis_list(dis_list, right_dis, 'right', right_cat)

           

           

            list_len = len(dis_list)

            i = 0

            while i < list_len and dis_list[i][0] < step:

                i += 1

            eql_idx = i

            while i < list_len and dis_list[i][0] == step:

                i += 1

            grt_idx = i

           

            rem_obj = map_size * map_size

            action = None

            for j in range(grt_idx, list_len):

                if self.remaining_objects[dis_list[j][2]] < rem_obj:

                    rem_obj = self.remaining_objects[dis_list[j][2]]

                    action = dis_list[j][1]

            if action is not None:
                self.grossY = "unknown"
                self.grossX = "unknown"
                return action

           

            rem_obj = map_size * map_size

            action = None

            for j in range(eql_idx, grt_idx):

                if self.remaining_objects[dis_list[j][2]] < rem_obj:

                    rem_obj = self.remaining_objects[dis_list[j][2]]

                    action = dis_list[j][1]

            if action is not None:
                self.grossY = "unknown"
                self.grossX = "unknown"
                return action

        return random.choice(list(ACTIONS))