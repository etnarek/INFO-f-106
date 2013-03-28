
from config import *


def human_to_indices(j, i):
	"""
	Transforme les coordonnées reçues en coordonnées utilisables par le programme.
	"""
	j = j.lower()
	j = ord(j) - ord('a')
	i -= 1
	return j, i

def save(filename, board, player):
    """
    Sauvegarde le jeu dans un fichier (extension = .dat)
    """
    game = ""
    game += str(player) + "\n"
    game += str(len(board)) + "\n"
    for i in board:
        for j in i:
            if len(str(j)) < 2:
                game += " " + str(j) + " "
            else:
                game += str(j) + " "
        game += "\n"

    fileopen = open(filename, 'w')
    fileopen.write(game)
    fileopen.close()
    return True

def load(filename):
    """
    Charge le fichier en mémoire pour continuer la partie commencée.
    """

    try:
        fileopen = open(filename, 'r')
        game = fileopen.readlines()
        fileopen.close()
    except:
        return True, False

    try:
        player = int(game[0])
        dimention = int(game[1])
        del game[0]
        del game[0]
        board = []

        for i in game:
            line_board = []
            line_game = i.replace("\n", "")
            for j in range(0, len(line_game), 3):
                if -2 <= int(i[j + 1]) <= 2:
                    if i[j] != "-":
                        line_board.append(int(i[j + 1]))

                    else:
                        line_board.append((int(i[j + 1])) * -1)
                else:
                    return False, True
            board.append(line_board)
        return board, player
    except:
        return False, True



def initBoard(dimension):
	"""
	Crée un damier de la dimension reçue en paramètre.
	Retourne le damier sous forme de matrice iXj .
	"""
	matrice = []
	for i in range(dimension):
		matrice.append([0] * dimension)
	if dimension < 4:
		matrice = False

	# si la matrice a une longueur impaire, il faut mettre trois lignes vides
	# au centre.
	elif dimension % 2 == 1:
		for i in range(len(matrice)):
			if i < (dimension - 3) / 2:
				for j in range(len(matrice[i])):
					if (i - j) % 2 == 1:
						matrice[i][j] = BLACK_PLAYER

			elif i >= ((dimension - 3) / 2) + 3:
				for j in range(len(matrice[i])):
					if (i - j) % 2 == 1:
						matrice[i][j] = WHITE_PLAYER

	# si la matrice a une longueur paire, il faut mettre deux lignes vides au
	# centre.
	elif dimension % 2 == 0:
		for i in range(len(matrice)):
			if i < (dimension / 2) - 1:
				for j in range(len(matrice[i])):
					if (j - i) % 2 == 1:
						matrice[i][j] = BLACK_PLAYER
			elif i > dimension / 2:
				for j in range(len(matrice[i])):
					if (j - i) % 2 == 1:
						matrice[i][j] = WHITE_PLAYER

	return matrice


