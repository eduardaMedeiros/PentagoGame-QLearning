import random
import pickle
import os
import pentago as Pentago

class Game():
    def __init__(self):
        self.path = "agent_data.pkl"

        if os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                self.agent = pickle.load(f)
        else:
            print("Nenhum agente encontrado :(")
            exit()

        self.game = Pentago.Pentago()

    def start(self):
        players = True if random.randint(0, 1) == 1 else False
        order = ["Minimax", "Q-Learning"] if players else ["Q-Learning", "Minimax"]
    
        while (not self.game.win and not self.game.tie):
            print(self.game)
            player = "Jogador 1 (" + '\033[37m' + '●' + '\033[0m' + ")" if self.game.first_player_turn else "Jogador 2 (" + '\033[30m' + '●' + '\033[0m' + ")"

            if((order[0] == "Q-Learning" and self.game.first_player_turn) or (order[1] == "Q-Learning" and not self.game.first_player_turn)):
                print(player, ": Q-Learning :", self.agent.play(self.game))
            else:
                print(player, ": Escolha seu movimento <B/P BD>: ", end="")
                action = input()
                self.game.play(action) if self.game.action_validate(action) else exit()
        
        self.agent.save()

        print(self.game)
        if (self.game.tie):
            print("Houve empate!")
        else:
            print("O branco ganhou!") if self.game.white else print("O preto ganhou!")

game = Game()
game.start()