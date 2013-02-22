import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from config import *
from draughtsFunctions import *

# Help Box
# Commentaire

class Interface(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title('Draughts')
		self.board_length = 500 #CONSTANTE

		self.board = initBoard(DIMENSION)
		self.player = WHITE_PLAYER
		self.hasPlayed = False
		self.hasCaptured = False
		self.end = False

		self.current_player = tk.Label(self, text='Joueur en cours: Blanc', padx=5, pady=5)
		self.current_player.grid(row=0,column=2, columnspan=len(self.board) )

		tk.Label(self, text='Captures blanches:').grid(row =1, column = 0, padx=len(self.board), pady=5)
		self.white_capture_label = tk.Label(self, text = 0)
		self.white_capture_label.grid(row =2, column = 0, padx=len(self.board), pady=5)
		tk.Label(self, text='Captures noires: ').grid(row =1, column = len(self.board)+4, padx=len(self.board), pady=5)
		self.black_capture_label = tk.Label(self, text = 0)
		self.black_capture_label.grid(row =2, column = len(self.board)+4, padx=len(self.board), pady=5)
		self.white_capture = 0
		self.black_capture = 0

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

		self.frame_button = tk.Frame(self)
		self.frame_button.grid(row=len(self.board)+4, column=0, columnspan=len(self.board)+6, pady=5)
		tk.Button(self.frame_button, text='Nouveau jeu', command=self.new_game).grid(row = 0, column=0, padx = 2)
		tk.Button(self.frame_button, text='Sauvegarder', command=self.save_game).grid(row = 0, column=1, padx = 2)
		tk.Button(self.frame_button, text='Charger', command=self.load_game).grid(row = 0, column=2, padx = 2)
		tk.Button(self.frame_button, text='Aide', command=self.help).grid(row = 0, column=3, padx = 2)

		self.bind("<F1>", self.help)
		self.bind("<Control-n>",self.new_game)
		self.bind("<Control-s>",self.save_game)
		self.bind("<Control-o>",self.load_game)



	def new_game(self, event = None):
		if messagebox.askyesno("Nouveau jeu", "Etes vous sur de vouloir recommencer le jeux?"):
			self.board = initBoard(DIMENSION)
			if self.player == BLACK_PLAYER:
				self.inverse()
			self.player = WHITE_PLAYER
			self.hasPlayed = False
			self.hasCaptured = False
			self.end = False
			self.white_capture = 0
			self.black_capture = 0
			self.white_capture_label.configure(text = self.white_capture)
			self.black_capture_label.configure(text = self.black_capture)
			self.canv = Board(self, 'white', self.board_length, self.board)
			self.canv.grid(row=2, column=2, rowspan=len(self.board), columnspan = len(self.board))

	def save_game(self, event = None):
		file_name = filedialog.asksaveasfilename(filetypes=[("Data Save", "*.dat"),("Tous","*")])
		if len(file_name) > 0:
			if save(file_name, self.board, self.player):
				messagebox.showinfo("Sauvegarde", "Sauvegarde réussie.")
			else:
				messagebox.showwarning("Sauvegarde", "Problème pendant la sauvegarde.")

	def load_game(self, event=None):
		file_name = filedialog.askopenfilename(filetypes=(("Data Save", ".dat"),("All files", "*.*")))
		if len(file_name) > 0:
			new_board, new_player = load(file_name)
			if (new_board and new_player):
				self.board = new_board
				self.hasPlayed = False
				self.hasCaptured = False
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
				self.canv = Board(self, 'white', self.board_length, self.board, new_player)
				self.canv.grid(row=2, column=2, rowspan=len(self.board), columnspan = len(self.board))
				if new_player == BLACK_PLAYER:
					self.inverse()
				self.end = checkEndOfGame(self.board, self.player)
				messagebox.showinfo("chargement", "Chargement réussi.")
			elif new_player:
				messagebox.showwarning("Chargement", "Le fichier est corrompu")
			elif new_board:
				messagebox.showwarning("Chargement", "Erreur de chargement")

	def help(self, evnt=None):
		self.help_win =help_window()
		self.help_win.mainloop()

	def inverse(self):
		self.player *= BLACK_PLAYER
		if self.player == WHITE_PLAYER:
			self.current_player.configure(text = "Joueur en cours: Blanc")
		elif self.player == BLACK_PLAYER:
			self.current_player.configure(text = "Joueur en cours: Noir")

		for i in range(len(self.board)):
			self.label_left[i].configure(text = len(self.board) + 1 - int(self.label_left[i].cget("text")))
			self.label_right[i].configure(text = len(self.board) + 1- int(self.label_right[i].cget("text")))
			self.label_up[i].configure(text = chr(2*ord('a') + len(self.board) - 1 - ord(self.label_up[i].cget("text"))))
			self.label_down[i].configure(text = chr(2*ord('a') + len(self.board) - 1 - ord(self.label_down[i].cget("text"))))
		self.canv.inverse()

	def get_player(self):
		return self.player

	def move(self, i, j, nex_i, nex_j, player):
		if i-nex_i !=0 and j - nex_j !=0:
			if nex_j - j >0 and player == WHITE_PLAYER:
				direction = "R"
			elif player == WHITE_PLAYER:
				direction = 'L'
			elif nex_j - j > 0:
				direction = 'L'
			else:
				direction = 'R'
			if nex_i - i > 0 and player == WHITE_PLAYER:
				direction += 'B'
			elif nex_i-i<0 and player == BLACK_PLAYER:
				direction +='B'
			length = abs(nex_i - i)
			errorMessge = checkMove(self.board, i, j, direction, player, length, self.hasPlayed, self.hasCaptured)

			if errorMessge == PAWN_ONLY_ONE_MOVE or errorMessge == NO_FREE_WAY:
				errorMessge, captured = checkMove(self.board, i, j, direction, player, length-1, self.hasPlayed, self.hasCaptured, True)
				if errorMessge == NO_ERROR and captured:
					length-=1
				else:
					errorMessge = PAWN_ONLY_ONE_MOVE

			if errorMessge == NO_ERROR:
				captured = movePiece(self.board, i, j, direction, length)
				self.canv.move(captured[0])
				self.hasPlayed = True

				if captured[1]:
					if self.player == WHITE_PLAYER:
						self.white_capture+=1
						self.white_capture_label.configure(text = self.white_capture)
					else:
						self.black_capture+=1
						self.black_capture_label.configure(text = self.black_capture)
					capture(self.board, captured[1][0], captured[1][1])
					self.canv.delete_pawn(captured[1][0], captured[1][1])
					self.hasCaptured = True
				self.end = checkEndOfGame(self.board, player)

				if self.end is not False:
					if self.player == WHITE_PLAYER:
						messagebox.showinfo("Fin", "Les blans gagnent.")
					elif self.player == BLACK_PLAYER:
						messagebox.showinfo("Fin", "Les noirs gagnent.")
					else:
						messagebox.showinfo("Fin", "Pat, aucun gagnant.")

			else:
				self.show_error(errorMessge)

	def show_error(self, err_code):
		messagebox.showerror("Erreur", strerr(err_code))



	def set_hasPlayed(self, bool):
		self.hasPlayed = bool
	def set_hasCaptured(self, bool):
		self.hasCaptured = bool
	def get_hasPlayed(self):
		return self.hasPlayed
	def get_end(self):
		return self.end
	def king(self, i, j):
		king = becomeKing(self.board, i,j)
		if king:
			self.canv.king(i,j)







class Board(tk.Canvas):
	def __init__(self,parent, bg, length, board, inversed = 1):
		tk.Canvas.__init__(self,parent, bg=bg, height=length, width=length)
		self.length = length
		self.len_board = len(board)
		self.ratio = (length/len(board))
		self.parent = parent
		for k in range(len(board)):
			for l in range(len(board)):
				if (k-l)%2 == 1 :
					self.create_rectangle(self.ratio*l,self.ratio*k, self.ratio*l+self.ratio, self.ratio*k+self.ratio, fill = "black")
		self.draw_Piece(board)
		self.inversed = inversed



		self.selected_object = False
		self.bind("<Button-1>", self.select_piece)

	def draw_Piece(self, board):
		i, j = 0,0
		self.pawn = {}
		for k in range(len(board)):
			for l in range(len(board)):
				player = board[k][l]
				if player !=0 and abs(player) < 2:
					self.pawn[self.create_pawn(self.ratio,i,j,player)] = [player, k, l]
				elif player !=0:
					self.pawn[self.create_pawn(self.ratio,i,j,player,True)] = [player, k, l]
				i+=1
			i=0
			j+=1
			
	def create_pawn(self, ratio, i, j, player, king = False):
		line = "white"
		width = 2
		if king:
			line = "red"
			width = 5
		color = "white" if player > 0 else "black"

		return self.create_oval(ratio*i+5,ratio*j+5,ratio*i+ratio-5,ratio*j+ratio-5, outline = line, fill = color, width=width)

	def select_piece(self, event):
		if self.parent.get_end is not False:
			select_object=self.find_closest(event.x, event.y)
			if not self.selected_object:
				if select_object[0] in self.pawn:
					self.select_new_pawn(select_object)

			elif select_object == self.selected_object:
				self.deslecet_pawn()
					
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
				self.parent.move(i, j, nex_i, nex_j, self.player)
		else:
			messagebox.showinfo("Fin", "La partie est déja finie.")

	def select_new_pawn(self, select_object):
		i = self.pawn[select_object[0]][1]
		j = self.pawn[select_object[0]][2]
		player = int(self.pawn[select_object[0]][0])
		if (player==self.parent.get_player()*abs(player)):
			self.itemconfig(select_object, fill="green")
			self.selected_object = select_object
			self.i = i
			self.j = j
			self.player = player
		else:
			self.parent.show_error(OPPONENT_PIECE)


	def deslecet_pawn(self):
		if self.selected_object:
			if self.pawn[self.selected_object[0]][0] == WHITE_PLAYER:
				self.itemconfig(self.selected_object, fill="white")
			else:
				self.itemconfig(self.selected_object, fill="black")
			if self.parent.get_hasPlayed():
				self.parent.king(self.pawn[self.selected_object[0]][1],self.pawn[self.selected_object[0]][2])
				self.parent.set_hasCaptured(False)
				self.parent.set_hasPlayed(False)
				self.parent.inverse()

			self.selected_object = False

	def inverse(self):

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
		if self.inversed == -1:
			i = self.len_board -1 -i
			j = self.len_board -1 -j
		pawn = self.find_closest(self.ratio*j+self.ratio//2,self.ratio*i+self.ratio//2)
		del self.pawn[pawn[0]]
		self.delete(pawn)

	def king(self, i, j):
		pawn = self.find_closest(self.ratio*j+self.ratio//2,self.ratio*i+self.ratio//2)
		self.itemconfig(pawn, width=5, outline="red")

class help_window(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title('Aide')

		tk.Label(self, text="Les différents pions:").grid(row=0,columnspan=4,pady=5)
		self.white_pawn = tk.Canvas(self, width = 50, height = 50, bg = "black")
		self.black_pawn = tk.Canvas(self, width = 50, height = 50, bg = "black")
		self.white_king = tk.Canvas(self, width = 50, height = 50, bg = "black")
		self.black_king = tk.Canvas(self, width = 50, height = 50, bg = "black")
		self.white_pawn.grid(row = 1, column = 0, padx=5, pady =2)
		self.white_king.grid(row = 2, column = 0, padx=5, pady =2)
		self.black_pawn.grid(row =1, column = 3, padx=5, pady =2)
		self.black_king.grid(row =2, column = 3, padx=5, pady =2)
		self.white_pawn.create_oval(5,5,45,45, fill = "white", outline = "white", width=2)
		self.black_pawn.create_oval(5,5,45,45, fill = "black", outline = "white", width=2)
		self.white_king.create_oval(5,5,45,45, fill = "white", outline = "red", width=5)
		self.black_king.create_oval(5,5,45,45, fill = "black", outline = "red", width=5)
		tk.Label(self, text="Pions blancs").grid(row=1, column=1, sticky=tk.W, padx=5, pady =2)
		tk.Label(self, text="Dammes blanches").grid(row=2, column=1, sticky=tk.W, padx=5, pady =2)
		tk.Label(self, text="Pions noirs").grid(row=1, column=2, sticky=tk.E, padx=5, pady =2)
		tk.Label(self, text="Dammes noires").grid(row=2, column=2, sticky=tk.E, padx=5, pady =2)



fenetre = Interface()
fenetre.mainloop()