def printBoard(board, player):
	"""
	Affiche le damier en fonction du joueur donné en paramètre.
	"""
	for i in range(player // 2, player * len(board) + player // 2, player):
		print(end=" ")
		for j in range(player // 2, player * len(board[i]) + player // 2, player):
			if board[i][j] == WHITE_PLAYER:
				print(WHITE_PAWN, end=" ")
			elif board[i][j] == BLACK_PLAYER:
				print(BLACK_PAWN, end=" ")
			elif board[i][j] == 2:
				print(WHITE_KING, end=" ")
			elif board[i][j] == -2:
				print(BLACK_KING, end=" ")
			else:
				if (j - i) % 2 == 1:
					print(BLACK_SQUARE, end=" ")
				else:
					print(WHITE_SQUARE, end=" ")
		print("| ", (i + len(board)) % len(board) + 1)

	print(" _" * len(board))

	print(end=" ")
	if player == WHITE_PLAYER:
		for i in range(len(board)):
			print(chr(ord('a') + i), end=" ")
		print()
	elif player == BLACK_PLAYER:
		for i in range(len(board), 0, -1):
			print(chr(ord('a') + i - 1), end=" ")
		print()


def movePiece(board, i, j, direction, length=1):
	"""
	Déplace la pièce des positions i, j du damier "board"
	vers la droite ('R') ou la gauche ('L')
	par rapport au joueur.
	"""
	if board[i][j] < 0:
		player = -1
	elif board[i][j] > 0:
		player = 1
	new_i, new_j = i, j
	capture = None
	try:
		if direction[1] == 'B':
			if direction[0] == 'L':
				new_i += length * player
				new_j -= length * player
				if board[new_i][new_j] != 0:
					capture = (new_i, new_j)
					new_i += player
					new_j -= player
			elif direction[0] == 'R':
				new_i += length * player
				new_j += length * player
				if board[new_i][new_j] != 0:
					capture = (new_i, new_j)
					new_i += player
					new_j += player

	except:
		if direction[0] == 'L':
			new_i -= length * player
			new_j -= length * player
			if board[new_i][new_j] != 0:
				capture = (new_i, new_j)
				new_i -= player
				new_j -= player
		elif direction[0] == 'R':
			new_i -= length * player
			new_j += length * player
			if board[new_i][new_j] != 0:
				capture = (new_i, new_j)
				new_i -= player
				new_j += player

	board[new_i][new_j] = board[i][j]
	board[i][j] = 0
	return ((new_i, new_j), capture)


def capture(board, i, j):
	"""
	Retire la pièce se trouvant aux positions i,j du damier.
	"""
	board[i][j] = 0


def becomeKing(board, i, j):
	"""
	Transforme la pièce aux positions i,j en dame.
	"""
	res = False
	if i == len(board) - 1 or i == 0:
		if -2 < board[i][j] < 2:
			board[i][j] *= 2
		res = True
	return res

def checkCapture(board, i, j, direction, player, length):
	"""
	Regarde si on capture un pièce lorsqu'on veut faire un coup.
	"""
	capture = False
	if length > 0:
		back = 1
		if direction[-1] == 'B' :
			back = -1 

		if direction[0] == 'L':
			i -= length * player * back
			j -= length * player 

		elif direction[0] == 'R':
			i -= length * player * back
			j += length * player 

		if 0 <= i < len(board) and 0 <= j < len(board[i]):
			if board[i][j] >= player * -1:

				if direction[0] == 'L':
					i -= player * back
					j -= player
				elif direction[0] == 'R':
					i -= player * back
					j += player
				if 0 <= i < len(board) and 0 <= j < len(board[i]):
					if board[i][j] == 0:
						capture = True
	return capture



def checkMove(board, i, j, direction, player, length=1, hasPlayed=False, hasCaptured=False):
	"""
	Regarde si le coup voulant être joué par player est possible et renvoye True dans ce cas.
	Sinon renvoie pourquoi le pion ne peut etre bougé.
	Le système de mouvement est basé sur la fonction movePiece.
	"""
	rigth_direction = ['L', 'R', 'LB', 'RB']
	capture = False
	if board[i][j] == 0:
		errCode = NO_PIECE
	elif -2 < board[i][j] < 2 and length > 1:
		errCode = PAWN_ONLY_ONE_MOVE
	elif direction not in rigth_direction:
		errCode = BAD_DIRECTION_FORMAT
	elif board[i][j] * player < 0:
		errCode = OPPONENT_PIECE
	else:
		new_i = i
		new_j = j
		back = 1
		if direction[-1] == 'B' :
			back = -1 

		if direction[0] == 'L':
			new_i -= length * player * back
			new_j -= length * player 

		elif direction[0] == 'R':
			new_i -= length * player * back
			new_j += length * player
		
		if new_i >= len(board) or new_j >= len(board):
			errCode = CANNOT_GO_OUTSIDE

		elif length > 1 and countFree(board, i, j, direction) + 1 < length:
			errCode = NO_FREE_WAY

		elif board[new_i][new_j] != 0 and board[new_i][new_j] * player > 0:
			errCode = SPACE_OCCUPIED

		elif board[new_i][new_j] != 0:
			capture = (new_i, new_j)
			if direction[0] == 'L':
				new_i -= player * back
				new_j -= player 

			elif direction[0] == 'R':
				new_i -= player * back
				new_j += player
				
			if not (0 <= new_i < len(board)) or not(0 <= new_j < len(board)):
				errCode = CANNOT_JUMP_OUTSIDE

			elif board[new_i][new_j] != 0 and board[new_i][new_j] * player < 0:
				errCode = TOO_LONG_JUMP
			else:
				errCode = NO_ERROR

		else:
			if hasPlayed :
				errCode = MUST_CAPTURE

			elif -2 < board[i][j] < 2:
				try:
					direction[1] == 'B'
					errCode = ONLY_KING_GO_BACK
				except:
					errCode = NO_ERROR
			else:
				errCode = NO_ERROR
	return errCode


def countFree(board, i, j, direction, player=None, length=0):
	"""
	Retourne la distance que peut faire une pièce sans devoir faire une capture.
	"""
	if not player:
		if board[i][j] < 0:
			player = -1
		elif board[i][j] > 0:
			player = 1
	if board[i][j] != 0:
		new_i = i
		new_j = j
		back = 1
		if direction[-1] == 'B' :
			back = -1 

		if direction[0] == 'L':
			new_i -= (length+1) * player * back
			new_j -= (length+1) * player 

		elif direction[0] == 'R':
			new_i -= (length+1) * player * back
			new_j += (length+1) * player
		if 0 <= new_i < len(board) and 0 <= new_j < len(board):
			if board[new_i][new_j] == 0:
				length = countFree(board, i, j, direction, player, length + 1)
	return length


def strerr(errCode):
	erreurs = {NO_ERROR: "aucune erreur",
			   PAWN_ONLY_ONE_MOVE: "Le pion ne peut se déplacer que d'une seule case en diagonale.",
			   BAD_DIRECTION_FORMAT: "Erreur de format de direction, les directions autorisées sont :L, R, LB et RB",
			   ONLY_KING_GO_BACK: "Seules les dames peuvent aller en arrière.",
			   SPACE_OCCUPIED: "La case de destination est déjà occupée.",
			   CANNOT_JUMP_OUTSIDE: "Une capture ne peut se terminer hors du damier.",
			   TOO_LONG_JUMP: "On ne peut prendre qu'une seule pièce à la fois.",
			   CANNOT_GO_OUTSIDE: "Les pièces ne peuvent sortir du damier de cette manière.",
			   NO_FREE_WAY: "La dame doit s'arrêter sur la case se trouvant juste après celle de capture.",
			   NO_PIECE: "Il n'y a pas de pièce à cette position.",
			   OPPONENT_PIECE: "Cette pièce ne vous appartient pas.",
			   MUST_CAPTURE: "Il faut capturer pour continuer de jouer."}
	return erreurs[errCode]


def checkEndOfGame(board, player):
	"""
	Vérifie si la partie est finie.
	Si oui, regarde en fonction du joueur à jouer s'il a gagné, perdu ou si c'est un matche nul.
	"""
	res = 0
	i = 0
	WHITE_PLAYER_PAWN = 0
	BLACK_PLAYER_PAWN = 0
	# Tant qu'on ne trouve pas de pion qui peut bouger, on en cherche un.
	while i < len(board) and res is not False:
		j = 0
		while j < len(board) and res is not False:
			if board[i][j] < 0:
				testPlayer = -1
			elif board[i][j] > 0:
				testPlayer = 1
			else:
				testPlayer = 0
			if testPlayer != 0:
				if testPlayer > 0:
					if res == BLACK_PLAYER and (checkMove(board, i, j, 'L', WHITE_PLAYER) == NO_ERROR or checkMove(board, i, j, 'R', WHITE_PLAYER) == NO_ERROR):
						res = False
					elif checkMove(board, i, j, 'L', WHITE_PLAYER) == NO_ERROR or checkMove(board, i, j, 'R', WHITE_PLAYER) == NO_ERROR:
						res = WHITE_PLAYER
				elif testPlayer < 0:
					if res == WHITE_PLAYER and (checkMove(board, i, j, 'L', BLACK_PLAYER) == NO_ERROR or checkMove(board, i, j, 'R', BLACK_PLAYER) == NO_ERROR):
						res = False
					elif checkMove(board, i, j, 'L', BLACK_PLAYER) == NO_ERROR or checkMove(board, i, j, 'R', BLACK_PLAYER) == NO_ERROR:
						res = BLACK_PLAYER
			# Si le pion est celui du joueur, celui-ci peut jouer
			if res == player:
				res = False
			j += 1
		i += 1

	if res is False:
		for i in board:
			WHITE_PLAYER_PAWN += i.count(WHITE_PLAYER)
			WHITE_PLAYER_PAWN += i.count(2)
			BLACK_PLAYER_PAWN += i.count(BLACK_PLAYER)
			BLACK_PLAYER_PAWN += i.count(-2)
		if WHITE_PLAYER_PAWN == 0:
			res = BLACK_PLAYER
		elif BLACK_PLAYER_PAWN == 0:
			res = WHITE_PLAYER
	return res
