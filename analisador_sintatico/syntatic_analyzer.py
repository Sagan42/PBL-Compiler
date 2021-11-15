from auxiliary_functions import Auxiliary_Functions
from semantic_analyzer   import Semantic_Analyzer
# <v_m_acess> encerra suas producoes com "vazio", logo, depois dele nao é necessario pegar um proximo token.
# Somente pega o proximo token depois de um "match"
class Syntatic_analyzer():
	"""docstring for Syntatic_analyzer"""
	def __init__(self, tokens, files):
		# Atributo que armazena todos os tokens a serem analisados. Estrutura [{"linha":  , "sigla": , "token":}, {"linha":  , "sigla": , "token":}, ...]
		# Consiste em um vetor de dicionarios.
		self.__tokens       = tokens
		# Atributo utilizado para escrever as mensagens de erro nos arquivos de saida.
		self.__files        = files
		# Atributo que armazena o token atual.
		# Estrutura: {"linha":  , "sigla": , "token":}
		self.__currentToken  = {}
		self.__functions_aux = Auxiliary_Functions()
		# Atributo que armazena a quantidade de erros detectados.
		self.__erros         = 0;
		self.__semantic_analyzer = Semantic_Analyzer()
		# Tabela de simbolos para constantes e variaveis
		self.__VC_Table      = {}
		# Atributo que armazena um dicionario de tokens especificos para auxiliar a analise semantica
		self.__lexema        = {}
		self.__currentScope  = ""

	def get_erros(self):
		return self.__erros

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
				print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
				return True
			else:
				return False
		elif(option == 2):
			if(self.__currentToken["sigla"] == token):
				print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"] )
				return True
			else:
				return False

	def Program(self):
		self.__currentToken = self.next_token()
		if(self.__functions_aux.First("declaration_reg",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_reg()
		# Comeca a analise de constantes
		self.__currentScope       = "global"
		self.declaration_const()
		self.declaration_var()
		# Comeca a analise de funcoes
		self.__currentScope       = "local"
		self.function_declaration()
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
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["{"])
						self.__error1_reg()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador \n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error1_reg()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo primitivo ou identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE", "inteiro","real","verdadeiro","falso","char","cadeia","vazio"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error3_reg()
		elif(self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_reg5()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ';' \n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [",",";"])
				self.__error2_reg()

	# <declaration_reg3>   ::= '}' <declaration_reg>
	def declaration_reg3(self):
		if(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			self.declaration_reg()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["}"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [";",",","IDE", "inteiro","real","verdadeiro","falso","char","cadeia","vazio"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error_elem_registro()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '.' \n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["."])
				self.__error_elem_registro()


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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error_elem_registro()
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["{"])
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__currentToken["token"] == "variaveis"):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'constantes'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["constantes"])
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.__currentToken["token"] == "variaveis"):
						return
					else:
						self.__currentToken = self.next_token()

	# <declaration_const1> ::= <primitive_type> id '=' <value> <declaration_const2> | '}'
	def declaration_const1(self):
		if(self.__functions_aux.First("primitive_type",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
			# Armazena a categoria que esta sendo analisada, constante ou variavel
			self.__VC_Table["categoria"] = "constante"
			# Armazena o tipo utilizado na declaracao
			self.__VC_Table["tipo"] = self.__currentToken["token"]
			self.__lexema["tipo"]   = self.__currentToken
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da constante
				self.__VC_Table["nome"]     = self.__currentToken["token"]
				# Como nao e vetor ou matriz, nao tem dimensao
				self.__VC_Table["dimensao"] = None
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
						# Armazena o valor recebido para inicializacao
						self.__VC_Table["init"]  = True
						self.__lexema["valor"]   = self.__currentToken
						self.__currentToken      = self.next_token()
						self.declaration_const2()
						return
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token para atribuição.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
							self.__error1_const()
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["="])
						self.__error1_const()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error1_const()
		elif(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}' ou tipo primitivo.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["}","inteiro", "real", "verdadeiro", "falso", "char", "cadeia", "vazio"])
				self.__error1_const()

	# <declaration_const2> ::= ',' id '=' <value> <declaration_const2> | ';' <declaration_const1>
	def declaration_const2(self):
		self.__VC_Table["escopo"] = self.__currentScope
		# Realiza analise semantica da constante declarada
		self.__semantic_analyzer.analyzer_var_const(self.__lexema,  self.__VC_Table)
		if(self.match(",", 1) == True):
			# Limpa o dicionario de tokens
			self.__lexema["valor"]  = {}
			self.__VC_Table["nome"] = ""
			self.__VC_Table["init"] = None
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da constante
				self.__VC_Table["nome"]  = self.__currentToken["token"]
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
						# Armazena o valor recebido para inicializacao
						self.__VC_Table["init"]  = True
						self.__lexema["tipo"]    = self.__currentToken
						self.__currentToken      = self.next_token()
						self.declaration_const2()
						return
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor para atribuição.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
							self.__error1_const()
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["="])
						self.__error1_const()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error1_const()
		elif(self.match(";", 1) == True):
			self.__lexema   = {}
			self.__VC_Table = {}
			self.__currentToken = self.next_token()
			self.declaration_const1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' , ';'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [",", ";"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["{"])
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__currentToken["token"] == "funcao"):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'variaveis'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["variaveis"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error1_var()
		elif(self.match("}", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando identificador ou token '}' or tipo primitivo.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["}", "inteiro", "real", "verdadeiro", "falso", "char", "cadeia", "vazio"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
					self.__error1_var()
		elif(self.__functions_aux.First("vector_matrix", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.vector_matrix()
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.declaration_var3()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '=', '[' , ',' , ';'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["=", "[", ",", ";"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [",", ";"])
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
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
						self.__error_vector_matrix()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token numérico.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["NRO"])
					self.__error_vector_matrix() 
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["["])
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
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
						self.__error_vector_matrix()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token numérico.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["NRO"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["[", "=", ",", ";"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["="])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["["])
				self.__error_vector_matrix()  

	# <init_matrix_1>   ::=     <value_with_IDE> <init_matrix_2>
	def init_matrix_1(self):
		if(self.__functions_aux.First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.init_matrix_2()
			return 
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor para inicialização.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["," , "]"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["["])
				self.__error_vector_matrix()  

	# <init_vector_1>   ::=     <value_with_IDE> <init_vector_2>
	def init_vector_1(self):
		if(self.__functions_aux.First("value_with_IDE", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.init_vector_2()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor para inicialização.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
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
			self.__erros += 1
			self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [",", "]"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["["])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
							return
						else:
							self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador ou numero.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO"])
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
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
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
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [".", "]"])
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
			return # vazio

	# =======================================================================================
	# === Gramatica para o comando escreva ==================================================
	# <write_cmd>   ::= escreva '(' <write_value> <write_value_list> ')' ';'
	def write_cmd(self):
		if(self.match("escreva", 1)):
			self.__currentToken = self.next_token()
			if(self.match("(", 1)):
				self.__currentToken = self.next_token()
				self.write_value()
				self.write_value_list()
				if(self.match(")", 1)):
					self.__currentToken = self.next_token()
					if(self.match(";", 1)):
						self.__currentToken = self.next_token()
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [";"])
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
						self.__error2escreva()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["("])
					self.__error1escreva()

	# <write_value_list> ::= ',' <write_value> <write_value_list> |
	def write_value_list(self):
		if(self.match(",", 1)):
			self.__currentToken = self.next_token()
			self.write_value()
			self.write_value_list()
		else:
			return # Vazio

	# <write_value>      ::= id <write_value_1> | number | cad | char
	def write_value(self):
		if(self.match("NRO", 2) == True or self.match("CAR", 2) == True or self.match("CAD", 2) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.write_value_1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor identificador, número, cadeia ou caracteres.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE", "NRO", "CAD", "CAR"])
				self.__error3escreva()
	
	# <write_value_1>    ::= <v_m_access> | <elem_registro> |
	def write_value_1(self):
		if(self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.v_m_access()
			return
		elif(self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.elem_registro()
			return
		else:
			return # Vazio


	# =======================================================================================
	# === Gramatica para o comando leia ====================================================
	# <read_cmd> ::= leia '(' <read_value> <read_value_list> ')' ';'
	def read_cmd(self):
		if(self.match("leia", 1)):
			self.__currentToken = self.next_token()
			if(self.match("(", 1)):
				self.__currentToken = self.next_token()
				self.read_value()
				self.read_value_list()
				if(self.match(")", 1)):
					self.__currentToken = self.next_token()
					if(self.match(";", 1)):
						self.__currentToken = self.next_token()
					else:
						if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [";"])
				else:
					if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
						self.__error2leia()
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["("])
					self.__error1leia()

	# <read_value_list> ::= ',' <read_value> <read_value_list> |
	def read_value_list(self):
		if(self.match(",", 1)):
			self.__currentToken = self.next_token()
			self.read_value()
			self.read_value_list()
		else:
			return # Vazio

	# <read_value>      ::= id <read_value_1>
	def read_value(self):
		if(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.read_value_1()
			return
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
				self.__error3leia()
	
	# <read_value_1>    ::= <v_m_access> | <elem_registro> |
	def read_value_1(self):
		if(self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.v_m_access()
			return
		elif(self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.elem_registro()
			return
		else:
			return # Vazio
	# =========================================================================================
	# =========================================================================================

	# ========================================================================================
	# === Gramatica para atribuicoes de variaveis ============================================
	# <var_atr>   ::= id <var_atr_1> 
	def var_atr(self):
		if(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.var_atr_1()
			return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
				self.__error_var_atr()
				return
	
	# <var_atr_1> ::= <atr> | <v_m_access> <atr> | <elem_registro> <atr> 
	def var_atr_1(self):
		if(self.__functions_aux.First("atr", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.atr()
			return
		elif(self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.v_m_access()
			self.atr()
			return
		elif(self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.elem_registro()
			self.atr()
			return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '=', '[' , '.'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["=", "[", "."])
				self.__error_var_atr()
				return
	
	# <atr>       ::= '=' <atr_1>
	def atr(self):
		if(self.match("=", 1) == True):
			self.__currentToken = self.next_token()
			self.atr_1()
			return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["="])
				self.__error_var_atr()
				return

	# <atr_1>     ::= number <atr_2> | boolean <atr_2> | cad <atr_2> | char <atr_2> | <expressao> <atr_2> | id <functionCall>
	def atr_1(self):
		if(self.match("NRO", 2) == True or self.match("verdadeiro", 1) == True or self.match("falso", 1) == True or self.match("CAD", 2) == True or self.match("CAR", 2) == True):
			self.__currentToken = self.next_token()
			self.atr_2()
		elif(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			self.expressao() # expressao pode ser um unico identificador
			if(self.__functions_aux.First("functionCall", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
				self.functionCall()
				return
			else:
				self.atr_2()
				return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando valor para atribuição.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO","CAR","CAD","verdadeiro","falso"])
				self.__error_var_atr()
				return

	# <atr_2> ::= ',' <var_atr> | ';'
	def atr_2(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			self.var_atr()
			return
		elif(self.match(";", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' , ';' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [",", ";"])
				self.__error_var_atr()
				return
	# =========================================================================================
	# =========================================================================================

	# =======================================================================================
	# === Gramática para declaração de função ==================================================
	# <function_declaration>  ::= funcao <type> <function_declaration1>
	def function_declaration(self):
		if(self.match("funcao", 1) == True):
			self.__currentToken = self.next_token()
			if(self.__functions_aux.First("type", self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.__currentToken = self.next_token()
				self.function_declaration1()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo de retorno'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['IDE','inteiro', 'real', 'verdadeiro', 'falso', 'char', 'cadeia', 'vazio'])
					self.__error_function_declaration()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'funcao'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['funcao'])
				self.__error_function_declaration()

	# <function_declaration1> ::= algoritmo <main_function> | <function_declaration2>
	def function_declaration1(self):
		if(self.match("algoritmo", 1) == True):
			self.__currentToken = self.next_token()
			self.main_function()
		elif(self.__functions_aux.First("function_declaration2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.function_declaration2()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador ou 'algoritmo'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['IDE', 'algoritmo'])
				self.__error2_function_declaration()

	# <function_declaration2> ::= id <function_parameters> '{' <function_body> '}' <function_declaration>
	def	function_declaration2(self):
		if(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.function_parameters()
			if(self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.function_body()
				if(self.match("}", 1) == True):
					self.__currentToken = self.next_token()
					self.function_declaration()
				else:
					if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
						self.function_declaration()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
					self.__error3_function_declaration()

	# <function_parameters>   ::= '(' <function_parameters1>
	def function_parameters(self):
		if(self.match("(", 1) == True):
			self.__currentToken = self.next_token()
			self.function_parameters1()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
				self.__error3_function_declaration()

	# <function_parameters1>  ::= <function_parameters2> id <function_parameters3> | ')'
	def function_parameters1(self):
		if(self.__functions_aux.First("function_parameters2", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.function_parameters2()
			if(self.match("IDE", 2) == True):
				self.__currentToken = self.next_token()
				self.function_parameters3()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['IDE'])
					self.__error3_function_declaration()
		elif(self.match(")", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo primitivo, identificador ou token ')'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [')','IDE','inteiro', 'real', 'verdadeiro', 'falso', 'char', 'cadeia', 'vazio'])
				self.__error3_function_declaration()

	# <function_parameters2>  ::=      <primitive_type>        | id
	def function_parameters2(self):
		if(self.__functions_aux.First("primitive_type", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando tipo primitivo ou identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['IDE','inteiro', 'real', 'verdadeiro', 'falso', 'char', 'cadeia', 'vazio'])
				self.__error3_function_declaration()

	# <function_parameters3>  ::= '['']' <function_parameters4>  | <function_parameters5>
	def function_parameters3(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("]", 1) == True):
				self.__currentToken = self.next_token()
				self.function_parameters4()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [']'])
					self.__error3_function_declaration()
		elif(self.__functions_aux.First("function_parameters5", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.function_parameters5()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '[', ',' , ')'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['[',',',')'])
				self.__error3_function_declaration()

	# <function_parameters4>  ::= '['']' <function_parameters5>  | <function_parameters5>
	def function_parameters4(self):
		if(self.match("[", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("]", 1) == True):
				self.__currentToken = self.next_token()
				self.function_parameters5()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [']'])
					self.__error3_function_declaration()
		elif(self.__functions_aux.First("function_parameters5", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.function_parameters5()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '[', ',' , ')'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['[',',',')'])
				self.__error3_function_declaration()

	# <function_parameters5>  ::= ','  <function_parameters1>  | ')'
	def function_parameters5(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			self.function_parameters1()
		elif(self.match(")", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ')'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [',',')'])
				self.__error3_function_declaration()
	# =======================================================================================
	# =======================================================================================
	

	# =======================================================================================
	# === Gramática para chamada de função ==================================================
	# <functionCall> ::= '(' <varList0>
	def functionCall(self):
		if(self.match("(", 1) == True):
			self.__currentToken = self.next_token()
			self.varList0()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
				self.__error_functionCall()

	# <varList0>     ::= <value_without_IDE> <varList2> | id <varList1> | ')' ';'
	def varList0(self):
		if(self.__functions_aux.First("value_without_IDE",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.varList2()
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.varList1()
		elif(self.match(")", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando ';'\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [';'])
					self.__error_functionCall()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando 'tipo primitivo', 'id' , ',' ou ')'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [',',')','IDE','inteiro', 'real', 'verdadeiro', 'falso', 'char', 'cadeia', 'vazio'])
				self.__error_functionCall()

	# <varList1>     ::= <varList2>     | <v_m_access> <varList2> | <elem_registro> <varList2>
	def varList1(self):
		if(self.__functions_aux.First("varList2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.varList2()
		elif(self.__functions_aux.First("v_m_access",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.v_m_access()
			self.varList2()
		elif(self.__functions_aux.First("elem_registro",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.elem_registro()
			self.varList2()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou '[' ou '.'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [',','[','.'])
				self.__error_functionCall()

	# <varList2>     ::= ',' <varList0> | ')' ';'
	def varList2(self):
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			self.varList0()
		elif(self.match(")", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match(";", 1) == True):
				self.__currentToken = self.next_token()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [';'])
					self.__error_functionCall()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ',' ou ')'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [',',')'])
				self.__error_functionCall()
	# =========================================================================================
	# =========================================================================================
	
	# <main_function> ::= <function_parameters> '{' <function_body> '}'
	def main_function(self):
		if(self.__functions_aux.First("function_parameters",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.function_parameters()
			if(self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.function_body()
				if(self.match("}", 1) == True):
					self.__currentToken = self.next_token()
				else:
					if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
	# =========================================================================================
	# =========================================================================================

	# == Gramatica para o loop ENQUANTO =======================================================
	# == Somente deve ser usada expressoes logicas, relacionais ou variaveis do tipo booleano.
	# =========================================================================================	
	# <com_enquanto> ::= enquanto '(' <args> ')' '{' <com_body> '}'
	def com_enquanto(self):
		if(self.match("enquanto", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("(", 1) == True):
				self.__currentToken = self.next_token()
				self.args()
				if(self.match(")", 1) == True):
					self.__currentToken = self.next_token()
					if(self.match("{", 1) == True):
						self.__currentToken = self.next_token()
						self.com_body()
						if(self.match("}", 1) == True):
							self.__currentToken = self.next_token()
						else:
							if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
								print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
								self.__erros += 1
								self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
								self.__error_com_enquanto_e_com_para()
					else:
						if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
							self.__error_com_enquanto_e_com_para()
				else:
					if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [')'])
						self.__error_com_enquanto_e_com_para()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
					self.__error_com_enquanto_e_com_para()

	# <args> ::= <expressao> |
	def args(self):
		if(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.expressao()
			return
		else:
			return # vazio
	# =========================================================================================
	# =========================================================================================	

	# == Gramatica para o loop PARA ===========================================================
	# =========================================================================================
	# <com_para> ::= para '(' <init> <stop> ';' <step> ')' '{' <com_body> '}'
	def com_para(self):
		if(self.match("para",1) == True):
			self.__currentToken = self.next_token()
			if(self.match("(",1) == True):
				self.__currentToken = self.next_token()
				self.init()
				self.stop()
				if(self.match(";",1) == True):
					self.__currentToken = self.next_token()
					self.step()
					if(self.match(")",1) == True):
						self.__currentToken = self.next_token()
						if(self.match("{",1) == True):
							self.__currentToken = self.next_token()
							self.com_body()
							if(self.match("}",1) == True):
								self.__currentToken = self.next_token()
								return
							else:
								if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
									print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
									self.__erros += 1
									self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
									self.__error_com_enquanto_e_com_para()
						else:
							if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
								print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
								self.__erros += 1
								self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
								self.__error_com_enquanto_e_com_para()
					else:
						if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [')'])
							self.__error_com_enquanto_e_com_para()
				else:
					if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [';'])
						self.__error_com_enquanto_e_com_para()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
					self.__error_com_enquanto_e_com_para()

	# <init> ::= <var_atr> | ';'
	def init(self):
		if(self.__functions_aux.First("var_atr", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.var_atr()
		elif(self.match(";",1) == True):
			self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'ou identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['IDE',';'])
				self.__error_com_enquanto_e_com_para()

	# <stop> ::= <expressao> |
	def stop(self):
		if(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.expressao()
			return
		else:
			return # vazio

	# <step> ::= <expressao> |
	def step(self):
		if(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.expressao()
			return
		else:
			return # vazio
	# =========================================================================================
	# =========================================================================================	
	# == Gramática para o comando se e senao ==================================================
	# =========================================================================================	
	# <se>                ::= 'se' '(' <expressao> ')' '{' <com_body> '}' <se_body>  
	def se(self):
		if(self.match("se", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("(", 1) == True):
				self.__currentToken = self.next_token()
				self.expressao()
				if(self.match(")", 1) == True):
					self.__currentToken = self.next_token()
					if(self.match("{", 1) == True):
						self.__currentToken = self.next_token()
						self.com_body()
						if(self.match("}", 1) == True):
							self.__currentToken = self.next_token()
							self.se_body()
							return
						else:
							if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
								print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
								self.__erros += 1
								self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
								self.__error4sesenao()
					else:
						if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
							print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '{'.\n")
							self.__erros += 1
							self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
							self.__error3sesenao()
				else:
					if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
						print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
						self.__erros += 1
						self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [')'])
						self.__error2sesenao()
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '('.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['('])
					self.__error1sesenao()

	# <se_body>           ::= <senao> | <>
	def se_body(self):
		if(self.__functions_aux.First("senao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.senao()
		else:
			return # Vazio

	# <senao>             ::= 'senao' <se_senao>
	def senao(self):
		if(self.match("senao", 1) == True):
			self.__currentToken = self.next_token()
			self.se_senao()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'senao'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['senao'])
				self.__error5sesenao()

	# <se_senao>          ::= <se> | '{' <com_body> '}' 
	def se_senao(self):
		if(self.__functions_aux.First("se", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.se()
		elif(self.match("{", 1) == True):
			self.__currentToken = self.next_token()
			self.com_body()
			if(self.match("}",1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '}'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['}'])
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'se' ou '{'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['{'])
				self.__error3sesenao()
	# =========================================================================================
	# =========================================================================================
	
	# =========================================================================================
	# == Gramatica para o corpo de comandos ===================================================
	# <com_body>        ::= <com_enquanto> <com_body> | <com_para> <com_body> | <se> <com_body> | <write_cmd> <com_body> | <read_cmd> <com_body> | 'id' <com_body_1> <com_body> | <com_retornar>
	def com_body(self):
		if(self.__functions_aux.First("com_enquanto", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.com_enquanto()
			self.com_body()
		elif(self.__functions_aux.First("com_para", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.com_para()
			self.com_body()
		elif(self.__functions_aux.First("se", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.se()
			self.com_body()
		elif(self.__functions_aux.First("write_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.write_cmd()
			self.com_body()
		elif(self.__functions_aux.First("read_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.read_cmd()
			self.com_body()
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.com_body_1()
			self.com_body()
		elif(self.__functions_aux.First("com_retornar", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.com_retornar()
		else:
			return # vazio

	# <com_body_1> ::= <functionCall> | <var_atr_1>
	def com_body_1(self):
		if(self.__functions_aux.First("functionCall", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.functionCall()
		elif(self.__functions_aux.First("var_atr_1", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.var_atr_1()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '(' ou '='.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['(','='])
				self.__error_function_body2()

	# <com_retornar> ::= retorno <com_retornar1> ';' | <>
	def com_retornar(self):
		if(self.match("retorno", 1) == True):
			self.__currentToken = self.next_token()
			self.com_retornar1()
			if(self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [';'])
		else:
			return # vazio

	# <com_retornar1> ::= <value_with_expressao> | <>
	def com_retornar1(self):
		if(self.__functions_aux.First("value_with_expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.value_with_expressao()
			return
		else:
			return # vazio
	# =========================================================================================
	# =========================================================================================

	def value_with_expressao(self):
		if(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.expressao()
			return
		elif(self.match("CAD", 2) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("CAR", 2) == True):
			self.__currentToken = self.next_token()
			return

	# =========================================================================================
	# == Gramatica para o corpo de funcao ===================================================
	# <function_body>         ::= <declaration_const> <function_body1> | <function_body1>
	def function_body(self):
		if(self.__functions_aux.First("declaration_const", self.__currentToken["token"], self.__currentToken["sigla"]) == True):	
			self.declaration_const()
			self.function_body1()
			return
		elif(self.__functions_aux.First("function_body1", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.function_body1()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'constantes' ou 'variaveis' ou restante do corpo da funcao.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["constantes", "variaveis", "enquanto", "para", "se", "escreva", "leia", "IDE","retorno"])
				self.__error_function_body()
	
	# <function_body1>        ::= <declaration_var>   <function_body2> | <function_body2>
	def function_body1(self):
		if(self.__functions_aux.First("declaration_var", self.__currentToken["token"], self.__currentToken["sigla"]) == True):	
			self.declaration_var()
			self.function_body2()
			return
		elif(self.__functions_aux.First("function_body2", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.function_body2()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'variaveis' ou restante do corpo da funcao.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["variaveis", "enquanto", "para", "se", "escreva", "leia", "IDE","retorno"])
				self.__error_function_body()		
	
	# <function_body2>        ::= <com_enquanto> <function_body2>  | <com_para> <function_body2>   | <se> <function_body2>
    # | <write_cmd> <function_body2> | <read_cmd> <function_body2> | <com_body_1> <function_body2> | <retornar>
	def function_body2(self):
		if(self.__functions_aux.First("com_enquanto", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.com_enquanto()
			self.function_body2()
		elif(self.__functions_aux.First("com_para", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.com_para()
			self.function_body2()
		elif(self.__functions_aux.First("se", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.se()
			self.function_body2()
		elif(self.__functions_aux.First("write_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.write_cmd()
			self.function_body2()
		elif(self.__functions_aux.First("read_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.read_cmd()
			self.function_body2()
		elif(self.match("IDE", 2) == True):
			self.__currentToken = self.next_token()
			self.com_body_1()
			self.function_body2()
		elif(self.__functions_aux.First("com_retornar", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.retornar()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token 'retorno' ou algum comando.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["enquanto", "para", "se", "escreva", "leia", "IDE","retorno"])
				self.__error_function_body2()

	# <retornar> ::= retorno <retornar1> ';'
	def retornar(self):
		if(self.match("retorno", 1) == True):
			self.__currentToken = self.next_token()
			self.retornar1()
			if(self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ';'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [";"])
					self.__error_function_body()

	# <retornar1> ::= cad | char | <expressao> | <>
	def retornar1(self):
		if(self.match("CAD", 2) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("CAR", 2) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.expressao()
		else:
			return # vazio
	# =========================================================================================
	# =========================================================================================
	
	# =================================================================================================
	# === Gramática para expressões numericas =========================================================
	# <exprNumber>   ::= <exprArt> | '(' <exprNumber> ')' <exprMultiPos> <exprNumber1>
	def exprNumber(self):
		if(self.__functions_aux.Follow("exprArt", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.exprArt()
		elif(self.match("(", 1) == True):
			self.__currentToken = self.next_token()
			self.exprNumber()
			if(self.match(")", 1) == True):
				self.__currentToken = self.next_token()
				self.exprMultiPos()
				self.exprNumber1()
			else:
				if (self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
					self.__erro1expr()
		else:
			if (self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando um número ou token '(', '+', '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["(","+","-"])
				self.__erro1expr()

	# <exprNumber1>  ::= <operatorSoma> <exprNumber> | <>
	def exprNumber1(self):
		if (self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.operatorSoma()
			self.exprNumber()
		else:
			return # vazio

	# =======================================================================================
	# === Gramática para expressões aritméticas =============================================
	# <exprValorMod> ::=  number | <operatorAuto0> <read_value> | <read_value> <operatorAuto>
	def exprValorMod(self):
		if(self.match("NRO", 2) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.__functions_aux.First("operatorAuto0", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.read_value()
		elif(self.__functions_aux.First("read_value", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.read_value()
			self.operatorAuto()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '++', '--'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["++", "--"])
				self.__erro1expr()

	# <exprMulti> ::= <operatorSoma> <exprValorMod> <exprMultiPos> | <exprValorMod> <exprMultiPos> | '(' <exprNumber>
	def exprMulti(self):
		if(self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.exprValorMod()
			self.exprMultiPos()
		elif(self.__functions_aux.Follow("exprValorMod",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
			self.exprValorMod()
			self.exprMultiPos()
		elif(self.__functions_aux.Follow("exprNumber",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
			self.exprNumber()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '+', '-', '++', '--' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--"])
				self.__erro1expr()

	# <exprArt>   ::= <exprMulti> <expr1>
	def exprArt(self):
		self.exprMulti()
		self.expr1()

	# <exprMultiPos> ::= <operatorMulti> <exprMulti> | <>
	def exprMultiPos(self):
		if(self.__functions_aux.First("operatorMulti", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.operatorMulti()
			self.exprMulti()
		else:
			return # vazio

	# <expr1> ::= <operatorSoma> <exprNumber> | <>
	def expr1(self):
		if(self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.operatorSoma()
			self.exprNumber()
		else:
			return # vazio

	# <operatorSoma> ::= '+' | '-'
	def operatorSoma(self):
		if(self.match("+", 1) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("-", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '+' ou '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+", "-"])
				self.__erro1expr()

	# <operatorMulti> ::= '*' | '/'
	def operatorMulti(self):
		if(self.match("*", 1) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("/", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '*' ou '/'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["*", "/"])
				self.__erro1expr()

	# <operatorAuto0> ::= '++' | '--'
	def operatorAuto0(self):
		if(self.match("++", 1) == True):
			self.__currentToken = self.next_token()
			return
		elif(self.match("--", 1) == True):
			self.__currentToken = self.next_token()
			return
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '+' ou '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+", "-"])
				self.__erro1expr()

	# <operatorAuto> ::= '++' | '--' | <>
	def operatorAuto(self):
		if(self.match("++", 1) == True):
			self.__currentToken = self.next_token()
		elif(self.match("--", 1) == True):
			self.__currentToken = self.next_token()
		else:
			return # vazio

	# =======================================================================================
	# === Gramática para expressões relacionais =============================================
	# <exprRel0>   ::= <exprRel> | '(' <expressao> ')'
	def exprRel0(self):
		if(self.__functions_aux.Follow("exprRel", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.exprRel()
		elif(self.match("(", 1) == True):
			self.__currentToken = self.next_token()
			self.expressao()
			if(self.match(")", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
					self.__erro1expr()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número, identificador ou token '+', '-', '++', '--', 'verdadeiro', 'falso' ou '('.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--","verdadeiro","falso","("])
				self.__erro1expr()

	# <exprRel>   ::= <exprArt> <exprRel1> | boolean <exprRel1>
	def exprRel(self):
		if(self.__functions_aux.Follow("exprArt", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.exprArt()
			self.exprRel1()
		elif(self.match("verdadeiro", 1) == True or self.match("falso", 1) == True):
			self.__currentToken = self.next_token()
			self.exprRel1()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '+', '-', '++', '--', 'verdadeiro', 'falso' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--","verdadeiro","falso"])
				self.__erro1expr()

	# <exprRel1> ::= <operatorRel> <exprRel0> | <>
	def exprRel1(self):
		if(self.__functions_aux.First("operatorRel", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.operatorRel()
			self.exprRel0()
		else:
			return

	# <operatorRel> ::= '==' | '>=' | '<=' | '!=' | '>' | '<'
	def operatorRel(self):
		if (self.match("==", 1) == True):
			self.__currentToken = self.next_token()
		elif (self.match(">=", 1) == True):
			self.__currentToken = self.next_token()
		elif (self.match("<=", 1) == True):
			self.__currentToken = self.next_token()
		elif (self.match("!=", 1) == True):
			self.__currentToken = self.next_token()
		elif (self.match(">", 1) == True):
			self.__currentToken = self.next_token()
		elif (self.match("<", 1) == True):
			self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '==', '>=', '<=', '!=', '>' ou '<'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['==', '>=', '<=', '!=', '>','<'])
				self.__erro1expr()

	# =======================================================================================
	# === Gramática para expressões lógicas =================================================
	# <expressao>   ::= <exprRel> <exprLog1> | '(' <expressao> ')' <exprLog2> | '!' <expressao>
	def expressao(self):
		if(self.__functions_aux.Follow("exprRel", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			self.exprRel()
			self.exprLog1()
		elif(self.match("(", 1) == True):
			self.__currentToken = self.next_token()
			self.expressao()
			if(self.match(")", 1) == True):
				self.__currentToken = self.next_token()
				self.exprLog2()
		elif(self.match("!", 1) == True):
			self.__currentToken = self.next_token()
			self.expressao()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '(', '!', , 'verdadeiro', 'falso' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","(", "!", "verdadeiro","falso"])
				self.__erro1expr()

	# <exprLog1> ::=  <operatorLog> <expressao> | <>
	def exprLog1(self):
		if(self.__functions_aux.First("operatorLog", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.operatorLog()
			self.expressao()
		else:
			return # vazio

	# <exprLog2> ::= <operatorLog> <expressao> | <operatorMulti> <expressao> | <operatorRel> <expressao> | <operatorSoma> <expressao> | <>
	def exprLog2(self):
		if (self.__functions_aux.First("operatorLog", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.expressao()
		elif (self.__functions_aux.First("operatorMulti", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.expressao()
		elif (self.__functions_aux.First("operatorRel", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.expressao()
		elif (self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentToken = self.next_token()
			self.expressao()
		else:
			return

	# <operatorLog> ::= '&&' | '||'
	def operatorLog(self):
		if(self.match("&&", 1) == True):
			self.__currentToken = self.next_token()
		elif(self.match("||", 1) == True):
			self.__currentToken = self.next_token()
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '&&' ou '||'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["&&", "||"])
				self.__erro1expr()

	# =======================================================================================
	# =======================================================================================

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
				self.declaration_var()
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
				self.function_declaration()
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
				self.function_declaration()
				return
			elif(self.__currentToken["token"] == "funcao"):
				return
			else:
				self.__currentToken = self.next_token()


	def __error_functionCall(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			# O conjunto Primeiro de <function_body2> e <com_body> sao iguais.
			# Por isso, so verifico um deles. 
			if(self.__functions_aux.First("function_body2",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				if(self.__currentToken["sigla"] == "IDE"):
					verificar = self.next_token()
					if(self.__functions_aux.First("functionCall", verificar['token'], verificar['sigla']) == True or self.__functions_aux.First("var_atr_1", verificar['token'], verificar['sigla']) == True):
						self.match("IDE",2)
						self.__currentToken = verificar
						self.com_body_1()
						return
					else: # Pega o proximo token porque esse identificador e uma variavel sendo passada como parametro
						self.__currentToken = verificar
				else:		
					self.function_body2()
					return
			else:
				self.__currentToken = self.next_token()


	# ERROR para a gramatica de atribuicao de variaveis
	def __error_var_atr(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			# O conjunto Primeiro de <function_body2> e <com_body> sao iguais.
			# Por isso, so verifico um deles. 
			if(self.__functions_aux.First("function_body2",self.__currentToken['token'], self.__currentToken['sigla']) == True):	
				self.function_body2()
				return
			else:
				self.__currentToken = self.next_token()


	# ERROR para a gramatica do corpo das funcoes
	def __error_function_body(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__currentToken["token"] == "funcao"):	
				self.function_declaration()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica do corpo das funcoes
	def __error_function_body2(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__functions_aux.First("com_enquanto",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("com_para",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("se",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("write_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("read_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__currentToken["token"] == "retorno"):
				self.retornar()
				return
			elif(self.__currentToken["token"] == "constantes"):
				self.declaration_const()
				self.function_body2()
				return
			elif(self.__currentToken["token"] == "variaveis"):
				self.declaration_var()
				self.function_body2()
				return
			elif(self.__currentToken["token"] == "funcao"):
				self.function_declaration()
				self.function_body2()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica de declaracao de funcoes
	def __error_function_declaration(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__functions_aux.First("function_declaration1",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_declaration1()
				return
			elif(self.__currentToken["token"] == "("):
				self.function_parameters()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica de declaracao de funcoes
	def __error2_function_declaration(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__currentToken["token"] == "("):
				self.function_parameters()
				return
			elif(self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.function_body()
				return
			elif(self.__functions_aux.First("com_enquanto",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("com_para",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("se",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("write_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("read_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__currentToken["token"] == "retorno"):
				self.retornar()
				return
			else:
				self.__currentToken = self.next_token()


	# ERROR para a gramatica de declaracao de funcoes
	def __error3_function_declaration(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.match(")",1) == True):
				self.__currentToken = self.next_token()
				return
			elif(self.__currentToken["token"] == "{"):
				return
			elif(self.__functions_aux.First("com_enquanto",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("com_para",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("se",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("write_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__functions_aux.First("read_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				self.function_body2()
				return
			elif(self.__currentToken["token"] == "retorno"):
				self.retornar()
				return
			else:
				self.__currentToken = self.next_token()


	def __error_elem_registro(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__functions_aux.Follow("elem_registro",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica de declaracao do Loop Enquanto e Para
	# Procura por outro comando
	def __error_com_enquanto_e_com_para(self):
		while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise
			if(self.__functions_aux.First("com_enquanto",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			elif(self.__functions_aux.First("com_para",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			elif(self.__functions_aux.First("se",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			elif(self.__functions_aux.First("write_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			elif(self.__functions_aux.First("read_cmd",self.__currentToken['token'], self.__currentToken['sigla']) == True):
				return
			elif(self.__currentToken["token"] == "retorno"):
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica comando leia
	def __error1leia(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__currentToken["sigla"] == "IDE"):
				self.read_value()
				return
			else:
				self.__currentToken = self.next_token()

	def __error2leia(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				self.__currentToken = self.next_token()

	def __error3leia(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if(self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
				self.read_value_1()
				return
			elif(self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
				self.read_value_1()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica do comando escreva
	def __error1escreva(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__currentToken["sigla"] == "IDE"):
				self.write_value()
				return
			elif (self.__currentToken["sigla"] == "NRO"):
				self.write_value()
				return
			elif (self.__currentToken["token"] == ","):
				self.write_value_list()
				return
			else:
				self.__currentToken = self.next_token()

	def __error2escreva(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.match(";", 1) == True):
				self.__currentToken = self.next_token()
				return
			else:
				self.__currentToken = self.next_token()

	def __error3escreva(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.write_value_1()
				return
			elif (self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.write_value_1()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica do se e se não
	def __error1sesenao(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__functions_aux.Follow("exprRel", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.expressao()
				return
			elif (self.__currentToken["token"] == "("):
				self.expressao()
				return
			elif (self.__currentToken["token"] == "!"):
				self.expressao()
				return
			else:
				self.__currentToken = self.next_token()

	def __error2sesenao(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.match("{", 1) == True):
				self.__currentToken = self.next_token()
				self.com_body()
				return
			else:
				self.__currentToken = self.next_token()

	def __error3sesenao(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if(self.__functions_aux.First("com_enquanto", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			elif(self.__functions_aux.First("com_para", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			elif(self.__functions_aux.First("se", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			elif(self.__functions_aux.First("write_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			elif(self.__functions_aux.First("read_cmd", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			elif(self.__currentToken["sigla"] == "IDE"):
				self.com_body()
				return
			elif(self.__functions_aux.First("com_retornar", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.com_body()
				return
			else:
				self.__currentToken = self.next_token()

	def __error4sesenao(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__functions_aux.First("senao", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.se_body()
				return
			else:
				self.__currentToken = self.next_token()

	def __error5sesenao(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__functions_aux.First("se", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
				self.se_senao()
				return
			elif (self.__currentToken["token"] == "{"):
				self.se_senao()
				return
			else:
				self.__currentToken = self.next_token()

	# ERROR para a gramatica de expressões
	def __erro1expr(self):
		while (self.__currentToken["token"] != ""):  # enquanto existem tokens para analise
			if (self.__currentToken["token"] == "enquanto"):
				self.com_body()
				return
			elif (self.__currentToken["token"] == "para"):
				self.com_body()
				return
			elif (self.__currentToken["token"] == "leia"):
				self.com_body()
				return
			elif (self.__currentToken["token"] == "escreva"):
				self.com_body()
				return
			elif(self.__currentToken["token"] == "se"):
				self.com_body()
				return
			elif(self.__currentToken["token"] == "senao"):
				self.com_body()
				return
			elif(self.__currentToken["token"] == "retorno"): 
				self.com_body()
				return
			else:
				self.__currentToken = self.next_token()

