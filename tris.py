import numpy as np

class Agente:
    def __init__(self):
         print("")

class Ambiente:

    def __init__(self):
        print("")

class Utente:
    def __init__(self):
        self.board = np.zeros((3, 3))  # creo una matrice 3 * 3 e la riempio di 0 (casella vuota)
        self.x = -1  # player 1
        self.o = 1  # player 2
    

    def is_empty(self, i, j):
        # ritorno se la casella a posizione i, j è vuota
        return self.board[i, j] == 0
    
    def take_action(self, env):
        # in loop fino a che non ottengo un comando
        while True:
            try:
                move = input("inserisci la casella in cui inserire il segno, formato i,j: ")
                i, j = [int(item.strip()) for item in move.split(',')]
                if env.is_empty(i, j):
                    env.board[i, j] = self.symbol
                    break
                else:
                    print("Please enter valid move")
            except:
                print("Please enter valid move")

class Agente:
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps  
        self.alpha = alpha  # velocità di apprendimento
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, symbol):
        self.symbol = symbol

    def reset_history(self):
        self.state_history = []

    def take_action(self, env):
        if np.random.rand() < self.eps:
            # azione random
            empty_moves = env.get_empty_moves()
            index = np.random.choice(len(empty_moves))
            next_move = empty_moves[index]
        else:
            next_move, _ = env.get_next_best_move(self)
        env.board[next_move[0], next_move[1]] = self.symbol

    def update_state_history(self, s):
        self.state_history.append(s)

    def update(self, env):
        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


def gioca():
    print("")

def main():
    print("inzio il gioco")
    print("agente -> x")
    print("utente -> o")

    #inizializzo l'ambiente
    env = Ambiente()


if __name__ == '__main__':
    main()