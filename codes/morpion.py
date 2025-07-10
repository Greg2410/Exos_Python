import math

# Initialisation de la grille
board = [" " for _ in range(9)]  # 3x3

def print_board():
    print("\n")
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print(" | ".join(row))
        if i < 2:
            print("---------")
    print()

def check_win(player):
    # Toutes les combinaisons gagnantes
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
        [0, 4, 8], [2, 4, 6]              # diagonales
    ]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_draw():
    return " " not in board

def get_available_moves():
    return [i for i, cell in enumerate(board) if cell == " "]

def minimax(is_maximizing):
    if check_win("O"):
        return 1
    elif check_win("X"):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves():
            board[move] = "O"
            score = minimax(False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves():
            board[move] = "X"
            score = minimax(True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score

def ia_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves():
        board[move] = "O"
        score = minimax(False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = "O"

def player_move():
    while True:
        try:
            move = int(input("Choisis une case (1-9) : ")) - 1
            if move in get_available_moves():
                board[move] = "X"
                break
            else:
                print("❌ Case invalide ou déjà prise.")
        except ValueError:
            print("❌ Entrez un nombre entre 1 et 9.")

def game():
    print("Bienvenue dans le Morpion !")
    print("Tu es X, l'ordinateur est O")
    print_board()

    while True:
        player_move()
        print_board()

        if check_win("X"):
            print("🏆 Tu as gagné !")
            break
        elif is_draw():
            print("🤝 Match nul !")
            break

        print("🤖 L'ordinateur joue...")
        ia_move()
        print_board()

        if check_win("O"):
            print("💻 L'ordinateur a gagné !")
            break
        elif is_draw():
            print("🤝 Match nul !")
            break

# Lancer le jeu
game()
