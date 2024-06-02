import csv
import random
import collections
import pickle
import os
import numpy as np

W = 'W'
B = 'B'

class Agent():
    def __init__(self, alpha, gamma, eps, eps_decay=0.005):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay

        self.player = None

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
    
    def get_reward(self, game, a):
        opponent = B if self.player == W else W
        reward = 0

        s = game.copy()
        s.play(a)

        if s.tie:
            return 500
        if s.win:
            return 1000 if (self.player == W and game.white) or (self.player == B and game.black) else -1000

        lines = s.get_lines()
        updates = []
        for line in lines:
            if line not in game.get_lines():
                updates.append(line)

        for update in updates:
            if s.get_sequences(update, opponent, 4):
                reward -= 150
                pass
            elif s.get_sequences(update, opponent, 3):
                reward -= 115
                pass
            elif s.get_sequences(update, 4 * opponent + self.player, 1) or (update, self.player + 4 * opponent, 1):
                reward += 110
                pass
            elif s.get_sequences(update, 3* opponent + self.player, 1)  or (update, self.player + 3 * opponent, 1):
                reward += 60
                pass
            elif s.get_sequences(update, self.player, 4):
                reward += 100
                pass
            elif s.get_sequences(update, self.player, 3):
                reward += 50
                pass
            elif s.get_sequences(update, self.player, 2):
                reward += 25
                pass
            elif s.get_sequences(update, self.player, 1):
                reward += 10
                pass
      
        return reward

    def get_state_key(self, s):
        key = self.player + '-'
        for row in s:
            for elt in row:
                if elt == None:
                    elt = '*'
                key += elt
        return key

    def update(self, s, s_, a, r):
        string_s = self.get_state_key(s)
        string_s_ = self.get_state_key(s_) if s_ is not None else None

        if s_ is not None:
            possible_actions = self.possible_actions(s_)
            Q_options = [self.Q[action][string_s_] for action in possible_actions]
            if Q_options:
                self.Q[a][string_s] += self.alpha*(r + self.gamma*max(Q_options) - self.Q[a][string_s])
            else:
                self.Q[a][string_s] += self.alpha*(r - self.Q[a][string_s])
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
        self.player = W if game.first_player_turn else B

        s = game.blocks
        a = self.get_action(s)
        r = self.get_reward(game, a)

        game.play(a)
        
        if not(game.win and game.tie):
            s_ = game.blocks
            self.update(s, s_, a, r)
        else:
            print(s)
            self.update(s, None, a, r)

        return a

    def save(self, path = "agent_data.pkl"):
        if os.path.isfile(path):
            os.remove(path)
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()
                    
    def save_crv(self, filename='q_table.csv'):
        states = list(next(iter(self.Q.values())).keys())
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([""] + states)

            for actions, value in self.Q.items():
                writer.writerow([actions] + [value[state] for state in states])