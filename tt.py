# tic tac toe game

class Board:
	x = 'x'
	o = 'o'
	b = '-'
	def __init__(self,startHuman = True):
		b = self.b
		self.board = [[b,b,b],[b,b,b],[b,b,b]]
		self.humanTurn = (not startHuman)*1
		self.history = []

	
	def placePiece(self, r, c, piece):
		if not self.available([r,c]):
			if piece != self.b:
				return False
		self.board[r][c] = piece
		if piece!= self.b:
			self.history.append((r,c,piece))
		else:
			self.history = self.history[:len(self.history)-1]
		return True

	def available(self,p):
		return self.board[p[0]][p[1]] == self.b
	
	def checkForWinner(self, piece):
		if piece ==  self.b:
			print("Invalid query")
			return False
		if self.checkV(piece) or self.checkH(piece) or self.checkD(piece):
			print("player "+piece+" WINS")
			return 2
		if self.catsGame():
			print("CATS games")
			return 1
	
	def checkV(self,piece):
		for i in range(0,3):
			winner = True
			for j in range(0,3):
				if self.board[j][i] != piece:
					winner = False
					break
			if winner:
				return winner
		return winner
	
	def checkH(self,piece):
		for i in range(0,3):
			winner = True
			for j in range(0,3):
				if self.board[i][j] != piece:
					winner = False
					break
			if winner:
				return winner
		return winner
				
	def checkD(self,piece):
		winner = True
		for i in range(0,3):
			if self.board[i][i] != piece:
				winner = False
				break
		if winner:
			return winner
		winner =  True
		for i in range(0,3):
			if self.board[2-i][i] != piece:
				winner = False
				break
		return winner

	def show(self):
		for i in self.board:
			for j in i:
				print(j,end=" ")
			print()

	def play(self,ai):
		players = [self.x,self.o]
		turn = 0
		opponent = 1
		while not self.checkForWinner(players[turn]):
			self.show()
			goodMove = False
			while not goodMove:
				if turn == self.humanTurn:
					print("Human Turn")
					row = input("Which Row number will you play on? ")-1
					col = input("Which Column number will you play on? ")-1
				else:
					print("Computer Turn")
					move =  ai.getMove(self,players[turn],opponent)
					row = move[0]
					col = move[1]
				goodMove = self.placePiece(row,col,players[turn])
			opponent = turn
			turn = (turn+1)%2


	def copyBoard(self):
		newBoard = [i[:] for i in self.board ]
		return newBoard

class AI:
	def __init__(self):
		self.optimal = [1,1]
		self.cornera = [[0,0],[2,2],[]

	def getMove(self,argBoard,piece,opponent):
		block = [] # block the win of opponent on next move
		setup = [] # set yourself up for atrapping the opponent
		blockSetup = [] # blockThem from trapping you
		regular = [] # make them have to block you
		regulatBlock = [] # block the ahead of time

		numMoves = len(argBoard.history) # how many turns have be taken so far
		tmp = argBoard.copyBoard() # a copy of the board 
		board = Board() # a new instance
		board.board=tmp # push the copy  to the new instance 
		# play in the center if available
		if board.available(self.optimal):
			return self.optimal

		# short range thinking
		for  i in range(0,10):
			r = i//3
			c = i%3
			# check if the spot is available 
			if board.placePiece(r,c,piece):
				# if we win by playing on that spot, play there!
				if board.checkForWinner(piece):
					return [r,c]
				wtw = self.waysToWin(board,piece)
				# okay so we played there, was that the finish of a trap?
				# yes, okay lets consider playing there
				if wtw>1:
					setup.append(i)
				# okay so we played there,  could we win next turn if they mess up?
				# yes, okay lets consider playing there
				if wtw == 1:
					regular.append(i)


				for j in range(0,10):
					oppR  = j//3
					oppC =  j%3
					if board.placePiece(oppR,oppC,opponent):	
						if board.checkForWinner(opponent) == 2:
							block.append(j)
						else:
							wtw = self.waysToWin(board,opponent)
							if wtw > 1:
								blockSetup.append(j)
							if wtw == 1:
								regulatBlock.append(j)
							board.placePiece(r,c,Board.b)

		setupAndBlock = [i in setup for i in block]
		regularAndBlock =  [i in regular for i in block]
		lenBlock = len(block)

		if lenBlock > 0:
			if sum(setupAndBlock):
				i = 0
				while not setupAndBlock[i]:
					i = i + 1
				return [block[i]//3 , block[i]%3]
			if sum(regularAndBlock):
				i = 0
				while not regularAndBlock[i]:
					i = i + 1
				return [block[i]//3 , block[i]%3]

		setupAndSetup = []





	def waysToWin(self,board,piece):
		pos = [0]*9
		for  i in range(0,10):
			r = i//3
			c = i%3
			if board.placePiece(r,c,piece,opponent):
				if board.checkForWinner(piece):
					pos[i] = 1
				else:
					board.placePiece(r,c,Board.b)
		return sum(pos)





x = Board.x
o = Board.o
blank = Board.b