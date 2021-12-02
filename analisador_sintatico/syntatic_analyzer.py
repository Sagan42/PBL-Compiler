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
		# Tabela de simbolos usada na captura dos dados para a analise semantica de registros, variaveis e constantes 
		self.__Table      = {}
		# Atributo que armazena um dicionario de tokens especificos para auxiliar a analise semantica
		self.__lexema        = {}
		# Atributo que armazena um array contendo todos os tokens utilizados em uma expressao.
		self.__expr_lexema   = []
		# Atributo que armazena os tokens referentes as variaveis utilizadas nas expressoes.
		self.__expr_var      = {}
		# Atributo que armazena os tipos de cada variavel/constante e numero utilizada em um expressao (na ordem em que aparecem)
		self.__expr_type     = []
		self.__currentScope  = ""
		# Array para armazenar os valores usados na inicializacao de vetores e matrizes. Cada posicao consiste
		# em um token. Tais valores são armazenados na ordem em que são lidos da cadeia de entrada.
		self.__VM_value      = []
		# atributo que diz qual estrutura sintatica esta sendo analisada no momento. Ex: registros, constantes, ......
		self.__currentElement = ""

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
		# Pega o primeiro token
		self.__currentToken = self.next_token()
		self.__currentScope = "global"
		if(self.__functions_aux.First("declaration_reg",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			self.__currentElement = "registro"
			self.declaration_reg()
		# Limpa o lexema e a tabela de simbolos auxiliar para iniciar a analise de constantes
		self.__lexema   = {}
		self.__Table    = {}
		# Comeca a analise de constantes
		self.__currentElement = "constante"
		self.declaration_const()
		# Limpa o lexema e a tabela de simbolos auxiliar para iniciar a analise de variaveis
		self.__lexema   = {}
		self.__Table    = {}
		self.__currentElement = "variaveis"
		self.declaration_var()
		# Comeca a analise de funcoes
		self.__currentScope   = "local"
		self.__currentElement = "funcao"
		self.function_declaration()
		self.__semantic_analyzer.Print_st_var_const()
	# ============================================================================================
	# === Gramatica para declaracao de elementos do tipo registro ================================
	# <declaration_reg>    ::= registro id '{' <declaration_reg1> |
	def declaration_reg(self):
		if(self.match("registro", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena o nome do registro declarado.
				# check__add sera True caso o armazenamento seja feito com sucesso
				self.__Table["check_add"] = self.__semantic_analyzer.addRegistry(self.__currentToken)
				self.__Table["name"]      = self.__currentToken
				self.__currentToken       = self.next_token()
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
			print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
			# Armazena o tipo do atributo do registro em analise.
			self.__lexema["type"] = self.__currentToken
			self.__currentToken   = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena o nome do atributo do registro em analise.
				self.__lexema["name"] = self.__currentToken
				self.__currentToken   = self.next_token()
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
			# Armazena o tipo do atributo do registro em analise.
			self.__lexema["type"] = self.__currentToken
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena o nome do atributo do registro em analise.
				self.__lexema["name"] = self.__currentToken
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
		# Faz a analise semantica do atributo caso o registro tenha sido armazenado com sucesso
		if(self.__Table["check_add"] == True):
			if(self.__lexema["dimensao"] == None): # Caso nao seja vetor ou matriz
				self.__semantic_analyzer.analyzer_Registry_Atributes(False, self.__Table["name"], self.__lexema)
			else:
				self.__semantic_analyzer.analyzer_Registry_Atributes(True, self.__Table["name"], self.__lexema)
		if(self.match(",", 1) == True):
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				self.__lexema["dimensao"] = None
				# Armazena o nome do atributo do registro em analise.
				self.__lexema["name"] = self.__currentToken
				self.__currentToken   = self.next_token()
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
			# Limpa o dicionario para iniciar uma nova analise
			self.__lexema = {}
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
			# Atributo do registro nao e um vetor ou matriz
			self.__lexema["dimensao"] = None
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
			# Armazena o lexema que esta compondo a estrutura de acesso ao registro
			if(self.__currentElement == "atribuicao"):
				self.__lexema["name"] += self.__currentToken["token"]
			elif(self.__currentElement == "expressao"):
				self.__expr_var["name"] += self.__currentToken["token"]
				# Armazena no vetor lexema, os tokens que auxiliarao para analise semantica das expressoes
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena o lexema que esta compondo a estrutura de acesso ao registro
				if(self.__currentElement == "atribuicao"):
					self.__lexema["name"] += self.__currentToken["token"]
				elif(self.__currentElement == "expressao"):
					self.__expr_var["name"] += self.__currentToken["token"]
					# Armazena no vetor lexema, os tokens que auxiliarao para analise semantica das expressoes
					self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.nested_elem_registro()
				if(result):
					return True
				else:
					return False
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error_elem_registro()
				return False
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '.' \n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["."])
				self.__error_elem_registro()
			return False


	# <nested_elem_registro>  ::= '.' id <nested_elem_registro1> | <v_m_access> <nested_elem_registro1> |
	def nested_elem_registro(self):
		if(self.match(".", 1) == True):
			# Armazena o lexema que esta compondo a estrutura de acesso ao registro
			if(self.__currentElement == "atribuicao"):
				self.__lexema["name"] += self.__currentToken["token"]
			elif(self.__currentElement == "expressao"):
				self.__expr_var["name"] += self.__currentToken["token"]
				# Armazena no vetor lexema, os tokens que auxiliarao para analise semantica das expressoes
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena o lexema que esta compondo a estrutura de acesso ao registro
				if(self.__currentElement == "atribuicao"):
					self.__lexema["name"] += self.__currentToken["token"]
				elif(self.__currentElement == "expressao"):
					self.__expr_var["name"] += self.__currentToken["token"]
					# Armazena no vetor lexema, os tokens que auxiliarao para analise semantica das expressoes
					self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.nested_elem_registro1()
				if(result):
					return True
				else:
					return False
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
					self.__error_elem_registro()
				return False
		elif(self.__functions_aux.First("v_m_access",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.v_m_access()
			result_1 = self.nested_elem_registro1()
			return (result and result_1) # Caso uma das funcoes retorne Falso, o resultado final e Falso
		else:
			return True # Vazio

	# <nested_elem_registro1> ::= <elem_registro> |
	def nested_elem_registro1(self):
		if(self.__functions_aux.First("elem_registro",self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.elem_registro()
			if(result):
				return True
			else:
				return False
		else:
			return True # Vazio
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
			self.__Table["categoria"] = "constante"
			# Armazena o tipo utilizado na declaracao
			self.__Table["tipo"] = self.__currentToken["token"]
			# Nao sao declarados elementos compostos como Contantes
			self.__lexema["composto"] = False
			self.__lexema["tipo"]     = self.__currentToken
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da constante
				self.__Table["nome"]     = self.__currentToken["token"]
				# Como nao e vetor ou matriz, nao tem dimensao
				self.__Table["dimensao"] = None
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
						# Armazena o valor recebido para inicializacao
						self.__Table["init"]  = True
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
		self.__Table["escopo"] = self.__currentScope
		# Realiza analise semantica da constante declarada
		self.__semantic_analyzer.analyzer_var_const(False,self.__currentToken["linha"], self.__lexema, self.__Table)
		if(self.match(",", 1) == True):
			# Limpa o dicionario de tokens
			self.__lexema["valor"]  = {}
			self.__Table["nome"] = ""
			self.__Table["init"] = None
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da constante
				self.__Table["nome"]  = self.__currentToken["token"]
				self.__currentToken = self.next_token()
				if(self.match("=", 1) == True):
					self.__currentToken = self.next_token()
					if(self.__functions_aux.First("value",self.__currentToken['token'], self.__currentToken['sigla']) == True):
						print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
						# Armazena o valor recebido para inicializacao
						self.__Table["init"]  = True
						self.__lexema["valor"]   = self.__currentToken
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
			self.__Table = {}
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
			print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
			# Armazena o tipo utilizado na declaracao
			self.__Table["tipo"]     = self.__currentToken["token"]
			# Variavel pode ser um elemento composto
			if(self.__currentToken["sigla"] == "IDE"):
				self.__lexema["composto"] = True
			else:
				self.__lexema["composto"] = False
			self.__lexema["tipo"]     = self.__currentToken
			# Armazena a categoria que esta sendo analisada, constante ou variavel ou matriz ou array
			self.__Table["categoria"] = "variavel" 
			self.__Table["dimensao"]  = None
			self.__currentToken       = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da constante
				self.__Table["nome"]     = self.__currentToken["token"]
				self.__currentToken      = self.next_token()
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
				print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
				# Armazena o valor recebido para inicializacao
				self.__Table["init"]     = True
				self.__lexema["valor"]   = self.__currentToken
				self.__currentToken      = self.next_token()
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
			self.__Table["init"]     = False
			self.declaration_var3()
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + " . Esperando token '=', '[' , ',' , ';'\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["=", "[", ",", ";"])
				self.__error1_var()


	# <declaration_var3> ::= ',' id <declaration_var2>  | ';' <declaration_var1> 
	def declaration_var3(self):
		self.__Table["escopo"] = self.__currentScope
		# Realiza analise semantica da variavel declarada
		if(self.__Table["dimensao"] == None):
			# Nao e vetor ou matriz
			self.__semantic_analyzer.analyzer_var_const(False,self.__currentToken["linha"], self.__lexema,  self.__Table)
		else:
			# E vetor ou matriz
			self.__semantic_analyzer.analyzer_var_const(True,self.__currentToken["linha"], self.__lexema,  self.__Table)
		if(self.match(",", 1) == True):
			# Limpa o dicionario de tokens
			self.__Table["nome"]     = ""
			self.__Table["dimensao"] = None
			self.__Table["init"]     = None
			self.__lexema["valor"]      = {}
			self.__currentToken = self.next_token()
			if(self.match("IDE", 2) == True):
				# Armazena nome da variavel
				self.__Table["nome"]  = self.__currentToken["token"]
				self.__currentToken = self.next_token()
				self.declaration_var2()
		elif(self.match(";", 1) == True):
			self.__lexema       = {}
			self.__Table     = {}
			self.__VM_value     = []
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
				# Pega a quantidade de linhas. (Caso seja um vetor, corresponde a quantidade de posicoes)
				self.__Table["dimensao"] = str(self.__currentToken["token"])
				# Armazena a categoria que esta sendo analisada, constante ou variavel ou matriz ou array
				self.__Table["categoria"]   = "array"
				self.__currentToken         = self.next_token()
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
				# Pega a quantidade de colunas. (Corresponde a uma matriz)
				self.__Table["dimensao"] = self.__Table["dimensao"] + "x" + str(self.__currentToken["token"])
				# Armazena a categoria que esta sendo analisada, constante ou variavel ou matriz ou array
				self.__Table["categoria"]   = "matriz" 
				self.__currentToken         = self.next_token()
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
			# Inicializacao de um vetor
			self.__Table["init"]     = True
			self.__currentToken = self.next_token()
			self.init_vector()
			self.declaration_var3()
			return
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Sem inicializacao do vetor
			self.__Table["init"]     = False
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
			# Inicializacao de uma matriz
			self.__Table["init"]     = True
			self.__currentToken = self.next_token()
			self.init_matrix()
			self.declaration_var3() 
		elif(self.__functions_aux.First("declaration_var3", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Sem inicializacao da matrix
			self.__Table["init"]     = False
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
			print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
			# Armazena o token usado na inicializacao.
			self.__VM_value.append(self.__currentToken)			
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
			if(self.__currentToken["token"] == ";"):
				# Armazena o token ";" . Ele faz a separacao das linhas da matriz.
				self.__VM_value.append(self.__currentToken)	
			self.__currentToken = self.next_token()
			self.init_matrix_1()
			return 
		elif(self.match("]", 1) == True):
			# Encerra a inicializacao da matriz
			self.__Table["valor"] = self.__VM_value
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
			print("[INFO] Token aceito [" + self.__currentToken["sigla"] + "]  : \"" + self.__currentToken["token"] + "\" Linha: " + self.__currentToken["linha"])
			# Armazena o token usado na inicializacao.
			self.__VM_value.append(self.__currentToken)
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
			# Encerra a inicializacao do vetor
			self.__Table["valor"] = self.__VM_value
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
			if(self.__currentElement == "expressao"):
				self.__expr_var["dimensao"] = []
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
			elif(self.__currentElement == "atribuicao"):
				self.__lexema["dimensao"] = []
			elif(self.__currentElement == "registro"):
				self.__lexema["dimensao"] = ""
			self.__currentToken = self.next_token()
			result = self.v_m_access1()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '['.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["["])
				if(self.__functions_aux.First("v_m_access1") == True):
					self.v_m_access1()
					return False
				else:
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.match("]",1) == True):
							self.__currentToken = self.next_token()
							self.v_m_access3()
							return False
						else:
							self.__currentToken = self.next_token()
			return False

	# <v_m_access1>  ::= id  <v_m_access2>                    | number ']' <v_m_access3> 
	def v_m_access1(self):
		if(self.match("IDE", 2) == True):
			if(self.__currentElement == "atribuicao"):
				# adiciona o primeiro index de acesso ao elemento.
				self.__lexema["dimensao"].append(self.__currentToken)
			elif(self.__currentElement == "expressao"):
				self.__expr_var["dimensao"].append(self.__currentToken)
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken) 
			self.__currentToken = self.next_token()
			result = self.v_m_access2()
			if(result):
				return True
			else:
				return False
		elif(self.match("NRO", 2) == True):
			# Verifica se o elemento atual sendo analisado e um registro
			if(self.__currentElement == "registro"):
				# Armazena o numero de linhas caso seja matriz, ou tamanho do vetor
				self.__lexema["dimensao"] = self.__lexema["dimensao"] + str(self.__currentToken["token"])
			elif(self.__currentElement == "atribuicao"):
				# adiciona o primeiro index de acesso ao elemento.
				self.__lexema["dimensao"].append(self.__currentToken)
			elif(self.__currentElement == "expressao"):
				self.__expr_var["dimensao"].append(self.__currentToken)
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			if(self.match("]", 1) == True):
				if(self.__currentElement == "expressao"):
					# Adiciona o token ao vetor lexema, para analise semantica.
					self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.v_m_access3()
				if(result):
					return True
				else:
					return False
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
							return False
						else:
							self.__currentToken = self.next_token()
				return False
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando identificador ou numero.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","NRO"])
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.match("]",1) == True):
						self.__currentToken = self.next_token()
						self.v_m_access3()
						return False
					elif(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
						return False
					else:
						self.__currentToken = self.next_token()
			return False

	# <v_m_access2>  ::= <elem_registro> ']' <v_m_access3>    | ']'        <v_m_access3>
	def v_m_access2(self):
		if(self.__functions_aux.First("elem_registro", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			if(self.__currentElement == "atribuicao"):
				# Informa que esta sendo feita a tentativa de acesso a um vetor ou matriz atraves de um elemento composto.
				# E nao e permitido
				self.__lexema["dimensao"] = "composto"
			elif(self.__currentElement == "expressao"):
				self.__expr_var["dimensao"] = "composto"
			self.elem_registro()
			if(self.match("]", 1) == True):
				if(self.__currentElement == "expressao"):
					# Adiciona o token ao vetor lexema, para analise semantica.
					self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.v_m_access3()
				if(result):
					return True
				else:
					return False
			else:
				if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ']' \n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["]"])
					while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
						if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
							return False
						else:
							self.__currentToken = self.next_token()
				return False
		elif(self.match("]", 1) == True):
			if(self.__currentElement == "expressao"):
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.v_m_access3()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '.' ou ']'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [".", "]"])
				while(self.__currentToken["token"] != ""): # enquanto existem tokens para analise 
					if(self.__functions_aux.Follow("v_m_access",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
						return False
					else:
						self.__currentToken = self.next_token()
			return False
	
	# <v_m_access3>   ::= '[' <v_m_access1>
	def v_m_access3(self):
		if(self.match("[", 1) == True):
			# Verifica se o elemento atual sendo analisado e um registro
			if(self.__currentElement == "registro"):
				self.__lexema["dimensao"] = self.__lexema["dimensao"] + "x"
			elif(self.__currentElement == "expressao"):
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.v_m_access1()
			if(result):
				return True
			else:
				return False
		else:
			return True # vazio

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
			return True # Vazio

	# <read_value>      ::= id <read_value_1>
	def read_value(self):
		if(self.match("IDE", 2) == True):
			if(self.__currentElement == "expressao"):
				self.__expr_var["name"]     = self.__currentToken["token"]
				self.__expr_var["dimensao"] = None 
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.read_value_1()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0): # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token identificador.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE"])
				self.__error3leia()
	
	# <read_value_1>    ::= <v_m_access> | <elem_registro> |
	def read_value_1(self):
		if(self.__functions_aux.First("v_m_access", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			result = self.v_m_access()
			if(result):
				return True
			else:
				return False
		elif(self.__functions_aux.First("elem_registro", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
			result = self.elem_registro()
			if(result):
				return True
			else:
				return False
		else:
			return True # Vazio
	# =========================================================================================
	# =========================================================================================

	# ========================================================================================
	# === Gramatica para atribuicoes de variaveis ============================================
	# <var_atr>   ::= id <var_atr_1> 
	def var_atr(self):
		if(self.match("IDE", 2) == True):
			self.__currentElement     = "atribuicao"
			# Armazena o nome da variavel que estara recebendo um valor por meio da atribuicao.
			self.__lexema["name"]     = self.__currentToken["token"]
			self.__lexema["dimensao"] = None
			self.__currentToken   = self.next_token()
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
		self.__currentElement = "atribuicao"
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
			# Realiza a analise semantica do lador esquerdo da atribuicao
			# Retorna True caso a analise tenha sido feito com sucesso. Dando seguimento a analise semantica
			# do lado direito da atribuicao.
			result = self.__semantic_analyzer.left_Assignment(self.__currentToken["linha"],self.__lexema)
			if(result == False):
				# Limpa o dicionario
				self.__lexema = {}
			self.__currentToken = self.next_token()
			self.atr_1(result)
			return
		else:
			if(self.number_of_tokens() > 0):
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '='.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["="])
				self.__error_var_atr()
				return

	# versao 1:  <atr_1>     ::= number <atr_2> | boolean <atr_2> | cad <atr_2> | char <atr_2> | <expressao> <atr_2> | id <functionCall>
	# versao 2:  <atr_1>     ::= cad <atr_2> | char <atr_2> | <expressao> <functionCall> <atr_2>
	def atr_1(self, do_analysis):
		if(self.match("CAD", 2) == True or self.match("CAR", 2) == True):
			# Verifica se o lado direito da atribuicao sera analisada
			if(do_analysis == True):
				if(self.__currentToken["sigla"] == "CAD"):
					self.__lexema["entry"] = "cadeia"
				elif(self.__currentToken["sigla"] == "CAR"):
					self.__lexema["entry"] = "char"
				self.__semantic_analyzer.right_Assignment(False, self.__currentToken["linha"], self.__lexema, None, self.__lexema["dimensao"], self.__lexema["name"])
			self.__currentToken = self.next_token()
			self.atr_2()
		elif(self.__functions_aux.First("expressao", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):			
			result_expr = self.expressao() # expressao pode ser um unico identificador
			if(self.__functions_aux.First("functionCall", self.__currentToken["token"], self.__currentToken["sigla"] ) == True):
				self.functionCall()
				return
			else:
				# Se a expressao e valida sintaticamente e o lado esquerdo da atribuicao tambem e valido, logo a analise semantica da expressa
				# e realizada.
				if(result_expr == True and do_analysis == True):
					print("FAZ ANALISE DA EXPRESSAO!!!!")
					print(self.__expr_type)
					self.__semantic_analyzer.right_Assignment(True, self.__currentToken["linha"], self.__expr_lexema, self.__expr_type,self.__lexema["dimensao"], self.__lexema["name"])
					self.__expr_type = []
					#self.__semantic_analyzer.atr_expression_analyzer(self.__currentToken["linha"], self.__expr_lexema, self.__expr_type)
					self.__expr_lexema = []
				else:
					self.__expr_lexema = []
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
			# Limpa o dicionarioa para uma nova analise
			self.__lexema = {}
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
		# Limpa o dicionario para uma nova analise
		self.__lexema = {}
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
			# Caso seja uma atribuicao, armazena o nome da variavel que estara recebendo um valor por meio da atribuicao.
			self.__lexema["name"]     = self.__currentToken["token"]
			self.__lexema["dimensao"] = None
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
			self.__currentElement = "atribuicao"
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
		# Limpa o dicionario para uma nova analise
		self.__lexema = {}
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
			# Caso seja uma atribuicao, armazena o nome da variavel que estara recebendo um valor por meio da atribuicao.
			self.__lexema["name"]     = self.__currentToken["token"]
			self.__lexema["dimensao"] = None
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
			return self.exprArt()
		elif(self.match("(", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.exprNumber()
			if(result):
				return True
			else:
				return False
			if(self.match(")", 1) == True):
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.exprMultiPos()
				if(result):
					result = self.exprNumber1()
					if(result):
						return True
					else:
						return False
				else:
					return False
			else:
				if (self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
					self.__erro1expr()
				return False
		else:
			if (self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando um número ou token '(', '+', '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["(","+","-"])
				self.__erro1expr()
			return False

	# <exprNumber1>  ::= <operatorSoma> <exprNumber> | <>
	def exprNumber1(self):
		if (self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.operatorSoma()
			if(result):
				result = self.exprNumber()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			return True # vazio

	# =======================================================================================
	# === Gramática para expressões aritméticas =============================================
	# <exprValorMod> ::=  number | <operatorAuto0> <read_value> | <read_value> <operatorAuto>
	def exprValorMod(self):
		if(self.match("NRO", 2) == True):
			# Verifica o tipo numerico utilizado na expressao (se e real ou inteiro)
			if( len(self.__currentToken["token"].split(".") ) > 1):
				self.__expr_type.append("real")
			else:
				self.__expr_type.append("inteiro")
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.__functions_aux.First("operatorAuto0", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.read_value()
			if(result):
				# Faz a análise da variavel/constante utilizada na expressao
				self.__semantic_analyzer.analyzer_param(self.__currentToken["linha"], self.__expr_var)
				self.__expr_type.append(self.__semantic_analyzer.return_var_type())
				return True
			else:
				return False
		elif(self.__functions_aux.First("read_value", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.read_value()
			if(result):
				# Faz a análise da variavel/constante utilizada na expressao
				self.__semantic_analyzer.analyzer_param(self.__currentToken["linha"], self.__expr_var)
				self.__expr_type.append(self.__semantic_analyzer.return_var_type())
				result = self.operatorAuto()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '++', '--'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["++", "--"])
				self.__erro1expr()
			return False

	# <exprMulti> ::= <operatorSoma> <exprValorMod> <exprMultiPos> | <exprValorMod> <exprMultiPos> | '(' <exprNumber>
	def exprMulti(self):
		if(self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.exprValorMod()
			if(result):
				result = self.exprMultiPos()
				if(result):
					return True
				else:
					return False
			else:
				return False
		elif(self.__functions_aux.Follow("exprValorMod",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
			result = self.exprValorMod()
			if(result):
				result = self.exprMultiPos()
				if(result):
					return True
				else:
					return False
			else:
				return False
		elif(self.__functions_aux.Follow("exprNumber",self.__currentToken["token"],self.__currentToken["sigla"]) == True):
			result = self.exprNumber()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '+', '-', '++', '--' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--"])
				self.__erro1expr()
			return False

	# <exprArt>   ::= <exprMulti> <expr1>
	def exprArt(self):
		result = self.exprMulti()
		if(result):
			result = self.expr1()
			if(result):
				return True
			else:
				return False
		else:
			return False

	# <exprMultiPos> ::= <operatorMulti> <exprMulti> | <>
	def exprMultiPos(self):
		if(self.__functions_aux.First("operatorMulti", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.operatorMulti()
			if(result):
				result = self.exprMulti()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			return True # vazio

	# <expr1> ::= <operatorSoma> <exprNumber> | <>
	def expr1(self):
		if(self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.operatorSoma()
			if(result):
				result = self.exprNumber()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			return True # vazio

	# <operatorSoma> ::= '+' | '-'
	def operatorSoma(self):
		if(self.match("+", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.match("-", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '+' ou '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+", "-"])
				self.__erro1expr()
			return False

	# <operatorMulti> ::= '*' | '/'
	def operatorMulti(self):
		if(self.match("*", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.match("/", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '*' ou '/'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["*", "/"])
				self.__erro1expr()
			return False

	# <operatorAuto0> ::= '++' | '--'
	def operatorAuto0(self):
		if(self.match("++", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.match("--", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '+' ou '-'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+", "-"])
				self.__erro1expr()
			return False

	# <operatorAuto> ::= '++' | '--' | <>
	def operatorAuto(self):
		if(self.match("++", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.match("--", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			return True # vazio

	# =======================================================================================
	# === Gramática para expressões relacionais =============================================
	# <exprRel0>   ::= <exprRel> | '(' <expressao> ')'
	def exprRel0(self):
		if(self.__functions_aux.Follow("exprRel", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			return self.exprRel()
		elif(self.match("(", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result == False):
				return False
			if(self.match(")", 1) == True):
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				return True
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
					self.__erro1expr()
				return False
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número, identificador ou token '+', '-', '++', '--', 'verdadeiro', 'falso' ou '('.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--","verdadeiro","falso","("])
				self.__erro1expr()
			return False

	# <exprRel>   ::= <exprArt> <exprRel1> | boolean <exprRel1>
	def exprRel(self):
		if(self.__functions_aux.Follow("exprArt", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			result = self.exprArt()
			if(result):
				result = self.exprRel1()
				if(result):
					return True
				else:
					return False
			else:
				return False
		elif(self.match("verdadeiro", 1) == True or self.match("falso", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__expr_type.append("booleano")
			self.__currentToken = self.next_token()
			result = self.exprRel1()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '+', '-', '++', '--', 'verdadeiro', 'falso' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["+","-","++","--","verdadeiro","falso"])
				self.__erro1expr()
			return False

	# <exprRel1> ::= <operatorRel> <exprRel0> | <>
	def exprRel1(self):
		if(self.__functions_aux.First("operatorRel", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.operatorRel()
			if(result):
				result = self.exprRel0()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			return True # Vazio

	# <operatorRel> ::= '==' | '>=' | '<=' | '!=' | '>' | '<'
	def operatorRel(self):
		if (self.match("==", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif (self.match(">=", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif (self.match("<=", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif (self.match("!=", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif (self.match(">", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif (self.match("<", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '==', '>=', '<=', '!=', '>' ou '<'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ['==', '>=', '<=', '!=', '>','<'])
				self.__erro1expr()
			return False

	# =======================================================================================
	# === Gramática para expressões lógicas =================================================
	# <expressao>   ::= <exprRel> <exprLog1> | '(' <expressao> ')' <exprLog2> | '!' <expressao>
	def expressao(self):
		self.__currentElement = "expressao"
		if(self.__functions_aux.Follow("exprRel", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
			result = self.exprRel()
			if(result):
				result = self.exprLog1()
				if(result):
					return True
				else:
					return False
			else:
				return False
		elif(self.match("(", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result == False):
				return False
			if(self.match(")", 1) == True):
				# Adiciona o token ao vetor lexema, para analise semantica.
				self.__expr_lexema.append(self.__currentToken)
				self.__currentToken = self.next_token()
				result = self.exprLog2()
				if(result):
					return True
				else:
					return False
			else:
				if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
					print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token ')'.\n")
					self.__erros += 1
					self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], [")"])
					self.__erro1expr()
				return False
		elif(self.match("!", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result):
				return True
			else:
				return False
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando número ou identificador ou token '(', '!', , 'verdadeiro', 'falso' .\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["IDE","(", "!", "verdadeiro","falso"])
				self.__erro1expr()
			return False

	# <exprLog1> ::=  <operatorLog> <expressao> | <>
	def exprLog1(self):
		if(self.__functions_aux.First("operatorLog", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			result = self.operatorLog()
			if(result):
				result = self.expressao()
				if(result):
					return True
				else:
					return False
			else:
				return False
		else:
			return True # vazio

	# <exprLog2> ::= <operatorLog> <expressao> | <operatorMulti> <expressao> | <operatorRel> <expressao> | <operatorSoma> <expressao> | <>
	def exprLog2(self):
		if (self.__functions_aux.First("operatorLog", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result):
				return True
			else:
				return False
		elif (self.__functions_aux.First("operatorMulti", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result):
				return True
			else:
				return False
		elif (self.__functions_aux.First("operatorRel", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result):
				return True
			else:
				return False
		elif (self.__functions_aux.First("operatorSoma", self.__currentToken['token'], self.__currentToken['sigla']) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			result = self.expressao()
			if(result):
				return True
			else:
				return False
		else:
			return True # Vazio

	# <operatorLog> ::= '&&' | '||'
	def operatorLog(self):
		if(self.match("&&", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		elif(self.match("||", 1) == True):
			# Adiciona o token ao vetor lexema, para analise semantica.
			self.__expr_lexema.append(self.__currentToken)
			self.__currentToken = self.next_token()
			return True
		else:
			if(self.number_of_tokens() > 0):  # Verifica se existe tokens a serem analisados.
				print("[ERROR] Erro sintático na linha " + self.__currentToken['linha'] + ". Esperando token '&&' ou '||'.\n")
				self.__erros += 1
				self.__files.write_in_file(self.__currentToken['linha'], self.__currentToken["token"], ["&&", "||"])
				self.__erro1expr()
			return False
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
				if(self.__functions_aux.First("function_body2", self.__currentToken["token"], self.__currentToken["sigla"]) == True):
					return
				elif(self.__currentToken["token"] == "funcao"):
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

