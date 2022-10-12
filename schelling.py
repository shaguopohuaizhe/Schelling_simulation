# /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author : Ziwen He
Email : ziwen.he@cripac.ia.ac.cn
Date : 09-08-2022
Description: The Schelling Model Simulations
'''
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import itertools
import random
import copy
import argparse
import json
import math


class Schelling:
    def __init__(self, width, height, empty_ratio, little_ratio, blue_ratio, similarity_threshold, n_iterations, initiation=1,
                 only_move_to_empty=True,
                 rmp=[1.0]*9,bmp=[1.0]*9,
                 gmp=[1.0]*9, red_mp=[0.05,0.05], blue_mp=[0.4,0.4], yellow_mp=[0.05,0.05], divide=2, races=3):
        self.width = width
        self.height = height
        # Define the particle number
        self.races = races
        self.empty_ratio = empty_ratio
        self.little_ratio = little_ratio
        self.blue_ratio = blue_ratio
        #self.yellow_ratio = yellow_ratio
        self.similarity_threshold = similarity_threshold
        #self.str = str
        #self.stb = stb
        #self.stg = stg
        self.n_iterations = n_iterations
        self.flag = only_move_to_empty
        self.initiation = initiation
        #self.move_prob = mp
        self.red_move_prob = rmp
        self.blue_move_prob = bmp
        self.yellow_move_prob = gmp
        self.red_mp = red_mp
        self.blue_mp = blue_mp
        self.yellow_mp = yellow_mp
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        self.divide = divide

    # Image
    def populate(self):
        self.old_step = 0
        if self.initiation == 1:
            self.empty_houses = []
            self.agents = {}
            # All Agents
            self.all_houses = list(itertools.product(range(self.width), range(self.height)))
            random.shuffle(self.all_houses)
            # Empty number
            self.n_empty = int(self.empty_ratio * len(self.all_houses))
            # Empry Position
            self.empty_houses = self.all_houses[:self.n_empty]
            # Agents positons
            self.remaining_houses = self.all_houses[self.n_empty:]
            # Ratio calculation

            self.n_red = int(self.little_ratio * len(self.remaining_houses))
            self.n_blue = int((self.blue_ratio +self.little_ratio)*len(self.remaining_houses))

            houses_by_race = []
            houses_by_race.append(self.remaining_houses[:self.n_red])
            houses_by_race.append(self.remaining_houses[self.n_red: self.n_blue])
            houses_by_race.append(self.remaining_houses[self.n_blue:])


            # coordinates
            for i in range(self.races):
                # create agents for each race
                self.agents = dict(
                    self.agents.items() +
                    dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
                )

        elif self.initiation == 2:
            self.empty_houses = []
            self.agents = {}

            self.all_houses = list(itertools.product(range(self.width), range(self.height)))

            little_space = max(2, int(math.sqrt(1 / (self.little_ratio * (1 - self.empty_ratio)))))
            n_little = int(self.width / little_space)
            little_list = [i * little_space for i in range(n_little - 1)]
            little_list.append(self.width - 1)
            houses_little = [(x, y) for x in little_list for y in little_list]

            self.remaining_houses = [x for x in self.all_houses if x not in houses_little]
            random.shuffle(self.remaining_houses)

            self.n_empty = int(self.empty_ratio * len(self.all_houses))
            self.empty_houses = self.remaining_houses[:self.n_empty]
            houses_most = [x for x in self.remaining_houses if x not in self.empty_houses]
            n_blue = int(self.blue_ratio * (len(self.all_houses)-self.n_empty))
            houses_blue = houses_most[:n_blue]
            houses_yellow = houses_most[n_blue:]

            houses_by_race = []

            houses_by_race.append(houses_little)
            houses_by_race.append(houses_blue)
            houses_by_race.append(houses_yellow)

            for i in range(self.races):
                # create agents for each race
                self.agents = dict(
                    self.agents.items() +
                    dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
                )
        elif self.initiation == 3:
            self.empty_houses = []
            self.agents = {}

            self.all_houses = list(itertools.product(range(self.width), range(self.height)))
            #self.remaining_houses = self.all_houses
            # random.shuffle(self.all_houses)
            self.remaining_houses = copy.deepcopy(self.all_houses)

            # self.n_empty = int( self.empty_ratio * len(self.all_houses) )
            # self.empty_houses = self.all_houses[:self.n_empty]

            # self.remaining_houses = self.all_houses[self.n_empty:]

            self.n_little = int(self.little_ratio * (1 - self.empty_ratio) * len(self.remaining_houses))
            
            houses_little = []
            for i in range(1):
                #point = random.choice(self.remaining_houses)
                point = (0.5 * self.width, 0.5 * self.height)
                for j in range(self.n_little):
                    if point not in houses_little and point in self.remaining_houses:
                        houses_little.append(point)
                        self.remaining_houses.remove(point)

                    x, y = point[0], point[1]
                    point = random.choice(
                        [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                         (x + 1, y + 1)])
                    if len(houses_little) == int((i + 1) * 0.1 * self.n_little / 1):
                        break

            random.shuffle(self.remaining_houses)

            self.n_empty = int(self.empty_ratio * len(self.all_houses))
            self.empty_houses = self.remaining_houses[:self.n_empty]
            self.n_most = self.width * self.height - self.n_empty - self.n_little
            houses_most = self.remaining_houses[self.n_empty:(self.n_empty + self.n_most)]
            houses_little += self.remaining_houses[(self.n_most + self.n_empty):]
            
            n_blue = int(self.blue_ratio * (len(self.all_houses)-self.n_empty))
            houses_blue = houses_most[:n_blue]
            houses_yellow = houses_most[n_blue:]

            houses_by_race = []

            houses_by_race.append(houses_little)
            houses_by_race.append(houses_blue)
            houses_by_race.append(houses_yellow)
            
            for i in range(self.races):
                # create agents for each race
                self.agents = dict(
                    self.agents.items() +
                    dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
                )

            #save_step = self.old_step
            #self.update()
            #self.initiation = 0
            #self.old_step = save_step
        elif self.initiation == 4:
            #self.width = 102
            #self.height = 102
            self.width = 100 + 2*(self.divide-1)
            #print(self.width)
            self.height = 100 + 2*(self.divide-1)
            self.empty_houses = []
            self.agents = {}
            # all agents
            self.all_houses = list(itertools.product(range(self.width), range(self.height)))
            if self.divide == 2:
                yellow_houses_1 = list(itertools.product(range(50,52), range(self.height)))
                yellow_houses_2 = list(itertools.product(range(50), range(50,52)))
                yellow_houses_3 = list(itertools.product(range(52,self.width), range(50,52)))
                yellow_houses = yellow_houses_1 + yellow_houses_2 + yellow_houses_3
            elif self.divide == 3:
                yellow_houses_1 = list(itertools.product(range(33,35), range(self.height)))
                yellow_houses_2 = list(itertools.product(range(69,71), range(self.height)))
                yellow_houses_3 = list(itertools.product(range(self.width), range(33,35)))
                yellow_houses_4 = list(itertools.product(range(self.width), range(69,71)))
                yellow_houses = list(set(yellow_houses_1 + yellow_houses_2 + yellow_houses_3 + yellow_houses_4)) 
            elif self.divide == 4:
                yellow_houses_1 = list(itertools.product(range(25,27), range(self.height)))
                yellow_houses_2 = list(itertools.product(range(52,54), range(self.height)))
                yellow_houses_3 = list(itertools.product(range(79,81), range(self.height)))
                yellow_houses_4 = list(itertools.product(range(self.width), range(25,27)))
                yellow_houses_5 = list(itertools.product(range(self.width), range(52,54)))
                yellow_houses_6 = list(itertools.product(range(self.width), range(79,81)))
                yellow_houses = list(set(yellow_houses_1 + yellow_houses_2 + yellow_houses_3 + yellow_houses_4 + yellow_houses_5 + yellow_houses_6)) 
            
            self.remaining_houses = [x for x in self.all_houses if x not in yellow_houses]
            random.shuffle(self.remaining_houses)
            
            #random.shuffle(self.all_houses)
            # number
            self.n_empty = int(self.empty_ratio * len(self.all_houses))
            # position
            self.empty_houses = self.remaining_houses[:self.n_empty]
            houses_other = [x for x in self.remaining_houses if x not in self.empty_houses]
            
            # agents calculation

            self.n_red = int(self.little_ratio * len(houses_other))
            self.n_blue = int((self.blue_ratio +self.little_ratio)*len(houses_other))

            houses_by_race = []
            houses_by_race.append(houses_other[:self.n_red])
            houses_by_race.append(houses_other[self.n_red: self.n_blue])
            houses_by_race.append(yellow_houses)


            # coordinates
            for i in range(self.races):
                # create agents for each race
                self.agents = dict(
                    self.agents.items() +
                    dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
                )
        elif self.initiation == 5:
            self.empty_houses = []
            self.agents = {}

            self.all_houses = list(itertools.product(range(self.width), range(self.height)))
            #self.remaining_houses = self.all_houses
            # random.shuffle(self.all_houses)
            self.remaining_houses = copy.deepcopy(self.all_houses)

            # self.n_empty = int( self.empty_ratio * len(self.all_houses) )
            # self.empty_houses = self.all_houses[:self.n_empty]

            # self.remaining_houses = self.all_houses[self.n_empty:]

            self.n_little = int(self.little_ratio * (1 - self.empty_ratio) * len(self.remaining_houses))
            
            houses_little = []
            for i in range(1):
                #point = random.choice(self.remaining_houses)
                point = (0.5 * self.width, 0.5 * self.height)
                for j in range(self.n_little):
                    if point not in houses_little and point in self.remaining_houses:
                        houses_little.append(point)
                        self.remaining_houses.remove(point)

                    x, y = point[0], point[1]
                    point = random.choice(
                        [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                         (x + 1, y + 1)])
                    if len(houses_little) == int((i + 1) * 0.3 * self.n_little / 1):
                        break

            random.shuffle(self.remaining_houses)

            self.n_empty = int(self.empty_ratio * len(self.all_houses))
            self.empty_houses = self.remaining_houses[:self.n_empty]
            self.n_most = self.width * self.height - self.n_empty - self.n_little
            houses_most = self.remaining_houses[self.n_empty:(self.n_empty + self.n_most)]
            houses_little += self.remaining_houses[(self.n_most + self.n_empty):]
            
            n_blue = int(self.blue_ratio * (len(self.all_houses)-self.n_empty))
            houses_blue = houses_most[:n_blue]
            houses_yellow = houses_most[n_blue:]

            houses_by_race = []

            houses_by_race.append(houses_little)
            houses_by_race.append(houses_blue)
            houses_by_race.append(houses_yellow)
            
            for i in range(self.races):
                # create agents for each race
                self.agents = dict(
                    self.agents.items() +
                    dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items()
                )

            #save_step = self.old_step
            #self.update()
            #self.initiation = 0
            #self.old_step = save_step
            
    # satisfied ratio (similarity)
    def is_unsatisfied(self, x, y, race):

        # race = self.agents[(x,y)]
        count_similar = 0
        count_different = 0
        around_empty_houses = []



        # 1、Up-left point
        if x > 0 and y > 0:
            if (x - 1, y - 1) not in self.empty_houses:
                if self.agents[(x - 1, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x - 1, y - 1))
        # top and left boundary
        elif race == 1:
            count_different += 1
        # 2、top point
        if y > 0:
            if (x, y - 1) not in self.empty_houses:
                if self.agents[(x, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x, y - 1))
        # top boundary
        elif race == 1:
            count_different += 1
        # 3、up-rifgt point
        if x < (self.width - 1) and y > 0:
            if (x + 1, y - 1) not in self.empty_houses:
                if self.agents[(x + 1, y - 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x + 1, y - 1))
        # top and right boundary
        elif race == 1:
            count_different += 1
        # 4、left
        if x > 0:
            if (x - 1, y) not in self.empty_houses:
                if self.agents[(x - 1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x - 1, y))
        # left boundary
        elif race == 1:
            count_different += 1
        # 5、right point
        if x < (self.width - 1):
            if (x + 1, y) not in self.empty_houses:
                if self.agents[(x + 1, y)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x + 1, y))
        # right boundary
        elif race == 1:
            count_different += 1
        # 6、left bottom point
        if x > 0 and y < (self.height - 1):
            if (x - 1, y + 1) not in self.empty_houses:
                if self.agents[(x - 1, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x - 1, y + 1))
        elif race == 1:
            count_different += 1
        # 7、bottom point
        if y < (self.height - 1):
            if (x, y + 1) not in self.empty_houses:
                if self.agents[(x, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x, y + 1))
        # bottom boundary
        elif race == 1:
            count_different += 1
        # 8、right top point
        if x < (self.width - 1) and y < (self.height - 1):
            if (x + 1, y + 1) not in self.empty_houses:
                if self.agents[(x + 1, y + 1)] == race:
                    count_similar += 1
                else:
                    count_different += 1
            else:
                around_empty_houses.append((x + 1, y + 1))
        # right and bottom boundary
        elif race == 1:
            count_different += 1
        if (count_similar + count_different) == 0:
            return False, 0, around_empty_houses
        else:
            return float(count_similar) / (
                        count_similar + count_different) < self.similarity_threshold[race-1], count_different, around_empty_houses

    # any neighboring empty 
    def is_open(self, agent, race):

        if agent not in self.searched_empty_houses:
            self.searched_empty_houses.append(agent)
        is_un, count, around_empty_houses = self.is_unsatisfied(agent[0], agent[1], race)

        around_empty_houses = [x for x in around_empty_houses if x not in self.searched_empty_houses]

        if not is_un:
            return True
        elif is_un and around_empty_houses == []:
            return False
        else:
            if len(around_empty_houses) == 1:
                return self.is_open(around_empty_houses[0], race)
            elif len(around_empty_houses) == 2:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1], race)
            elif len(around_empty_houses) == 3:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race)
            elif len(around_empty_houses) == 4:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race) \
                       or self.is_open(around_empty_houses[3], race)
            elif len(around_empty_houses) == 5:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race) \
                       or self.is_open(around_empty_houses[3], race) or self.is_open(around_empty_houses[4], race)
            elif len(around_empty_houses) == 6:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race) \
                       or self.is_open(around_empty_houses[3], race) or self.is_open(around_empty_houses[4],
                                                                                     race) or self.is_open(
                    around_empty_houses[5], race)
            elif len(around_empty_houses) == 7:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race) \
                       or self.is_open(around_empty_houses[3], race) or self.is_open(around_empty_houses[4],
                                                                                     race) or self.is_open(
                    around_empty_houses[5], race) \
                       or self.is_open(around_empty_houses[6], race)
            elif len(around_empty_houses) == 8:
                return self.is_open(around_empty_houses[0], race) or self.is_open(around_empty_houses[1],
                                                                                  race) or self.is_open(
                    around_empty_houses[2], race) \
                       or self.is_open(around_empty_houses[3], race) or self.is_open(around_empty_houses[4],
                                                                                     race) or self.is_open(
                    around_empty_houses[5], race) \
                       or self.is_open(around_empty_houses[6], race) or self.is_open(around_empty_houses[7], race)

    def update(self):
        if self.n_iterations == -1:
            self.n_iterations = 100000000
        # print(self.flag)
        # Moving Tendency
        #prob = {i: self.move_prob[i] for i in range(9)}
        red_prob = {i: self.red_move_prob[i] for i in range(9)}
        blue_prob = {i: self.blue_move_prob[i] for i in range(9)}
        yellow_prob = {i: self.yellow_move_prob[i] for i in range(9)}
        red_num = []
        blue_num = []
        yellow_num = []
        self.sat = 0
        # 'flag: 0 means only move to empty, 1 means can move to color'
        if self.flag == 0:
            for i in range(self.n_iterations):
                print('iter:', i)
                self.old_agents = copy.deepcopy(self.agents)
                n_changes = 0
                if self.sat >= int(0.4 * (1 - self.empty_ratio) * self.little_ratio * self.width * self.height):
                    break
                self.sat = 0

                for agent in self.old_agents:
                    # color
                    race = self.agents[agent]

                    # number counting
                    is_un, count, around_empty_houses = self.is_unsatisfied(agent[0], agent[1], race)
                    # initiation=1 
                    if self.initiation == 3 and race == 1 and not is_un:
                        self.sat += 1

                    # different neighboring agents
                    if is_un and around_empty_houses != []:  # count>4 and around_empty_houses != []:
                        # moving tendency
                        #p = prob[count]
                        # probability
                        if race == 1:
                            p = red_prob[count]
                        elif race == 2:
                            p = blue_prob[count]
                        elif race == 3:
                            p = yellow_prob[count]

                        if n_changes == 0 and p > 0.0:
                            self.searched_empty_houses = []
                            if self.is_open(agent, race):
                                n_changes += 1
                        # prob = {5:0.25,6:0.5,7:0.75,8:1.0}

                        rand = random.random()
                        if rand < p:
                            # race = self.agents[agent]
                            empty_house = random.choice(around_empty_houses)
                            self.agents[empty_house] = race
                            del self.agents[agent]
                            self.empty_houses.remove(empty_house)
                            self.empty_houses.append(agent)
                            # n_changes += 1
                        '''for empty in around_empty_houses:
                            #to do
                            if 
                            is_un, count, new_around_empty_houses = self.is_unsatisfied(empty)
                            if is_un:
                                around_empty_houses+=new_around_empty_houses
                            else:
                                n_changes +=1
                                break
                            if around_empty_houses==[]:
                                n_changes +=1
                                break

                        n_changes += 1'''
                        # print 'Iteration: %d , Number of changes: %d' %(i+1, n_changes)
                if n_changes == 0:
                    self.old_step += i
                    return self.old_step, -1, 1
        else:
            # print("red-blue")
            for i in range(self.n_iterations):
                print('iter:', i)
                self.old_agents = copy.deepcopy(self.agents)
                n_changes = 0
                if self.sat >= int(0.4 * (1 - self.empty_ratio) * self.little_ratio * self.width * self.height):
                    break
                self.sat = 0

                for agent in self.old_agents:
                    race = self.agents[agent]
                    is_un, count, around_empty_houses = self.is_unsatisfied(agent[0], agent[1], race)
                    if self.initiation == 3 and race == 1 and not is_un:
                        self.sat += 1
                    if is_un:  # and count>4:
                        # prob = {5:0.25,6:0.5,7:0.75,8:1.0}
                        # count is the number of agent with different color  
                        #p = prob[count]
                        if race == 1:
                            p = red_prob[count]
                        elif race == 2:
                            p = blue_prob[count]
                        elif race == 3:
                            p = yellow_prob[count]
                        rand = random.random()
                        if rand < p:

                            # race = self.agents[agent]
                            x = agent[0]
                            y = agent[1]

                            if race == 1 or race == 2:
                                red = []
                                blue = []
                                yellow = []
                                empty = []
                                around_list = list(itertools.product([-1,0,1],repeat=2))
                                around_list.remove((0,0))
                                # centeral point
                                #around_in = ([x,y]+around_list) and self.all_houses
                                around_in = [(x+a[0],y+a[1]) for a in around_list]
                                #print(around_in)
                                #print(self.all_houses)
                                around_in = list(set(self.all_houses)&set(around_in))
                                #print(around_in)
                                for ar in around_in:
                                    if ar in self.empty_houses:
                                        empty.append(ar)
                                    elif self.agents[ar] == 1:#red
                                        red.append(ar)
                                    elif self.agents[ar] == 2:#blue
                                        blue.append(ar)
                                    elif self.agents[ar] == 3:#yellow
                                        yellow.append(ar)

                                rand = random.random()
                                p_r = len(red)*self.red_mp[race-1] if red != [] else 0
                                p_b = len(blue)*self.blue_mp[race-1] if blue != [] else 0
                                p_g = len(yellow)*self.yellow_mp[race-1] if yellow != [] else 0
                                p_e = len(empty)*(1 - self.red_mp[race-1] - self.blue_mp[race-1] - self.yellow_mp[race-1]) if empty != [] else 0
                                #print(len(red))
                                #print(len(blue))
                                #print(len(yellow))
                                #print(len(empty))
                                
                                p_sum = p_r + p_b + p_g + p_e
                                p_r, p_b, p_g, p_e = p_r/p_sum, p_b/p_sum, p_g/p_sum, p_e/p_sum
                                
                                if rand < p_r:
                                    around_house = random.choice(red)
                                elif rand < p_b+p_r:
                                    around_house = random.choice(blue)    
                                elif rand < p_g+p_b+p_r:
                                    around_house = random.choice(yellow)
                                else:
                                    around_house = random.choice(empty)
                            else:

                                # center
                                if x > 0 and x < (self.width - 1) and y > 0 and y < (self.height - 1):
                                    around_house = random.choice(
                                        [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1),
                                         (x, y + 1), (x + 1, y + 1)])
                                # top boundary
                                elif x == 0 and y > 0 and y < (self.height - 1):
                                    around_house = random.choice(
                                        [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x + 1, y + 1)])
                                # bottom boundary
                                elif x == (self.width - 1) and y > 0 and y < (self.height - 1):
                                    around_house = random.choice(
                                        [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1)])
                                # left boundary
                                elif y == 0 and x > 0 and x < (self.width - 1):
                                    around_house = random.choice(
                                        [(x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)])
                                # right boundary
                                elif y == (self.height - 1) and x > 0 and x < (self.width - 1):
                                    around_house = random.choice(
                                        [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y)])
                                # peak
                                elif x == 0 and y == 0:
                                    around_house = random.choice([(x + 1, y), (x, y + 1), (x + 1, y + 1)])
                                elif x == 0 and y == (self.height - 1):
                                    around_house = random.choice([(x, y - 1), (x + 1, y - 1), (x + 1, y)])
                                elif y == 0 and x == (self.width - 1):
                                    around_house = random.choice([(x - 1, y), (x, y + 1), (x - 1, y + 1)])
                                elif y == (self.height - 1) and x == (self.width - 1):
                                    around_house = random.choice([(x, y - 1), (x - 1, y), (x - 1, y - 1)])

                            if around_house not in self.empty_houses:
                                around_race = self.agents[around_house]
                                self.agents[around_house] = race
                                self.agents[agent] = around_race
                            else:
                                self.agents[around_house] = race
                                del self.agents[agent]
                                self.empty_houses.remove(around_house)
                                self.empty_houses.append(agent)
                        if p > 0.0:
                            n_changes += 1

                # print 'Iteration: %d , Number of changes: %d' %(i+1, n_changes)
                if n_changes == 0:
                    self.old_step += i
                    return self.old_step, -1, 1
        self.old_step += self.n_iterations
        sr = self.satisfaction_ratio()
        return self.old_step, 0, sr

    def satisfaction_ratio(self):
        self.old_agents = copy.deepcopy(self.agents)
        count_sat = 0
        count_all = 0
        for agent in self.old_agents:
            race = self.agents[agent]
            if race == 1:
                is_un, count, around_empty_houses = self.is_unsatisfied(agent[0], agent[1], race)
                if not is_un:
                    count_sat += 1
                count_all += 1
        sr = 1.0 * count_sat / count_all
        return sr

    def plot(self, title, file_name):
        fig, ax = plt.subplots(figsize=(0.125 * self.width, 0.125 * self.height))
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'r', 2: 'b', 3: 'y', 4: 'c', 5: 'm', 6: 'g', 7: 'k'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)
        plt.close()

    def save(self):
        filename = open('agents.json', 'w')
        filename.write(str(self.agents))
        filename.close()
        filename = open('empty.json', 'w')
        filename.write(str(self.empty_houses))
        filename.close()
        filename = open('step.json', 'w')
        filename.write(str(self.old_step))
        filename.close()
        filename = open('agents-{}.json'.format(self.old_step), 'w')
        filename.write(str(self.agents))
        filename.close()
        filename = open('empty-{}.json'.format(self.old_step), 'w')
        filename.write(str(self.empty_houses))
        filename.close()
        filename = open('satisfation.json', 'a')
        filename.write(str(self.satisfaction_ratio())+'\n')
        filename.close()
        # with open('empty.json', 'w') as f_obj:
        #    json.dump(self.empty_houses, f_obj)

    def read(self):
        fr = open("agents.json", 'r')
        self.agents = eval(fr.read())
        fr.close()
        fr = open("empty.json", 'r')
        self.empty_houses = eval(fr.read())
        fr.close()
        fr = open("step.json", 'r')
        self.old_step = eval(fr.read())
        fr.close()
        self.initiation = 0
        # print(self.agents)
        # fr.close()
        # with open('empty.json', 'r') as f_obj:
        #    self.empty_houses = json.load(f_obj)
        #    print(self.empty_houses)




def main():
    ##First Simulation
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", default=50, type=int, help="width")
    parser.add_argument("--h", default=50, type=int, help='height')
    parser.add_argument("--er", default=0.5, type=float, help='empty_ratio')
    # prob blue + red(little) < 1, yellow + blue + red(little) = 1
    parser.add_argument("--lr", default=0.5, type=float, help='red_ratio')
    parser.add_argument("--br", default=0.5, type=float, help='blue_ratio')

    #parser.add_argument("--st", default=0.5, type=float, help='similarity_threshold')
    parser.add_argument('--st', default=[0.5, 0.5, 0.5], nargs='+', type=float, help='similarity_threshold of red, blue, yellow')
    #parser.add_argument("--str", default=0.5, type=float, help='similarity_threshold of red')
    #parser.add_argument("--stb", default=0.5, type=float, help='similarity_threshold of blue')
    #parser.add_argument("--stg", default=0.5, type=float, help='similarity_threshold of yellow')
    parser.add_argument("--init", default=1, type=int,
                        help='initiation, 1 means random, 2 means uniform, 3 means segregated(10%%), 4 means 1D(or 2D)/3D，5means segregated(30%%)')
    parser.add_argument("--n", default=10000, type=int, help='n_iterations, -1 means final')
    parser.add_argument("--f", default=0, type=int, help='flag: 0 means only move to empty, 1 means can move to color')
    #parser.add_argument('--mp', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float,
    #                    help='move prob,0-8')
    # thermo Red Moving tendency
    parser.add_argument('--rmpt', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float,
                        help='move tend thermo,0-8')
    # thermo blue Moving tendency
    parser.add_argument('--bmpt', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float,
                        help='move tend thermo,0-8')
    # thermo yellow Moving tendency
    parser.add_argument('--gmpt', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float, help='move tend thermo,0-8')
    # Moving Tendency Kinetic
    parser.add_argument('--rmpk', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float,
                        help='move tend kinetic,0-8')
    parser.add_argument('--bmpk', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float,
                        help='move tend kinetic,0-8')
    parser.add_argument('--gmpk', default=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], nargs='+', type=float, help='move tend kinetic,0-8')

    parser.add_argument("--con", default=0, type=int, help='continue from last time? 0 means no, 1 means yes')
    parser.add_argument("--red_p", default=[0.05, 0.05], nargs='+', type=float, help='exchange prob of red move to red, to blue')
    parser.add_argument("--blue_p", default=[0.4, 0.4], nargs='+', type=float, help='exchange prob of blue move to red, to blue')
    parser.add_argument("--yellow_p", default=[0.05, 0.05], nargs='+', type=float, help='exchange prob of yellow move to red, to blue')
    parser.add_argument("--re", default=1, type=int, help='repeat n times')
    parser.add_argument("--divide", default=2, type=int, help='divide into n * n pieces')

    args = parser.parse_args()

    rmp = [args.rmpt[i] * args.rmpk[i] for i in range(len(args.rmpt))]
    bmp = [args.bmpt[i] * args.bmpk[i] for i in range(len(args.bmpt))]
    gmp = [args.gmpt[i] * args.gmpk[i] for i in range(len(args.gmpt))]
    
    # width, height, empty_ratio, little_ratio, similarity_threshold, n_iterations, initiation, only_move_to_empty, races = 3
    schelling_1 = Schelling(args.w, args.h, args.er, args.lr, args.br,
                            args.st, args.n, args.init, args.f, rmp, bmp, gmp, args.red_p, args.blue_p, args.yellow_p, args.divide)
    # continue
    if args.con != 0:
        schelling_1.read()
    # initializing
    else:
        schelling_1.populate()
        schelling_1.plot('Schelling Model with 3 colors: Initial State', 'schelling_initial.png')
        
    for re in range(args.re):
        step, if_final, sr = schelling_1.update()
        
        if if_final == 0:
            schelling_1.plot(
                'Step: {} , Similarity Threshold: {}% , Segregation Percentage: {}%'.format(step, 100 * args.st[0], 100 * sr),
                'schelling_step{}.png'.format(step))
        else:
            schelling_1.plot(
                'Final Step: {} , Similarity Threshold: {}%'.format(step, 100 * args.st[0]),
                'schelling_final_step{}.png'.format(step))

        schelling_1.save()


if __name__ == "__main__":
    main()
