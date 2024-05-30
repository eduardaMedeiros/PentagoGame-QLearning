import random
import pentago as Pentago
import minimax as Minimax
import agent as Agent

class GameLearning():
    def __init__(self, alpha=0.5, gamma=0.9, eps=0.1):
        self.agent = Agent.Agent(alpha, gamma, eps)
        self.minimax = Minimax.Minimax()

        self.games_played = 0

    def begin_teaching(self, episodes):
        while self.games_played < episodes:
            self.game = Pentago.Pentago()
            self.start()
            self.games_played += 1
    
            if self.games_played % 1000 == 0:
                print("Jogadas realizadas: %i" % self.games_played)
       
        self.agent.save()

    def start(self):
        players = False
        order = ["Minimax", "Q-Learning"] if players else ["Q-Learning", "Minimax"]
    
        while (not self.game.win and not self.game.tie):
            print(self.game)
            player = "Jogador 1 (" + '\033[37m' + '●' + '\033[0m' + ")" if self.game.first_player_turn else "Jogador 2 (" + '\033[30m' + '●' + '\033[0m' + ")"

            if((order[0] == "Minimax" and self.game.first_player_turn) or (order[1] == "Minimax" and not self.game.first_player_turn)):
                print("Minimax pensando...")
                print(player, ": Minimax :", self.minimax.play(self.game))
            else:
                print("Q-learning calculando...")
                print(player, ": Q-Learning :", self.agent.play(self.game))
           
        print(self.game)
        if (self.game.tie):
            print("Houve empate!")
        elif (self.game.white):
            print("O branco ganhou!")
        else:
            print("O preto ganhou!")

game = GameLearning()
game.begin_teaching(1)

