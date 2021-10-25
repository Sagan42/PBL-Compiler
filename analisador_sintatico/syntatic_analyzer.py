from auxiliary_functions import Auxiliary_Functions

# <v_m_acess> encerra suas producoes com "vazio", logo, depois dele nao é necessario pegar um proximo token.
# Somente pega o proximo token depois de um "match"
class Syntatic_analyzer():
	"""docstring for Syntatic_analyzer"""
	def __init__(self, tokens):
		# Atributo que armazena todos os tokens a serem analisados. Estrutura [{"linha":  , "sigla": , "token":}, {"linha":  , "sigla": , "token":}, ...]
		# Consiste em um vetor de dicionarios.
		self.__tokens       = tokens;
		# Atributo que armazena o token atual.
		# Estrutura: {"linha":  , "sigla": , "token":}
		self.__currentToken = {};
		self.__functions_aux = Auxiliary_Functions()

	# Metodo que retorna o proximo token a ser analisado.
	def next_token(self):
		# Retorna o proximo token para analise
		if(len(self.__tokens) > 0):
			return self.__tokens.pop(0)
		else:
			# Acabou todos os tokens
			print("[INFO] Tokens finalizados.")
			return {"linha": "", "sigla": "", "token": ""}

	def number_of_tokens(self):
		return len(self.__tokens)

	def refresh_tokens(self, new_tokens):
		if(len(self.__tokens) == 0):
			# Insere o novos tokens (passagem por referencia)
			self.__tokens = new_tokens
			print("[INFO] Tokens atualizados com sucesso.")
		else:
			print("[WARNING] Ainda existem tokens a serem analisados.")


	def match(self,token, option):
		if(option == 1):
			if(self.__currentToken["token"] == token):
				print("[INFO] Token aceito: \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"] + "\n")
				return True
			else:
				return False
		elif(option == 2):
			if(self.__currentToken["sigla"] == token):
				print("[INFO] Token aceito: \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"] + "\n")
				return True
			else:
				return False

	def Program(self):
		self.__currentToken = self.next_token()
		if(self.__functions_aux.First("declaration_reg",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg()
		self.declaration_const()
		self.declaration_var()


	# ============================================================================================
	# === Gramatica para declaracao de elementos do tipo registro ================================
	# <declaration_reg>    ::= registro id '{' <declaration_reg1> |
	def declaration_reg(self):
		if(self.match("registro", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				if(self.match("{", 1) == True):
					self.__currentToken = self.next_token()
					self.declaration_reg1()
					return
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'\n")
						self.__error1_reg()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador \n")
					if(self.match("{",1)):
						self.__currentToken = self.next_token()
						self.declaration_reg1()
						return
					else:
						self.__error1_reg()
		return # Nao existe declaracao de registro

	# <declaration_reg1>   ::= <primitive_type> id <declaration_reg4> <declaration_reg2> | id id <declaration_reg4> <declaration_reg2> 
	def declaration_reg1(self):
		if(self.__functions_aux.First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg4()
				self.declaration_reg2()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador." +"\n")
					self.__error1_reg()
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg4()
				self.declaration_reg2()
				return 
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador \n")
					self.__error1_reg()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo primitivo ou identificador.\n")
				self.__error2_reg()

	# <declaration_reg2>   ::= ',' id <declaration_reg2> | ';' <declaration_reg5>
	def declaration_reg2(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg4()
				self.declaration_reg2()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador \n")
					self.__error3_reg()
		elif(self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_reg5()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ';' \n")
				self.__error2_reg()

	# <declaration_reg3>   ::= '}' <declaration_reg>
	def declaration_reg3(self):
		if(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_reg()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'\n")
				self.__error1_reg()

	# <declaracao_reg4>   ::= <v_m_access> |
	def declaration_reg4(self):
		if(self.__functions_aux.First("v_m_access",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.v_m_access()
			return
		else:
			return

	# <declaration_reg5>   ::= <declaration_reg1> | <declaration_reg3>
	def declaration_reg5(self):
		if(self.__functions_aux.First("declaration_reg1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg1()
		elif(self.__functions_aux.First("declaration_reg3",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg3()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo primitivo ou identificador ou ',' ou ';'\n")
				self.__error1_reg()
	# =========================================================================================
	# =========================================================================================

	# =======================================================================================
	# === Gramatica para acesso a elementos do tipo registro ================================
	# <elem_registro>         ::= '.' id <nested_elem_registro>
	def elem_registro(self):
		if(self.match(".", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.nested_elem_registro()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token.\n")


	# <nested_elem_registro>  ::= '.' id <nested_elem_registro1> | <v_m_access> <nested_elem_registro1> |
	def nested_elem_registro(self):
		if(self.match(".", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.nested_elem_registro1()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
		elif(self.__functions_aux.First("v_m_access",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.v_m_access()
			self.nested_elem_registro1()
			return
		else:
			return # Vazio

	# <nested_elem_registro1> ::= <elem_registro> |
	def nested_elem_registro1(self):
		if(self.__functions_aux.First("elem_registro",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.elem_registro()
			return
		else:
			return # Vazio
	# =========================================================================================
	# =========================================================================================
	

	# =======================================================================================
	# === Gramatica para declaracao do bloco de constantes ==================================
	# <declaration_const>  ::= constantes '{' <declaration_const1>
	def declaration_const(self):
		if(self.match("constantes", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.declaration_const1()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'\n")
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__currentToken["token"] == "variaveis"):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'constantes'\n")
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.__currentToken["token"] == "variaveis"):
						return
					else:
						self.__currentToken = self.next_token()

	# <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
	def declaration_const1(self):
		if(self.__functions_aux.First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.__currentToken = self.next_token()
						self.declaration_const2()
						return
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token para atribuição.\n")
							self.__error1_const()
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='\n")
						self.__error1_const()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador.\n")
					self.__error1_const()
		elif(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}' ou tipo primitivo.\n")
				self.__error1_const()

	# <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
	def declaration_const2(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						self.__currentToken = self.next_token()
						self.declaration_const2()
						return
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor para atribuição.\n")
							self.__error1_const()
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='\n")
						self.__error1_const()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador\n")
					self.__error1_const()
		elif(self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_const1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' , ';'\n")
				self.__error1_const()
	# =========================================================================================
	# =========================================================================================
	

	# =======================================================================================
	# === Gramatica para declaracao do bloco de variaveis ===================================
	# <declaration_var>  ::= variaveis '{' <declaration_var1>
	def declaration_var(self):
		if(self.match("variaveis", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.declaration_var1()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__currentToken["token"] == "funcao"):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'variaveis'.\n")
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.__currentToken["token"] == "funcao"):
						return
					else:
						self.__currentToken = self.next_token()

	
	# <declaration_var1> ::= <type> id <declaration_var2> | '}' 
	def declaration_var1(self):
		if(self.__functions_aux.First("type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.declaration_var2()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token identificador.\n")
					self.__error1_var()
		elif(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador ou token '}' or tipo primitivo.\n")
				self.__error1_var()

	# <declaration_var2> ::= '=' <value> <declaration_var3> | <vector_matrix> | <declaration_var3>
	def declaration_var2(self):
		if(self.match("=", 1) == True):
			self.__currentToken = self.next_token()
			if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.__currentToken = self.next_token()
				self.declaration_var3()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando valor para atribuição.\n")
					self.__error1_var()
		elif(self.__functions_aux.First("vector_matrix", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.vector_matrix()
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '=', '[' , ',' , ';'\n")
				self.__error1_var()


	# <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1> 
	def declaration_var3(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.declaration_var2()
		elif(self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_var1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token ',' , ';'\n")
				self.__error1_var()
	# =========================================================================================
	# =========================================================================================
	

	# =======================================================================================
	# === Gramatica para declaracao de vetores e matrizes ===================================
	# <vector_matrix>   ::= '[' number ']' <vector_matrix_1>
	def vector_matrix(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("NRO", 2) == True):
				self.__currentToken = self.next_token()
				if(self.match("]", 1) == True):
					self.__currentToken = self.next_token()
					self.vector_matrix_1()
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'.\n") 
						self.__error_vector_matrix()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token numérico.\n")
					self.__error_vector_matrix() 
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				self.__error_vector_matrix() 


	# <vector_matrix_1> ::= '[' number ']' <vector_matrix_2> | '=' <init_vector> <declaration_var3> | <declaration_var3>
	def vector_matrix_1(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("NRO", 2) == True):
				self.__currentToken = self.next_token()
				if(self.match("]",1) == True):
					self.__currentToken = self.next_token()
					self.vector_matrix_2()
					return
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'\n")
						self.__error_vector_matrix()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token numérico.\n")
					self.__error_vector_matrix() 
		elif(self.match("=", 1) == True):
			self.__currentToken = self.next_token()
			self.init_vector()
			self.declaration_var3()
			return
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '[' , '=' , ',' , ';'\n")
				self.__error_vector_matrix() 
	
	# <vector_matrix_2> ::= '=' <init_matrix> <declaration_var3> | <declaration_var3>
	def vector_matrix_2(self):
		if(self.match("=", 1) == True):
			self.__currentToken = self.next_token()
			self.init_matrix()
			self.declaration_var3() 
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='.\n")
				self.__error_vector_matrix() 
	# =========================================================================================
	# =========================================================================================
	

	# =========================================================================================
	# === Gramatica para inicializacao de vetores e matrizes ==================================
	# <init_matrix>     ::= '[' <init_matrix_1>
	def init_matrix(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			self.init_matrix_1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				self.__error_vector_matrix()  

	# <init_matrix_1>   ::=     <value_with_IDE> <init_matrix_2>
	def init_matrix_1(self):
		if(self.__functions_aux.First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.init_matrix_2()
			return 
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor numérico ou identificador para inicialização.\n")
				self.__error_vector_matrix() 

	# <init_matrix_2>   ::= ',' <init_matrix_1> | ';' <init_matrix_1> | ']' 
	def init_matrix_2(self):
		if(self.match(",", 1) == True or self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			self.init_matrix_1()
			return 
		elif(self.match("]", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ']'.\n")
				self.__error_vector_matrix()  

	# <init_vector>     ::= '[' <init_vector_1>
	def init_vector(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			self.init_vector_1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				self.__error_vector_matrix()  

	# <init_vector_1>   ::=     <value_with_IDE> <init_vector_2>
	def init_vector_1(self):
		if(self.__functions_aux.First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.init_vector_2()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor numérico para inicialização.\n")
				self.__error_vector_matrix() 

	# <init_vector_2>   ::= ',' <init_vector_1> | ']'
	def init_vector_2(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			self.init_vector_1()
			return
		elif(self.match("]", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ']'.\n")
			self.__error_vector_matrix()
	# =========================================================================================
	# =========================================================================================
	

	# =======================================================================================
	# === Gramatica para acesso a vetores e matrizes ========================================
	# <v_m_access>   ::= '[' <v_m_access1>
	def v_m_access(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			self.v_m_access1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				if(self.__functions_aux.First("v_m_access1") == True):
					self.v_m_access1()
					return
				else:
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.match("]",1) == True):
							self.__currentToken = self.next_token()
							self.v_m_access3()
							return
						else:
							self.__currentToken = self.next_token()

	# <v_m_access1>  ::= id  <v_m_access2>                    | number ']' <v_m_access3> 
	def v_m_access1(self):
		if(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.v_m_access2()
			return
		elif(self.match("NRO", 2) == True):
			self.__currentToken = self.next_token()
			if(self.match("]", 1) == True):
				self.__currentToken = self.next_token()
				self.v_m_access3()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'.\n")
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador ou numero.\n")
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.match("]",1) == True):
						self.__currentToken = self.next_token()
						self.v_m_access3()
						return
					elif(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
						return
					else:
						self.__currentToken = self.next_token()

	# <v_m_access2>  ::= <elem_registro> ']' <v_m_access3>    | ']'        <v_m_access3>
	def v_m_access2(self):
		if(self.__functions_aux.First("elem_registro", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.elem_registro()
			if(self.match("]", 1) == True):
				self.__currentToken = self.next_token()
				self.v_m_access3()
				return
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']' \n")
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
							return
						else:
							self.__currentToken = self.next_token()
		elif(self.match("]", 1) == True):
			self.__currentToken = self.next_token()
			self.v_m_access3()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '.' ou ']'.\n")
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
						return
					else:
						self.__currentToken = self.next_token()
	
	# <v_m_access3>   ::= '[' <v_m_access1>
	def v_m_access3(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			self.v_m_access1()
			return
		else:
			return
	# =========================================================================================
	# =========================================================================================
	def __error1_reg(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.__currentToken["token"] == "registro"):
				self.declaration_reg()
				return
			elif(self.__currentToken["token"] == "constantes"):
				return
			else:
				self.__currentToken = self.next_token()

	def __error2_reg(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg5()
				return
			elif(self.match("}", 1) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg()
				return
			elif(self.__currentToken["token"] == "registro"):
				self.declaration_reg()
				return
			elif(self.__currentToken["token"] == "constantes"):
				return
			else:
				self.__currentToken = self.next_token()

	def __error3_reg(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.__currentToken["token"] == ";" or self.__currentToken["token"] == ","):
				self.declaration_reg2()
				return
			elif(self.match("}", 1) == True):
				self.__currentToken = self.next_token()
				self.declaration_reg()
				return
			else:
				self.__currentToken = self.next_token()

	def __error1_const(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.__currentToken["token"] == "," or self.__currentToken["token"] == ";"):
				self.declaration_const2()
				return
			elif(self.match("}",1) == True):
				self.__currentToken = self.next_token()
				return
			elif(self.__currentToken["token"] == "variaveis"):
				return
			else:
				self.__currentToken = self.next_token()	


	def __error1_var(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.__functions_aux.First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_var1()
				return
			elif(self.match("}",1) == True):
				self.__currentToken = self.next_token()
				return
			elif(self.__currentToken["token"] == "funcao"):
				return
			else:
				self.__currentToken = self.next_token()


	def __error_vector_matrix(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
			if(self.__functions_aux.First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.declaration_var1()
				return
			elif(self.match("}",1) == True):
				self.__currentToken = self.next_token()
				return
			elif(self.__currentToken["token"] == "funcao"):
				return
			else:
				self.__currentToken = self.next_token()






		

			








