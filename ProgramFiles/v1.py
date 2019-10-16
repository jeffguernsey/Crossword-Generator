import random
class CrossWord:
	def __init__(self,dimensions,wordList,letters,wordCount):
		self.crosswordGrid = [[0 for i in range(dimensions)] for j in range(dimensions)]
		self.letterDict = {}
		self.usedWords  = {}
		self.wordList   = wordList
		self.letters = letters
		self.remainingWords = wordCount
		for word in wordList:
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
		self.usedWords[startingWord] = True
		#Randomly insert word into an available space on the board
		initialX = random.randrange(0,15 - len(startingWord))
		initialY = random.randrange(0,15 - len(startingWord))
		for i in range(len(startingWord)):
			self.crosswordGrid[initialX + i][initialY] = startingWord[i]
		attempts = 0
		#Okay, lets start by doing a depth first search of my
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

			letter = self.crosswordGrid[posX][posY]
			possibleWords = self.letterDict[letter]
			random.shuffle(possibleWords)
			for word in possibleWords:
				if word in self.usedWords:
					continue
				if self.insertWord(posX,posY,word):
					self.remainingWords -= 1
					self.usedWords[word] = True
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
				return True

			if self.horizontalCheck(posX,posY,posLetter,word):
				startPoint = posY - posLetter
				for i in range(startPoint, startPoint + len(word)):
					self.crosswordGrid[posX][i] = word[i - startPoint]
				return True
		#could not insert this word at this position
		return False

	def verticalCheck(self,posX,posY,posLetter,word):
		valid = True
		
		startPoint = posX - posLetter
		if startPoint < 0 or startPoint + len(word) - 1 > len(self.crosswordGrid):
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
		if startPoint < 0 or startPoint + len(word) - 1 > len(self.crosswordGrid[0]):
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
		visited[(X,Y)] = True
		if random.randrange(0,3) == 1 and self.isValidWordPosition(X,Y):
			return X,Y


		if self.checkPoint(X+1,Y) and (X+1,Y) not in visited:
			posX,posY = self.dfs(X+1,Y,visited)
			if posX != -1:
				return posX,posY

		if self.checkPoint(X-1,Y) and (X-1,Y) not in visited:
			posX,posY = self.dfs(X-1,Y,visited)
			if posX != -1:
				return posX,posY

		if self.checkPoint(X,Y+1) and (X,Y+1) not in visited:
			posX,posY = self.dfs(X,Y+1,visited)
			if posX != -1:
				return posX,posY

		if self.checkPoint(X,Y-1) and (X,Y-1) not in visited:
			posX,posY = self.dfs(X,Y-1,visited)
			if posX != -1:
				return posX,posY

		return -1,-1

	def isValidWordPosition(self,X,Y):
		#Their are 6 valid positions
		if not (X >= 0 and X < len(self.crosswordGrid) or not (Y >= 0 and Y < len(self.crosswordGrid[0]))):
			return False
		if self.crosswordGrid[X][Y] == 0:
			return False

		adjacent = 0
		adjacent += self.checkPoint(X-1,Y+1)
		adjacent += self.checkPoint(X-1,Y-1)
		adjacent += self.checkPoint(X-1,Y)
		adjacent += self.checkPoint(X+1,Y)
		adjacent += self.checkPoint(X+1,Y+1)
		adjacent += self.checkPoint(X+1,Y-1)
		adjacent += self.checkPoint(X,Y+1)
		adjacent += self.checkPoint(X,Y-1)
		#This had a bug in it, what happens if the start of two words share a letter?
		#That position is invalid
		return adjacent <= 2 and self.isNotCornerCase(X,Y)

	def isValidHorizontalLetterPosition(self,X,Y):
		#Current Version Does not accept exiting letters in space
		#Checks to see if position is open as well as checks to see that it has no surronding letters in cardinal directions
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return False
		valid = True
		if self.crosswordGrid[X][Y] != 0:
			return False

		if X + 1 < len(self.crosswordGrid):
			valid = valid and not self.checkPoint(X+1,Y)
		if X - 1 >= 0:
			valid = valid and not self.checkPoint(X-1,Y)

		return valid

	def isValidVerticalLetterPosition(self,X,Y):
		#Current Version Does not accept exiting letters in space
		#Checks to see if position is open as well as checks to see that it has no surronding letters in cardinal directions
		if X < 0 or X >= len(self.crosswordGrid) or Y < 0 or Y >= len(self.crosswordGrid[0]):
			return False
		valid = True
		if self.crosswordGrid[X][Y] != 0:
			return False

		if Y + 1 < len(self.crosswordGrid[0]):
			valid = valid and not self.checkPoint(X,Y+1)
		if Y - 1 >= 0:
			valid = valid and not self.checkPoint(X,Y-1)

		return valid
		

	def isNotCornerCase(self,X,Y):
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

	def checkPoint(self,X,Y):
		if not (X >= 0 and X < len(self.crosswordGrid)) or not(Y >= 0 and Y < len(self.crosswordGrid[0])):
			return 0
		if self.crosswordGrid[X][Y] == 0:
			return 0
		return 1

	def displayCrossWord(self):
		print("")
		for row in self.crosswordGrid:
			for letter in row:
				if letter == 0:
					print("   ",end = "")
				else:
					print(" " + str(letter) + " ",end = "")
			print("")