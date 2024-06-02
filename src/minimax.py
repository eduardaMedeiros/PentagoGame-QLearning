class Minimax:
    def __init__(self):
        self.visited = dict()
        self.node_expanded = 0
        self.deep_expanded = 0

    def alpha_beta(self, game, deep_max, deep=0):
        best_actions = [None]

        def alpha_beta_aux(M, game, deep_max, deep, alpha, beta, best_actions):
            M.deep_expanded = max(M.deep_expanded, deep)

            if(deep >= deep_max):
                return game.utilities()
            elif(game.utility() == game.util_max):
                return game.util_max
            elif(game.utility() == game.util_min):
                return game.util_min
            else:
                actions = game.possible_actions()

                best_action = None
                best_util = None

                for action in actions:
                    next = game.copy()
                    next.play(action)

                    if(str(next.blocks) in M.visited):
                        next_util = M.visited[str(next.blocks)]
                    else:
                        next_util = alpha_beta_aux(M, next, deep_max, deep+1, alpha, beta, best_actions)
                        M.visited[str(next.blocks)] = next_util

                    M.node_expanded += 1
                    if(best_action == None):
                        best_action = action
                        best_util = next_util
                    
                    if(next_util == None):
                        next_util = 0

                    if(best_util == None):
                        best_util = 0

                    if(best_util < next_util if game.first_player_turn else best_util > next_util):
                        best_action = action
                        best_util = next_util

                    if(game.first_player_turn):
                        alpha = max(alpha, int(next_util))
                    else:
                        beta = min(beta, int(next_util))

                    if(beta <= alpha):
                        break

                best_actions[0] = best_action
                return best_util

        alpha_beta_aux(self, game, deep_max, deep, float("-inf"), float("inf"), best_actions)
        return best_actions[0]

    def play(self, game, deep_max = 2):
        self.node_expanded = 0
        self.deep_expanded = 0

        action = self.alpha_beta(game, deep_max)
        game.play(action)

        self.visited.clear()
        return action 