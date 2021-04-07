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
GAMMA = 0.999
DELTA = 0.001 #* 10**4

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
            s_b.pos = POSITION_EAST # teleport
            return [[0.85, s_a], [0.15, s_b]]

        elif a == ACTION_STAY:
            s_b.pos = POSITION_EAST # teleport
            return [[0.85, s_a], [0.15, s_b]]

        elif a == ACTION_GATHER:
            s_a.mat = min(2, s_a.mat + 1)
            return [[0.75, s_a], [0.25, s_b]]
        return []

    elif s.pos == POSITION_NORTH:

        if a == ACTION_DOWN:
            s_a.pos = POSITION_CENTER
            s_b.pos = POSITION_EAST
            return [[0.85, s_a], [0.15, s_b]]
        
        elif a == ACTION_STAY:
            s_b.pos = POSITION_EAST    
            assert s_b.pos != s.pos, "modifies"
            return [[0.85, s_a], [0.15, s_b]]
        
        elif a == ACTION_CRAFT:
            if s.mat == 0:
                return []
            s_c = deepcopy(s)
            s_a.mat -= 1
            s_b.mat -= 1
            s_c.mat -= 1
            s_a.arrow = min(3, s_a.arrow + 1)             
            s_b.arrow = min(3, s_b.arrow + 2)
            s_c.arrow = min(3, s_c.arrow + 3)
            return [[0.5, s_a], [0.35, s_b], [0.15, s_c]]
        return []

    elif s.pos == POSITION_EAST:
        
        if a == ACTION_LEFT:
            s_a.pos = POSITION_CENTER
            return [[1, s_a]]
        
        elif a == ACTION_STAY:
            return [[1, s]]
        
        elif a == ACTION_SHOOT:
            if s.arrow == 0:
                return []
            h = s.mm_health 
            s_a.mm_health = max(0, s.mm_health - 1)
            s.arrow -= 1
            s_a.arrow -= 1
            if h:
                assert s_a.mm_health != s.mm_health, "equal" 
            return [[0.9, s_a], [0.1, s]]
        
        elif a == ACTION_HIT:
            s_a.mm_health = max(0, s.mm_health - 2)
            return [[0.2, s_a], [0.8, s]]

        return []

    elif s.pos == POSITION_WEST:

        if a == ACTION_RIGHT:
            s_a.pos = POSITION_CENTER
            return [[1, s_a]]
        
        elif a == ACTION_STAY:
            return [[1, s]]    
        
        elif a == ACTION_SHOOT:
            if s.arrow == 0:
                return []
            s.arrow -= 1
            s_a.arrow -= 1
            s_a.mm_health = max(0, s.mm_health - 1)
            return [[0.25, s_a], [0.75, s]]
        
        return []

    elif s.pos == POSITION_CENTER:
        
        if a == ACTION_DOWN:
            s_a.pos = POSITION_SOUTH
            s_b.pos = POSITION_EAST
            return [[0.85, s_a], [0.15, s_b]]
        
        elif a == ACTION_LEFT:
            s_a.pos = POSITION_WEST
            s_b.pos = POSITION_EAST
            return [[0.85, s_a], [0.15, s_b]]
        
        elif a == ACTION_RIGHT:
            s_a.pos = POSITION_EAST
            s_b.pos = POSITION_EAST
            return [[0.85, s_a], [0.15, s_b]]
        
        elif a == ACTION_STAY:
            s_b.pos = POSITION_EAST
            return [[0.85, s], [0.15, s_b]]

        elif a == ACTION_SHOOT:
            if s.arrow == 0:
                return []
            s.arrow -= 1
            s_a.arrow -= 1
            s_a.mm_health = max(0, s.mm_health - 1)
            return [[0.5, s_a], [0.5, s]]
        
        elif a == ACTION_HIT:
            s_a.mm_health = max(0, s.mm_health - 2)
            return [[0.1, s_a], [0.9, s]]

        return []

    raise ValueError

