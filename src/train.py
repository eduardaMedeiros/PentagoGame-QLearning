import random
import pickle
import os
import pentago as Pentago
import minimax as Minimax
import agent as Agent

class GameLearning():
    def __init__(self, alpha=0.8, gamma=0.7, eps=0.9):
        self.path = "agent_data.pkl"
        self.txt = "log_train.txt"

        if os.path.isfile(self.path):
            self.size_path = os.path.getsize(self.path)
            with open(self.path, 'rb') as f:
                self.agent = pickle.load(f)
        else:
            self.agent = Agent.Agent(alpha, gamma, eps)

        self.minimax = Minimax.Minimax()

        self.games_played = 0
        self.ties = 0
        self.agent_wins = 0
        self.minimax_wins = 0

    def begin_teaching(self, episodes):
        while (self.games_played < episodes) and (self.size_path <= 1 * 1024 * 1024 * 1024):
            self.games_played += 1
            self.game = Pentago.Pentago()

            print(f"============= INICIANDO JOGO {self.games_played} =============")
            self.start()
            
            self.size_path = os.path.getsize(self.path)
            if self.games_played % 500 == 0:
                self.agent.save()
            
            
        print("Vitórias Q-Learning: " + str(self.agent_wins))
        print("Vitórias Minimax: " + str(self.minimax_wins))
        print("Empates: " + str(self.ties))
        
    def log_text(self, txt):
        if os.path.isfile(self.txt):
            with open(self.txt, 'a') as f:
                f.write(txt + "\n")

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
        else:
            if (self.game.white):
                if(order[0] == "Minimax"):
                    self.minimax_wins += 1
                else:
                    self.agent_wins += 1

                print("O branco ganhou!") 
                self.log_text(f"{self.games_played} - {order[0]}")
            else:
                if(order[1] == "Minimax"):
                    self.minimax_wins += 1
                else:
                    self.agent_wins += 1

                print("O preto ganhou!")
                self.log_text(f"{self.games_played} - {order[1]}")
            
game = GameLearning()
game.begin_teaching(2)

