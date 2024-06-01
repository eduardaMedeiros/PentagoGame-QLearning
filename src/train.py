import random
import pickle
import os
import pentago as Pentago
import minimax as Minimax
import agent as Agent

class GameLearning():
    def __init__(self, alpha=0.8, gamma=0.7, eps=0.9):
        self.path = "agent_data.pkl"

        if os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                self.agent = pickle.load(f)
        else:
            self.agent = Agent.Agent(alpha, gamma, eps)

        self.minimax = Minimax.Minimax()

        self.games_played = 0
        self.ties = 0
        self.white_win = 0
        self.black_win = 0

    def begin_teaching(self, episodes):
        while self.games_played < episodes:
            self.game = Pentago.Pentago()
            self.start()
            self.games_played += 1
            
        print("Vitórias Branco: " + str(self.white_win))
        print("Vitórias Preto: " + str(self.black_win))
        print("Empates: " + str(self.ties))
        
        self.agent.save()

    def start(self):
        players = True if random.randint(0, 1) == 1 else False
        order = ["Minimax", "Q-Learning"] if players else ["Q-Learning", "Minimax"]
    
        while (not self.game.win and not self.game.tie):
            player = "Jogador 1 (" + '\033[37m' + '●' + '\033[0m' + ")" if self.game.first_player_turn else "Jogador 2 (" + '\033[30m' + '●' + '\033[0m' + ")"

            if((order[0] == "Minimax" and self.game.first_player_turn) or (order[1] == "Minimax" and not self.game.first_player_turn)):
                print(player, ": Minimax :", self.minimax.play(self.game))
            else:
                print(player, ": Q-Learning :", self.agent.play(self.game))
           
        print(self.game)
        if (self.game.tie):
            self.ties += 1
            print("Houve empate!")
        elif (self.game.white):
            self.white_win += 1
            print("O branco ganhou!")
        else:
            self.black_win += 1
            print("O preto ganhou!")

game = GameLearning()
game.begin_teaching(5)
