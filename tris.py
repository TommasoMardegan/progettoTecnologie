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