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

		self.current_player = tk.Label(self, text='Current player: White', padx=5, pady=5)
		self.current_player.grid(row=0,column=2, columnspan=len(self.board) )

		tk.Label(self, text='White Capture:').grid(row =1, column = 0, padx=len(self.board), pady=5)
		self.white_capture_label = tk.Label(self, text = 0)
		self.white_capture_label.grid(row =2, column = 0, padx=len(self.board), pady=5)
		tk.Label(self, text='Black Capture: ').grid(row =1, column = len(self.board)+4, padx=len(self.board), pady=5)
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
		tk.Button(self.frame_button, text='New Game', command=self.new_game).grid(row = 0, column=0, padx = 2)
		tk.Button(self.frame_button, text='Save Game', command=self.save_game).grid(row = 0, column=1, padx = 2)
		tk.Button(self.frame_button, text='Load Game', command=self.load_game).grid(row = 0, column=2, padx = 2)
		tk.Button(self.frame_button, text='Help', command=self.help).grid(row = 0, column=3, padx = 2)

		self.bind("<F1>", self.help)



	def new_game(self):
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

	def save_game(self):
		file_name = filedialog.asksaveasfilename(filetypes=[("Data Save", "*.dat"),("Tous","*")])
		if len(file_name) > 0:
			if save(file_name, self.board, self.player):
				messagebox.showinfo("Sauvegarde", "Sauvegarde réussie.")
			else:
				messagebox.showwarning("Sauvegarde", "Problème pendant la sauvegarde.")

	def load_game(self):
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
			self.current_player.configure(text = "Current Player: White")
		elif self.player == BLACK_PLAYER:
			self.current_player.configure(text = "Current Player: Black")

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
						messagebox.showinfo("Win", "White player win.")
					elif self.player == BLACK_PLAYER:
						messagebox.showinfo("Win", "Black player win.")
					else:
						messagebox.showinfo("Null", "Nobody win.")

			else:
				self.show_error(errorMessge)

	def show_error(self, err_code):
		messagebox.showerror("Error", strerr(err_code))



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







class Board(tk.Canvas):  # réécrir les for comm avec draw piece
	def __init__(self,parent, bg, length, board, inversed = 1):
		tk.Canvas.__init__(self,parent, bg=bg, height=length, width=length)
		self.length = length
		self.len_board = len(board)
		self.rapport = (length/len(board))
		self.parent = parent
		for k in range(len(board)):
			for l in range(len(board)):
				if (k-l)%2 == 1 :
					self.create_rectangle(self.rapport*l,self.rapport*k, self.rapport*l+self.rapport, self.rapport*k+self.rapport, fill = "black")
		self.draw_Piece(board)
		self.inversed = inversed



		self.selected_object = False
		self.bind("<Button-1>", self.select_piece)

	def draw_Piece(self, board):
		i, j = 0,0
		self.pawn = {}
		for k in range(len(board)):
			for l in range(len(board)):

				if board[k][l] ==WHITE_PLAYER:
					self.pawn[self.create_oval(self.rapport*i+5,self.rapport*j+5,self.rapport*i+self.rapport-5,self.rapport*j+self.rapport-5, outline = "white", fill = "white", width=2)] = [WHITE_PLAYER, k, l]
				elif board[k][l]==BLACK_PLAYER:
					self.pawn[self.create_oval(self.rapport*i+5,self.rapport*j+5,self.rapport*i+self.rapport-5,self.rapport*j+self.rapport-5, outline = "white", fill = "Black", width=2)] = [BLACK_PLAYER, k, l]
				elif board[k][l]>0:
					self.pawn[self.create_oval(self.rapport*i+5,self.rapport*j+5,self.rapport*i+self.rapport-5,self.rapport*j+self.rapport-5, outline = "red", fill = "white", width=5)] = [WHITE_PLAYER, k, l]
				elif board[k][l]<0:
					self.pawn[self.create_oval(self.rapport*i+5,self.rapport*j+5,self.rapport*i+self.rapport-5,self.rapport*j+self.rapport-5, outline = "red", fill = "black", width=5)] = [BLACK_PLAYER, k, l]
				i+=1
			i=0
			j+=1

	def select_piece(self, event):
		if self.parent.get_end is not False:
			select_object=self.find_closest(event.x, event.y)
			if not self.selected_object:
				if select_object[0] in self.pawn:
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

			elif select_object == self.selected_object:
				self.deslecet_pawn()
				if self.parent.get_hasPlayed():
					self.parent.set_hasCaptured(False)
					self.parent.set_hasPlayed(False)
					self.parent.inverse()
			else:
				nex_i = event.y
				nex_j = event.x
				nex_i = int(nex_i//self.rapport)
				nex_j = int(nex_j//self.rapport)
				i = self.i
				j = self.j
				if self.inversed == -1:
					nex_i = self.len_board - 1- nex_i
					nex_j = self.len_board - 1- nex_j
				self.parent.move(i, j, nex_i, nex_j, self.player)
		else:
			messagebox.showinfo("Win", "La partie est déja finie.")

	def deslecet_pawn(self):
		if self.selected_object:
			if self.pawn[self.selected_object[0]][0] == WHITE_PLAYER:
				self.itemconfig(self.selected_object, fill="white")
			else:
				self.itemconfig(self.selected_object, fill="black")
			if self.parent.get_hasPlayed():
				self.parent.king(self.pawn[self.selected_object[0]][1],self.pawn[self.selected_object[0]][2])

			self.selected_object = False

	def inverse(self):

		for i in self.pawn:
			if self.inversed == 1:
				y= self.len_board -1 - self.pawn[i][1]
				x= self.len_board -1 - self.pawn[i][2]
			else:
				y= self.pawn[i][1]
				x= self.pawn[i][2]
			self.coords(i, self.rapport*x+5, self.rapport*y+5, self.rapport*x+self.rapport-5, self.rapport*y+self.rapport-5)
		self.inversed *=-1

	def move(self, next):
		i,j =next
		k,l = j,i
		if self.inversed == -1:
			k = self.len_board -1 -k
			l = self.len_board -1 -l
		self.coords(self.selected_object, self.rapport*k+5, self.rapport*l+5, self.rapport*k+self.rapport-5, self.rapport*l+self.rapport-5)
		self.pawn[self.selected_object[0]][1] = i
		self.pawn[self.selected_object[0]][2] = j
		self.i, self.j = i, j

	def delete_pawn(self, i, j):
		if self.inversed == -1:
			i = self.len_board -1 -i
			j = self.len_board -1 -j
		pawn = self.find_closest(self.rapport*j+self.rapport//2,self.rapport*i+self.rapport//2)
		del self.pawn[pawn[0]]
		self.delete(pawn)

	def king(self, i, j):
		pawn = self.find_closest(self.rapport*j+self.rapport//2,self.rapport*i+self.rapport//2)
		self.itemconfig(pawn, width=5, outline="red")

class help_window(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title('Help')



fenetre = Interface()
fenetre.mainloop()
