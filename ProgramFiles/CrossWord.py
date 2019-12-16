import random
import tkinter
class CrossWord:
	def __init__(self,dimensions,wordList,letters,wordCount):
		self.crosswordGrid = [[0 for i in range(dimensions)] for j in range(dimensions)]
		self.revealed      = [[False for i in range(dimensions)] for j in range(dimensions)]
		self.letterDict = {}#This dict is used to quickly choose a suitable word to put in the crossword
		self.usedWords  = {}#This keeps track of all words used so far
		self.wordList   = wordList#List of all possible words
		self.letters = letters
		self.remainingWords = wordCount#Number of words to put in the crossword
		for word in wordList[::-1]:
			for letter in word:
				if letter not in self.letterDict:
					self.letterDict[letter] = [word]
				else:
					self.letterDict[letter].append(word)

	def makeCrossWord(self):
		if len(self.wordList) < self.remainingWords:
			return False
		#Input is a list of words
		#Output is a crossword puzzle grid
		#Start building crossword from longest possible word
		startingWord = self.wordList[-1]
		#Randomly insert word into an available space on the board
		initialX = random.randrange(0,len(self.crosswordGrid) - len(startingWord))
		initialY = random.randrange(0,len(self.crosswordGrid) - len(startingWord))
		self.usedWords[startingWord] = [initialX,initialY,'v']
		for i in range(len(startingWord)):
			self.crosswordGrid[initialX + i][initialY] = startingWord[i]
		attempts = 0
		#Generate the crossword
		while(self.remainingWords > 0):
			attempts += 1
			if attempts > 1000:
				print("Generating New Letters")
				return False
			#Do a dfs from initial positions and return a valid position to insert a new word
			visited = {}
			posX,posY = self.dfs(initialX,initialY,visited)
			if posX == posY and posX == -1:
				continue
			#Attempt to insert possible words into the chosen place
			letter = self.crosswordGrid[posX][posY]
			possibleWords = self.letterDict[letter]
			for word in possibleWords:
				if word in self.usedWords:
					continue
				val = self.insertWord(posX,posY,word)
				if val == 1:
					self.remainingWords -= 1
					self.usedWords[word] = [posX,posY,'v']
					break
				elif val == 2:
					self.remainingWords -= 1
					self.usedWords[word] = [posX,posY,'h']
					break

		return True

	def insertWord(self,posX,posY,word):
		targetLetter = self.crosswordGrid[posX][posY]
		letterPositions = []
		for i in range(len(word)):
			if word[i] == targetLetter:
				letterPositions.append(i)

		#Okay, how do i tell if i should insert it vertically or horizontally?
		#Why not try both, one will work if possible
		for posLetter in letterPositions:

			if self.verticalCheck(posX,posY,posLetter,word):
				startPoint = posX - posLetter
				for i in range(startPoint, startPoint + len(word)):
					self.crosswordGrid[i][posY] = word[i - startPoint]
				return 1

			if self.horizontalCheck(posX,posY,posLetter,word):
				startPoint = posY - posLetter
				for i in range(startPoint, startPoint + len(word)):
					self.crosswordGrid[posX][i] = word[i - startPoint]
				return 2
		#could not insert this word at this position
		return 0

	def verticalCheck(self,posX,posY,posLetter,word):
		valid = True
		
		startPoint = posX - posLetter
		if startPoint < 0 or startPoint + len(word) > len(self.crosswordGrid):
			return False
		if startPoint - 1 >= 0 and self.crosswordGrid[startPoint-1][posY] != 0:
			return False
		if startPoint + len(word) < len(self.crosswordGrid) and self.crosswordGrid[startPoint + len(word)][posY] != 0:
			return False
		for i in range(startPoint, startPoint + len(word)):
			if not self.isValidVerticalLetterPosition(i,posY) and not word[i-startPoint] == self.crosswordGrid[i][posY]:
				valid = False
		return valid

	def horizontalCheck(self,posX,posY,posLetter,word):
		valid = True
		startPoint = posY - posLetter
		if startPoint < 0 or startPoint + len(word) > len(self.crosswordGrid[0]):
			return False
		if startPoint - 1 >= 0 and self.crosswordGrid[posX][startPoint-1] != 0:
			return False
		if startPoint + len(word) < len(self.crosswordGrid) and self.crosswordGrid[posX][startPoint + len(word)] != 0:
			return False
		
		for i in range(startPoint, startPoint + len(word)):
			if not self.isValidHorizontalLetterPosition(posX,i) and not word[i-startPoint] == self.crosswordGrid[posX][i]:
				valid = False
		return valid

	def dfs(self,X,Y,visited):
		#This function does a dfs from an initial position and looks for a valid position to place a new word
		#Visited contains the location we have been in order to stop backtracking
		visited[(X,Y)] = True
		if random.randrange(0,3) == 1 and self.isValidWordPosition(X,Y):
			return X,Y


		if self.positionContainsLetter(X+1,Y) and (X+1,Y) not in visited:
			posX,posY = self.dfs(X+1,Y,visited)
			if posX != -1:
				return posX,posY

		if self.positionContainsLetter(X-1,Y) and (X-1,Y) not in visited:
			posX,posY = self.dfs(X-1,Y,visited)
			if posX != -1:
				return posX,posY

		if self.positionContainsLetter(X,Y+1) and (X,Y+1) not in visited:
			posX,posY = self.dfs(X,Y+1,visited)
			if posX != -1:
				return posX,posY

		if self.positionContainsLetter(X,Y-1) and (X,Y-1) not in visited:
			posX,posY = self.dfs(X,Y-1,visited)
			if posX != -1:
				return posX,posY

		return -1,-1

	def isValidWordPosition(self,X,Y):
		#Returns whether or not the desired position can legally support a word
		if not (X >= 0 and X < len(self.crosswordGrid) or not (Y >= 0 and Y < len(self.crosswordGrid[0]))):
			return False
		if self.crosswordGrid[X][Y] == 0:
			return False

		adjacent = 0
		adjacent += self.positionContainsLetter(X-1,Y+1)
		adjacent += self.positionContainsLetter(X-1,Y-1)
		adjacent += self.positionContainsLetter(X-1,Y)
		adjacent += self.positionContainsLetter(X+1,Y)
		adjacent += self.positionContainsLetter(X+1,Y+1)
		adjacent += self.positionContainsLetter(X+1,Y-1)
		adjacent += self.positionContainsLetter(X,Y+1)
		adjacent += self.positionContainsLetter(X,Y-1)
		#Corner case here where two words are perpendicular and share an endpoint
		return adjacent <= 2 and self.isNotCornerCase(X,Y)

	def isValidHorizontalLetterPosition(self,X,Y):
		#Current Version Does not accept exiting letters in space
		#Checks to see if position is open as well as checks to see that it has no surronding letters in cardinal directions
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return False
		valid = True
		if self.crosswordGrid[X][Y] != 0:
			return False

		#Only need to check perpendicular values
		if X + 1 < len(self.crosswordGrid):
			valid = valid and not self.positionContainsLetter(X+1,Y)
		if X - 1 >= 0:
			valid = valid and not self.positionContainsLetter(X-1,Y)

		return valid

	def isValidVerticalLetterPosition(self,X,Y):
		#Current Version Does not accept exiting letters in space
		#Checks to see if position is open as well as checks to see that it has no surronding letters in cardinal directions
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return False
		valid = True
		if self.crosswordGrid[X][Y] != 0:
			return False

		#Only need to check perpendicular values
		if Y + 1 < len(self.crosswordGrid[0]):
			valid = valid and not self.positionContainsLetter(X,Y+1)
		if Y - 1 >= 0:
			valid = valid and not self.positionContainsLetter(X,Y-1)

		return valid
		

	def isNotCornerCase(self,X,Y):
		#This checks for a corner case when two words are perpendicular at a mutual endpoint
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return True
		#4 corner cases
		valid = True
		valid = valid and self.cornerCaseCheck(X-1,Y+1,X,Y)
		valid = valid and self.cornerCaseCheck(X-1,Y-1,X,Y)
		valid = valid and self.cornerCaseCheck(X+1,Y+1,X,Y)
		valid = valid and self.cornerCaseCheck(X+1,Y-1,X,Y)

		return valid

	def cornerCaseCheck(self,X,Y,ogX,ogY):
		#This function is given an X,Y that represents the direction diagonally that we are testing
		#If both the vertical and horizontal grids have a value in that direction return False
		#Else return True
		if ogX < 0 or ogX >= len(self.crosswordGrid) or ogY < 0 or ogY >= len(self.crosswordGrid[0]):
			return True
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return True
		if self.crosswordGrid[ogX][Y] != 0 and self.crosswordGrid[X][ogY] != 0:
			return False
		return True

	def positionContainsLetter(self,X,Y):
		if not (X >= 0 and X < len(self.crosswordGrid)) or not(Y >= 0 and Y < len(self.crosswordGrid[0])):
			return 0
		if self.crosswordGrid[X][Y] == 0:
			return 0
		return 1


	def displayCrossWordTKinter(self,DisplayWindow,letters):
		for row in range(len(self.crosswordGrid)):
			for col in range(len(self.crosswordGrid[0])):
				if self.crosswordGrid[row][col] != 0:
					if self.revealed[row][col] == False:
						tkinter.Label(DisplayWindow, text="",
			        	 borderwidth=2,relief = "solid" ,font = (16),width = 3).grid(row=row+1,column=col)
					else:
						tkinter.Label(DisplayWindow, text=self.crosswordGrid[row][col],
			        	 borderwidth=2,relief = "solid" ,font = (16),width = 3).grid(row=row+1,column=col)

		DisplayWindow.update()


	def initCrossWordTKinter(self,DisplayWindow,letters):
		for row in range(len(self.crosswordGrid)):
			for col in range(len(self.crosswordGrid[0])):
				if self.crosswordGrid[row][col] != 0:
					if self.revealed[row][col] == False:
						tkinter.Label(DisplayWindow, text="",
			        	 borderwidth=2,relief = "solid" ,font = (16),width = 3).grid(row=row + 1,column=col)
					else:
						tkinter.Label(DisplayWindow, text=self.crosswordGrid[row][col],
			        	 borderwidth=2,relief = "solid" ,font = (16),width = 3).grid(row=row + 1,column=col)

		tkinter.Label(DisplayWindow,text = "Available Letters:",font = (16)).grid(row = row + 2,columnspan = len(self.crosswordGrid))
		tkinter.Label(DisplayWindow,text = letters,font = (16)).grid(row = row + 3,columnspan = len(self.crosswordGrid))
		EntryObj = tkinter.Entry(DisplayWindow)
		EntryObj.grid(row= row + 4, columnspan = len(self.crosswordGrid))
		
		DisplayWindow.update()
		return EntryObj


	def displayWinScreen(self,DisplayWindow):
		#Updates the GUI with a label that says YOU WIN and displays it
		tkinter.Label(DisplayWindow, text="YOU WIN!!!",
			        	 borderwidth=2,relief = "solid" ,font = (26)).grid(row=0,column=0,columnspan = len(self.crosswordGrid) ,rowspan = len(self.crosswordGrid))
		tkinter.Button(DisplayWindow, text="Quit", command=Reveal).grid(row = len(self.crosswordGrid) + 4, column = len(self.crosswordGrid) + 4, columnspan = len(self.crosswordGrid))
		DisplayWindow.update()

	def reveal(self,guess):
		#Reveals the word in the crossword
		x = self.usedWords[guess][0]
		y = self.usedWords[guess][1]
		direction = self.usedWords[guess][2]
		index = 0
		if direction == 'v':
			while(x + index < len(self.crosswordGrid) and  self.crosswordGrid[x+index][y] != 0):
				self.revealed[x+index][y] = True
				index += 1
			index = 0
			while(x - index >= 0 and self.crosswordGrid[x-index][y] != 0):
				self.revealed[x-index][y] = True
				index += 1

		else:
			while(y+index < len(self.crosswordGrid[0]) and self.crosswordGrid[x][y + index] != 0):
				self.revealed[x][y+index] = True
				index += 1
			index = 0
			while(y - index >= 0 and self.crosswordGrid[x][y - index] != 0):
				self.revealed[x][y-index] = True
				index += 1
