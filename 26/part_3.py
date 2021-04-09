import numpy as np
from copy import deepcopy
from functools import reduce
from operator import add
import os

POSITIONS_RANGE = 5
MATERIALS_RANGE = 3
ARROWS_RANGE = 4
MM_STATE_RANGE = 2
MM_HEALTH_RANGE = 5

POSITIONS_VALUES = tuple(range(POSITIONS_RANGE))
MATERIALS_VALUES = tuple(range(MATERIALS_RANGE))
ARROWS_VALUES = tuple(range(ARROWS_RANGE))
MM_STATE_VALUES = tuple(range(MM_STATE_RANGE))
MM_HEALTH_VALUES = tuple(range(MM_HEALTH_RANGE))

POSITION_WEST = 0
POSITION_NORTH = 1
POSITION_EAST = 2
POSITION_SOUTH = 3
POSITION_CENTER = 4
POSITION_ARR = ('W', 'N', 'E', 'S', 'C')

MM_STATE_DORMANT = 0
MM_STATE_READY = 1
MM_STATE_ARR = ('D', 'R')

MM_HEALTH_FACTOR = 25

NUM_ACTIONS = 10
ACTION_UP = 0
ACTION_LEFT = 1 
ACTION_RIGHT = 2
ACTION_DOWN = 3
ACTION_STAY = 4
ACTION_HIT = 5
ACTION_SHOOT = 6
ACTION_CRAFT = 7
ACTION_GATHER = 8
ACTION_NONE = 9
ACTION_ARR = ('UP', 'LEFT', 'RIGHT', 'DOWN', 'STAY', 'HIT', 'SHOOT', 'CRAFT', 'GATHER', 'NONE')

arr = [1/2, 1, 2]
X = 26
Y = arr[X % 3]
STEP_COST = -10/Y

class State:
    def __init__(self, pos, mat, arrow, mm_state, mm_health):
        if (pos not in POSITIONS_VALUES) or (mat not in MATERIALS_VALUES) or \
            (arrow not in ARROWS_VALUES) or (mm_state not in MM_STATE_VALUES) or \
                (mm_health not in MM_HEALTH_VALUES):
            raise ValueError 

        self.pos = pos
        self.mat = mat
        self.arrow = arrow
        self.mm_state = mm_state
        self.mm_health = mm_health

    def get_state(self):
        return (self.pos, self.mat, self.arrow, self.mm_state, self.mm_health)

    def get_hash(self):
        return (self.pos * (MATERIALS_RANGE * ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE) + 
                self.mat * (ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE) +
                self.arrow * (MM_STATE_RANGE * MM_HEALTH_RANGE) +
                self.mm_state * MM_HEALTH_RANGE +
                self.mm_health)

    def valid_action(self, action):
        if action == ACTION_NONE:
            return (self.mm_health == 0)

        if self.mm_health == 0:
            return False

        if action == ACTION_SHOOT:
            return (self.pos == POSITION_CENTER or self.pos == POSITION_EAST or self.pos == POSITION_WEST) and (self.arrow > 0)

        if action == ACTION_HIT:
            return (self.pos == POSITION_CENTER or self.pos == POSITION_EAST)

        if action == ACTION_GATHER:
            return self.pos == POSITION_SOUTH

        if action == ACTION_CRAFT:
            return self.pos == POSITION_NORTH and self.mat > 0

        if action == ACTION_UP:
            return self.pos == POSITION_SOUTH or self.pos == POSITION_CENTER

        if action == ACTION_RIGHT:
            return self.pos == POSITION_WEST or self.pos == POSITION_CENTER

        if action == ACTION_LEFT:
            return self.pos == POSITION_EAST or self.pos == POSITION_CENTER

        if action == ACTION_DOWN:
            return self.pos == POSITION_NORTH or self.pos == POSITION_CENTER

        raise ValueError('invalid action')

    def get_actions(self):
        actions = []
        for i in range(NUM_ACTIONS):
            if self.valid_action(i):
                actions.append(i)
        return actions

    def get_scaled_distrib(self, distrib):
        next_distrib = []


        if self.mm_state == MM_STATE_READY:
            for p, s in distrib:
                next_distrib.append((p*0.5, s))
            if self.pos == POSITION_CENTER or state.pos == POSITION_EAST:
                next_distrib.append((1, State(self.pos, self.mat, 0, MM_STATE_DORMANT, min(4, self.mm_health + 1))))


        
        for state in states:
            next_states.append(State(state.pos, state.mat, state.arrow, MM_STATE_DORMANT, state.mm_health))
        return next_states

    def get_prob_state(self, action):
        if action not in self.get_actions():
            raise ValueError

        if action == ACTION_NONE:
            return []

        if self.mm_state == MM_STATE_READY:

            if self.pos == POSITION_CENTER:
                return [
                    (0.5, s_a),
                    (0.5, s_b)
                ]

        if action == ACTION_SHOOT:
            s_a = State(self.pos, self.mat, self.arrow - 1, self.mm_state, self.mm_health - 1)
            s_b = State(self.pos, self.mat, self.arrow - 1, self.mm_state, self.mm_health)

            if self.pos == POSITION_WEST:
                return [
                    (0.25, s_a),
                    (0.75, s_b)
                ]

            elif self.pos == POSITION_CENTER:
                return [
                    (0.5, s_a),
                    (0.5, s_b)
                ]
            elif self.pos == POSITION_EAST:
                return [
                    (0.9, s_a),
                    (0.1, s_b)
                ]
            else:
                raise ValueError 

        if action == ACTION_HIT:
            s_a = State(self.pos, self.mat, self.arrow - 1, self.mm_state, self.mm_health - 1)
            s_b = State(self.pos, self.mat, self.arrow - 1, self.mm_state, self.mm_health)

            if self._po

                
    
    def __str__(self):
        return f'({POSITION_ARR[self.pos]},{self.mat},{self.arrow},{MM_STATE_ARR[self.mm_state]},{self.mm_health * MM_HEALTH_FACTOR})'
