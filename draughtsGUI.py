
# Import de base
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.font as font
import random
from config import *
from draughtsFunctions import *


class Interface(tk.Tk):
	"""
	La classe Interface permet de créer la fenêtre autour du canvas. Elle fait appel à la classe Board pour dessiner le canvas.

	Elle est héritée de la classe Tk du module tkinter

	Cette classe comprend les fonctions suivantes:
		__init__() 			initialise la classe
		new_game() 			crée un nouveau jeu
		save_game() 			sauvegarde le jeu
		load_game() 			charge un jeu sauvegardé
		help() 				appelle la classe help_window
		inverse() 			permet un changement de joueur en inversant l'interface
		move() 				bouge une pièce
		direction_length() 		retourne la longueur et direction à partir des coordonnées.
		capture() 			s'occupe des captures
		king() 				transforme un pion en dame si besoin
		show_end() 			affiche un message de fin
		showerror() 			affiche les messages d'erreurs
		get_player() 			retourne le joueur en cours
		set_hasPlayed() 		permet de changer la valeur hasPlayed
		set_hasCaptured() 		permet de changer la valeur de hasCaptured
		get_hasPlayed() 		permet de savoir ce que vaut hasPlayed
		get_end() 			permet de savoir si le jeu est fini

	et a les attributs suivants:
		board 				contient la matrice du damier
		player 				contient le joueur en cours
		hasPlayed 			vrais si le joueur à bougé une pièce
		hasCaptured 			vrai si le joueur a capturé une pièce
		end 				vrai si la partie est finie
		current_player 			référence vers le Label contenant le joueur
		white_capture_label		référence vers le Label pour les captures blanches
		black_capture_label		référence vers le Label pour les captures noires
		white_capture 			contient le nombre de captures blanches
		black_capture 			contient le nombre de captures noires
		label_left			liste de référence vers les Label à gauche du canvas
		label_right 			liste de référence vers les Label à droite du canvas
		label_up 			liste de référence vers les Label en haut du canvas
		label_down 			liste de référence vers les Label en bas du canvas
		canv 				référence vers le damier 			
	"""

	def __init__(self):
		"""
		Crée la fenêtre de base avec les différents boutons, textes et appelle la classe Board pour créer le canvas.
		"""
		tk.Tk.__init__(self)

		# Paramètres de la fenêtre
		self.title('Draughts')
		self.board_length = 500  #CONSTANTE
		self.resizable(width=False, height=False)
		underline = font.Font(self, underline = True)
		underline_petit = font.Font(self, underline = True, size = 10)

		# Variables pour le travail
		self.board = initBoard(DIMENSION)
		self.player = WHITE_PLAYER
		self.hasPlayed = False
		self.hasCaptured = False
		self.end = False
		self.white_player = None
		self.black_player = None

		#joueur en cours
		self.current_player = tk.Label(self, text='Joueur en cours: Blanc',font = underline, padx=5, pady=5)
		self.current_player.grid(row=0,column=2, columnspan=len(self.board) )

		# Comptage des prises
		tk.Label(self, text='Captures blanches:', font = underline_petit).grid(row =1, column = 0, padx=len(self.board), pady=5)
		self.white_capture_label = tk.Label(self, text = 0)
		self.white_capture_label.grid(row =2, column = 0, padx=len(self.board), pady=5)
		tk.Label(self, text='Captures noires: ', font = underline_petit).grid(row =1, column = len(self.board)+4, padx=len(self.board), pady=5)
		self.black_capture_label = tk.Label(self, text = 0)
		self.black_capture_label.grid(row =2, column = len(self.board)+4, padx=len(self.board), pady=5)
		self.white_capture = 0
		self.black_capture = 0

		# Damier avec les chiffres et lettres autour
		j=0
		self.label_left = []
		self.label_right = []
		self.label_up = []
		self.label_down = []
		for i in range(len(self.board)):
			self.label_left.append(tk.Label(self, text=i+1))
			self.label_left[i].grid(row =2+j, column = 1, sticky=tk.E)
			self.label_right.append(tk.Label(self, text=i+1))
			self.label_right[i].grid(row =2+j, column = len(self.board)+2, sticky=tk.W)
			self.label_up.append(tk.Label(self, text=chr(ord('a')+i)))
			self.label_up[i].grid(row =1, column = 2+j, sticky=tk.S)
			self.label_down.append(tk.Label(self, text=chr(ord('a')+i)))
			self.label_down[i].grid(row =len(self.board)+2, column = 2+j, sticky=tk.N)
			j+=1
		self.canv = Board(self, 'white', self.board_length, self.board)
		self.canv.grid(row=2, column=2, rowspan=len(self.board), columnspan = len(self.board))

		# Boutons
		self.frame_button = tk.Frame(self)
		self.frame_button.grid(row=len(self.board)+4, column=0, columnspan=len(self.board)+6, pady=5)
		tk.Button(self.frame_button, text='Nouveau jeu', command=self.new_game).grid(row = 0, column=0, padx = 2)
		tk.Button(self.frame_button, text='Sauvegarder', command=self.save_game).grid(row = 0, column=1, padx = 2)
		tk.Button(self.frame_button, text='Charger', command=self.load_game).grid(row = 0, column=2, padx = 2)
		tk.Button(self.frame_button, text='IA', command=self.startIa).grid(row = 0, column=3, padx = 2)
		tk.Button(self.frame_button, text='Aide', command=self.help).grid(row = 0, column=4, padx = 2)

		# Gestion d'événement
		self.bind("<F1>", self.help)
		self.bind("<Control-n>",self.new_game)
		self.bind("<Control-s>",self.save_game)
		self.bind("<Control-o>",self.load_game)
		self.bind("<Control-q>",self.exit)
		self.bind("<Control-i>",self.startIa)

	def exit(self, event):
		self.quit()	

	def new_game(self, event = None):
		"""
		Permet de rénitialiser le jeu.
		"""
		if messagebox.askyesno("Nouveau jeu", "Êtes-vous sûr de vouloir recommencer le jeu ?"):
			self.board = initBoard(DIMENSION)

			# inversion des éléments pour revenir au cas où les blancs jouent
			if self.player == BLACK_PLAYER:
				self.inverse()

			# Remise à zéro des variables
			self.player = WHITE_PLAYER
			self.hasPlayed = False
			self.hasCaptured = False
			self.end = False
			self.white_capture = 0
			self.black_capture = 0
			self.white_capture_label.configure(text = self.white_capture)
			self.black_capture_label.configure(text = self.black_capture)
			self.white_player = None
			self.black_player = None

			# Recréation du canvas
			self.canv = Board(self, 'white', self.board_length, self.board)
			self.canv.grid(row=2, column=2, rowspan=len(self.board), columnspan = len(self.board))

	def save_game(self, event = None):
		"""
		Permet de sauvegarder le jeu (au format *.dat de préférence.)
		"""
		file_name = filedialog.asksaveasfilename(filetypes=[("Data Save", "*.dat"),("Tous","*")])
		if len(file_name) > 0:
			if save(file_name, self.board, self.player):
				messagebox.showinfo("Sauvegarde", "Sauvegarde réussie.")
			else:
				messagebox.showwarning("Sauvegarde", "Problème pendant la sauvegarde.")

	def load_game(self, event=None):
		"""
		Charge une partie de préférence au format *.dat.
		Vérifie que le fichier n'est pas erroné.
		"""
		file_name = filedialog.askopenfilename(filetypes=(("Data Save", ".dat"),("All files", "*.*")))
		if len(file_name) > 0:
			new_board, new_player = load(file_name)
			if (new_board and new_player):
				if self.player == BLACK_PLAYER:
					self.inverse()

				# Chargement des nouveaux attributs
				self.board = new_board
				self.hasPlayed = False
				self.hasCaptured = False

				# Compte du nombre de pièces déjà capturées
				white_count = 0
				black_count = 0
				total = (len(self.board)-2)//2
				total *= (len(self.board)+1)//2
				for i in range(len(self.board)):
					for j in range(len(self.board)):
						if self.board[i][j] > 0:
							white_count +=1
						elif self.board[i][j] < 0:
							black_count +=1
				self.white_capture = total - white_count
				self.black_capture = total - black_count
				self.white_capture_label.configure(text = self.white_capture)
				self.black_capture_label.configure(text = self.black_capture)

				# Création du damier
				self.canv = Board(self, 'white', self.board_length, self.board)
				self.canv.grid(row=2, column=2, rowspan=len(self.board), columnspan = len(self.board))

				# Inversion du damier si c'est aux noirs de jouer.
				if new_player == BLACK_PLAYER:
					self.inverse()

				# Vérification que le jeu n'est pas déjà terminé.
				self.end = checkEndOfGame(self.board, self.player)
				messagebox.showinfo("chargement", "Chargement réussi.")
			elif new_player:
				messagebox.showwarning("Chargement", "Le fichier est corrompu")
			elif new_board:
				messagebox.showwarning("Chargement", "Erreur de chargement")

	def help(self, evnt=None):
		"""
		Affiche la fenêtre d'aide.
		"""
		self.help_win =help_window()
		self.help_win.mainloop()

	def inverse(self):
		"""
		Inversion de tous les éléments de l'interface graphique en rapport avec le damier.
		"""
		# Inversion des textes
		self.player *= BLACK_PLAYER
		if self.player == WHITE_PLAYER:
			self.current_player.configure(text = "Joueur en cours: Blanc")
		elif self.player == BLACK_PLAYER:
			self.current_player.configure(text = "Joueur en cours: Noir")

		# Inversion du contour du damier
		for i in range(len(self.board)):
			self.label_left[i].configure(text = len(self.board) + 1 - int(self.label_left[i].cget("text")))
			self.label_right[i].configure(text = len(self.board) + 1- int(self.label_right[i].cget("text")))
			self.label_up[i].configure(text = chr(2*ord('a') + len(self.board) - 1 - ord(self.label_up[i].cget("text"))))
			self.label_down[i].configure(text = chr(2*ord('a') + len(self.board) - 1 - ord(self.label_down[i].cget("text"))))

		# Appel de fonction pour l'inversion du canvas
		self.canv.inverse()

	def move(self, i, j, nex_i, nex_j, player):
		"""
		Déplacement d'un pion d'abord dans la matrice puis sur le canvas avec gestion des erreurs.
		prend aussi en compte les captures.
		"""
		if i-nex_i !=0 and j - nex_j !=0:

			# Tranformation des coordonnées en direction
			direction, length = self.direction_length(i,j,nex_i,nex_j,player)
			
			errorMessge = checkMove(self.board, i, j, direction, player, length, self.hasPlayed, self.hasCaptured)

			# Vérifier que le message d'erreur n'est pas à cause de l'envie de manger une pièce.
			if errorMessge == PAWN_ONLY_ONE_MOVE or errorMessge == NO_FREE_WAY:
				captured = checkCapture(self.board, i, j, direction, player, length - 1)
				if captured:
					length-=1
					errorMessge = NO_ERROR

			if errorMessge == NO_ERROR:

				#on bouge la pièce dans la matrice et le canvas
				captured = movePiece(self.board, i, j, direction, length)
				self.canv.move(captured[0])
				self.hasPlayed = True

				# On s'occupe de la capture s'il faut
				if captured[1]:
					self.capture(captured)
				
				# On regarde si le jeu n'est pas terminé.
				self.end = checkEndOfGame(self.board, player)
				if self.end is not False:
					self.show_end()

			else:
				self.show_error(errorMessge)

	def direction_length(self, i, j, nex_i, nex_j, player):
		"""
		Cette fonction reçoit en paramètre deux couples de coordonnées et le joueur.
		Elle retourne la direction utilisée par les autres fonctions.
		"""
		# Gauche / Droite
		if nex_j - j >0 and player == WHITE_PLAYER:
			direction = "R"
		elif player == WHITE_PLAYER:
			direction = 'L'
		elif nex_j - j > 0:
			direction = 'L'
		else:
			direction = 'R'

		# Retour en arrière.
		if nex_i - i > 0 and player == WHITE_PLAYER:
			direction += 'B'
		elif nex_i-i < 0 and player == BLACK_PLAYER:
			direction +='B'

		# Longueur du déplacement
		length = abs(nex_i - i)
		return direction, length


	def capture(self, captured):
		"""
		Permet la capture d'une pièce sur le damier.
		"""
		# Ajoute 1 à la personne qui a capturé la pièce
		if self.player == WHITE_PLAYER:
			self.white_capture+=1
			self.white_capture_label.configure(text = self.white_capture)
		else:
			self.black_capture+=1
			self.black_capture_label.configure(text = self.black_capture)

		# Capture la pièce dans la matrice et sur le damier
		capture(self.board, captured[1][0], captured[1][1])

		self.canv.delete_pawn(captured[1][0], captured[1][1])
		if self.player == BLACK_PLAYER:
			if self.white_player is not None:
				self.white_player.remove(captured[1][0], captured[1][1])
		elif self.player == WHITE_PLAYER:
			if self.black_player is not None:
				self.black_player.remove(captured[1][0], captured[1][1])
				
		self.hasCaptured = True

	def king(self, i, j):
		"""
		Transforme un pièce en dame si elle est arrivée au bout du damier.
		"""
		king = becomeKing(self.board, i,j)
		if king:
			self.canv.king(i,j)

	def show_end(self):
		"""
		Affiche un message lorsque la partie est terminée en disant qui a gagné.
		"""

		if self.end == WHITE_PLAYER:
			messagebox.showinfo("Fin", "Les blans gagnent.")
		elif self.end == BLACK_PLAYER:
			messagebox.showinfo("Fin", "Les noirs gagnent.")
		else:
			messagebox.showinfo("Fin", "Pat, aucun gagnant.")


	def show_error(self, err_code):
		"""
		Affiche les messages d'erreurs.
		"""
		messagebox.showerror("Erreur", strerr(err_code))

	def startIa(self, event = None):
		if messagebox.askyesno('IA', "Voulez-vous que l'IA joue les noirs? (sinon les blancs)"):
			self.black_player = Computer(self, self.board, -1)
		else:
			self.white_player = Computer(self, self.board, 1)

	def nextPlaying(self):
		if self.player == WHITE_PLAYER:
			if self.white_player is not None:
				self.playIa(WHITE_PLAYER)
		else:
			if self.black_player is not None:
				self.playIa(BLACK_PLAYER)

	def playIa(self, player):
		if self.end is False:
			if player == WHITE_PLAYER:
				ia = self.white_player
			else:
				ia = self.black_player

			coord = ia.findMove()

			self.canv.select(coord[0], coord[1])

			captured = movePiece(self.board, coord[0], coord[1], coord[2], coord[3])
			self.canv.move(captured[0])
			ia.move((coord[0], coord[1]),captured[0])
			self.hasPlayed = True

			# On s'occupe de la capture s'il faut
			if captured[1]:
				self.capture(captured)
				self.rafleIa(ia, captured[0][0], captured[0][1])
			
			# On regarde si le jeu n'est pas terminé.
			self.end = checkEndOfGame(self.board, player)
			if self.end is not False:
				self.show_end()
			self.canv.deselect_pawn()

	def rafleIa(self, ia, i, j):
		coord = True
		while self.hasCaptured and coord:
			coord = ia.rafle(i,j)
			if coord:
				captured = movePiece(self.board, coord[0], coord[1], coord[2], coord[3])
				self.canv.move(captured[0])
				ia.move((coord[0], coord[1]),captured[0])
				self.hasPlayed = True

				# On s'occupe de la capture s'il faut
				if captured[1]:
					self.capture(captured)


	# getter:
	def get_player(self):
		return self.player
	def get_hasPlayed(self):
		return self.hasPlayed
	def get_end(self):
		return self.end

	def get_board(self):
		return self.board

	# setter
	def set_hasPlayed(self, bool):
		self.hasPlayed = bool
	def set_hasCaptured(self, bool):
		self.hasCaptured = bool

	
