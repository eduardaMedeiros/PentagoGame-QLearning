import random
import pickle
import os
import pentago as Pentago
import minimax as Minimax
import agent as Agent

class GameLearning():
    def __init__(self, alpha=0.1, gamma=0.9, eps=1):
        self.path = "agent_data.pkl"

        if os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                self.agent = pickle.load(f)
        else:
            self.agent = Agent.Agent(alpha, gamma, eps)

        self.minimax = Minimax.Minimax()
        self.playMinimax = False

        self.games_played = 0
        self.ties = 0
        self.agent_wins = 0
        self.opponent_wins = 0

    def begin_teaching(self, episodes):
        while self.games_played < episodes:
            self.games_played += 1
            self.game = Pentago.Pentago()

            print(f"============= INICIANDO JOGO {self.games_played} =============")
            self.start()

        self.agent.save()

        print("Vitórias Q-Learning: " + str(self.agent_wins))
        print("Vitórias Oponente: " + str(self.opponent_wins))
        print("Empates: " + str(self.ties))

    def start(self):
        players = True if random.randint(0, 1) == 1 else False
        order = ["Oponente", "Q-Learning"] if players else ["Q-Learning", "Oponente"]
    
        while (not self.game.win and not self.game.tie):
            player = "Jogador 1 (" + '\033[37m' + '●' + '\033[0m' + ")" if self.game.first_player_turn else "Jogador 2 (" + '\033[30m' + '●' + '\033[0m' + ")"

            if((order[0] == "Oponente" and self.game.first_player_turn) or (order[1] == "Oponente" and not self.game.first_player_turn)):
                print(player, ": Oponente :", self.minimax.play(self.game)) if self.playMinimax else print(player, ": Oponente :", self.agent.play(self.game))
            else:
                print(player, ": Q-Learning :", self.agent.play(self.game))
           
        if (self.game.tie):
            self.ties += 1
            print("Houve empate!")
        else:
            if (self.game.white):
                if(order[0] == "Oponente"):
                    self.opponent_wins += 1
                else:
                    self.agent_wins += 1

                print("O branco ganhou!") 
            else:
                if(order[1] == "Oponente"):
                    self.opponent_wins += 1
                else:
                    self.agent_wins += 1

                print("O preto ganhou!")
            
game = GameLearning()
game.begin_teaching(1e5)

