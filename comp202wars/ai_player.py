# Authors: Christian Tian, Anton Sushchenko, Manon Boisselier, Alexandre Tawil, Nicholas McConnell
# ID: 261001835
# Group: 17D

from consts import *

def distance(pos, y, x):
    # return positive difference in Y and X coordinates
    if pos[0] > y:
        YDistance = pos[0] - y
    else:
        YDistance = y - pos[0]
    if pos[1] > x:
        XDistance = pos[1] - x
    else:
        XDistance = x - pos[1]
        
    return YDistance + XDistance

class Player(GamePlayer):
    def __init__(self):
        self.name = "Modesty"
        self.group = "17D"
        self.grossY = "unknown"
        self.grossX = "unknown"
        self.cobjtype0 = 0
        self.cobjtype1 = 0
        self.cobjtype2 = 0
       
    def mybot(self, game_map, cur_pos):
        '''(list, tuple) -> Bot
        Returns the Bot object for this player.
        '''
        i, j = cur_pos
        bots = game_map[i][j]
        assert len(bots) != 0
        for bot in bots:
            if bot.i == self.i:
                return bot

    def value(self, game_map, cur_pos, object):
        ''' (list, tuple, GameObject) -> int
        Returns an integer of object category value which is inversely proportional to how many more we need to win
        '''
        mybot = self.mybot(game_map, cur_pos)
        cobjectToWin0 = (self.cobjtype0 // 2) + 1 - mybot.collected_objects[0]
        cobjectToWin1 = (self.cobjtype1 // 2) + 1 - mybot.collected_objects[1]
        cobjectToWin2 = (self.cobjtype2 // 2) + 1 - mybot.collected_objects[2]
       
        #win harder, if we have already won just revert to basic algorithm to finish game faster by getting everything
        if (cobjectToWin0 <= 0 and cobjectToWin1 <= 0 and cobjectToWin2 <= 0):
            return 1
        if (cobjectToWin0 <= 0 and cobjectToWin1 <= 0):
            return 1
        if (cobjectToWin1 <= 0 and cobjectToWin2 <= 0):
            return 1
        if (cobjectToWin2 <= 0 and cobjectToWin0 <= 0):
            return 1
       
        if object.obj_type == 0:
            if cobjectToWin0 <= 0:
                return 0
            return 1/cobjectToWin0
        elif object.obj_type == 1:
            if cobjectToWin1 <= 0:
                return 0
            return 1/cobjectToWin1
        else:
            assert(object.obj_type == 2)
            if cobjectToWin2 <= 0:
                return 0
            return 1/cobjectToWin2
       
    def step(self, game_map, turn, cur_pos):
        map_size = len(game_map)
       
        #count total items on first turn
        if turn == 0:
            for i in range(0, map_size):
                for j in range(0, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            if game_map[i][j][0].obj_type == 0:
                                self.cobjtype0 += 1
                            elif game_map[i][j][0].obj_type == 1:
                                self.cobjtype1 += 1
                            else:
                                assert(game_map[i][j][0].obj_type == 2)
                                self.cobjtype2 += 1
        
        fineUp = 0
        fineDown = 0
        fineLeft = 0
        fineRight = 0
       
        #fine motor control up
        if cur_pos[0] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1]][0]):
                    fineUp = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1]][0])
                           
        #fine motor control down
        if cur_pos[0] < map_size - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1]][0]):
                    fineDown = self.value(game_map, cur_pos, game_map[cur_pos[0] + 1][cur_pos[1]][0])
           
        #fine motor control left
        if cur_pos[1] > 0:
            if game_map[cur_pos[0]][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0]][cur_pos[1] - 1][0]):
                    fineLeft = self.value(game_map, cur_pos, game_map[cur_pos[0]][cur_pos[1] - 1][0])
                           
        #fine motor control right
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
           
        fineUpperLeft = 0
        fineLowerRight = 0
        fineUpperRight = 0
        fineLowerLeft = 0
       
        #fine motor control upper left
        if cur_pos[0] > 0 and cur_pos[1] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] - 1][0]):
                    fineUpperLeft = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1] - 1][0])
                           
        #fine motor control lower right
        if cur_pos[0] < map_size - 1 and cur_pos[1] < map_size - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1] + 1][0]):
                    fineLowerRight = self.value(game_map, cur_pos, game_map[cur_pos[0] + 1][cur_pos[1] + 1][0])
           
        #fine motor upper right
        if cur_pos[0] > 0 and cur_pos[1] < map_size - 1:
            if game_map[cur_pos[0] - 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] + 1][0]):
                    fineUpperRight = self.value(game_map, cur_pos, game_map[cur_pos[0] - 1][cur_pos[1] + 1][0])
                           
        #fine motor control lower left
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
       
        grossUp = 0
        grossDown = 0
        grossLeft = 0
        grossRight = 0
        
        #gross motor control up
        if cur_pos[0] > 0:
            for i in range(0, cur_pos[0]):
                for j in range(0, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossUp += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)

        #gross motor control down
        if cur_pos[0] < map_size - 1:
            for i in range(cur_pos[0] + 1, map_size):
                for j in range(0, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossDown += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)
                           
        #gross motor control left
        if cur_pos[1] > 0:
            for i in range(0, map_size):
                for j in range(0, cur_pos[1]):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossLeft += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)

        #gross motor control right
        if cur_pos[1] < map_size - 1:
            for i in range(0, map_size):
                for j in range(cur_pos[1] + 1, map_size):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossRight += self.value(game_map, cur_pos, game_map[i][j][0])/distance(cur_pos,i,j)
                           
        #find nominal desired gross direction            
        grossMax = max(grossUp, grossDown, grossLeft, grossRight)
       
        direction = "up"
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
        if direction == "down" and self.grossY == "up" and grossUp == 0 and grossLeft > 0:
            direction = "left"
        elif direction == "down" and self.grossY == "up" and grossUp == 0 and grossRight > 0:
            direction = "right"
        elif direction == "up" and self.grossY == "down" and grossDown == 0 and grossLeft > 0:
            direction = "left"
        elif direction == "up" and self.grossY == "down" and grossDown == 0 and grossRight > 0:
            direction = "right"
        elif direction == "left" and self.grossX == "right" and grossRight == 0 and grossUp > 0:
            direction = "up"
        elif direction == "left" and self.grossX == "right" and grossRight == 0 and grossDown > 0:
            direction = "down"
        elif direction == "right" and self.grossX == "left" and grossLeft == 0 and grossUp > 0:
            direction = "up"
        elif direction == "right" and self.grossX == "left" and grossLeft == 0 and grossDown > 0:
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

