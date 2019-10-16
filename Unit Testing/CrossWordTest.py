import unittest
import os
import sys
cwd = os.getcwd()
sys.path.append(cwd + '/../ProgramFiles/')
from CrossWord import CrossWord

class validLetterPos(unittest.TestCase):
	maxDiff = None
	def setUp(self):
		self.CrossWord = CrossWord(5,[],[],5)

	def testpositionContainsLetter(self):
		self.CrossWord.crosswordGrid = [['a','b',0,0,0],[0,0,0,0,0],[0,'c',0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
		#self.CrossWord.displayCrossWord()
		self.assertEqual(self.CrossWord.positionContainsLetter(0,0),1)
		self.assertEqual(self.CrossWord.positionContainsLetter(10,0),0)
		self.assertEqual(self.CrossWord.positionContainsLetter(0,1),1)
		self.assertEqual(self.CrossWord.positionContainsLetter(3,3),0)

	def testCornerCaseCheck(self):
		self.CrossWord.crosswordGrid = [['a','b',0,0,0],['c',0,0,0,0],[0,'d','e','f',0],[0,0,'g',0,0],[0,0,'h',0,0]]
		self.assertEqual(self.CrossWord.cornerCaseCheck(0,0,1,1),False)
		self.assertEqual(self.CrossWord.cornerCaseCheck(0,0,-1,-1),True)
		self.assertEqual(self.CrossWord.cornerCaseCheck(2,2,3,3),False)
		self.assertEqual(self.CrossWord.cornerCaseCheck(2,2,1,1),True)
		self.assertEqual(self.CrossWord.cornerCaseCheck(2,2,1,3),True)
		self.assertEqual(self.CrossWord.cornerCaseCheck(2,2,3,1),False)
		self.assertEqual(self.CrossWord.cornerCaseCheck(4,4,5,5),True)
		self.assertEqual(self.CrossWord.cornerCaseCheck(4,4,3,3),True)

	def testisNotCornerCase(self):
		self.CrossWord.crosswordGrid = [['a','b',0,0,0],['c',0,0,0,0],[0,'d','e','f',0],[0,0,'g',0,0],[0,0,'h',0,0]]
		self.assertEqual(self.CrossWord.isNotCornerCase(0,0),False)
		self.assertEqual(self.CrossWord.isNotCornerCase(0,1),True)
		self.assertEqual(self.CrossWord.isNotCornerCase(1,1),False)
		self.assertEqual(self.CrossWord.isNotCornerCase(2,2),False)
		self.assertEqual(self.CrossWord.isNotCornerCase(4,4),True)
		self.assertEqual(self.CrossWord.isNotCornerCase(5,5),True)

	def testisValidWordPosition(self):
		self.CrossWord.crosswordGrid = [[0, 0, 0, 0, 't', 0, 0, 0, 'a', 0, 0, 0, 0], [0, 0, 0, 0, 'h', 0, 0, 0, 'r', 'a', 'i', 'l', 's'], [0, 0, 0, 0, 'e', 0, 0, 0, 'e', 0, 0, 0, 0], ['d', 'i', 's', 'm', 'a', 'y', 0, 'g', 'a', 'r', 'y', 0, 0], [0, 0, 0, 0, 't', 0, 0, 'a', 0, 0, 0, 0, 0], [0, 'd', 'o', 'o', 'r', 0, 0, 'l', 0, 0, 0, 0, 0], [0, 0, 0, 0, 'e', 'a', 'g', 'l', 'e', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 'r', 'a', 'n', 'g', 'e', 0]]
		#[[0, 0, 0, 0, t, 0, 0, 0, a, 0, 0, 0, 0],
		# [0, 0, 0, 0, h, 0, 0, 0, r, a, i, l, s],
		# [0, 0, 0, 0, e, 0, 0, 0, e, 0, 0, 0, 0],
		# [d, i, s, m, a, y, 0, g, a, r, y, 0, 0],
		# [0, 0, 0, 0, t, 0, 0, a, 0, 0, 0, 0, 0],
		# [0, d, o, o, r, 0, 0, l, 0, 0, 0, 0, 0],
		# [0, 0, 0, 0, e, a, g, l, e, 0, 0, 0, 0],
		# [0, 0, 0, 0, 0, 0, o, 0, 0, 0, 0, 0, 0],
		# [0, 0, 0, 0, 0, 0, o, r, a, n, g, e, 0]]
		#self.CrossWord.displayCrossWord()
		self.assertEqual(self.CrossWord.isValidWordPosition(3,0),True)
		self.assertEqual(self.CrossWord.isValidWordPosition(3,4),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(3,5),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(5,5),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(5,6),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(6,6),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(6,7),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(3,7),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(3,8),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(3,9),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(2,8),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(1,8),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(0,4),True)
		self.assertEqual(self.CrossWord.isValidWordPosition(8,6),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(8,7),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(8,11),True)
		self.assertEqual(self.CrossWord.isValidWordPosition(8,-1),False)
		self.assertEqual(self.CrossWord.isValidWordPosition(0,0),False)

	def testinsertWord(self):
		self.CrossWord.crosswordGrid = [[0, 0, 0, 0, 't', 0, 0, 0, 'a', 0, 0, 0, 0], [0, 0, 0, 0, 'h', 0, 0, 0, 'r', 'a', 'i', 'l', 's'], [0, 0, 0, 0, 'e', 0, 0, 0, 'e', 0, 0, 0, 0], ['d', 'i', 's', 'm', 'a', 'y', 0, 'g', 'a', 'r', 'y', 0, 0], [0, 0, 0, 0, 't', 0, 0, 'a', 0, 0, 0, 0, 0], [0, 'd', 'o', 'o', 'r', 0, 0, 'l', 0, 0, 0, 0, 0], [0, 0, 0, 0, 'e', 'a', 'g', 'l', 'e', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 'r', 'a', 'n', 'g', 'e', 0]]
		#[[0, 0, 0, 0, t, 0, 0, 0, a, 0, 0, 0, 0],
		# [0, 0, 0, 0, h, 0, 0, 0, r, a, i, l, s],
		# [0, 0, 0, 0, e, 0, 0, 0, e, 0, 0, 0, 0],
		# [d, i, s, m, a, y, 0, g, a, r, y, 0, 0],
		# [0, 0, 0, 0, t, 0, 0, a, 0, 0, 0, 0, 0],
		# [0, d, o, o, r, 0, 0, l, 0, 0, 0, 0, 0],
		# [0, 0, 0, 0, e, a, g, l, e, 0, 0, 0, 0],
		# [0, 0, 0, 0, 0, 0, o, 0, 0, 0, 0, 0, 0],
		# [0, 0, 0, 0, 0, 0, o, r, a, n, g, e, 0]]
		#self.assertEqual(self.CrossWord.isValidLetterPosition(2,1),True)
		#Testing Multiple possibilities for insertion
		self.CrossWord.insertWord(3,1,'wiki')
		self.CrossWord.displayCrossWord()
		correctAnswer = [[0, 'w', 0, 0, 't', 0, 0, 0, 'a', 0, 0, 0, 0], [0, 'i', 0, 0, 'h', 0, 0, 0, 'r', 'a', 'i', 'l', 's'], [0, 'k', 0, 0, 'e', 0, 0, 0, 'e', 0, 0, 0, 0], ['d', 'i', 's', 'm', 'a', 'y', 0, 'g', 'a', 'r', 'y', 0, 0], [0, 0, 0, 0, 't', 0, 0, 'a', 0, 0, 0, 0, 0], [0, 'd', 'o', 'o', 'r', 0, 0, 'l', 0, 0, 0, 0, 0], [0, 0, 0, 0, 'e', 'a', 'g', 'l', 'e', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 'r', 'a', 'n', 'g', 'e', 0]]
		self.assertEqual(self.CrossWord.crosswordGrid,correctAnswer)
		#Testing not enough room
		self.CrossWord.crosswordGrid = [[0, 0, 0, 0, 't', 0, 0, 0, 'a', 0, 0, 0, 0], [0, 0, 0, 0, 'h', 0, 0, 0, 'r', 'a', 'i', 'l', 's'], [0, 0, 0, 0, 'e', 0, 0, 0, 'e', 0, 0, 0, 0], ['d', 'i', 's', 'm', 'a', 'y', 0, 'g', 'a', 'r', 'y', 0, 0], [0, 0, 0, 0, 't', 0, 0, 'a', 0, 0, 0, 0, 0], [0, 'd', 'o', 'o', 'r', 0, 0, 'l', 0, 0, 0, 0, 0], [0, 0, 0, 0, 'e', 'a', 'g', 'l', 'e', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 'r', 'a', 'n', 'g', 'e', 0]]
		self.CrossWord.insertWord(1,10,'wiki')
		correctAnswer = [[0, 0, 0, 0, 't', 0, 0, 0, 'a', 0, 0, 0, 0], [0, 0, 0, 0, 'h', 0, 0, 0, 'r', 'a', 'i', 'l', 's'], [0, 0, 0, 0, 'e', 0, 0, 0, 'e', 0, 0, 0, 0], ['d', 'i', 's', 'm', 'a', 'y', 0, 'g', 'a', 'r', 'y', 0, 0], [0, 0, 0, 0, 't', 0, 0, 'a', 0, 0, 0, 0, 0], [0, 'd', 'o', 'o', 'r', 0, 0, 'l', 0, 0, 0, 0, 0], [0, 0, 0, 0, 'e', 'a', 'g', 'l', 'e', 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 'o', 'r', 'a', 'n', 'g', 'e', 0]]
		self.assertEqual(self.CrossWord.crosswordGrid,correctAnswer)

		self.CrossWord.crosswordGrid = [[0, 0, 'b', 0, 0], [0, 0, 'a', 0, 0], [0, 0, 'r', 'a', 't'], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
		self.CrossWord.insertWord(2,2,'car')
		correctAnswer = [[0, 0, 'b', 0, 0], [0, 0, 'a', 0, 0], [0, 0, 'r', 'a', 't'], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
		self.assertEqual(self.CrossWord.crosswordGrid,correctAnswer)

unittest.main()