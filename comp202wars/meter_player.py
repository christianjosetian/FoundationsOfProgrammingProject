import random
import time
from consts import *
from pygame.locals import *

class Player(GamePlayer):
    def __init__(self):
        self.name = "Meter"
        self.group = "Meter"
        self.grossY = ""
        self.grossX = ""
        self.cobjtype0 = 0
        self.cobjtype1 = 0
        self.cobjtype2 = 0
       
    def distance( self, pos, y, x ):
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
   
    def value( self, objtype ):
        #object categories have value inversely proportional to orginal number
        if objtype == 0:
            return 1/self.cobjtype0
        elif objtype == 1:
            return 1/self.cobjtype1
        else:
            return 1/self.cobjtype2
       
    def step(self, game_map, turn, cur_pos):
       
        #get game dimensions, support rectangular
        YMax = len(game_map)
        XMax = len(game_map[0])
       
        #count total items on first turn
        if turn == 0:
            for i in range(0, YMax):
                for j in range(0, XMax):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            if 0 == game_map[i][j][0].obj_type:
                                self.cobjtype0 += 1
                            elif 1 == game_map[i][j][0].obj_type:
                                self.cobjtype1 += 1
                            else:
                                assert( 2 == game_map[i][j][0].obj_type )
                                self.cobjtype2 += 1
                             
        #fine motor control up
        fineMax = 0
        fineUp = 0
        fineDown = 0
        fineLeft = 0
        fineRight = 0
       
        if cur_pos[0] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1]][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineUp = self.value(game_map[cur_pos[0] - 1][cur_pos[1]][0].obj_type)
                           
        #fine motor control down
        if cur_pos[0] < YMax - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1]]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1]][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineDown = self.value(game_map[cur_pos[0] + 1][cur_pos[1]][0].obj_type)
           
        #fine motor control left
        if cur_pos[1] > 0:
            if game_map[cur_pos[0]][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0]][cur_pos[1] - 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineLeft = self.value(game_map[cur_pos[0]][cur_pos[1] - 1][0].obj_type)
                           
        #fine motor control right
        if cur_pos[1] < XMax - 1:
            if game_map[cur_pos[0]][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0]][cur_pos[1] + 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineRight = self.value(game_map[cur_pos[0]][cur_pos[1] + 1][0].obj_type)
 
        #find nominal desired fine direction   (one step)        
        fineMax = fineUp
        fineMax = max( fineMax, fineDown )
        fineMax = max( fineMax, fineLeft )
        fineMax = max( fineMax, fineRight )
        if fineMax > 0:
            direction = ""
            if fineUp == fineMax:
                direction = "up"
            elif fineDown == fineMax:
                direction = "down"
            elif fineLeft == fineMax:
                direction = "left"
            else:
                assert( fineRight == fineMax )
                direction = "right"
            return direction
           
        fineUpperLeft = 0
        fineLowerRight = 0
        fineUpperRight = 0
        fineLowerLeft = 0
       
        #fine motor control upper left
        if cur_pos[0] > 0 and cur_pos[1] > 0:
            if game_map[cur_pos[0] - 1][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] - 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineUpperLeft = self.value(game_map[cur_pos[0] - 1][cur_pos[1] - 1][0].obj_type)
                           
        #fine motor control lower right
        if cur_pos[0] < YMax - 1 and cur_pos[1] < XMax - 1:
            if game_map[cur_pos[0] + 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1] + 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineLowerRight = self.value(game_map[cur_pos[0] + 1][cur_pos[1] + 1][0].obj_type)
           
        #fine motor upper right
        if cur_pos[0] > 0 and cur_pos[1] < XMax - 1:
            if game_map[cur_pos[0] - 1][cur_pos[1] + 1]:
                if GameObject == type(game_map[cur_pos[0] - 1][cur_pos[1] + 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineUpperRight = self.value(game_map[cur_pos[0] - 1][cur_pos[1] + 1][0].obj_type)
                           
        #fine motor control lower left
        if cur_pos[0] < YMax - 1 and cur_pos[1] > 0:
            if game_map[cur_pos[0] + 1][cur_pos[1] - 1]:
                if GameObject == type(game_map[cur_pos[0] + 1][cur_pos[1] - 1][0]):
                    self.grossY = "unknown"
                    self.grossX = "unknown"
                    fineLowerLeft = self.value(game_map[cur_pos[0] + 1][cur_pos[1] - 1][0].obj_type)
       
        #compute value of step based on second step
        fineUp = fineUpperLeft + fineUpperRight
        fineDown = fineLowerLeft + fineLowerRight
        fineLeft = fineUpperLeft + fineLowerLeft
        fineRight = fineUpperRight + fineLowerRight
       
        #find nominal desired fine direction (two step)        
        fineMax = fineUp
        fineMax = max( fineMax, fineDown )
        fineMax = max( fineMax, fineLeft )
        fineMax = max( fineMax, fineRight )
        if fineMax > 0:
            direction = ""
            if fineUp == fineMax:
                direction = "up"
            elif fineDown == fineMax:
                direction = "down"
            elif fineLeft == fineMax:
                direction = "left"
            else:
                assert( fineRight == fineMax )
                direction = "right"
            return direction
       
        #gross motor control up
        grossUp = 0
        if cur_pos[0] > 0:
            for i in range(0, cur_pos[0]):
                for j in range(0, XMax):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossUp += self.value(game_map[i][j][0].obj_type)/self.distance(cur_pos,i,j)

        #gross motor control down
        grossDown = 0
        if cur_pos[0] < YMax - 1:
            for i in range(cur_pos[0] + 1, YMax):
                for j in range(0, XMax):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossDown += self.value(game_map[i][j][0].obj_type)/self.distance(cur_pos,i,j)
                           
        #gross motor control left
        grossLeft = 0
        if cur_pos[1] > 0:
            for i in range(0, YMax):
                for j in range(0, cur_pos[1]):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossLeft += self.value(game_map[i][j][0].obj_type)/self.distance(cur_pos,i,j)

        #gross motor control right
        grossRight = 0
        if cur_pos[1] < XMax - 1:
            for i in range(0, YMax):
                for j in range(cur_pos[1] + 1, XMax):
                    if game_map[i][j]:
                        if GameObject == type(game_map[i][j][0]):
                            grossRight += self.value(game_map[i][j][0].obj_type)/self.distance(cur_pos,i,j)
                           
        #find nominal desired gross direction            
        grossMax = grossUp
        grossMax = max( grossMax, grossDown )
        grossMax = max( grossMax, grossLeft )
        grossMax = max( grossMax, grossRight )
       
        direction = ""
        if grossUp == grossMax:
            direction = "up"
        elif grossDown == grossMax:
            direction = "down"
        elif grossLeft == grossMax:
            direction = "left"
        else:
            assert( grossRight == grossMax )
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
        elif direction == "left" and self.grossX == "right" and grossLeft == 0 and grossUp > 0:
            direction = "up"
        elif direction == "left" and self.grossX == "right" and grossLeft == 0 and grossDown > 0:
            direction = "down"
        elif direction == "right" and self.grossX == "left" and grossRight == 0 and grossUp > 0:
            direction = "up"
        elif direction == "right" and self.grossX == "left" and grossRight == 0 and grossDown > 0:
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