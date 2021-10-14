import string

class Auxiliary_Functions():
	"""docstring for Auxiliary_Functions"""
	def __init__(self):


	# Funcao que verifica se um símbolo terminal pertence ao conjunto primeiro de um nao-terminal da linguagem.
	def First(self, non_terminal, token, sigla):
		if(non_terminal == "vector_matrix"):
			if(token == '['):
				return True
			else:
				return False
		elif(non_terminal == "value"):
			if(sigla == "NRO" or token == "verdadeiro" or token == "falso" or sigla == "CAD" or sigla == "CAR"):
				return True
			else:
				return False
		elif(non_terminal == "declaration_var1"):
			if(token == "}" or token == "inteiro" or token == "real" or token == "booleano" or token == "char" or token == "cadeia" or token == "vazio" or sigla == "IDE"):
				return True
			else:
				return False
		elif(non_terminal == "declaration_var2"):
			if(non_terminal ==)
		elif(non_terminal == "declaration_var3"):
			if(token == ',' or token == ';'):
				return True
			else:
				return False


	def __First_