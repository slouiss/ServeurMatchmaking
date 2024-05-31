class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]  # Plateau de jeu vide
        self.current_player = "X"  # Joueur actuel (commence avec X)
        self.winner = None  # Variable pour stocker le gagnant

    def make_move(self, position):
        if self.board[position] == " ":  # Vérifie si la case est vide
            self.board[position] = self.current_player  # Place le symbole du joueur
            self.check_winner()  # Vérifie s'il y a un gagnant après chaque coup
            self.toggle_player()  # Change de joueur pour le prochain tour
            return True  # Mouvement valide
        else:
            return False  # Mouvement invalide

    def check_winner(self):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
            [0, 4, 8], [2, 4, 6]  # diagonales
        ]

        for pos in winning_positions:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != " ":
                self.winner = self.board[pos[0]]  # Un joueur a gagné
                return

    def toggle_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"  # Change de joueur

    def is_board_full(self):
        return " " not in self.board  # Vérifie si le plateau est plein (match nul)

    def reset_game(self):
        self.board = [" " for _ in range(9)]  # Réinitialise le plateau
        self.current_player = "X"  # Remet le joueur initial
        self.winner = None  # Réinitialise le gagnant
