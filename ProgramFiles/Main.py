import os
import random
import tkinter
from DictionaryTrie import Trie 
from CrossWord import CrossWord

def weightedRandomLetter():
	#These weightings are based on the below site
	#http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
	index = random.randrange(0,10000)
	if index < 1202:
		return 'e'
	elif index < 2112:
		return 't'
	elif index < 2924:
		return 'a'
	elif index < 3692:
		return 'o'
	elif index < 4423:
		return 'i'
	elif index < 5118:
		return 'n'
	elif index < 5746:
		return 's'
	elif index < 6348:
		return 'r'
	elif index < 6940:
		return 'h'
	elif index < 7372:
		return 'd'
	elif index < 7770:
		return 'l'
	elif index < 8058:
		return 'u'
	elif index < 8329:
		return 'c'
	elif index < 8590:
		return 'm'
	elif index < 8820:
		return 'f'
	elif index < 9031:
		return 'y'
	elif index < 9240:
		return 'w'
	elif index < 9443:
		return 'g'
	elif index < 9625:
		return 'p'
	elif index < 9774:
		return 'b'
	elif index < 9885:
		return 'v'
	elif index < 9954:
		return 'k'
	elif index < 9971:
		return 'x'
	elif index < 9982:
		return 'q'
	elif index < 9992:
		return 'j'
	else:
		return 'z'

def populateTrie(MainTrie):
	#Use a relative path to retrieve our dictionary
	CWD = os.getcwd()
	assetPath = os.path.relpath('..\\Assets\\engmix.txt', CWD)
	file = open(assetPath,"r",errors='ignore')

	#Setup the Trie as well as a dictionary of lower case letters
	letterInAlphabet = 'abcdefghijklmnopqrstuvwxyz'
	Alphabet = {}
	for letter in letterInAlphabet:
		Alphabet[letter] = True

	for letter in letterInAlphabet:
		MainTrie.insertLetter(letter)

	#For each word in the file insert it into the trie if it only consists of letters
	for word in file:
		flag = False
		for letter in word.lower().strip():
			if letter not in Alphabet:
				flag = True
				break
		if flag:
			continue

		MainTrie.insert(word.lower().strip())

	return MainTrie

def setUpTrie():
	#Setup up our Trie and populate it with the contents of the dictionary
	MainTrie = Trie("")

	populateTrie(MainTrie)

	return MainTrie


#Initialize Variables
MainTrie = setUpTrie()
ready = False
crossWordSize = 10 # This represents the size of the N*N crossword
numberOfWords = 4 # This represents the number of words to put in the crossword
minWordSize = 3  #Minimum word length
maxWordSize = 8 #Maximum word length
#Until we get a valid crossword continue to attempt to create one
while not ready:

	#Randomly generate letters based on the frequency with which they appear in english words
	letters = []
	for i in range(6):
		letters.append(weightedRandomLetter())

	wordList = {}
	#Get all words that contain the randomly generated letters
	MainTrie.getAllConstrainedWords(minWordSize,maxWordSize,letters,wordList)
	lengthSortedWordList = sorted(list(wordList.keys()),key = len)
	crossWord = CrossWord(crossWordSize,lengthSortedWordList,letters,numberOfWords)
	ready = crossWord.makeCrossWord()
#At this point we have a completed crossword
#We have letters and a list of words
#GUI
def makeGuess(event):
	#Checks the guess, updates GUI
	guess = entryObj.get()
	if guess in crossWord.usedWords:
		crossWord.reveal(guess)
		del crossWord.usedWords[guess]
	if not crossWord.usedWords:
		crossWord.displayCrossWordTKinter(DisplayWindow,letters)
		crossWord.displayWinScreen(DisplayWindow)
		return
	entryObj.delete(0, 'end')
	crossWord.displayCrossWordTKinter(DisplayWindow,letters)

def exit():
	#Destroys display window
	DisplayWindow.destroy()

def Reveal():
	#Reveals all words and provides a quit button
	tkinter.Button(DisplayWindow, text="  Quit  ", command=exit).grid(row = 0, column = 0, columnspan = crossWordSize)
	for word in crossWord.usedWords:
		crossWord.reveal(word)
	crossWord.displayCrossWordTKinter(DisplayWindow,letters)

#Initialize tkinter GUI
DisplayWindow = tkinter.Tk()
tkinter.Button(DisplayWindow, text="Reveal", command=Reveal).grid(row = 0, column = 0, columnspan = crossWordSize)
entryObj = crossWord.initCrossWordTKinter(DisplayWindow,letters)
#Binds the enter key to the makeGuess function
DisplayWindow.bind('<Return>', makeGuess)
#Start the GUI
DisplayWindow.mainloop()

