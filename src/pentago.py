import re, copy
import numpy as np

BLACK = '\033[30m' + '●' + '\033[0;0m'
WHITE = '\033[37m' + '●' + '\033[0;0m'

W = 'W'
B = 'B'

class Pentago:
    def __init__(self):
        self.white = False
        self.black = False

        self.util_max = 1000
        self.util_min = -1000

        self.win = False
        self.tie = False
        self.first_player_turn = True
        
        self.blocks = [[None] * 9 for _ in range(4)]
    
    def __str__(self):
        start = '\033[1;31m' + "+-------+-------+\n" + '\033[0;0m' 
        text = [start]

        for block in range(2, 5, 2):
            for i in range(0, 7, 3):
                for j in range(block - 2, block):
                    text.append('\033[1;31m' + "| " + '\033[0;0m')
                    for k in range(3):
                        val = self.get_position_player(j, i + k)
                        text.append(WHITE + " " if val == W else BLACK + " ") if val != None else text.append('\033[1;31m' + "• " + '\033[0;0m')

                text.append('\033[1;31m' + "|\n" + '\033[0;0m')
            text.append(start)
            
        return ''.join(text)

    def play(self, action):
        actions = re.split(' |/', action)
        
        block = int(actions[0]) - 1
        position = int(actions[1]) - 1
        block_rotation = int(actions[2][0]) - 1
        rotation = actions[2][1]

        self.blocks[block][position] = W if self.first_player_turn else B
 
        lst = np.array(self.blocks[block_rotation]).reshape(3, 3)
        if(rotation in ("R", "r")):
            lst = np.rot90(lst, -1).flatten().tolist()
        else:
            lst = np.rot90(lst, 1).flatten().tolist()
      
        self.blocks[block_rotation] = lst
        self.first_player_turn = not self.first_player_turn

        self.winner()
    
    def calc_utility(self, max, min):
        lines = self.get_lines()
        utility = 0
        scores = [1, 2, 10, 100]

        for line in lines:
            if self.get_sequences(line, max, 5):
                return self.util_max
        
            if self.get_sequences(line, max, 5):
                return self.util_min
        
        for line in lines:
            if self.get_sequences(line, max, 4):
                utility += scores[3]
                pass
            elif self.get_sequences(line, max, 3):
                utility += scores[2]
                pass
            elif self.get_sequences(line, max, 2):
                utility += scores[0]
            
        for line in lines:
            if self.get_sequences(line, min, 4):
                utility -= scores[3]
                pass
            elif self.get_sequences(line, min, 3):
                utility -= scores[2]
                pass
            elif self.get_sequences(line, min, 2):
                utility -= scores[0]
    
        if utility == 0:
            for i in range(4):
                if self.blocks[i][4] == max:
                    utility += scores[1]
                if self.blocks[i][4] == min:
                    utility -= scores[1]
     
        return utility
    
    def utility(self):
        return self.calc_utility(W, B) if self.first_player_turn else -self.calc_utility(B, W)
    
    def utilities(self):
        return self.calc_utility(W, B) + -self.calc_utility(B, W)
    
    def winner(self):
        white = self.calc_utility(W, B)
        black = -self.calc_utility(B, W)

        if(len(self.possible_actions()) == 0):
            self.tie = True

        if (white == self.util_max):
            self.white = True
        
        if (black == self.util_min):
            self.black = True
        
        if (self.white and self.black):
            self.tie = True
        elif (self.white or self.black):
            self.win = True
    
    def possible_actions(self):
        actions = []
        for b in range(4):
            for p in range(9):
                for rb in range(4):
                    if(self.blocks[b][p] == None):
                        actions.append(str(b + 1) + "/" + str(p + 1) + " " + str(rb + 1) + "L")
                        actions.append(str(b + 1) + "/" + str(p + 1) + " " + str(rb + 1) + "R")
        return actions
    
    def get_lines(self):
        lst = []
        def convert(l, c):
            def convert_inner(l, c):
                return l * 3 + c

            return 2 * int(l / 3) + int(c / 3), convert_inner(l % 3, c % 3)

        for r in range(6):
            for c in range(6):
                b, p = convert(r, c)
                lst.append(self.blocks[b][p])
      
        matrix = [lst[i * 6:(i + 1) * 6] for i in range(6)]
        lines = matrix + list(map(list, zip(*matrix)))

        lines.append([matrix[i][i] for i in range(6)])
        lines.append([matrix[i + 1][i] for i in range(5)])
        lines.append([matrix[i][i + 1] for i in range(5)])
        lines.append([matrix[i][5 - i] for i in range(6)])
        lines.append([matrix[i + 1][5 - i] for i in range(5)])
        lines.append([matrix[i][4 - i] for i in range(5)])

        return lines      
    
    def get_sequences(self, line, player, size):
        string = ''.join(map(str, line))
        sequence = player * size
        return sequence in string
        
    def get_position_player(self, block, position):
        return self.blocks[block][position]

    def copy(self):
        return copy.deepcopy(self)