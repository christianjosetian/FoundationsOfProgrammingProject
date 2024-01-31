import random
import math
import time
from consts import *
from pygame.locals import *
    
def distance( y1, y2, x1, x2 ):
    # return positive difference in Y and X coordinates
    return abs( y1 - y2 ) + abs( x1 - x2 )

class Player(GamePlayer):
    def __init__(self):
        self.name = "TSP Version"
        self.group = '1A'
        self.myBot = None
        self.bot_list = [] # <[bot0,bot1,...] in order of Bot.i>
        self.obj_list = [] # <[GameObject_i,GameObject_j,...]>
        self.remaining_objects = [] # <[remaining0,remaining1,remaining2]> in each category
        self.collected_objects = [] # <[collected0,collected1,collected2]> in each category
        self.endgame = "false"

    def insert_bot_to_list(self, bot_list, bot):
        '''(list, Bot) -> NoneType
        Insert given bot to bot_list such that bot_list is in order of Bot.i ([bot0,bot1,...]).
        '''
        k = 0
        while k < len(bot_list) and bot.i > bot_list[k].i:
            k += 1
        bot_list.insert(k, bot)
    
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
            
    def get_all_bots_and_objects_on_map( self, game_map ):
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
                        self.insert_bot_to_list(bot_list, bot)

                        # accumulate the collected objects in each categories
                        for cat in range(len(GAMEOBJECT_TYPES)): # banana, coin, cauldron
                            collected_objects[cat] += bot.collected_objects[cat]
       
        return bot_list, obj_list, remaining_objects, collected_objects
      
    def permute(self, obj_list):
        result = []
        
        if (len(obj_list) == 1):
            return [obj_list[:]]
        
        for i in range( len(obj_list) ):
            objT = obj_list.pop(0)
            perms = self.permute(obj_list)
            for perm in perms:
                perm.append(objT)
            result.extend(perms)
            obj_list.append(objT)
            
        return result
    
    def cost( self, game_map, cur_pos, obj_list, costMax ):
        cobjectToWin = [0,0,0]
        for i in range(0, 3):
            cobjectToWin[i] = (self.myBot.collected_objects[i] + self.remaining_objects[i])//2 + 1

        cobjectHave = [0,0,0]
        for i in range(0, 3):
            cobjectHave[i] = self.myBot.collected_objects[i]

        cost = distance( cur_pos[0], obj_list[0].position[0], cur_pos[1], obj_list[0].position[1] )
        for iobj in range(1, len(obj_list)):
            cobjectHave[obj_list[iobj-1].obj_type] += 1
            cat_won = 0
            for i in range(0, 3):
                if cobjectHave[i]>=cobjectToWin[i] : cat_won += 1
            if cat_won >= 2:
                break
            cost += distance( obj_list[iobj].position[0], obj_list[iobj-1].position[0], obj_list[iobj].position[1], obj_list[iobj-1].position[1] )
            if cost > costMax:
                return costMax + 1
        return cost

    def step(self, game_map, turn, cur_pos):
       
        #get game dimensions, support rectangular
        MapLength = len(game_map)
        assert( MapLength == len(game_map[0]) )
       
        #determine count of objects to win for each category
        self.myBot = self.get_my_bot(game_map, cur_pos)
        self.bot_list, self.obj_list, self.remaining_objects, self.collected_objects = self.get_all_bots_and_objects_on_map(game_map)

        #get all permutations of object list in list of lists
        perms = self.permute( self.obj_list )
        
        #for each permutation compute cost in steps to win
        i_step = 0
        cost_step = self.cost(game_map, cur_pos, perms[0], MapLength*MapLength )
        for i in range(1,len(perms) ):
            cost = self.cost(game_map, cur_pos, perms[i], cost_step )
            if ( cost < cost_step ):
                i_step = i
                cost_step = cost
            
        #for cheapest cost to win make step towards first object
        #print("Best path is ", i_step, " with the following with cost ", cost_step)
        #print("     ", perms[i_step][0].position[1], perms[i_step][0].position[0],
        #      distance( cur_pos[0], perms[i_step][0].position[0], cur_pos[1], perms[i_step][0].position[1] ) )
        #for i in range(1, len(perms[i_step])):
        #    print("     ", perms[i_step][i].position[1], perms[i_step][i].position[0],
        #          distance( perms[i_step][i-1].position[0], perms[i_step][i].position[0], perms[i_step][i-1].position[1], perms[i_step][i].position[1] ) )
                       
        object_step = perms[i_step][0]
        direction = 'up'
        if object_step.position[0] > cur_pos[0]:
            direction = 'down'
        if object_step.position[0] < cur_pos[0]:
            direction = 'up'
        if object_step.position[1] > cur_pos[1]:
            direction = 'right'
        if object_step.position[1] < cur_pos[1]:
            direction = 'left'
        
        return direction
