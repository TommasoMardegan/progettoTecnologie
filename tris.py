import numpy as np
import pickle

class Agente:
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps  # probabilità di esplorazione
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

class Ambiente:
    def __init__(self):
        self.board = np.zeros((3, 3))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.max_states = 3 ** (3 * 3)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, symbol):
        if self.game_over() and self.winner == symbol:
            return 1
        else:
            return 0

    def game_over(self):
        if self.ended:
            return True

        players = [self.x, self.o]
        for i in range(3):
            for player in players:
                if self.board[i].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        for j in range(3):
            for player in players:
                if self.board[:, j].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True

        for player in players:
            if self.board.trace() == player * 3 or np.fliplr(self.board).trace() == player * 3:
                self.winner = player
                self.ended = True
                return True

        if not np.any(self.board == 0):
            self.winner = None
            self.ended = True
            return True

        self.winner = None
        return False

    def get_state(self):
        state = 0
        loop_index = 0
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == self.x:
                    state_value = 1
                elif self.board[i, j] == self.o:
                    state_value = 2
                else:
                    state_value = 0
                state += (3 ** loop_index) * state_value
                loop_index += 1
        return state

    def get_empty_moves(self):
        empty_moves = []
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):
                    empty_moves.append((i, j))
        return empty_moves

    def get_next_best_move(self, agent):
        best_value = -1
        next_best_move = None
        best_state = None
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):
                    self.board[i, j] = agent.symbol
                    state = self.get_state()
                    self.board[i, j] = 0
                    if agent.V[state] > best_value:
                        best_value = agent.V[state]
                        best_state = state
                        next_best_move = (i, j)
        return next_best_move, best_state

    def draw_board(self):
        for i in range(3):
            print(" -------------")
            for j in range(3):
                print(" ", end="")
                if self.board[i, j] == self.x:
                    print("| x", end=" ")
                elif self.board[i, j] == self.o:
                    print("| o", end=" ")
                else:
                    print("|  ", end=" ")
            print("|")
        print(" -------------")
        print("\n")

    def save_state(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.board, f)

    def load_state(self, filename):
        with open(filename, 'rb') as f:
            self.board = pickle.load(f)

class Utente:
    def __init__(self):
        self.board = np.zeros((3, 3))  # creo una matrice 3 * 3 e la riempio di 0 (casella vuota)
        self.x = -1  # player 1
        self.o = 1  # player 2

    def set_symbol(self, symbol):
        self.symbol = symbol

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

def gioca(agent, user, env):
    current_player = None
    while not env.game_over():
        current_player = user if current_player == agent else agent
        current_player.take_action(env)
        state = env.get_state()
        agent.update_state_history(state)
        env.draw_board()

        # Chiediamo se l'utente vuole salvare il gioco dopo ogni mossa
        save = input("Vuoi salvare il gioco? (s/n): ").strip().lower()
        if save == 's':
            filename = input("Inserisci il nome del file: ").strip()
            env.save_state(filename)
            print(f"Gioco salvato in {filename}")

    agent.update(env)

    if env.winner == user.symbol:
        print("You win!")
    elif env.winner == agent.symbol:
        print("Agent wins!")
    else:
        print("It's a draw!")

def main():
    print("Inizio il gioco")
    print("Agente -> x")
    print("Utente -> o")

    env = Ambiente()
    agent = Agente()
    user = Utente()
    user.set_symbol(env.o)
    agent.set_symbol(env.x)

    V = np.zeros(env.max_states)
    agent.setV(V)

    # Chiedi all'utente se vuole caricare uno stato di gioco esistente
    load = input("Vuoi caricare uno stato di gioco esistente? (s/n): ").strip().lower()
    if load == 's':
        filename = input("Inserisci il nome del file: ").strip()
        env.load_state(filename)
        print(f"Gioco caricato da {filename}")

    gioca(agent, user, env)

if __name__ == '__main__':
    main()
