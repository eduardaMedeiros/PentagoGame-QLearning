import csv
import random
import collections

import numpy as np

class Agent():
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay

        self.Q = {}
        self.actions = self.possible_actions( [[None] * 9 for _ in range(4)])   
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
      
    def get_action(self, s):
        string_s = self.get_state_key(s)
        actions_s = self.possible_actions(s)

        if random.random() < self.eps:
            action = actions_s[random.randint(0,len(actions_s)-1)]
        else:
            values = np.array([self.Q[a][string_s] for a in actions_s])
            ix_max = np.where(values == np.max(values))[0]

            if len(ix_max) > 1:
                ix_select = np.random.choice(ix_max, 1)[0]
            else:
                ix_select = ix_max[0]
            action = actions_s[ix_select]

        self.eps *= (1.-self.eps_decay)
        return action
    
    def get_state_key(self, s):
        key = ''
        for row in s:
            for elt in row:
                if elt == None:
                    elt = '*'
                key += elt
        return key

    def update(self, s, s_, a, r):
        string_s = self.get_state_key(s)
        string_s_ = self.get_state_key(s_)

        if s_ is not None:
            possible_actions = self.possible_actions(s_)
            Q_options = [self.Q[action][string_s_] for action in possible_actions]
            self.Q[a][string_s] += self.alpha*(r + self.gamma*max(Q_options) - self.Q[a][string_s])
        else:
            self.Q[a][string_s] += self.alpha*(r - self.Q[a][string_s])

    def possible_actions(self, s):
        actions = []
        for b in range(4):
            for p in range(9):
                for rb in range(4):
                    if(s[b][p] == None):
                        actions.append(str(b + 1) + "/" + str(p + 1) + " " + str(rb + 1) + "L")
                        actions.append(str(b + 1) + "/" + str(p + 1) + " " + str(rb + 1) + "R")
        return actions
    
    def play(self, game):
        s = game.blocks
        a = self.get_action(s)

        game.play(a)
    
        if not(game.win and game.tie):
            r = 0
            s_ = game.blocks
            self.update(s, s_, a, r)
        else:
            if game.white and game.black:
                r = 0.5
            elif game.white:
                r = 1
            else:
                r = -(1*1)

            self.update(s, None, a, r)

        return a

    def save(self, filename='q_table.csv'):
        states = list(next(iter(self.Q.values())).keys())
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([""] + states)

            for actions, value in self.Q.items():
                writer.writerow([actions] + [value[state] for state in states])
                    