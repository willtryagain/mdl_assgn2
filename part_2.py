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
ACTION_ARR = ('UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'CRAFT', 'GATHER', 'NONE')

arr = [1/2, 1, 2]
X = 26
Y = arr[X % 3]
STEP_COST = -10/Y
GAMMA = 0.999
DELTA = 0.001

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

    def __str__(self):
        return f'({POSITION_ARR[self.pos]},{self.mat},{self.arrow},{MM_STATE_ARR[self.mm_state]},{self.mm_health * MM_HEALTH_FACTOR})'

def get_prob_next_state(s, a):
    """
    get next state and transition probability
    after doing action a in state s
    """    
    s_a = deepcopy(s)
    s_b = deepcopy(s)
    if s.pos == POSITION_SOUTH:
        if a == ACTION_UP:
            s_a.pos = POSITION_CENTER
            s_b.pos = POSITION_EAST
            return [[0.85, s_a], [0.15, s_b]]
        elif a == ACTION_STAY:
            s_b.pos = POSITION_EAST    
            return [[0.85, s_a], [0.15, s_b]]
        elif a == ACTION_GATHER:
            s_a.mat = min(2, s_a.mat + 1)
            return [[0.75, s_a], [0.25, s_b]]
        return None

def get_utility(prob_state, U):
    utility = STEP_COST
    for p, s in prob_state:
        utility += p * GAMMA * U[s.pos][s.mat][s.arrow][s.mm_state][s.mm_health]
    return utility

def get_scaled_utility(U, s, a):
    total_utility = 0
    prob_state = get_prob_next_state(s, a)
    if s.mm_state ==  MM_STATE_DORMANT:

        for i in range(len(prob_state)):
            prob_state[i][1].mm_state = MM_STATE_READY
        total_utility += 0.2 * get_utility(prob_state, U)

        for i in range(len(prob_state)):
            prob_state[i][1].mm_state = MM_STATE_DORMANT
        total_utility += 0.8 * get_utility(prob_state, U)
    return total_utility        
    
U = np.zeros((POSITIONS_RANGE, MATERIALS_RANGE, ARROWS_RANGE, MM_STATE_RANGE, MM_HEALTH_RANGE))   
# for state, U_s in np.ndenumerate(U):
#     if state[0] == 0:
#         continue
#     s = State(*state)
#     for action in range(NUM_ACTIONS):
#         r = get_next_state_prob(s, action)
#         if r:
#             print(ACTION_ARR[action], r[0][0], r[0][1], r[1][0], r[1][1]) 

print(get_scaled_utility(U, State(POSITION_SOUTH, 0, 0, MM_STATE_DORMANT, 1), ACTION_UP))