def get_utility(prob_state, U, attacked=False, state=None):
    utility = STEP_COST
    if attacked:
        if state.pos == POSITION_EAST or state.pos == POSITION_CENTER:
            state.mm_health = min(4, state.mm_health + 1)
            utility += -40 + GAMMA * U[state.pos][state.mat][0][state.mm_state][state.mm_health]
        else:
            for p, s in prob_state:
                assert s.mm_state == MM_STATE_DORMANT, "wrong state"
                if s.mm_health == 0:
                    utility += p * (GAMMA * U[s.pos][s.mat][s.arrow][s.mm_state][s.mm_health] + 50)
                else:
                    utility += p * GAMMA * U[s.pos][s.mat][s.arrow][s.mm_state][s.mm_health]

    else:
        for p, s in prob_state:
            if s.mm_health == 0:
                utility += p * (GAMMA * U[s.pos][s.mat][s.arrow][s.mm_state][s.mm_health] + 50)
            else:
                utility += p * GAMMA * U[s.pos][s.mat][s.arrow][s.mm_state][s.mm_health]
            
    
    return utility

def get_scaled_utility(U, s, a):
    total_utility = 0
    prob_state = get_prob_next_state(s, a)
    if len(prob_state) == 0:
        return None
    if s.mm_state == MM_STATE_DORMANT:

        for i in range(len(prob_state)):
            prob_state[i][1].mm_state = MM_STATE_READY
        total_utility += 0.2 * get_utility(prob_state, U)

        for i in range(len(prob_state)):
            prob_state[i][1].mm_state = MM_STATE_DORMANT
        total_utility += 0.8 * get_utility(prob_state, U)
    
    elif s.mm_state == MM_STATE_READY:

        total_utility += 0.5 * get_utility(prob_state, U)

        # when attack is not successful other states will take place
        for i in range(len(prob_state)):
            prob_state[i][1].mm_state = MM_STATE_DORMANT

        s.mm_state = MM_STATE_DORMANT
        total_utility += 0.5 * get_utility(prob_state, U, True, s)

    else:
        raise ValueError
    return total_utility        
    
def save_policy(index, U, P, path, mode='a+'):
    with open(path, mode) as f:
        f.write('iteration={}\n'.format(index))
        U = np.around(U, 3)
        for state, utility in np.ndenumerate(U):
            s = State(*state)
            f.write('{}:{}=[{:.3f}]\n'.format(s, ACTION_ARR[P[state]], utility))
        f.write('\n')

def value_iteration(path):

    U = np.zeros((POSITIONS_RANGE, MATERIALS_RANGE, ARROWS_RANGE, MM_STATE_RANGE, MM_HEALTH_RANGE))   
    P = np.full((POSITIONS_RANGE, MATERIALS_RANGE, ARROWS_RANGE, MM_STATE_RANGE, MM_HEALTH_RANGE), -1, dtype='int')   

    index = 0
    while True:
        delta = np.NINF
        U_next = np.zeros(U.shape)

        for state, U_s in np.ndenumerate(U):
            if state[4] == 0:
                continue

            best_util = np.NINF
            best_action = None

            s = State(*state)
            for action in range(NUM_ACTIONS):
                cur_utility = get_scaled_utility(U, s, action)
                if cur_utility == None:
                    continue
                if cur_utility and best_util < cur_utility:
                    best_util = cur_utility
                    best_action = action

            U_next[state] = best_util
            P[state] = best_action
            delta = max(delta, abs(best_util - U_s))
        
        U = deepcopy(U_next)

        save_policy(index, U, P, path)
        index += 1

        if delta < DELTA:
            break

    return index

# print(get_scaled_utility(U, State(POSITION_SOUTH, 0, 0, MM_STATE_DORMANT, 1), ACTION_UP))

os.makedirs('outputs', exist_ok=True)

path = 'outputs/part_2_trace.txt'
f = open(path, 'r+')
f.truncate(0) # need '0' when using r+
value_iteration(path)