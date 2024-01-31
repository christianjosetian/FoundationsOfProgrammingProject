# Authors: Christian Tian, Anton Sushchenko, Manon Boisselier, Alexandre Tawil, Nicholas McConnell
# ID: 261001835
# Group: 17D

from consts import *

def distance(pos, y, x):
    # return positive difference in Y and X coordinates
    return abs( pos[0] - y ) + abs( pos[1] - x )

class Player(GamePlayer):
    def __init__(self):
        self.name = "Aggregate"
        self.group = "17D"
        self.grossY = "unknown"
        self.grossX = "unknown"
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
      
    def top1_and_top2(self, bot_list, cat):
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
            return cat_col[0], 0
        else:
            return 0, 0

    def value( self, game_map, cur_pos, object ):
        # if game is over just mop up board
        if self.endgame == "true":
            return 1
        
        # get the top 1 and top 2 object numbers bots collected in this category
        cat = object.obj_type
        top1, top2 = self.top1_and_top2(self.bot_list, cat)

        # object of this category is not needed if the category is won by any player
        if top2 + self.remaining_objects[cat] < top1:
            return 0

        # object of this category is not needed if my bot cannot catch the leader
        if self.myBot.collected_objects[cat] + self.remaining_objects[cat] < top1:
            return 0

        #object categories have value inversely proportional to how many more we need to win
        cobjectToWin = (top1 - self.myBot.collected_objects[cat] + self.remaining_objects[cat])//2 + 1
        #print("Value of this category is:", cat, ": ", cobjectToWin )
        
        return 1/cobjectToWin

       
    def step(self, game_map, turn, cur_pos):
        map_size = len(game_map)
       
        #initialize variables
        self.myBot = self.get_my_bot(game_map, cur_pos)
        self.bot_list, self.obj_list, self.remaining_objects, self.collected_objects = self.get_all_bots_and_objects_on_map(game_map)
        
        #fine motor control up
        fineUp = 0
        if cur_pos[0] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1]][0]):
                    fineUp = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1]][0])
                           
        #fine motor control down
        fineDown = 0
        if cur_pos[0] < map_size - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1]][0]):
                    fineDown = self.value(game_map, cur_pos, game_map[cur_pos[0] + 1][cur_pos[1]][0])
           
        #fine motor control left
        fineLeft = 0
        if cur_pos[1] > 0:
            if game_map[cur_pos[0]][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0]][cur_pos[1] - 1][0]):
                    fineLeft = self.value(game_map, cur_pos, game_map[cur_pos[0]][cur_pos[1] - 1][0])
                           
        #fine motor control right
        fineRight = 0
        if cur_pos[1] < map_size - 1:
            if game_map[cur_pos[0]][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0]][cur_pos[1] + 1][0]):
                    fineRight = self.value(game_map, cur_pos, game_map[cur_pos[0]][cur_pos[1] + 1][0])
 
        #find nominal desired fine direction   (one step)        
        fineMax = max(fineUp, fineDown, fineLeft, fineRight)
        if fineMax > 0:
            direction = ""
            if fineUp == fineMax:
                direction = "up"
            elif fineDown == fineMax:
                direction = "down"
            elif fineLeft == fineMax:
                direction = "left"
            else:
                assert(fineRight == fineMax)
                direction = "right"
               
            self.grossY = "unknown"
            self.grossX = "unknown"
            return direction
           
        #fine motor control upper left
        fineUpperLeft = 0
        if cur_pos[0] > 0 and cur_pos[1] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] - 1][0]):
                    fineUpperLeft = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1] - 1][0])
                           
        #fine motor control lower right
        fineLowerRight = 0
        if cur_pos[0] < map_size - 1 and cur_pos[1] < map_size - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1] + 1][0]):
                    fineLowerRight = self.value(game_map, cur_pos, game_map[cur_pos[0] + 1][cur_pos[1] + 1][0])
           
        #fine motor upper right
        fineUpperRight = 0
        if cur_pos[0] > 0 and cur_pos[1] < map_size - 1:
            if game_map[cur_pos[0] - 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] + 1][0]):
                    fineUpperRight = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1] + 1][0])
                           
        #fine motor control lower left
        fineLowerLeft = 0
        if cur_pos[0] < map_size - 1 and cur_pos[1] > 0:
            if game_map[cur_pos[0] + 1][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1] - 1][0]):
                    fineLowerLeft = self.value(game_map, cur_pos, game_map[cur_pos[0] + 1][cur_pos[1] - 1][0])
       
        #compute value of step based on second step
        fineUp = fineUpperLeft + fineUpperRight
        fineDown = fineLowerLeft + fineLowerRight
        fineLeft = fineUpperLeft + fineLowerLeft
        fineRight = fineUpperRight + fineLowerRight
       
        #find nominal desired fine direction (two step)        
        fineMax = max(fineUp, fineDown, fineLeft, fineRight)
        if fineMax > 0:
            direction = ""
            if fineUp == fineMax:
                direction = "up"
            elif fineDown == fineMax:
                direction = "down"
            elif fineLeft == fineMax:
                direction = "left"
            else:
                assert(fineRight == fineMax)
                direction = "right"
               
            self.grossY = "unknown"
            self.grossX = "unknown"
            return direction
       
        #gross motor control up
        grossUp = 0
        if cur_pos[0] > 0:
            for i in range(0, cur_pos[0]):
                for j in range(0, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossUp += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)

        #gross motor control down
        grossDown = 0
        if cur_pos[0] < map_size - 1:
            for i in range(cur_pos[0] + 1, map_size):
                for j in range(0, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossDown += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)
                           
        #gross motor control left
        grossLeft = 0
        if cur_pos[1] > 0:
            for i in range(0, map_size):
                for j in range(0, cur_pos[1]):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossLeft += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)

        #gross motor control right
        grossRight = 0
        if cur_pos[1] < map_size - 1:
            for i in range(0, map_size):
                for j in range(cur_pos[1] + 1, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossRight += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)
                           
        #find nominal desired gross direction            
        grossMax = max(grossUp, grossDown, grossLeft, grossRight)
        
        #if game is over and either we won or lost just mop up the board
        if grossMax == 0:
            assert( self.endgame == "false" )
            self.endgame = "true"
            
        if grossUp == grossMax:
            direction = "up"
        elif grossDown == grossMax:
            direction = "down"
        elif grossLeft == grossMax:
            direction = "left"
        else:
            assert(grossRight == grossMax)
            direction = "right"
       
        #hysteresis to avoid getting stuck between two equal object cohorts
        if direction == "down" and self.grossY == "up" and grossUp == 0:
            if self.grossX == "unknown":
                if grossLeft > grossRight:
                    direction = "right"
                else:
                    direction = "left"
            elif self.grossX == "left" and grossLeft > 0:
                direction == "left"
            elif self.grossX == "right" and grossRight > 0:
                direction = "right"
        elif direction == "up" and self.grossY == "down" and grossDown == 0:
            if self.grossX == "unknown":
                if grossLeft > grossRight:
                    direction = "right"
                else:
                    direction = "left"
            elif self.grossX == "left" and grossLeft > 0:
                direction = "left"
            elif self.grossX == "right" and grossRight > 0:
                direction = "right"
        elif direction == "right" and self.grossX == "left" and grossLeft == 0:
            if self.grossY == "unknown":
                if grossUp > grossDown:
                    direction = "up"
                else:
                    direction = "down"
            elif self.grossY == "up" and grossUp > 0:
                direction = "up"
            elif self.grossY == "down" and grossDown > 0:
                direction = "down"
        elif direction == "left" and self.grossX == "right" and grossRight == 0:
            if self.grossY == "unknown":
                if grossUp > grossDown:
                    direction = "up"
                else:
                    direction = "down"
            elif self.grossY == "up" and grossUp > 0:
                direction = "up"
            elif self.grossY == "down" and grossDown > 0:
                direction = "down"
        elif direction == "down" and self.grossY == "up" and grossUp > 0:
             direction = "up"
        elif direction == "up" and self.grossY == "down" and grossDown > 0:
            direction = "down"
        elif direction == "right" and self.grossX == "left" and grossLeft > 0:
            direction = "left"
        elif direction == "left" and self.grossX == "right" and grossRight > 0:
            direction = "right"

       
        if direction == "up" or direction == "down":
            self.grossY = direction
        elif direction == "left" or direction == "right":
            self.grossX = direction

        return direction

