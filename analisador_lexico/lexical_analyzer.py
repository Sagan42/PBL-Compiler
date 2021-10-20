from auxiliary_functions import Auxiliary_functions

class Lexical_analyzer:
	"""Classe responsável por analisador uma cadeia de caracteres com o intuito de identificar estruturas léxicas de uma linguagem."""
	def __init__(self):
		self.__lexema    = ""
		self.__key_words = {"algoritmo": "", "variaveis": "", "constantes": "", "registro": "", "funcao": "", "retorno": "", "vazio": "", "se": "", "senao": "",
			"enquanto": "", "para": "", "leia": "", "escreva": "", "inteiro": "", "real": "", "booleano": "", "char": "", "cadeia": "", "verdadeiro": "", "falso": ""}
		self.__functions = Auxiliary_functions()
	
	def auto_keywords_identifier(self, line, initial):
		state         = 1
		self.__lexema = ""
		index = initial
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				if(self.__functions.isLetter(c)):
					index += 1
					self.__lexema+= c
					state = 2
			elif(state == 2):
				if(self.__functions.isLetter(c) == True or self.__functions.isDigit(c) == True or c == '_'):
					index += 1
					self.__lexema+= c
					state = 2
				elif(self.__functions.isDelimiter(c)):
					if(self.__key_words.get(self.__lexema) != None):
						return ["PRE", self.__lexema, index]
					else:
						return ["IDE", self.__lexema, index]
				elif(self.__functions.isOperatorRelational(c) == True or self.__functions.isArithmeticOperators(c) == True or self.__functions.isLogicalOperators(c) == True):
					return self.auto_erro_operator(line,index)
				else:
					if(self.__key_words.get(self.__lexema) != None):
						return ["PRE", self.__lexema, index]
					else:
						return ["IDE", self.__lexema, index]
		else:
			if(self.__key_words.get(self.__lexema) != None):
				return ["PRE", self.__lexema, index]
			else:
				return ["IDE", self.__lexema, index]

	def auto_erro_operator(self,line, index):
		while(index < len(line)):
			c = line[index]
			if(self.__functions.isDelimiter(c)):
				return ["OpMF", self.__lexema, index]
			else:
				self.__lexema += c
				index += 1
		else:
			return ["OpMF", self.__lexema, index]  # Acabou a linha e não encontrou um delimitador


	def auto_erro_number(self, line, index):
		while(index < len(line)):
			c = line[index]
			if(self.__functions.isDelimiter(c)):
				return ["NMF", self.__lexema, index]
			else:
				self.__lexema += c
				index += 1
		else:
			return ["NMF", self.__lexema, index] # Acabou a linha e não encontrou um delimitador


	def auto_relational_operators(self, line, initial):
		state     = 1
		self.__lexema = ""
		index = initial
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				if(c == '!'):
					state      = 2
					self.__lexema += c
					index += 1
				elif(c == '>' or c == '<' or c == '='):
					state      = 3
					self.__lexema += c
					index += 1
			elif(state == 2):
				if(c == '='):
					state      = 4
					self.__lexema += c
					index += 1
				elif(c == '>' or c == '<' or c == '!'):
					state       = 5   # erro
					self.__lexema += c
					index += 1
			elif(state == 3):
				if(c == '='):
					state = 4
					self.__lexema += c
					index += 1
				elif(self.__functions.isDelimiter(c)):
					return ["REL", self.__lexema, index]
				else:
					state = 5          # erro
					self.__lexema += c
					index += 1
			elif(state == 4):
				if(self.__functions.isDelimiter(c)):
					return ["REL", self.__lexema, index]
				else:
					state = 5          # erro
					self.__lexema +=c
					index += 1
			elif(state == 5):
				return self.auto_erro_operator(line, index)
		else:
			return ["REL", self.__lexema, index]


	def auto_arithmetic_operators(self,line, initial):
		state     = 1
		self.__lexema = ""
		index = initial
		while (index < len(line)):
			c = line[index]
			if(state == 1):
				if(c == '*' or c == '/'):
					state = 2
					self.__lexema += c
					index +=1
				elif(c == '-'):
					state = 5
					self.__lexema += c
					index +=1
				elif(c == '+'):
					state = 3
					self.__lexema += c
					index +=1
			elif(state == 2):
				if(self.__functions.isDelimiter(c)):
					return ["ART", self.__lexema, index]
				else:
					state = 7    # Erro
					self.__lexema += c
					index +=1
			elif(state == 3):
				if(c == '+'):
					state = 4
					self.__lexema += c
					index +=1
				elif(self.__functions.isDelimiter(c)):
					return ["ART", self.__lexema, index]
				else:
					state = 7    # Erro
					self.__lexema += c
					index +=1
			elif(state == 4):
				if(self.__functions.isDelimiter(c)):
					return ["ART", self.__lexema, index]
				else:
					state = 7    # Erro
					self.__lexema += c
					index +=1
			elif(state == 5):
				if(c == '-'):
					state = 6
					self.__lexema += c
					index +=1
				elif(self.__functions.isDelimiter(c)):
					return ["ART", self.__lexema, index]
				else:
					state = 7    # Erro
					self.__lexema += c
					index +=1
			elif(state == 6):
				if(self.__functions.isDelimiter(c)):
					return ["ART", self.__lexema, index]
				else:
					state = 7    # Erro
					self.__lexema += c
					index +=1
			elif(state == 7):
				return self.auto_erro_operator(line, index)
		else:
			return ["ART", self.__lexema, index]

	def auto_logical_operators(self, line, initial):
		state = 1
		index = initial
		self.__lexema = ""
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				if(c == "|"):
					state = 2
					self.__lexema += c
					index +=1
				elif(c == "&"):
					state = 4
					self.__lexema += c
					index +=1
				elif(c == "!"):
					state = 6
					self.__lexema += c
					index +=1
			elif(state == 2):
				if(c == "|"):
					state = 3
					self.__lexema += c
					index +=1
				else: # caso receba qualquer símbolo que nao seja um "!". Pode ser até mesmo um delimitador
					state = 7 # erro
			elif(state == 3):
				if(self.__functions.isDelimiter(c)):
					return ["LOG", self.__lexema, index]
				else:
					state = 7 # erro
			elif(state == 4):
				if(c == "&"):
					state = 5
					self.__lexema += c
					index +=1
				else: # caso receba qualquer símbolo que nao seja um "!". Pode ser até mesmo um delimitador
					state = 7 # erro
			elif(state == 5):
				if(self.__functions.isDelimiter(c)):
					return ["LOG", self.__lexema, index]
				else:
					state = 7 # erro
			elif(state == 6):
				if(self.__functions.isDelimiter(c)):
					return ["LOG", self.__lexema, index]
				else:
					state = 7 # erro
			elif(state == 7):
				return self.auto_erro_operator(line, index)
		else:
			if(self.__lexema == "&&" or self.__lexema == "||" or self.__lexema == "!"):
				return ["LOG", self.__lexema, index]
			else:
				return ["OpMF", self.__lexema, index]


	def auto_numbers(self, line, initial):
		state = 1
		index = initial
		self.__lexema = ""
		while(index < len(line)):
			c = line[index]
			if(state == 1): # Se entrou nesse automato é porque o primeiro caractere analisado é um digito
				state = 2
				self.__lexema += c
				index +=1
			elif(state == 2):
				if(self.__functions.isSymbol(c) == True or self.__functions.isOperatorRelational(c) == True or self.__functions.isArithmeticOperators(c) == True or self.__functions.isLogicalOperators(c) == True):
					return self.auto_erro_number(line, index)				
				elif(self.__functions.isDigit(c)):
					state = 2
					self.__lexema += c
					index +=1
				elif(c == '.'):
					state = 3
					self.__lexema += c
					index +=1
				elif(self.__functions.isDelimiter(c)):
					return ["NRO", self.__lexema, index]
				elif(c == "\'" or c == "\""):
					return ["NRO", self.__lexema, index]
				else:
					state = 5 # erro
			elif(state == 3):
				if(self.__functions.isDigit(c)):
					state = 4
					self.__lexema += c
					index +=1
				else:
					state = 5 # erro
			elif(state == 4):
				if(self.__functions.isSymbol(c) == True or self.__functions.isOperatorRelational(c) == True or self.__functions.isArithmeticOperators(c) == True or self.__functions.isLogicalOperators(c) == True):
					return self.auto_erro_number(line, index)
				elif(c == "."):
					state = 5 # erro
				elif(self.__functions.isDigit(c)):
					state = 4
					self.__lexema += c
					index +=1
				elif(self.__functions.isDelimiter(c)):
					return ["NRO", self.__lexema, index]
				elif(c == "\'" or c == "\""):
					return ["NRO", self.__lexema, index]
				else:
					state = 5 # erro
			elif(state == 5): # leio ate encontrar um delimitador menos o delimitador "."
				if(c == "."):
					state = 5
					self.__lexema += c
					index +=1
				elif(self.__functions.isDelimiter(c)): # se não é um ponto, podemos usar a funcao isDelimiter() para verificar os outros delimitadores.
					return ["NMF", self.__lexema, index]
				else:
					state = 5
					self.__lexema += c
					index +=1
				if(index >= len(line)): # Verifica se acabou a linha
					return ["NMF", self.__lexema, index]
		else:
			return ["NRO", self.__lexema, index]

	def auto_character(self, line, initial):
		state = 1
		index = initial
		self.__lexema = ""
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				if(c == '\''):
					state = 2
					self.__lexema += c
					index +=1
			elif(state == 2):
				if(c == "\\"): # caso receba um caractere \
					state = 6
					self.__lexema += c
					index +=1
				elif(c == "\"" or ord(c) < 32 or ord(c) > 126): # caso receba um caractere " ou qualquer outro fora da faixa da tabela ascii.
					state = 5 # erro
					self.__lexema += c
					index +=1
				elif(c == "\'"): # caso receba um caractere '
					state = 4
					self.__lexema += c
					index +=1
				else:
					state = 3
					self.__lexema += c
					index +=1
			elif(state == 3):
				if(c == "\'"): # caso receba um caractere '
					state = 4
					self.__lexema += c
					index +=1
				elif(c == " "):
					return ["CaMF", self.__lexema, index]
				else:
					state = 5 # erro
					self.__lexema += c
					index +=1
			elif(state == 4):
				return ["CAR", self.__lexema, index]
			elif(state == 5): # ESTADO DE ERRO (faz a leitura até reconhecer a finalização da linha ou do caractere)
				state = 5
				if(c == '\''):
					if(line[index - 1] == "\\"):
						if(line[index + 1] == "\'"):
							self.__lexema += c
							self.__lexema += line[index + 1] # adiciono ao lexema a aspas analisada
							index +=2 						 # Pula a aspas que foi analisada
							return ["CaMF", self.__lexema, index]
					index += 1
					self.__lexema += c
					return ["CaMF", self.__lexema, index]
				elif(self.__functions.isDelimiter(c)): # Caso encontre um caractere " " ou qualquer delimitador
					return ["CaMF", self.__lexema, index]
				else:
					self.__lexema += c
					index +=1 
			elif(state == 6):
				if(c == "\'"): # caso receba um caractere '
					state = 7
					self.__lexema += c
					index +=1
				else:
					state = 5 # erro
					self.__lexema += c
					index += 1
			elif(state == 7):
				if(c == "\'"): # caso receba um caractere '
					state = 8
					self.__lexema += c
					index +=1
				else:
					return ["CAR", self.__lexema, index]
			elif(state == 8):
				return ["CAR", self.__lexema, index]
		else:
			return ["CaMF", self.__lexema, index]

	def auto_symbol(self, line, initial):
		state = 1
		index = initial
		self.__lexema = ""
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				before = line[index-1] # Verifica se antes do símbolo existe algum delimitador
				after  = line[index+1] # Verifica se depois do símbolo existe algum delimitador
				state  = 2
				index += 1
				if(self.__functions.invalid_symbol(c)):
					self.__lexema += c
				elif(self.__functions.isDelimiter(before)):
					if(self.__functions.isDelimiter(after)):
						return ["SIB", c,index]
					self.__lexema += c
				else:
					self.__lexema += c
			elif(state == 2):
				if(self.__functions.isSymbol(c) or self.__functions.invalid_symbol(c)):
					self.__lexema += c
					index +=1
				elif(c == self.__functions.isLogicalOperators(c) == True or c == self.__functions.isArithmeticOperators(c) == True or c == self.__functions.isOperatorRelational(c) == True):
					return self.auto_erro_operator(line, index)
				else:
					return ["SII", self.__lexema, index]
		else:
			return ["SII", self.__lexema, index]

	def auto_string(self, line, initial):
		state = 1
		index = initial
		self.__lexema = ""
		erro = False
		while(index < len(line)):
			c = line[index]
			if(state == 1):
				state = 2
				index +=1
				self.__lexema += c
			elif(state == 2):
				if(c == "\""): # Caractere "
					state = 4
					index +=1
					self.__lexema += c
				elif(c == "\\"): # Caractere \
					state = 3
					index +=1
					self.__lexema += c
				elif(c == "\'" or self.__functions.invalid_symbol(c) == True): # Caractere ' ou fora da faixa permitida da tabela ascii
					state = 5    # erro
				else:
					state = 2
					index +=1
					self.__lexema += c
			elif(state == 3):
				if(c == "\'" or self.__functions.invalid_symbol(c) == True):
					state = 5 # erro
				elif(c == "\\"):
					state  = 3
					index += 1
					self.__lexema += c
				else:
					state  = 2
					index += 1
					self.__lexema += c
			elif(state == 4):
				if(erro == True):
					return ["CMF", self.__lexema, index]
				else:
					return ["CAD", self.__lexema, index]
			elif(state == 5): # Caso entre no estado de erro, realiza as leituras até encontrar o final da cadeia de caracteres ou finalizar a linha
				state = 2
				index +=1
				self.__lexema += c
				erro = True
		else:
			return ["CMF", self.__lexema, index]


	def auto_comment(self, content, current_line, initial):
		state = 1
		self.__lexema  = ""
		initial_coment = current_line # armazena onde o comentario de bloco foi iniciado
		while(current_line < len(content)):
			nextLine         = content[current_line]
			index            = initial
			while(index < len(nextLine)):
				c = nextLine[index]
				if(state == 1):
					if(c == "{"):
						state = 2
						index +=1
						self.__lexema += c
				elif(state == 2):
					if(c == "#"):
						state = 3
						index +=1
						self.__lexema += c
				elif(state == 3):
					if(c == "#"):
						self.__lexema += c
						self.__lexema += nextLine[index + 1]
						if(nextLine[index + 1] == "}"):
							index +=2
							return [current_line, index, True, initial_coment, self.__lexema] # Comentario de bloco finalizado. Retorna a linha atual e a próxima posição para analise
						else:
							state = 3
							index +=2
					else:
						state = 3
						index +=1
						self.__lexema += c
			else:
				state   = 3
				initial = 0
				current_line += 1
		else:
			return [current_line, 0, False, initial_coment, self.__lexema]