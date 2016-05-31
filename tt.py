# tic tac toe game

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Board:
	# some const values
	x = 'x'
	o = 'o'
	b = '-'

	# set up of the board
	def __init__(self):
		b = self.b
		self.board = [[b,b,b],[b,b,b],[b,b,b]]
		self.history = []

	# how to place a peice and keep track of all relevant moves
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

	# check if a spot is available
	def available(self,p):
		return self.board[p[0]][p[1]] == self.b
	
	# check if piece has won
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
	
	# check if it was a cats game
	def catsGame(self):
		return len(self.history) == 9

	# check the columns for winners
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
	
	# check the horizontals for winners
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
			
	# check the diagonal for winnes	
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

	# make the board look pretty
	def show(self):
		for i in self.board:
			for j in i:
				print(j,end=" ")
			print()

	# lets play!
	def play(self,ai,startHuman = True):
		self.humanTurn = (not startHuman)*1
		players = [self.x,self.o]
		turn = 0
		opponent = 1
		while not self.checkForWinner(players[(turn+1)%2]):
			os.system('clear')
			self.show()
			goodMove = False
			counter = 0
			while not goodMove:
				if turn == self.humanTurn:
					if counter > 0:
						print("You can NOT play there. Please try another location")
					print("Human Turn")
					counter = counter +1 
					row = int(float(input("Which Row number will you play on? ")))-1
					col = int(float(input("Which Column number will you play on? ")))-1
				else:
					print("Computer Turn")
					move =  ai.getMove(self,players[turn],players[opponent])
					row = move[0]
					col = move[1]
				goodMove = self.placePiece(row,col,players[turn])
			opponent = turn
			turn = (turn+1)%2
			print('\n')
		self.show()


	# copy the board by value
	def copyBoard(self):
		newBoard = [i[:] for i in self.board ]
		return newBoard



class AI:
	# a simple minded individual
	def __init__(self):
		self.center = [1,1]
		self.corners = [(2,0),(0,2),(0,0),(2,2)]
		self.edges = [(1,0),(0,1),(2,1),(1,2)]
		self.verbose = True
	def getMove(self,argBoard,piece,opponent):
		# return the move in a list [row,column]
		turnNum = len(argBoard.history)
		board = Board() # copy of the board to test with
		t = argBoard.copyBoard() 
		board.board = t
		if argBoard.available(self.center): # take the center if available
			return self.center
		if self.verbose:
			print("No center Available")

		for i in range(0,9): # get a win if available 
			r = i//3
			c = i%3
			if board.placePiece(r,c,piece):
				if board.checkForWinner(piece):
					return [r,c]
				board.placePiece(r,c,Board.b)
		if self.verbose:
			print("No option to win")

		for i in range(0,9): # block a win if available
			r = i//3
			c = i%3
			if board.placePiece(r,c,opponent):
				if board.checkForWinner(opponent):
					return [r,c]
				board.placePiece(r,c,Board.b)
		if self.verbose:
			print("No option to block")

		if turnNum <= 2:
			for i in self.corners: # take a corner otherwise
				if argBoard.available(i):
					return i
		if self.verbose:
			print("turns above 2, checking edges")

		for i in self.edges: # take an edge otherwise
			if argBoard.available(i):
				return i
		if self.verbose:
			print("no edge available")

		for i in self.corners: # take a corner otherwis
			if argBoard.available(i):
				return i

class WebInter:
	# used for xpathing to spots on the page
	names = ["square top left", "square top", "square top right",
		"square left", "square", "square right", 
		"square bottom left", "square bottom", "square bottom right"]
	# used to initiate the interface
	def __init__(self,driver):
		self.driver = driver
		self.prevBoard = None
		self.verbose = True
	# used to check if a piece is at a certain position
	def checkValue(self,postiion,piece):
		if piece == Board.x:
			pattern = "//*/div[@class='"+WebInter.names[postiion]+"']/div[@class='x']"
		elif piece ==Board.o:
			pattern = "//*/div[@class='"+WebInter.names[postiion]+"']/div[@class='o']"
		try:
			elem = self.driver.find_element_by_xpath(pattern)
			return True
		except:
			return False
	# used click on an element. It will wait a little after the click
	def click(self,postiion):
		pattern = "//*/div[@class='"+WebInter.names[postiion]+"']"
		elem = self.driver.find_element_by_xpath(pattern)
		print("Clicking...")
		elem.click()
		self.wait()
		print("...Done")
	# used to wait 
	def wait(self):
		time.sleep(.75)
	# used to send the board into something recognizable for our ai
	def makeBoard(self):
		board = Board()
		for i in range(0,9):
			r = i//3
			c = i%3 
			if self.checkValue(i,Board.x):
				board.board[r][c] = Board.x
			if self.checkValue(i,Board.o):
				board.board[r][c] = Board.o
		if self.verbose:
			print("displaying board...")
			board.show()
		return board
	# used to restart the game
	def restart(self):
		# wait a little before clicking
		self.wait()
		pattern = "//*/div[@class='restart']"
		elem = self.driver.find_element_by_xpath(pattern)
		elem.click()




x = Board.x
o = Board.o
blank = Board.b

# b =  Board()
# ai = AI()
# b.play(ai)


# a function to pit an online comp player against this one
def siliwars():
	# go to the website
	driver = webdriver.Firefox()
	driver.get("http://playtictactoe.org/")
	# set up the interface
	w = WebInter(driver)
	# initiate our player
	ai = AI()
	# get the board state from the web
	board = w.makeBoard()
	# set up the number of times to play
	i = 0
	limit = 10
	# keep re-playing till the end of the limits
	while i < limit and not (board.checkForWinner(Board.x) or board.checkForWinner(Board.o)):
		# get the move from the our player
		m = ai.getMove(board, Board.x, Board.o )
		try:
			# try inputing to the website
			# the assumption is that our ai has properly read the board and will
			# give a valid response move
			p = m[0]*3+m[1]
			w.click(p)
		except:
			# if it is not the case the above is true then we must be at the 
			# end of the game. So we restart and count 
			w.restart()
			i = i + 1
		# get the board state after we have moved and give time for the other to move
		board = w.makeBoard()

	# let the user know that we are about to close out the browser
	print("Closing Browser in...")
	t = 5
	for i in range(0,t):
		time.sleep(1)
		print(t-i," Seconds")
	# close the browsers
	driver.close()

# pit the ai against the website
siliwars()

