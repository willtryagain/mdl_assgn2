
import numpy as np
import cvxpy as cp
import json
import os

POSITIONS_RANGE = 5
MATERIALS_RANGE = 3
ARROWS_RANGE = 4
MM_STATE_RANGE = 2
MM_HEALTH_RANGE = 5
NUM_STATES = POSITIONS_RANGE * MATERIALS_RANGE * ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE

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
        return (POSITION_ARR[self.pos], self.mat, self.arrow, MM_STATE_ARR[self.mm_state], self.mm_health)

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

        if action != ACTION_STAY:
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
            if self.pos == POSITION_CENTER or self.pos == POSITION_EAST:
                next_distrib.append((1, State(self.pos, self.mat, 0, MM_STATE_DORMANT, min(4, self.mm_health + 1))))
            else:
                for p, s in distrib:
                    next_distrib.append((p*0.5, State(s.pos, s.mat, s.arrow, MM_STATE_DORMANT, s.mm_health)))

        elif self.mm_state == MM_STATE_DORMANT:
            for p, s in distrib:
                next_distrib.append((p*0.8, s))
            for p, s in distrib:
                next_distrib.append((p*0.2, State(s.pos, s.mat, s.arrow, MM_STATE_READY, s.mm_health)))    

        else:
            raise ValueError

        return next_distrib

    def get_distrib(self, action):
        if action not in self.get_actions():
            print(self)
            print(ACTION_ARR[action])
            print(ACTION_ARR[action] for action in  self.get_actions())
            raise ValueError

        if action == ACTION_NONE:
            return []

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
            s_a = State(self.pos, self.mat, self.arrow, self.mm_state, max(0, self.mm_health - 2))
            # s_b = State(self.pos, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_CENTER:
                return [
                    (0.1, s_a),
                    # (0.9, s_b)
                ]
            elif self.pos == POSITION_EAST:
                return [
                    (0.2, s_a),
                    # (0.1, s_b)
                ]
            else:
                raise ValueError 

                
        if action == ACTION_GATHER:

            if self.mat == 2:
                return []

            s_a = State(self.pos, self.mat + 1, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_SOUTH:
                return [
                    (0.75, s_a)
                ]

            else:
                raise ValueError 

        if action == ACTION_CRAFT:

            if self.arrow == 3:
                return []

            s_a = State(self.pos, self.mat, min(3, self.arrow + 1), self.mm_state, self.mm_health)
            s_b = State(self.pos, self.mat, min(3, self.arrow + 2), self.mm_state, self.mm_health)
            s_c = State(self.pos, self.mat, min(3, self.arrow + 3), self.mm_state, self.mm_health)


            if self.pos == POSITION_NORTH:
                return [
                    (0.5, s_a),
                    (0.35, s_b),
                    (0.15, s_c)
                ]

            else:
                raise ValueError 

        if action == ACTION_STAY:

            s_a = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_EAST or self.pos == POSITION_WEST:
                return []

            return [
                (0.15, s_a)
            ]

        if action == ACTION_UP:

            s_b = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_CENTER:
                s_a = State(POSITION_NORTH, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            elif self.pos == POSITION_SOUTH:
                s_a = State(POSITION_CENTER, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            else:
                raise ValueError

        if action == ACTION_DOWN:

            s_b = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_CENTER:
                s_a = State(POSITION_SOUTH, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            elif self.pos == POSITION_NORTH:
                s_a = State(POSITION_CENTER, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            else:
                raise ValueError

        if action == ACTION_LEFT:

            s_b = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_CENTER:
                s_a = State(POSITION_WEST, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            elif self.pos == POSITION_EAST:
                s_a = State(POSITION_CENTER, self.mat, self.arrow, self.mm_state, self.mm_health)

                return [
                    (1, s_a),
                ]
                
            else:
                raise ValueError

        if action == ACTION_RIGHT:

            s_b = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)

            if self.pos == POSITION_CENTER:
                s_a = State(POSITION_EAST, self.mat, self.arrow, self.mm_state, self.mm_health)
                
                return [
                    (0.85, s_a),
                    (0.15, s_b)
                ]

            elif self.pos == POSITION_WEST:
                s_a = State(POSITION_CENTER, self.mat, self.arrow, self.mm_state, self.mm_health)

                return [
                    (1, s_a),
                ]
                
            else:
                raise ValueError

        raise ValueError


    def __str__(self):
        return f'({POSITION_ARR[self.pos]},{self.mat},{self.arrow},{MM_STATE_ARR[self.mm_state]},{self.mm_health * MM_HEALTH_FACTOR})'

    @classmethod
    def get_state_from_hash(self, index):
        if type(index) != int:
            raise ValueError

        if not (0 <= index < NUM_STATES):
            raise ValueError

        pos = index // (MATERIALS_RANGE * ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE)
        index = index % (MATERIALS_RANGE * ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE)

        mat = index // (ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE)
        index = index % (ARROWS_RANGE * MM_STATE_RANGE * MM_HEALTH_RANGE)

        arrow = index // (MM_STATE_RANGE * MM_HEALTH_RANGE)
        index = index % (MM_STATE_RANGE * MM_HEALTH_RANGE)

        mm_state = index // MM_HEALTH_RANGE
        index = index % MM_HEALTH_RANGE

        mm_health = index

        return State(pos, mat, arrow, mm_state, mm_health)

class IJ:

    def __init__(self):
        self.c = self.get_columns_dim()
        self.r = self.get_r()
        self.a = self.get_a()
        self.alpha = self.get_alpha()
        self.x = self.quest()
        self.policy = []
        self.sol_dict = {}
        self.objective = 0.0

    def get_columns_dim(self):
        d = 0
        for i in range(NUM_STATES):
            d += len(State.get_state_from_hash(i).get_actions())

        return d

    def get_a(self):
        a = np.zeros((NUM_STATES, self.c), dtype=np.float64)

        index = 0
        for i in range(NUM_STATES):
            state = State.get_state_from_hash(i)
            actions = state.get_actions()

            for action in actions:
                a[i][index] += 1
                
                next_distrib = state.get_distrib(action)
                next_distrib = state.get_scaled_distrib(next_distrib)

                for p, s in next_distrib:
                    a[s.get_hash()][index] -= p

                index += 1
        
        return a

    def get_r(self):
        r = np.full((1, self.c), STEP_COST)

        index = 0
        for i in range(NUM_STATES):
            actions = State.get_state_from_hash(i).get_actions()

            for action in actions:
                if action == ACTION_NONE:
                    r[0][index] = 0
                index += 1

        return r

    def get_alpha(self):
        alpha = np.zeros((NUM_STATES, 1))
        s = State(POSITIONS_VALUES[-1], MATERIALS_VALUES[-1], ARROWS_VALUES[-1], MM_STATE_VALUES[-1], MM_HEALTH_VALUES[-1]).get_hash()
        alpha[s][0] = 1
        return alpha

    def quest(self):
        x = cp.Variable((self.c, 1), 'x')

        constraints = [
            cp.matmul(self.a, x) == self.get_alpha(),
            x >= 0
        ] 

        objective = cp.Maximize(cp.matmul(self.r, x))
        problem = cp.Problem(objective, constraints)

        solution = problem.solve()
        self.objective = solution
        arr = list(x.value)
        l = [float(val) for val in arr]
        return l

    def get_policy(self):
        index = 0
        for i in range(NUM_STATES):
            s = State.get_state_from_hash(i)
            actions = s.get_actions()
            action_index = np.argmax(self.x[index : index + len(actions)]) 
            index += len(actions)
            best_action = actions[action_index]
            local = []
            local.append(list(s.get_state()))
            local.append(ACTION_ARR[best_action])
            self.policy.append(local)

        
    def generate_dict(self):
        self.sol_dict["a"] = self.a.tolist()
        r = [float(val) for val in np.transpose(self.r)]
        self.sol_dict["r"] = r
        alpha = [float(val) for val in self.alpha]
        self.sol_dict["alpha"] = alpha
        self.sol_dict["x"] = self.x
        self.sol_dict["policy"] = self.policy
        self.sol_dict["objective"] = float(self.objective)


    def save_output(self):
        path = "outputs/part_3_output.json"
        obj = json.dumps(self.sol_dict)
        with open(path, 'w+') as f:
            f.write(obj)

    def run(self):
        os.makedirs('outputs', exist_ok=True)
        self.quest()
        self.get_policy()
        self.generate_dict()
        self.save_output()

ij = IJ()
ij.run()
