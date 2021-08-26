import string

class Auxiliary_functions:
	"""docstring for auxiliary_functions"""
	def __init__(self):
		pass

	def isLetter(self, character):
		letter = "abcdefghijlmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"
		if character in letter:
			return True
		return False

	def isDigit (self, character):
		digit = '0123456789'
		if character in digit:
			return True
		return False

	def isDelimiter(self, character):
		delimiter = ";,(){}[]"
		if character in delimiter:
			return True
		elif(ord(character) == 32 or ord(character) == 9): # " " ou \t
			return True
		else:
			return False

	def isOperatorRelational(self, character):
		operators = "!=><"
		if character in operators:
			return True
		else:
			return False

	def isLogicalOperators(self, character):
		operators = "!&|"
		if character in operators:
			return True
		else:
			return False

	def isArithmeticOperators(self, character):
		operators = "+-*/"
		if character in operators:
			return True
		else:
			return False
