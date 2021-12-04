class Semantic_Analyzer(object):
	"""docstring for Semantic_Analyzer"""
	def __init__(self, files):
		self.__files = files
		# st = simbol table
		# Tabela de simbolos para variaveis e constantes
		self.__st_var_const = {}
		# Tabela de simbolos para registros
		self.__st_registry  = {}
		# Atributo que armazena o tipo esperado no retorno de uma atribuicao
		self.__atr_expected_type = ""
		# Atributo que armazena o tipo de uma determinada variavel/constante ou numero em analise
		self.__expected_type = ""
		self.__left_atr      = ""
		self.__erros         = 0

	def get_erros(self):
		return self.__erros

	# Metodo para escrever os erros no arquivo de saida
	def __error(self, error_text):
		self.__erros += 1
		self.__files.write_semantic_error(error_text)
		print(error_text)

	def Print_st_var_const(self):
		print("===================================================================================")
		print("[INFO] Tabela de simbolos para variaveis e constantes. ============================")
		a = list(self.__st_var_const.items())
		for x in range(len(a)):
			print(a[x])
			print("\n")
		print("===================================================================================")
	# ========================================================================================
	# ========================================================================================
	# Metodo para armazenar dados na tabela de varaveis e constantes.
	def add_var_const(self, name, data):
		new_entry = { "tipo": data["tipo"], "categoria": data["categoria"], "dimensao": data["dimensao"], "escopo": data["escopo"], "init": data["init"] }
		# Adiciona um novo elemento
		self.__st_var_const[ name ] = new_entry
	# ========================================================================================
	# ========================================================================================
	# Metodo que armazena qual o tipo esperado em uma atribuicao.
	def set_atr_return_type(self, value):
		self.__expected_type = value
	# ========================================================================================
	# ========================================================================================
	# Funcao para realizar a analise semantica da declaracao de variaveis e constantes.
	def analyzer_var_const(self,isVM, linha, lexema, table):
		# == Primeira verificacao: analise dos nomes. ========================================
		try:
			check = self.__st_var_const[ table["nome"] ]
			if((check["categoria"] == "variavel" and table["categoria"] == "variavel") or (check["categoria"] == "constante" and table["categoria"] == "constante")):
				if(check["escopo"] == "local" and table["escopo"] == "local"):
					# erro de declaracao de variaveis locais redeclaracadas.
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
					return
				elif(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de declaracao de variaveis locais com o mesmo nome de uma global.
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma " + check["categoria"] + " global.")
						return
					elif(table["escopo"] == "global"):
						# erro de declaracao de variaveis globais redeclaracadas.
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
						return
			if( (check["categoria"] == "variavel" and table["categoria"] == "constante") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel global com o mesmo nome de uma constante local
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
						return
			if( (check["categoria"] == "constante" and table["categoria"] == "variavel") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante global.
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")
						return
					elif(table["escopo"] == "global"):
						# erro de variavel global com o mesmo nome de uma constante global.
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")				
						return
				elif(check["escopo"] == "local"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante local.
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
						return
		except Exception as e:
			# Nao existe variavel ou constante armazenadas com este nome.
			# Insere um novo dado
			data = { "tipo": table["tipo"],"categoria": table["categoria"], "dimensao": table["dimensao"], "escopo": table["escopo"], "init": table["init"] }
			# Adiciona um novo elemento
			self.add_var_const(table["nome"],data)
		# == FIM da Primeira verificacao =========================================
		# == Segunda Verificacao: analise da inicializacao =======================
		if(table["init"] == True):
			if(lexema["composto"] == False):
				if(isVM): # verifica se e vetor ou matriz
					self.__check_init_VM(linha, lexema, table)
					return
				else:
					self.__check_init_var_const(linha, lexema, table)
					return
			else:
				self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" nao e permitido inicializacao em tipos compostos.")
		# == Fim da Segunda Verificacao ==========================================
		
	def __check_init_VM(self, linha, lexema, table):
		size = table["dimensao"].split("x")
		if(len(size) == 1):                   # Um vetor
			values      = table["valor"]      # table["valor"] contem a lista de token utilizados na inicializacao
			array_type  = lexema["tipo"]      
			vector_type = array_type["token"] # Tipo do vetor declarado. Ex: inteiro, real, cadeia....
			sigla       = array_type["sigla"] # Sigla correspondente ao tipo do vetor declarado.
			size        = int(size[0])
			# Verifica se todas as posicoes foram inicializadas
			if((len(values)-1) > (size)):
				self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando espaço de inicializacao alem do que foi declarado.")
			elif((len(values)-1) < size):
				self.__error("[ERROR: linha " + linha + "] Erro semantico: Inicialize todas as posicoes da " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" .")
			# Verifica se as posicoes foram inicializadas corretamente. 
			if(vector_type == "inteiro" or vector_type == "real"):
				for x in range(len(values)):  
					token = values[x]
					if(token["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
						v = str(token["token"])     # converte para string
						if(vector_type == "inteiro"):
							if(len(v.split(".")) > 1):  # Verifica se o valor e um inteiro
								self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						elif(vector_type == "real"):
							if(len(v.split(".")) == 1):  # Verifica se o valor e um real
								self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
					elif(token["sigla"] == "IDE"):                     # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[token["token"]]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == vector_type):
								if(IDE["init"] == False):
									self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel " + token["token"] + " nao foi declarada.")
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
			if(vector_type == "char" or vector_type == "cadeia" or vector_type == "booleano"):
				for x in range(len(values)):  
					token = values[x]
					if(token["sigla"] == "PRE"):                   # Verifica se o valor recebido e uma palavra reservada
						if(token["token"] == "verdadeiro" or token["token"] == "falso"):
							pass
						else:
							self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
					elif(token["sigla"] == "CAR" or token["sigla"] == "CAD"):
						pass # Tudo ok
					elif(token["sigla"] == "IDE"):                       # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[ token["token"] ]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == vector_type):
								if(IDE["init"] == False):
									self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel " + token["token"] + " nao foi declarada.")
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
		elif(len(size) == 2): # E uma Matriz
			# Primeiramente verifica se todos os valores estao sendo utilizados corretamente.
			values      = table["valor"]      # table["valor"] contem a lista de token utilizados na inicializacao
			array_type  = lexema["tipo"]      
			matrix_type = array_type["token"] # Tipo do vetor declarado. Ex: inteiro, real, cadeia....
			sigla       = array_type["sigla"] # Sigla correspondente ao tipo do vetor declarado.
			# Verifica se cada posicao foi inicializada corretamente. 
			columns        = int(size[1])
			lines          = int(size[0])
			matrix_columns = 0
			matrix_lines   = 0                        # Armazena o numero de linhas encontradas na declaracao da matriz.
			if(matrix_type == "inteiro" or matrix_type == "real"):
				for x in range(len(values)):
					token           = values[x]
					if( token["sigla"] == "NRO" or token["sigla"] == "IDE" or (token["token"] != ";") ):
						matrix_columns += 1
					if(token["token"] == ";" or (x == (len(values)-1)) ):        # Finalizei a analise de uma linha da matriz
						if(matrix_columns > columns):
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Linha " + str(matrix_lines) + " da matriz esta ultrapassando o numero de colunas que foi definido." )
						elif(matrix_columns < columns):
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as colunas da linha " + str(matrix_lines) + " da matriz.")
						matrix_columns = 0            # Reinicia a contagem para a analise da proxima linha
						matrix_lines  += 1            # Aumenta a contagem das linhas em 1
					elif(token["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
						v = str(token["token"])       # converte para string
						if(matrix_type == "inteiro"):
							if(len(v.split(".")) > 1):  # Verifica se o valor e um inteiro
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						elif(matrix_type == "real"):
							if(len(v.split(".")) == 1):  # Verifica se o valor e um real
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
					elif(token["sigla"] == "IDE"):                     # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[token["token"]]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == matrix_type):
								if(IDE["init"] == False):
									self.__error("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi declarada.")
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
				# Fim da declaracao da matrix
				if(matrix_lines > lines):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Numero de linhas na inicializacao esta ultrapassando o limite definido na declaracao." )
				elif(matrix_lines  < lines):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as linhas da matriz.")
			elif(matrix_type == "char" or matrix_type == "cadeia" or matrix_type == "booleano"):
				for x in range(len(values)):  
					token = values[x]
					if( token["sigla"] == "NRO" or token["sigla"] == "IDE" or (token["token"] != ";") ):
						matrix_columns += 1
					if(token["token"] == ";" or (x == (len(values)-1))):        # Finalizei a analise de uma linha da matriz
						if(matrix_columns > columns):
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Linha " + str(matrix_lines) + " da matriz esta ultrapassando o numero de colunas que foi definido." )
						elif(matrix_columns < columns):
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as colunas da linha " + str(matrix_lines) + " da matriz.")
						matrix_columns = 0            # Reinicia a contagem para a analise da proxima linha
						matrix_lines  += 1            # Aumenta a contagem das linhas em 1
					elif(token["sigla"] == "PRE"):    # Verifica se o valor recebido e uma palavra reservada            
						if(token["token"] == "verdadeiro" or token["token"] == "falso"):
							pass
						else:
							self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: \"" + matrix_type + "\".\n")
					elif(token["sigla"] == "CAR" or token["sigla"] == "CAD"):
						pass # Tudo ok
					elif(token["sigla"] == "IDE"):                       # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[ token["token"] ]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == matrix_type):
								if(IDE["init"] == False):
									self.__error("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi declarada.")
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines) + ". Esperado um valor do tipo: \"" + matrix_type + "\".\n")
				# Fim da declaracao da matrix
				if(matrix_lines > lines):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Numero de linhas na inicializacao esta ultrapassando o limite definido na declaracao." )
				elif(matrix_lines  < lines):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as linhas da matriz.")
	
	def __check_init_var_const(self, linha, lexema, table):
		if(table["tipo"] == "vazio"):
			self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" está usando vazio como tipo.")
			self.__error("Esperado tipo: inteiro, real, char, cadeia, booleano.\n")
		else:
			valor = lexema["valor"]             # Pega o token utilizado na inicializacao
			tipo  = lexema["tipo"]              # Pega o token utilizado no tipo da constante/variavel
			if(tipo["token"] == "inteiro"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 1): # Verifica se o valor e um inteiro
						return
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "real"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 2): # Verifica se o valor e um real
						return
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "booleano"):
				if(valor["token"] == "verdadeiro" or valor["token"] == "falso"):  # Verifica se o valor de inicializacao e um booleano.
					return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "char"):
				if(valor["sigla"] == "CAR"):  # Verifica se o valor de inicializacao e um char.
					return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "cadeia"):
				if(valor["sigla"] == "CAD"): # Verifica se o valor de inicializacao e uma cadeia de caracteres.
					return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao. Esperado um valor do tipo: " + tipo["token"] + "\n")
					return

	# Metodo que armazena na tabela de registro, um novo registro declarado caso ele ainda nao exista
	def addRegistry(self, name_token):
		try:
			# Verifica o novo registro ja existe
			check = self.__st_registry[ name_token["token"] ]
			self.__error("[ERROR: linha " + name_token["linha"] + "] Erro semantico: registro \"" + name_token["token"] + "\" ja existe.")
			return False
		except Exception as e:
			# Nao existe registro com esse nome, logo, armarzena
			# Cada linha dessa nova entrada e um atributo do novo registro enviado
			self.__st_registry[name_token["token"]] = {}
			return True

	def analyzer_Registry_Atributes(self, isVM, name, lexema):
		registry = self.__st_registry[name["token"]]
		atr_name = lexema["name"]     # Nome do atributo
		atr_type = lexema["type"]     # Tipo do atributo
		atr_dim  = lexema["dimensao"] # Dimensao do atributo (para vetor e matriz)
		line     = atr_name["linha"]  # Linha atual do arquivo de entrada
		try:
			# Verificar se novo atributo ja foi declarado antes atraves do token recebido.
			check_atribute = registry[atr_name["token"]]
			# Se nao der excessao, e porque o atributo ja existe
			self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta sendo declarado mais de uma vez.")
			return
		except Exception as e:
			if(atr_type["token"] == "vazio" or atr_type["sigla"] == "IDE"):
				self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo invalido para atributos em elementos compostos. Esperado tipo: \"inteiro\", \"real\", \"booleano\", \"cadeia\", \"char\".")
			else:
				# Caso nao exista, dá seguimento à analise
				if(isVM == False): # Nao e vetor ou matriz
					# Armazena na tabela o novo atributo
					registry[atr_name["token"]]       = {"type": atr_type["token"], "dimensao": None}
					self.__st_registry[name["token"]] = registry
				elif(isVM == True): # E vetor ou matriz
					size = lexema["dimensao"].split("x")
					if(len(size) == 1): # E vetor
						try:
							# Tenta converter o valor para int
							linha = int(size[0])
							# Caso nao de execessao, continua...
							linha = size[0]
							if(len(linha.split(".")) > 1):  # Verifica se o valor e um inteiro
								self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento. Esperado um valor numerico do tipo: \"inteiro\".")							
							else:
								# Armazena na tabela o novo atributo
								registry[atr_name["token"]]		  = {"type": atr_type["token"], "dimensao": linha}
								self.__st_registry[name["token"]] = registry
						except Exception as e:
							self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento. Esperado um valor numerico do tipo: \"inteiro\".")
					elif(len(size) == 2): # E matriz
						try:
							# Tenta converter os valores para int
							linha  = int(size[0])
							coluna = int(size[1])
							# Caso nao de execessao, continua...
							linha  = size[0]
							coluna = size[1]
							if(len(linha.split(".")) > 1 or len(coluna.split(".")) > 1):  # Verifica se os valores sao inteiros
								self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento. Esperado um valor numerico do tipo: \"inteiro\".")								
							else: 
								# Armazena na tabela o novo atributo
								registry[atr_name["token"]]       = {"type": atr_type["token"], "dimensao": size}
								self.__st_registry[name["token"]] = registry
						except Exception as e:
							self.__error("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento. Esperado um valor numerico do tipo: \"inteiro\".")
	# =========================================================================
	# =========================================================================
	# Metodo para analisar o lado direito de um atribuicao
	def right_Assignment(self, isExpr, linha, lexema, tipos, dim, name):
		result = True
		# Categoria da variavel que ira receber o valor atribuido
		categoria = ""
		# Verifica se o valor recebido por meio da atribuicao e uma variavel/constante ou expressao
		if(isExpr == False):
			# Nao e uma expressao (aritmetica, logica ou relacional).
			# Verifica se o valor recebido e igual ao esperado.
			if(self.__atr_expected_type != lexema["entry"]):
				result = False
				self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida em \"" + lexema["name"] + ". Esperando um valor do tipo: \"" + self.__atr_expected_type + "\"")
				self.__atr_expected_type = ""
		elif(isExpr == True):
			if(self.__atr_expected_type == "inteiro"):
				# Verifica se todos os tipos utilizados na expressao, sao inteiros
				for x in range(len(tipos)):
					if(tipos[x] != "inteiro"):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo inteiro.")
						break
				# Verifica se esta sendo utilizado alguma operacao logica na expressao
				for x in range(len(lexema)):
					token = lexema[x]
					if(self.check_log_rel("logico", token["token"]) == True or self.check_log_rel("relacional", token["token"]) == True):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo inteiro. Nao utilize operacoes logicas ou relacionais.")
						break
			elif(self.__atr_expected_type == "real"):
				# Verifica se existe pelo menos um valor do tipo real para que o resultado gerado seja real.
				# Os demais podem ser do tipo inteiro
				search = False
				for x in range(len(tipos)):
					if(tipos[x] == "real"):
						search = True
					elif(tipos[x] == "booleano" or tipos[x] == "cadeia" or tipos[x] == "char"):
						search = False
						break
				if(search == False):
					result = False
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo real. Utilize variaveis inteiras junto com reais, ou somente reais.")
				# Verifica se esta sendo utilizado alguma operacao logica na expressao
				for x in range(len(lexema)):
					token = lexema[x]
					if(self.check_log_rel("logico", token["token"]) == True or self.check_log_rel("relacional", token["token"]) == True):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo real. Nao utilize operacoes logicas ou relacionais.")
						break
			elif(self.__atr_expected_type == "cadeia"):
				if(len(tipos) == 1):
					if(tipos[0] != "cadeia"):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo cadeia.")
				else:
					result = False
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Nao e permitido operacoes com variaveis do tipo cadeia.")
			elif(self.__atr_expected_type == "char"):
				if(len(tipos) == 1):
					if(tipos[0] != "cadeia"):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo char.")
				else:
					result = False
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Nao e permitido operacoes com variaveis do tipo char.")
			elif(self.__atr_expected_type == "booleano"):
				if(len(tipos) == 1):
					if(tipos[0] != "booleano"):
						result = False
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - Esperando um valor do tipo booleano.")
		# Verifica se ocorreu tudo certo com o processo de atribuicao
		if(result == True):
			# Caso seja um elemento composto, ja separada, com o intuito de pegar o nome da variavel.
			name = name.split(".")
			search = self.__get_var_const(name[0])
			# Atribuicao feita com sucesso
			# Armazena na tabela de variaveis e constantes os dados referentes a ela.
			if(dim == None): # E uma variavel simples
				categoria = "variavel"
			elif(len(dim) == 1): # E vetor
				categoria = "array"
			elif(len(dim) == 2): # E matriz
				categoria = "matriz"
			data   = { "tipo": self.__atr_expected_type, "categoria": categoria, "dimensao": None, "escopo": search["escopo"], "init": True }
			self.add_var_const(self.__left_atr,data)
	# =========================================================================
	# =========================================================================
	# Metodo para analizar se o token é algum do conjunto relacional ou logico
	def check_log_rel(self, tipo, token):
		if(tipo == "logico"):
			if(token == "&&" or token == "||" or token == "!"):
				return True
			else:
				return False
		elif(tipo == "relacional"):
			if(token == "==" or token == "!=" or token == ">" or token == ">=" or token == "<" or token == "<=" or token == "="):
				return True
			else:
				return False
	# =========================================================================
	# =========================================================================
	# Metodo para analizar se o token é algum do conjunto aritmetico
	def check_art(self, token):
		if(token == "+" or token == "++" or token == "-" or token == "--" or token == "*" or token == "/"):
			return True
		else:
			return False
	# =========================================================================
	# =========================================================================
	# Metodo para analizar semanticamente o lado esquerdo de uma atribuicao
	def left_Assignment(self, linha, lexema):
		# Verifica se o elemento corresponde ao acesso a um registro
		var = lexema["name"].split(".")
		if( len(var) > 1 ):
			# Analise do acesso a um registro
			result =  self.__registry_access(lexema, linha, True)
			# Verifica se a analise ocorreu com sucesso
			if(result == True):
				# Armazena temporariamente o lexema recebido
				self.__left_atr = ""
				self.__left_atr = lexema["name"]
				if(lexema["dimensao"] != None):
					if(len(lexema["dimensao"]) == 1): # E um vetor
						dim    = lexema["dimensao"]
						coluna = dim[0]
						self.__left_atr += "[" + str(coluna["token"]) + "]"
					elif(len(lexema["dimensao"]) == 2): # E uma matriz
						dim    = lexema["dimensao"]
						linha  = dim[0]
						coluna = dim[1]
						self.__left_atr += "[" + str(linha["token"]) + "]" + "[" + str(coluna["token"]) + "]"
			return result
		else:
			# Nome da variavel de atribuicao
			nome = lexema["name"]
			# Busca através do nome na tabela de simbolos para variaveis e constantes.
			check = self.__get_var_const(nome)
			if(check != ""):
				# Armazena o tipo de dados que o identificador em analise recebe 
				self.__atr_expected_type = check["tipo"]
				# Verifica se o identificador pertecente a uma constante
				if(check["categoria"] == "constante"):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - \"" + nome + "\" e uma constante.")
					return False
				elif(check["categoria"] == "matriz" or check["categoria"] == "array"):
					return self.__access_vector_matrix(nome, check, lexema, linha)
				else:
					if(lexema["dimensao"] == None):
						return True # Consiste em uma variavel simples.
					elif(len(lexema["dimensao"]) >= 1):
						self.__error("[ERROR: linha " + linha + "] Erro semantico: \"" + nome + "\" nao e nem vetor nem matriz.")		
						return False
			else:
				# Como nao foi declarada, nao existe nenhum tipo associado a ela.
				self.__atr_expected_type = ""
				self.__error("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - \"" + nome + "\" nao foi declarado.")
				return False

	# =========================================================================
	# Metodo que realiza a analise semantica de acesso a vetores e matrizes
	def __access_vector_matrix(self, nome, data, lexema, linha):
		if(lexema["dimensao"] == "composto"):
			self.__error("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\". Elementos compostos nao sao permitidos como index de vetor ou matriz.")
			return False
		elif(lexema["dimensao"] == None): # Verifica se foi passados os index de acesso
			# Nenhum index foi informado.
			self.__error("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\". Nenhum index foi informado.")
			return False
		else:
			# Pode ser um vetor ou uma matriz
			# Nesta parte, "dimensao" corresponde ao index de acesso informado na atribuicao. Ex: a[2] = ...
			size = lexema["dimensao"]
			if(len(size) == 1): # VETOR =================================================================
				if(data["categoria"] == "array"):
					# Realiza analise do index do vetor
					return self.__analysis_Vector(nome, size[0], linha)
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\" nao e um vetor.")
					return False
			elif(len(size) == 2): # MATRIZ ===============================================================
				if(data["categoria"] == "matriz"):
					# Realiza analise dos index da matriz
					return self.__analysis_Matrix(nome, size[0], size[1], linha)
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\" nao e uma matriz.")
					return False
		return False
	# =========================================================================
	# =========================================================================
	# Metodo que realiza a analise do index de acesso de uma matriz
	def __analysis_Matrix(self, nome, coluna, linha, assignment_line ):
		x      = [coluna, linha]
		result = True
		for i in range(len(x)):
			index = x[i]
			if(index["sigla"] == "IDE"):
				# Verifica se esse identificador foi declarado.
				test = self.__get_var_const(index["token"])
				if(test != ""):
					if(test["categoria"] == "variavel" or test["categoria"] == "constante"):
						if(test["tipo"] != "inteiro"):
							self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido na matriz - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".")
							result = False
					else:
						self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido na matriz - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".") 
						result = False
				else:
					self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido - \"" + test["token"] + " nao foi declarado.") 
					result = False
			elif(index["sigla"] == "NRO"):
				number = coluna["token"]
				# Verifica se o index recebido e um inteiro
				if(len(number.split(".")) > 1):
					self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso Invalido - na matriz \"" + nome + "\". Esperando index do tipo \"inteiro\".")
					result = False
		return result
	# =========================================================================
	# =========================================================================
	# Metodo que realiza a analise do index de acesso de um vetor
	def __analysis_Vector(self, nome, coluna, assignment_line ):
		if(coluna["sigla"] == "IDE"):
			# Verificar se esse identificador foi declarado.
			test = self.__get_var_const(coluna["token"])
			if(test != ""):
				if(test["categoria"] == "variavel" or test["categoria"] == "constante"):
					if(test["tipo"] == "inteiro"):
						return True
					else:
						self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido no vetor - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".")
						return False
				else:
					self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido no vetor - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".") 
					return False
			else:
				self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido - \"" + test["token"] + " nao foi declarado.") 
				return False
		elif(coluna["sigla"] == "NRO"):
			number = coluna["token"]
			# Verifica se o index recebido e um inteiro
			if(len(number.split(".")) > 1):
				self.__error("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso Invalido - no vetor \"" + nome + "\". Esperando index do tipo \"inteiro\".")
				return False
			else:
				return True
	# =========================================================================
	# =========================================================================
	# Metodo para buscar um valor na tabela de simbolos para variaveis e constantes 
	def __get_var_const(self, entrada):
		try:
			return self.__st_var_const[entrada]
		except Exception as e:
			return ""
	# =========================================================================
	# =========================================================================
	# Metodo para buscar um valor na tabela de simbolos para registros.
	# Retorna a tabela com os atribuitos de um determinado registro. 
	def __get_registry(self, entrada):
		try:
			return self.__st_registry[entrada]
		except Exception as e:
			return ""
	# =========================================================================
	# =========================================================================
	# Metodo para verificar se um tipo passado como parametro e um tipo primitivo.
	def __check_primitive_Type(self, tipo):
		if(tipo == "inteiro" or tipo == "real" or tipo == "cadeia" or tipo == "booleano" or tipo == "char"):
			return True
		else:
			return False
	# =========================================================================
	# Metodo que busca uma entrada dentro de uma tabela qualquer passada como parametro
	def __get_TableData(self, table, entrada):
		try:
			return table[entrada]
		except Exception as e:
			return ""
	# =========================================================================
	# =========================================================================
	# Metodo que realiza a analise semantica do acesso a registros.
	# O parametro "isAtr" consiste em um booleano que informa se esse acesso e para uma variavel à esquerda da atribuicao ou nao
	def __registry_access(self, lexema, linha, isAtr):
		campos    = lexema["name"].split(".")
		# Verifica se a variavel foi declarada.
		var = self.__get_var_const(campos[0])
		if(var != ""):
			# Veririca se a variavel e realmente um elemento composto
			if(self.__check_primitive_Type(var["tipo"]) == False):
				# Busca os atributos desse tipo composto encontrado.
				registry  = self.__get_registry(var["tipo"])
				# Como nao e permitido registro de registro, so existira um nivel de acesso.
				# Ex: Joao.idade, Joao.carros[0]
				if(lexema["dimensao"] != None):
					# O atributo acessado e um vetor ou matriz
					check = campos[1].split("[")
					# Verifica se o atributo acessado existe no registro.
					atr = self.__get_TableData(registry, check[0])
					if(atr != ""):
						if(isAtr == True):
							# Armazena o tipo de dados que o atributo acessado recebe.
							self.__atr_expected_type = atr["type"]
						else:
							# Armazena o tipo de dados que o atributo acessado recebe.
							self.__expected_type = atr["type"]
						if(lexema["dimensao"] == "composto"):
							categoria = "variavel"
						elif(len(atr["dimensao"]) == 1):
							categoria = "array"
						elif(len(atr["dimensao"]) == 2):
							categoria = "matriz"
						# Realiza a analise do acesso ao vetor/matriz
						return self.__access_vector_matrix(check[0], {"categoria": categoria}, lexema, linha)
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atributo \"" + check[0] + "\" nao foi declarado.")
						return False
				else:
					# O atributo e uma variavel simples.
					# Verifica se o atributo acessado existe no registro.
					atr = self.__get_TableData(registry, campos[1])
					if(atr != ""):
						if(isAtr == True):
							# Armazena o tipo de dados que o atributo acessado recebe.
							self.__atr_expected_type = atr["type"]
						else:
							# Armazena o tipo de dados que o atributo acessado recebe.
							self.__expected_type = atr["type"]
						return True
					else:
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Atributo \"" + campos[1] + "\" nao foi declarado.")
						return False
			else:
				self.__error("[ERROR: linha " + linha + "] Erro semantico: \"" + campos[0] + "\" nao e um elemento composto.")
		else:
			# Como nao foi declarada, nao existe nenhum tipo associado a ela.
			self.__expected_type = ""
			self.__error("[ERROR: linha " + linha + "] Erro semantico: \"" + campos[0] + "\" nao foi declarado.")
		return False

	# =========================================================================
	# =========================================================================
	# Metodo para analizar as variaveis e constantes utilizadas em expressoes, comandos, etc
	def analyzer_param(self, linha, lexema):
		# Verifica se o elemento corresponde ao acesso a um registro
		if( len( lexema["name"].split(".")) > 1 ):
			# Analise do acesso a um registro
			result =  self.__registry_access(lexema, linha, False)
			# Retorna True se a analise ocorreu com sucesso.
			return result
		else:
			# Nome da variavel de atribuicao
			nome = lexema["name"]
			# Busca através do nome na tabela de simbolos para variaveis e constantes.
			check = self.__get_var_const(nome)
			if(check != ""):
				# Armazena o tipo de dados que o identificador em analise recebe 
				self.__expected_type = check["tipo"]
				# Verifica se e um vetor ou matriz
				if(check["categoria"] == "matriz" or check["categoria"] == "array"):
					return self.__access_vector_matrix(nome, check, lexema, linha)
				else:
					if(lexema["dimensao"] == None):
						return True # Consiste em uma variavel simples.
					elif(len(lexema["dimensao"]) >= 1):
						self.__error("[ERROR: linha " + linha + "] Erro semantico: \"" + nome + "\" nao e nem vetor nem matriz.")		
						return False
			else:
				# Como nao foi declarada, nao existe nenhum tipo associado a ela.
				self.__expected_type = ""
				self.__error("[ERROR: linha " + linha + "] Erro semantico: \"" + nome + "\" nao foi declarado.")
				return False
	# =========================================================================
	# =========================================================================
	# Metodo que retorna o tipo da ultima variavel analisada.
	def return_var_type(self):
		return self.__expected_type
	# =========================================================================
	# =========================================================================
	# Metodo que realiza a analise de uma expressao para determinada estrutura (se, para, enquanto)
	def expression_analyzer(self, linha, estrutura, lexema, tipos):
		if(estrutura == "se" or estrutura == "enquanto"):
			if(len(tipos) == 1):
				if(tipos[0] != "booleano"):
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Esperando um valor do tipo booleano.")
			else:
				# Verifica se existe algum operacao aritmetica. (nao e permitido)
				for x in range(len(lexema)):
					token = lexema[x]
					if(self.check_art(token["token"]) == True):
						self.__error("[ERROR: linha " + linha + "] Erro semantico: Nao sao permitidas expressoes aritmeticas na condicao do comando \"" + estrutura + "\".")
						break
			return True
		elif(estrutura == "para"):
			pass

	# Verifica a sobrecarga.
	def function_overload_analyzer(self, name, qtd, type, linha):
		control = 0
		if len(name) > 1:
			for i in range(len(name)):
				if name[i] == name[len(name) - 1] and i != len(name) - 1:
					if qtd[i] == qtd[len(name) - 1]:
						for j in range(len(type[i])):
							if type[i][j] == type[len(name) - 1][j]:
								control += 1
							if control == len(type[i]):
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Sobrecarga inválida, assinaturas idênticas.")


	# Verifica se a função foi declarada na hora da chamada.
	def function_check_declaration(self, nameF, nameT, linha):
		if nameF != 'algoritmo':
			if nameF in nameT:
				return
			else:
				self.__error("[ERROR: linha " + linha + "] Erro semantico: Função" + nameF + "não declarada.")


	# Verifica se todos os parâmetros foram passados.
	def function_check_param(self, qtdF, nameF, qtdT, nameT, linha):
		for i in range(len(nameT)):
			if nameF == nameT[i]:
				if qtdT[i] == qtdF:
					return
				else:
					self.__error("[ERROR: linha " + linha + "] Erro semantico: Função" + nameF + "espera mais parâmetros.")

	# Verifica a ordem dos parâmetros na chamada da função, através de seus tipos
	def function_check_ord_param(self, nameF, nameT, paramF, typeT, linha):
		for i in range(len(nameT)):
			if nameF == nameT[i]:
				if typeT[i] != 'NULL':
					for j in range(len(typeT[i])):
						aux = self.__get_var_const(paramF[j])
						aux2 = self.__get_registry(paramF[j])
						if aux == "" and aux2 == "":
							self.__error("[ERROR: linha " + linha + "] Erro semantico: Função" + nameF + "recebeu parâmetros não declarados.")
							print('ERRO DE CHAMADA!!!')
						elif len(aux) > 0:
							if aux['tipo'] != typeT[i][j]:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Função" + nameF + "recebeu parâmetros em ordens divergentes.")
								print('ERRO DE CHAMADA!!!')
						elif len(aux2) > 0:
							if aux2['tipo'] != typeT[i][j]:
								self.__error("[ERROR: linha " + linha + "] Erro semantico: Função" + nameF + "recebeu parâmetros em ordens divergentes.")
								print('ERRO DE CHAMADA!!!')