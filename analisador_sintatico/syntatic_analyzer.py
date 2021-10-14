from auxiliary_functions import Auxiliary_functions

class Syntatic_analyzer():
	"""docstring for Syntatic_analyzer"""
	def __init__(self, tokens):
		# Atributo que armazena todos os tokens a serem analisados. Estrutura [{"linha":  , "sigla": , "token":}, {"linha":  , "sigla": , "token":}, ...]
		# Consiste em um vetor de dicionarios.
		self.__tokens       = tokens;
		# Atributo que armazena o token atual.
		# Estrutura: {"linha":  , "sigla": , "token":}
		self.__currentToken = {}; 

	# Metodo que retorna o proximo token a ser analisado.
	def next_token():
		return

	# <declaration_reg>    ::= registro id '{' <declaration_reg1> |
	def declaration_reg():
		if(self.__currentToken['token'] == "registro"):
			self.__currentToken = next_token()
			if(self.__currentToken['token'] == "IDE"):
				self.__currentToken = next_token()
				if(self.__currentToken['token'] == "{"):
					self.__currentToken = next_token()
					if(First("declaration_reg1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.declaration_reg1()
						return
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '}'\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador \n")
		else:
			return # Nao existe declaration de registro


	# <declaration_reg1>   ::= <primitive_type> id <declaration_reg4> <declaration_reg2> | id id <declaration_reg4> <declaration_reg2> 
	def declaration_reg1():
		if(First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = next_token()
			if(First("declaration_reg4",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_reg4()
				self.__currentToken = next_token()
				if(First("declaration_reg2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_reg2()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
		elif(self.__currentToken['sigla'] == "IDE"):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(First("declaration_reg4",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_reg4()
					self.__currentToken = next_token()
					if(First("declaration_reg2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.declaration_reg2()
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador \n")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando tipo primitivo ou identificador \n")				


	# <declaration_reg2>   ::= ',' id <declaration_reg2> | ';' <declaration_reg5>
	def declaration_reg2():
		if(self.__currentToken['token'] == ","):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(First("declaration_reg2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_reg2()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador \n")
		elif(self.__currentToken['token'] == ";"):
			self.__currentToken = next_token()
			if(First("declaration_reg5",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_reg5()
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ',' ou ';' \n")

	# <declaration_reg3>   ::= '}' <declaration_reg>
	def declaration_reg3():
		if(self.__currentToken['token'] == "}"):
			self.__currentToken = next_token()
			if(First("declaration_reg",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_reg()
			else:
				return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '}'\n")

	# <declaracao_reg4>   ::= <v_m_access> |
	def declaration_reg4():
		if(First("v_m_access",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.v_m_access()
		else:
			return

	# <declaration_reg5>   ::= <declaration_reg1> | <declaration_reg3>
	def declaration_reg5():
		if(First("declaration_reg1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg1()
		elif(First("declaration_reg3",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg3()
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")

	# <declaration_const>  ::= constantes '{' <declaration_const1>
	def declaration_const():
		if(self.__currentToken['token'] == "constantes"):
			self.__currentToken = next_token()
			if(self.__currentToken['token'] == "{"):
				self.__currentToken = next_token()
				if(First("declaration_const1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_const1()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '}' \n")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token 'constantes' \n")

	# <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
	def declaration_const1():
		if(First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(self.__currentToken['token'] == "="):
					if(First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.__currentToken = next_token()
						if(First("declaration_const2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
							self.declaration_const2()
							return
						else:
							print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador")
		elif(self.__currentToken['token'] == "}"):
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador ou token '}' or 'inteiro', 'real', 'booleano', 'char', 'cadeia', 'vazio'")


	# <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
	def declaration_const2():
		if(self.__currentToken['token'] == ','):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(self.__currentToken['token'] == "="):
					if(First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.__currentToken = next_token()
						if(First("declaration_const2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
							self.declaration_const2()
							return
						else:
							print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador")
		elif(self.__currentToken['token'] == ';'):
			self.__currentToken = next_token()
			if(First("declaration_const1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_const1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ',' , ';' ")


	#<declaration_var>  ::= variaveis '{' <declaration_var1>
	def declaration_var():
		if(self.__currentToken['token'] == "variaveis"):
			self.__currentToken = next_token()
			if(self.__currentToken['token'] == "{"):
				self.__currentToken = next_token()
				if(First("declaration_var1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var1()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '}'")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token 'variaveis'")

	
	# <declaration_var1> ::= <type> id <declaration_var2> | '}' 
	def declaration_var1():
		if(First("type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(First("declaration_var2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var2()
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador")
		elif(self.__currentToken['token'] == "}"):
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador ou token '}' or 'inteiro', 'real', 'booleano', 'char', 'cadeia', 'vazio'")


	#<declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
	def declaration_var2():
		if(self.__currentToken['token'] == "="):
			self.__currentToken = next_token()
			if(First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.__currentToken = next_token()
				if(First("declaration_var3",self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var3()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha']. + " . Esperando token ',' ou ';'")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando valor numerico, booleano, caractere ou cadeia de caracteres")
		elif(First("vector_matrix", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.vector_matrix()
		elif(First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '=', '[' , ',' , ';' ")


	#<declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1> 
	def declaration_var3():
		if(self.__currentToken['token'] == ','):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "IDE"):
				self.__currentToken = next_token()
				if(First("declaration_var2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var2()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'])
		elif(self.__currentToken['token'] == ';'):
			self.__currentToken = next_token()
			if(First("declaration_var1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_var1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ',' , ';' ")



	#<vector_matrix>   ::= '[' number ']' <vector_matrix_1>
	def vector_matrix():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "NRO"):
				self.__currentToken = next_token()
				if(self.__currentToken['token'] == "]"):
					self.__currentToken = next_token()
					if(First("vector_matrix_1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.vector_matrix_1()
						return
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 


	#<vector_matrix_1> ::= '[' number ']' <vector_matrix_2> | '=' <init_vector> <declaration_var3> | <declaration_var3>
	def vector_matrix_1():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == "NRO"):
				self.__currentToken = next_token()
				if(self.__currentToken['token'] == "]"):
					self.__currentToken = next_token()
					if(First("vector_matrix_2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.vector_matrix_2()
						return
					else:
						print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		elif(self.__currentToken['token'] == '='):
			self.__currentToken = next_token()
			if(First("init_vector", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_vector()
				self.__currentToken = next_token()
				if(First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var3()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
		elif(First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 

	
	#<vector_matrix_2> ::= '=' <init_matrix> <declaration_var3> | <declaration_var3>
	def vector_matrix_2():
		if(self.__currentToken['token'] == '='):
			self.__currentToken = next_token()
			if(First("init_matrix", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_matrix()
				if(First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.declaration_var3()
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		elif(First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 


	# <init_matrix>     ::= '[' <init_matrix_1>
	def init_matrix():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(First("init_matrix_1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_matrix_1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 


	# <init_matrix_1>   ::=     <value_with_IDE> <init_matrix_2>
	def init_matrix_1():
		if(First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = next_token()
			if(First("init_matrix_2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_matrix_2()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 

	
	# <init_matrix_2>   ::= ',' <init_matrix_1> | ';' <init_matrix_1> | ']' 
	def init_matrix_2():
		if(self.__currentToken['token'] == ',' or self.__currentToken['token'] == ';'):
			self.__currentToken = next_token()
			if(First("init_matrix_1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_matrix_1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		elif(self.__currentToken['token'] == ']'):
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 


	# <init_vector>     ::= '[' <init_vector_1>
	def init_vector():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(First("init_vector_1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_vector_1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 

	# <init_vector_1>   ::=     <value_with_IDE> <init_vector_2>
	def init_vector_1():
		if(First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = next_token()
			if(First("init_vector_2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_vector_2()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 

	# <init_vector_2>   ::= ',' <init_vector_1> | ']'
	def init_vector_2():
		if(self.__currentToken['token'] == ','):
			self.__currentToken = next_token()
			if(First("init_vector_1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.init_vector_1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		elif(self.__currentToken['token'] == ']'):
			return
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 


	# <v_m_access>   ::= '[' <v_m_access1>
	def v_m_access():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(First("v_m_access1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.v_m_access1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n") 

	# <v_m_access1>  ::= id  <v_m_access2>                    | number ']' <v_m_access3> 
	def v_m_access1():
		if(self.__currentToken['sigla'] == 'IDE'):
			self.__currentToken = next_token()
			if(First("v_m_access2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.v_m_access2()
				return
		elif(self.__currentToken['sigla'] == 'NRO'):
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == ']'):
				self.__currentToken = next_token()
				if(First("v_m_access3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.v_m_access3()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ']' \n")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador ou numero \n")


	# <v_m_access2>  ::= <elem_registro> ']' <v_m_access3>    | ']'        <v_m_access3>
	def v_m_access2():
		if(First("elem_registro", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.elem_registro()
			self.__currentToken = next_token()
			if(self.__currentToken['sigla'] == ']'):
				self.__currentToken = next_token()
				if(First("v_m_access3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
					self.v_m_access3()
					return
				else:
					print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ']' \n")
		elif(self.__currentToken['sigla'] == ']'):
			self.__currentToken = next_token()
			if(First("v_m_access3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.v_m_access3()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
		else:
			print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")

	# <v_m_access3>   ::= '[' <v_m_access1>
	def v_m_access3():
		if(self.__currentToken['token'] == '['):
			self.__currentToken = next_token()
			if(First("v_m_access1", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.v_m_access1()
				return
			else:
				print("Erro sintático na linha " + self.__currentToken['linha'] + "\n")
		else:
			return







		

			