class Board(tk.Canvas):
	"""
	cette classe s'occupe de dessiner le damier et de bouger les pions.

	Elle est héritée de la classe Canvas du module tkinter

	Elle contient les fonctions suivantes:
		__init__() 			charge les différents eléments du canvas
		draw_Piece() 			s'occupe de dire quand on doit dessiner une pièce avec create_pawn()
		create_pawn()			dessine les pièces demandées sur le canvas
		select_piece() 			s'occupe de l'événement généré lorsqu'on clique sur une pièce.
		select_new_pawn() 		fonction appelée si on sélectionne un pion sans avoir sélectionné avant.
		deselect_pawn() 		fonction utilisée lors de la désélection d'un pion
		inverse() 			inverse les pions du canvas
		move() 				bouge les pièces sur le canvas
		delete_pawn() 			supprime un pion du canvas
		king() 				transforme un pion en dame

	et a comme attributs:
		length       			largeur du canvas
		len_board    			nombre de cases de largeur du damier
		ratio  				rapport entre length et len_board 
		parent  			lien vers la fenêtre parente
		inversed  			est à -1 si le damier est inversé
		selected_object  		contient l'objet qui est sélectionné est à false par défaut
		pawn  				dictionnaire contenant toute les pièces dessinées sur le canvas pour les bouger plus facilement.
		i  				ligne de la dernière pièce selectionnée
		j  				colonne de la dernière pièce selectionnée
		player  			joueur de la dernière pièce selectionnée
	"""

	def __init__(self,parent, bg, length, board):
		"""
		Initialise le canvas et ses attributs.
		"""
		tk.Canvas.__init__(self,parent, bg=bg, height=length, width=length)

		# Attributs
		self.length = length
		self.len_board = len(board)
		self.ratio = (length/len(board))
		self.parent = parent
		self.inversed = 1
		self.selected_object = False


		# Dessin des cases et des pièces
		for k in range(len(board)):
			for l in range(len(board)):
				if (k-l)%2 == 1 :
					self.create_rectangle(self.ratio*l,self.ratio*k, self.ratio*l+self.ratio, self.ratio*k+self.ratio, fill = "black")
		self.draw_Piece(board)
		
		# Evenement
		self.bind("<Button-1>", self.select_piece)

	def draw_Piece(self, board):
		"""
		Permet de dessiner les pièces du damier grace a un appel à create_pawn.
		s'occupe aussi de la création du dictionnaire de pièces.
		"""
		i, j = 0,0
		self.pawn = {}

		for k in range(len(board)):
			for l in range(len(board)):
				player = board[k][l]
				if player !=0 and abs(player) < 2:
					self.pawn[self.create_pawn(self.ratio,i,j,player)] = [player, k, l]
				elif player !=0:
					self.pawn[self.create_pawn(self.ratio,i,j,player,True)] = [player/abs(player), k, l]
				i+=1
			i=0
			j+=1
			
	def create_pawn(self, ratio, i, j, player, king = False):
		"""
		Dessine les pièces sur le canvas
		"""
		line = "white"
		width = 2
		if king:
			line = "red"
			width = 5
		color = "white" if player > 0 else "black"

		return self.create_oval(ratio*i+5,ratio*j+5,ratio*i+ratio-5,ratio*j+ratio-5, outline = line, fill = color, width=width)

	def select(self, i, j):
		if self.inversed == -1:
			i = self.len_board -1 -i
			j = self.len_board -1 -j

		i = i*self.ratio + self.ratio//2
		j = j*self.ratio + self.ratio//2
		select_object = self.find_closest(j, i)
		self.select_new_pawn(select_object)

	def select_piece(self, event):
		"""
		S'occupe de la sélection des pièces lorsqu'un event est généré sur le canvas (clic de souris)
		"""
		if self.parent.get_end() is False:
			select_object=self.find_closest(event.x, event.y)

			# On sélectionne une nouvele pièce
			if not self.selected_object:
				if select_object[0] in self.pawn:
					self.select_new_pawn(select_object)

			# On désélectionne la pièce
			elif select_object == self.selected_object:
				self.deselect_pawn()
			
			# on sélectionne une nouvelle case pour la pièce
			else:
				nex_i = event.y
				nex_j = event.x
				nex_i = int(nex_i//self.ratio)
				nex_j = int(nex_j//self.ratio)
				i = self.i
				j = self.j
				if self.inversed == -1:
					nex_i = self.len_board - 1- nex_i
					nex_j = self.len_board - 1- nex_j

				# appel vers la fonction move générale.
				self.parent.move(i, j, nex_i, nex_j, self.player)

		else:
			messagebox.showinfo("Fin", "La partie est déja finie.")

	def select_new_pawn(self, select_object):
		"""
		Sélection d'une nouvelle piece.
		"""
		i = self.pawn[select_object[0]][1]
		j = self.pawn[select_object[0]][2]
		player = int(self.pawn[select_object[0]][0])

		# Vérification que c'est bien la pièce du joueur.
		if (player==self.parent.get_player()*abs(player)):
			self.itemconfig(select_object, fill="green")
			self.selected_object = select_object
			self.i = i
			self.j = j
			if player > 0:
				self.player = WHITE_PLAYER
			elif player < 0:
				self.player = BLACK_PLAYER

		else:
			self.parent.show_error(OPPONENT_PIECE)


	def deselect_pawn(self):
		"""
		Quand on reclique sur une pièce pour la désélectionner.
		"""
		if self.selected_object:
			selected_object = self.selected_object
			self.selected_object = False

			if self.pawn[selected_object[0]][0] == WHITE_PLAYER:
				self.itemconfig(selected_object, fill="white")
			else:
				self.itemconfig(selected_object, fill="black")

			# Si on a joué, on termine le tour.
			if self.parent.get_hasPlayed():
				self.parent.king(self.pawn[selected_object[0]][1],self.pawn[selected_object[0]][2])
				self.parent.set_hasCaptured(False)
				self.parent.set_hasPlayed(False)
				self.parent.inverse()
				self.parent.nextPlaying()


	def inverse(self):
		"""
		Inverse toutes les pièces du damier lors du changement de joueur.
		"""
		for i in self.pawn:
			if self.inversed == 1:
				y= self.len_board -1 - self.pawn[i][1]
				x= self.len_board -1 - self.pawn[i][2]
			else:
				y= self.pawn[i][1]
				x= self.pawn[i][2]

			self.coords(i, self.ratio*x+5, self.ratio*y+5, self.ratio*x+self.ratio-5, self.ratio*y+self.ratio-5)

		self.inversed *=-1

	def move(self, next):
		"""
		Bouge une pièce sur le damier.
		"""
		i,j =next
		k,l = j,i
		if self.inversed == -1:
			k = self.len_board -1 -k
			l = self.len_board -1 -l

		self.coords(self.selected_object, self.ratio*k+5, self.ratio*l+5, self.ratio*k+self.ratio-5, self.ratio*l+self.ratio-5)

		self.pawn[self.selected_object[0]][1] = i
		self.pawn[self.selected_object[0]][2] = j

		self.i, self.j = i, j

	def delete_pawn(self, i, j):
		"""
		supprime une pièce du damier
		"""
		if self.inversed == -1:
			i = self.len_board -1 -i
			j = self.len_board -1 -j

		pawn = self.find_closest(self.ratio*j+self.ratio//2,self.ratio*i+self.ratio//2)
		del self.pawn[pawn[0]]
		self.delete(pawn)
		
	def king(self, i, j):
		"""
		Transforme une pièce du damier en dame.
		"""
		pawn = self.find_closest(self.ratio*j+self.ratio//2,self.ratio*i+self.ratio//2)
		self.itemconfig(pawn, width=5, outline="red")


class help_window(tk.Tk):
	"""
	Cette classe permet d'afficher la fenêtre d'aide.

	Elle est héritée de la classe Tk du module tkinter

	Elle n'a comme fonction que:
		__init__() 		charge les différents éléments de la fenêtre d'aide.
	"""

	def __init__(self):
		"""
		Initialise la fenêtre d'aide.
		"""
		tk.Tk.__init__(self)
		self.title('Aide')
		self.resizable(width=False, height=False)
		underline = font.Font(self, underline = True)
		underline_petit = font.Font(self, underline = True, size = 10)

		# Aide sur les différents types de pions
		tk.Label(self, text="Les différents pions:", font = underline).grid(row=0,columnspan=4,pady=5)
		white_pawn = tk.Canvas(self, width = 50, height = 50, bg = "black")
		black_pawn = tk.Canvas(self, width = 50, height = 50, bg = "black")
		white_king = tk.Canvas(self, width = 50, height = 50, bg = "black")
		black_king = tk.Canvas(self, width = 50, height = 50, bg = "black")
		white_pawn.grid(row = 1, column = 0, padx=5, pady =2)
		white_king.grid(row = 2, column = 0, padx=5, pady =2)
		black_pawn.grid(row =1, column = 3, padx=5, pady =2)
		black_king.grid(row =2, column = 3, padx=5, pady =2)
		white_pawn.create_oval(5,5,45,45, fill = "white", outline = "white", width=2) # Dessins de pions
		black_pawn.create_oval(5,5,45,45, fill = "black", outline = "white", width=2)
		white_king.create_oval(5,5,45,45, fill = "white", outline = "red", width=5)
		black_king.create_oval(5,5,45,45, fill = "black", outline = "red", width=5)
		tk.Label(self, text="Pions blancs").grid(row=1, column=1, sticky=tk.W, padx=5, pady =2)
		tk.Label(self, text="Dames blanches").grid(row=2, column=1, sticky=tk.W, padx=5, pady =2)
		tk.Label(self, text="Pions noirs").grid(row=1, column=2, sticky=tk.E, padx=5, pady =2)
		tk.Label(self, text="Dames noires").grid(row=2, column=2, sticky=tk.E, padx=5, pady =2)

		# Explications des règles de base
		tk.Label(self, text="Règles:", font = underline).grid(row = 3, columnspan=4, pady=5)
		tk.Label(self, text="Déplacements:", font = underline_petit).grid(row = 4, column = 0, sticky = tk.N + tk.E, pady = 3, padx = 5)
		deplacement = "Les pions ne peuvent se déplacer que d'une seule case en diagonale\n"
		deplacement += "et ne peuvent aller en arrière sauf pour prendre.\n\n"
		deplacement += "Les dames peuvent se déplacer dans n'importe quelle diagonale\n"
		deplacement+= "et du nombre d'autant de case possible tant que le chemin est libre."
		tk.Label(self, text=deplacement, justify=tk.LEFT).grid(row=4, column = 1, columnspan =3, sticky = tk.W, pady = 3, padx = 5)

		# Explication pour les prises
		tk.Label(self, text="Prise:", font = underline_petit).grid(row=5, column=0, sticky=tk.N + tk.E, pady = 5, padx = 5)
		prise = "Pour prendre un pion à l'adversaire, il faut être à une case si on a un pion\n"
		prise += "Les dames doivent être dans la même diagonale et qu'il n'y ait aucun pion dans le chemin.\n\n"
		prise+="Il faut ensuite une place libre après le pion dans la même direction.\n"
		prise += "La dame est obligée de s'arrêter juste après le pion.\n\n"
		prise += "Après une prise, on peut continuer à prendre."
		tk.Label(self, text = prise, justify=tk.LEFT).grid(row = 5, column = 1, columnspan = 3, sticky = tk.W, pady = 5, padx = 5)


class Computer(object):
	"""docstring for Computer"""
	def __init__(self, parent, board, color):
		"""
		"""
		self.pawn = []
		for i in range(len(board)):
			for j in range(len(board)):
				if board[i][j] * color > 0:
					self.pawn.append([i,j,False])
		self.color = color
		self.parent = parent

	def findMove(self): # changer les nonms des variables pour une mailleur compréhension
		"""
		"""
		found = False
		board = self.parent.get_board()
		directions = ['L', 'R', 'LB', 'RB']

		if len(self.pawn) > 10:
			pawn = random.sample(self.pawn, 10)
		else:
			pawn = self.pawn

		# Regarde si on peut capturer une pièce (parmi 10)
		k = 0
		while k < len(pawn):
			i = pawn[k][0]
			j = pawn[k][1]

			for direction in directions:
				if abs(board[i][j]) >1:
					length = countFree(board, i, j, direction, self.color)
				else:
					length = 1				
				if checkCapture(board, i , j, direction, self.color, length):
					if checkMove(board, i, j, direction, self.color, length) == NO_ERROR:
						return i, j, direction, length
			k+=1					

		# Regarde si on peut bouger une pièce sans être capturé (parmi 10)
		if len(self.pawn) > 10:
			pawn = random.sample(self.pawn, 10)
		else:
			pawn = self.pawn

		k = 0
		while k < len(pawn):
			i = pawn[k][0]
			j = pawn[k][1]

			for direction in directions:
				length = countFree(board, i, j, direction, self.color)-1
				if length > 0:
					if abs(board[i][j]) == 1:
						length = 1
					if checkMove(board, i, j, direction, self.color, length) == NO_ERROR:
						if (board[i+2][j] == -self.color and board[i][j+2] == 0) or (board[i][j+2] == -self.color and board[i+2][j] == 0):
							return i, j, directions, length
			k+=1

		# Sinon, on essaye de bouger une des pièces.
		k = 0
		while k < len(self.pawn):
			i = self.pawn[k][0]
			j = self.pawn[k][1]
			for direction in directions:
				if abs(board[i][j]) >1:
					length = countFree(board, i, j, direction, self.color)
				else:
					length = 1
				if checkMove(board, i, j, direction, self.color, length) == NO_ERROR:
					return i, j, direction, length
			k+=1

	def move(self,start, end):
		"""
		"""
		i,j = start
		next_i, next_j = end
		for k in self.pawn:
			if k[0] == i and k[1] == j:
				k[0] = next_i
				k[1] = next_j

	def remove(self, i, j):
		"""
		"""
		found = False
		k=0
		while not found and k < len(self.pawn):
			if self.pawn[k][0] == i and self.pawn[k][1] == j:
				del self.pawn[k]
				found = True
			k+=1

	def rafle(self, i, j):
		directions = ['L', 'R', 'LB', 'RB']
		board = self.parent.get_board()
		for direction in directions:
			if abs(board[i][j]) >1:
				length = countFree(board, i, j, direction, self.color)
			else:
				length = 1
			if checkMove(board, i, j, direction, self.color, length, True, True) == NO_ERROR:
				return i,j,direction,length
		return False

		

if __name__ == '__main__':
	fenetre = Interface()
	fenetre.mainloop()
