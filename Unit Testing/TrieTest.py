import unittest
import os
import sys
cwd = os.getcwd()
sys.path.append(cwd + '/../ProgramFiles/')
from DictionaryTrie import Trie

class TrieTest(unittest.TestCase):
	def setUp(self):
		CWD = os.getcwd()
		assetPath = os.path.relpath('..\\Assets\\engmix.txt', CWD)
		file = open(assetPath,"r",errors='ignore')

		letterInAlphabet = 'abcdefghijklmnopqrstuvwxyz'
		Alphabet = {}
		for letter in letterInAlphabet:
			Alphabet[letter] = True

		self.MainTrie = Trie("")

		for letter in letterInAlphabet:
			self.MainTrie.insertLetter(letter)


		for word in file:
			flag = False
			for letter in word.lower().strip():
				if letter not in Alphabet:
					flag = True
					break
			if flag:
				continue

			self.MainTrie.insert(word.lower().strip())

		file.close()

	def testWordExistence(self):
		#This test case is to test whether or not various words exist in the Trie
		self.assertEqual(self.MainTrie.containsWord('word'),True)
		self.assertEqual(self.MainTrie.containsWord('Word'),False)
		self.assertEqual(self.MainTrie.containsWord('123'),False)
		self.assertEqual(self.MainTrie.containsWord('deface'),True)
		self.assertEqual(self.MainTrie.containsWord(''),False)

	def testTrieInsert(self):
		self.assertEqual(self.MainTrie.containsWord('abcdefg'),False)
		self.assertEqual(self.MainTrie.insert('abcdefg'),True)
		self.assertEqual(self.MainTrie.containsWord('abcdefg'),True)
		#Test to confirm that we can use abnormal characters
		self.assertEqual(self.MainTrie.containsWord('Abc12defg!'),False)
		self.assertEqual(self.MainTrie.insert('Abc12defg!'),True)
		self.assertEqual(self.MainTrie.containsWord('Abc12defg!'),True)
		#Test empty input
		self.assertEqual(self.MainTrie.containsWord(''),False)
		self.assertEqual(self.MainTrie.insert(''),True)
		self.assertEqual(self.MainTrie.containsWord(''),True)


	def testGetRandomWord(self):
		for i in range(2,10):
			self.assertEqual(len(self.MainTrie.getRandomWord(i)[0]),i)
			word = self.MainTrie.getRandomWord(i)[0]
			self.assertEqual(self.MainTrie.containsWord(word),True)
		self.assertEqual(len(self.MainTrie.getRandomWord(25)[0]),0)
		word = self.MainTrie.getRandomWord(25)[0]
		self.assertEqual(self.MainTrie.containsWord(word),False)

	def testGetRandomWordFromLetters(self):
		letters = ['a','o','l','e','k','c','p']
		word = self.MainTrie.getRandomConstrainedWord(4,letters)[0]
		self.assertEqual(len(word),4)
		self.assertEqual(self.MainTrie.containsWord(word),True)

unittest.main()