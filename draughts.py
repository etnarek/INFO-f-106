
from config import *
from draughtsFunctions import *

def play(player_now, board):
    """
    Fonction s'occupant du jeux, lorsque qu'un joueur veut bouger une pièce.
    """
    rafle = True
    hasPlayed = False
    hasCaptured = False
    i, j = -1, -1
    while rafle: # Si il y a une rafle ou que le joueur commence
        rafle = False
        if i == -1 and j == -1: # pas besoin de redemander les coordonées lors d'une rafle
            coordinates = input(
                "Quel pion voulez-vous déplacer? Coordonnées du style a5: ")
            coordinates = coordinates.lower()
            if len(coordinates) == 2:
                if coordinates[0].isdigit():
                    i = int(coordinates[0])
                    j = coordinates[1]
                    j, i = human_to_indices(j, i)
                elif coordinates[1].isdigit():
                    i = int(coordinates[1])
                    j = coordinates[0]
                    j, i = human_to_indices(j, i)
                else:
                    print("Mauvais format de coordonnées.")
                    rafle = True

            else:
                print("Il faut deux coordonnées pour que ça fonctionne.")
                rafle = True
        else:
            printBoard(board, player_now)
        if not rafle: # sert à savoir s'il ne s'est pas trompé
            direction = input("Dans quelle direction doit se déplacer la pièce?(L/R), ajouter B pour aller en arrière: ")
            direction = direction.upper()
            if direction != "Q":
                length = input("Quel est la longueur du déplacement? ")
                if length.isdigit():
                    length = int(length)
                    erreur = checkMove(board, i, j, direction, player_now,
                                       length, hasPlayed, hasCaptured)
                    if  erreur != NO_ERROR and hasCaptured:
                        print(strerr(erreur))
                        print("Tapez Q comme direction pour quitter le mode rafle.")
                        rafle = True
                    elif erreur != NO_ERROR:
                        print(strerr(erreur))
                        rafle = True
                        i, j = -1, -1
                    else:
                        captured = movePiece(board, i, j, direction, length)
                        hasPlayed = True
                        if captured[1]:
                            i, j = captured[0]
                            capture(board, captured[1][0], captured[1][1])
                            rafle = True
                            hasCaptured = True
                            print("Tapez Q comme direction pour quitter le mode rafle.")
                        else:
                            rafle = False
                else:
                    print("Mauvais format de longueur.")
                    rafle = True
                    i, j = -1, -1
    becomeKing(board, i, j)


def results(board, player_now):
    """
    Fonction affichant les résultats de la partie dans la console.
    """
    if checkEndOfGame(board, player) == 0:
        print("*" * 70)
        print("La partie s'est terminée sur un nul.")
        print("*" * 70)
    elif checkEndOfGame(board, player) == BLACK_PLAYER:
        print("*" * 70)
        print("Les noirs ont gagné.")
        print("*" * 70)
    elif checkEndOfGame(board, player) == WHITE_PLAYER:
        print("*" * 70)
        print("Les blancs ont gagné.")
        print("*" * 70)


def main():
    """
    Commence une partie de dame.
    Deux joueurs (WHITE = 1 and BLACK = -1).
    le jeux se termine lorsqu'un joueur ne peut plus bouger.
    """
    # Initialisation :
    board = initBoard(10)
    player_now = WHITE_PLAYER  # joueur en cours
    choice = 0
    null = 'n'

    # Tant que le joueur en cours peut jouer, on continue.
    while checkEndOfGame(board, player_now) is False and choice != 5 and null != 'o':
        print("_" * 70)
        print("c'est au joueur", ((player_now // 2) * (-1)) + 1, " de jouer")
        # A savoir : -1//2 = -1 et 1//2 = 0

        printBoard(board, player_now)
        print("Que voulez-vous faire?")
        print("(1) Déplacer une pièce")
        print("(2) Sauver la partie")
        print("(3) Charger une partie")
        print("(4) Proposer une partie nulle à l'adversaire")
        print("(5) Quitter")

        choice = input(">>>")
        if choice.isdigit():
            choice = int(choice)

            if choice == 1:
                play(player_now, board)
                # on change le joueur
                player_now *= (-1)

            elif choice == 2:
                filename = input("Quel est le nom de la sauvegarde? ")
                save(filename, board, player_now)

            elif choice == 3:
                filename = input("Quel est le nom de la sauvegarde? ")
                new_board, new_player_now = load(filename)
                if new_board and new_player_now:
                    board = new_board
                    player_now = new_player_now

            elif choice == 4:
                print("Joueur", ((player_now * (-1) // 2) * (-1)) + 1, ".")
                null = input("Etes-vous d'accord avec l'autre joueur pour une partie nulle? (o/n) ")
                null = null.lower()

            elif choice == 5:
                print("*" * 70)
                print("Au revoir.")
                print("*" * 70)

            else:
                print("Veuillez entre un chiffre entre 1 et 5")
        else:
            print("Veuillez entrer un chiffre")

    if choice != 5:
        if null == 'o':
            print("*" * 70)
            print("La partie s'est terminée sur un nul.")
            print("*" * 70)
        else:
            results(board, player_now)


if __name__ == '__main__':
    main()
