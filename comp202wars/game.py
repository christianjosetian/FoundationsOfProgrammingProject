from consts import *
from gui import GameGUI

import copy
import random
import traceback
from collections import defaultdict
from timeit import default_timer as timer

class Map:
    def __init__(self, size, players, obj_proportion):
        self.size = size
        self.gameObject = []
        self.bots = [Bot(player, player.i) for player in players]
        self.num_players = len(players)

        self.max_gameObject = int(obj_proportion * self.size ** 2)
        self.gameObject_assignments = None

        self.gen_map()

    def gen_map(self):
        random.seed() # Sorry David & co.!
        cts = [1, 3, 5, 7, 9, 11, 13]
        cts = [ct for ct in cts]
        cts = random.choices(cts, k=3)
        random.shuffle(cts)
        self.num_gameObjects = {
            obj_type: cts[i] for i, obj_type in enumerate(GAMEOBJECT_TYPES)
        }
        overage = sum(self.num_gameObjects.values()) - self.max_gameObject
        if overage > 0:
            for obj, val in self.num_gameObjects.items():
                self.num_gameObjects[obj] -= (overage//3)-1
                if self.num_gameObjects[obj] <= 0:
                    self.num_gameObjects[obj] = 1
        gameObject_pos = []
        
        for obj_type in self.num_gameObjects:
            for i in range(self.num_gameObjects[obj_type]):
                while True:
                    candidate = (random.randint(0, self.size-1), random.randint(0, self.size-1))
                    if candidate not in gameObject_pos:
                        gameObject_pos.append(candidate)
                        gameObject = GameObject((candidate[0], candidate[1]), GAMEOBJECT_TYPES[obj_type])
                        self.gameObject.append(gameObject)
                        break

        for bot in self.bots:
            while True:
                candidate = (random.randint(0, self.size-1), random.randint(0, self.size-1))
                if candidate not in gameObject_pos:
                    bot.set_pos(candidate)
                    break

class Engine:
    def __init__(self, players, map_size, max_turns, obj_proportion):
        self.turn = 0
        self.MAX_TURNS = max_turns
        self.map = Map(map_size, players, obj_proportion)

    def get_state(self):
        map_vec = [[[[] for j in range(self.map.size)] for i in range(self.map.size)] for i in range(len(self.map.bots))]
        
        tops = self.get_category_tops()
        for bot in self.map.bots:
            bot.category_tops = tops[bot]
            for i in range(len(self.map.bots)):
                new_bot = Bot.copy_Bot(bot)
                map_vec[i][bot.position[0]][bot.position[1]].append(new_bot)
        
        for gameObject in self.map.gameObject:
            for i in range(len(self.map.bots)):
                obj = GameObject(gameObject.position, gameObject.obj_type)
                map_vec[i][gameObject.position[0]][gameObject.position[1]] = [obj]
                
        return GameState(self.map.bots, map_vec, self.turn)
    
    def step(self, actions):
        if self.turn > self.MAX_TURNS:
            return GameStatus.TIMEOUT
        self.turn += 1

        gameObject_collected = False
        for bot, act in actions:
            bot_pos = bot.position
            pos_delta = [0, 0]
            
            if act == ACTIONS["up"]:
                pos_delta[0] -= 1
            elif act == ACTIONS["down"]:
                pos_delta[0] += 1
            elif act == ACTIONS["left"]:
                pos_delta[1] -= 1
            elif act == ACTIONS["right"]:
                pos_delta[1] += 1

            new_pos = (bot_pos[0] + pos_delta[0], bot_pos[1] + pos_delta[1])
            
            valid_move = 0 <= new_pos[0] < self.map.size and 0 <= new_pos[1] < self.map.size
            if not valid_move:
                continue
            
            bot.position = new_pos
            for gameObject in self.map.gameObject:
                if gameObject.position == new_pos:
                    bot.add_object(gameObject.obj_type)
                    self.map.gameObject.remove(gameObject)
                    gameObject_collected = True

            if len(self.map.gameObject) == 0:
                return GameStatus.ALL_GAMEOBJECTS_COLLECTED
        
        if gameObject_collected:
            return GameStatus.GAMEOBJECT_COLLECTED
        return GameStatus.IN_PROGRESS
    
    def get_category_tops(self):
        top_per_category = defaultdict(int)
        top_players = defaultdict(list)
        
        for bot in self.map.bots:
            for i, cat in enumerate(GAMEOBJECT_TYPES):
                if bot.collected_objects[i] > top_per_category[cat]:
                    top_players[cat] = []
                if bot.collected_objects[i] >= top_per_category[cat]:
                    top_players[cat].append(bot)
                    top_per_category[cat] = bot.collected_objects[i]
        num_tops = defaultdict(int) # [0] * len(self.map.bots)
        for cat in top_players:
            tops = top_players[cat]
            if len(tops) > 1: # skip ties
                continue
            top_bot = tops[0]
            num_tops[top_bot] += 1
        return num_tops
    
    def start(self, check_timing, gui):
        status = GameStatus.IN_PROGRESS
        timings = defaultdict(int)
        
        assert(len(set([bot.i for bot in self.map.bots])) == len(self.map.bots))
        
        while status in [GameStatus.IN_PROGRESS, GameStatus.GAMEOBJECT_COLLECTED]:
            state = self.get_state()
            if gui is not None:
                gui.update_screen(state)
            actions = []
            for i, bot in enumerate(self.map.bots):
                if check_timing:
                    start = timer()
                
                # call bot's step method
                try:
                    x = bot.step(state.map[i], state.turn)
                except:
                    raise ValueError(f"The step method for the player <{bot.name}> raised an exception. The traceback is as follows:\n{traceback.format_exc()}")
                
                if check_timing:
                    end = timer()
                    diff = end - start
                    timings[bot.name] += diff
                
                if x not in ACTIONS:
                    raise ValueError(f"The step method for the player <{bot.name}> did not return a valid directional string; instead, <{x}> was returned.")
                actions.append((bot, ACTIONS[x]))
            status = self.step(actions)
            if gui is not None and status == GameStatus.GAMEOBJECT_COLLECTED:
                gui.play_sound('collect')
        
        state = self.get_state()
        if gui is not None:
            if status == GameStatus.ALL_GAMEOBJECTS_COLLECTED:
                gui.play_sound('gameover')
            gui.update_screen(state, game_over=True)
        
        #if status == GameStatus.TIMEOUT:
        #    print("*** max turns reached")
        
        max_tops = max([bot.category_tops for bot in state.bots])
        winners = [bot.name for bot in self.map.bots if bot.category_tops == max_tops]
        #if len(winners) > 1:
        #    winners = []
        return winners, timings, state.turn

def main(players, map_size, max_turns, obj_proportion, check_timing, gui):
    engine = Engine(players, map_size, max_turns, obj_proportion)    
    return engine.start(check_timing, gui)
