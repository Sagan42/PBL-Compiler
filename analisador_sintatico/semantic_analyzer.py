class Semantic_Analyzer(object):
	"""docstring for Semantic_Analyzer"""
	def __init__(self):
		# st = simbol table
		# Tabela de simbolos para variaveis e constantes
		self.__st_var_const = {}
		# Tabela de simbolos para registros
		self.__st_registry  = {}

	def Print_st_var_const(self):
		print("===================================================================================")
		print("[INFO] Tabela de simbolos para variaveis e constantes. ============================")
		a = list(self.__st_var_const.items())
		for x in range(len(a)):
			print(a[x])
			print("\n")
		print("===================================================================================")

	# Funcao para realizar a analise semantica da declaracao de variaveis e constantes.
	def analyzer_var_const(self,isVM, linha, lexema, table):
		# == Primeira verificacao: analise dos nomes. ========================================
		try:
			check = self.__st_var_const[ table["nome"] ]
			if((check["categoria"] == "variavel" and table["categoria"] == "variavel") or (check["categoria"] == "constante" and table["categoria"] == "constante")):
				if(check["escopo"] == "local" and table["escopo"] == "local"):
					# erro de declaracao de variaveis locais redeclaracadas.
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
				elif(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de declaracao de variaveis locais com o mesmo nome de uma global.
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma " + check["categoria"] + " global.")
					elif(table["escopo"] == "global"):
						# erro de declaracao de variaveis globais redeclaracadas.
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
			if( (check["categoria"] == "variavel" and table["categoria"] == "constante") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel global com o mesmo nome de uma constante local
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
			if( (check["categoria"] == "constante" and table["categoria"] == "variavel") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante global.
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")
					elif(table["escopo"] == "global"):
						# erro de variavel global com o mesmo nome de uma constante global.
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")				
				elif(check["escopo"] == "local"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante local.
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
		except Exception as e:
			# Nao existe variavel ou constante armazenadas com este nome.
			# Insere um novo dado
			data = { "tipo": table["tipo"],
					"categoria": table["categoria"],
					"dimensao": table["dimensao"],
					"escopo": table["escopo"],
					"init": table["init"] }
			# Adiciona um novo elemento
			self.__st_var_const[ table["nome"] ] = data
		# == FIM da Primeira verificacao =========================================
		# == Segunda Verificacao: analise da inicializacao =======================
		if(table["init"] == True):
			if(isVM): # verifica se e vetor ou matriz
				self.__check_init_VM(linha, lexema, table)
				return
			else:
				self.__check_init_var_const(linha, lexema, table)
				return
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
				print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando espaço de inicializacao alem do que foi declarado.")
			elif((len(values)-1) < size):
				print("[ERROR: linha " + linha + "] Erro semantico: Inicialize todas as posicoes da " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" .")
			# Verifica se as posicoes foram inicializadas corretamente. 
			if(vector_type == "inteiro" or vector_type == "real"):
				for x in range(len(values)):  
					token = values[x]
					if(token["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
						v = str(token["token"])     # converte para string
						if(vector_type == "inteiro"):
							if(len(v.split(".")) > 1):  # Verifica se o valor e um inteiro
								print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
								print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						elif(vector_type == "real"):
							if(len(v.split(".")) == 1):  # Verifica se o valor e um real
								print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
								print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
					elif(token["sigla"] == "IDE"):                     # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[token["token"]]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == vector_type):
								if(IDE["init"] == False):
									print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
								print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel " + token["token"] + " nao foi declarada.")
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
			if(vector_type == "char" or vector_type == "cadeia" or vector_type == "booleano"):
				for x in range(len(values)):  
					token = values[x]
					if(token["sigla"] == "PRE"):                   # Verifica se o valor recebido e uma palavra reservada
						if(token["token"] == "verdadeiro" or token["token"] == "falso"):
							pass
						else:
							print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
							print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
					elif(token["sigla"] == "CAR" or token["sigla"] == "CAD"):
						pass # Tudo ok
					elif(token["sigla"] == "IDE"):                       # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[ token["token"] ]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == vector_type):
								if(IDE["init"] == False):
									print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
								print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\". Variavel " + token["token"] + " nao foi declarada.")
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: \"" + vector_type + "\" na posicao " + str(x) + " do vetor.\n")
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
							print("[ERROR: linha " + linha + "] Erro semantico: Linha " + str(matrix_lines) + " da matriz esta ultrapassando o numero de colunas que foi definido." )
						elif(matrix_columns < columns):
							print("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as colunas da linha " + str(matrix_lines) + " da matriz.")
						matrix_columns = 0            # Reinicia a contagem para a analise da proxima linha
						matrix_lines  += 1            # Aumenta a contagem das linhas em 1
					elif(token["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
						v = str(token["token"])       # converte para string
						if(matrix_type == "inteiro"):
							if(len(v.split(".")) > 1):  # Verifica se o valor e um inteiro
								print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
								print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						elif(matrix_type == "real"):
							if(len(v.split(".")) == 1):  # Verifica se o valor e um real
								print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
								print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
					elif(token["sigla"] == "IDE"):                     # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[token["token"]]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == matrix_type):
								if(IDE["init"] == False):
									print("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
								print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							print("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi declarada.")
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
						print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
				# Fim da declaracao da matrix
				if(matrix_lines > lines):
					print("[ERROR: linha " + linha + "] Erro semantico: Numero de linhas na inicializacao esta ultrapassando o limite definido na declaracao." )
				elif(matrix_lines  < lines):
					print("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as linhas da matriz.")
			elif(matrix_type == "char" or matrix_type == "cadeia" or matrix_type == "booleano"):
				for x in range(len(values)):  
					token = values[x]
					if( token["sigla"] == "NRO" or token["sigla"] == "IDE" or (token["token"] != ";") ):
						matrix_columns += 1
					if(token["token"] == ";" or (x == (len(values)-1))):        # Finalizei a analise de uma linha da matriz
						if(matrix_columns > columns):
							print("[ERROR: linha " + linha + "] Erro semantico: Linha " + str(matrix_lines) + " da matriz esta ultrapassando o numero de colunas que foi definido." )
						elif(matrix_columns < columns):
							print("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as colunas da linha " + str(matrix_lines) + " da matriz.")
						matrix_columns = 0            # Reinicia a contagem para a analise da proxima linha
						matrix_lines  += 1            # Aumenta a contagem das linhas em 1
					elif(token["sigla"] == "PRE"):    # Verifica se o valor recebido e uma palavra reservada            
						if(token["token"] == "verdadeiro" or token["token"] == "falso"):
							pass
						else:
							print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
							print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
					elif(token["sigla"] == "CAR" or token["sigla"] == "CAD"):
						pass # Tudo ok
					elif(token["sigla"] == "IDE"):                       # Verifica se foi utilizado um identificador
						try:
							IDE = self.__st_var_const[ token["token"] ]  # Busca na tabela de simbolos para variaveis e constantes o identificador usado
							if(IDE["tipo"] == matrix_type):
								if(IDE["init"] == False):
									print("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi inicializada.")
							else:
								print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
								print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
						except Exception as e:
							# identificador utilizado ainda nao foi declarado.
							print("[ERROR: linha " + linha + "] Erro semantico: Variavel \"" + token["token"] + "\" nao foi declarada.")
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: Matriz " + table["nome"] + "\" usando tipo incorreto para inicializacao na linha " + str(matrix_lines))
						print("Esperado um valor do tipo: \"" + matrix_type + "\".\n")
				# Fim da declaracao da matrix
				if(matrix_lines > lines):
					print("[ERROR: linha " + linha + "] Erro semantico: Numero de linhas na inicializacao esta ultrapassando o limite definido na declaracao." )
				elif(matrix_lines  < lines):
					print("[ERROR: linha " + linha + "] Erro semantico: Preencha todas as linhas da matriz.")
	
	def __check_init_var_const(self, linha, lexema, table):
		if(table["tipo"] == "vazio"):
			print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" está usando vazio como tipo.")
			print("Esperado tipo: inteiro, real, char, cadeia, booleano.\n")
		else:
			valor = lexema["valor"]             # Pega o token utilizado na inicializacao
			tipo  = lexema["tipo"]              # Pega o token utilizado no tipo da constante/variavel
			if(tipo["token"] == "inteiro"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 1): # Verifica se o valor e um inteiro
						return
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "real"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 2): # Verifica se o valor e um real
						return
					else:
						print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "booleano"):
				if(valor["token"] == "verdadeiro" or valor["token"] == "falso"):  # Verifica se o valor de inicializacao e um booleano.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "char"):
				if(valor["sigla"] == "CAR"):  # Verifica se o valor de inicializacao e um char.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "cadeia"):
				if(valor["sigla"] == "CAD"): # Verifica se o valor de inicializacao e uma cadeia de caracteres.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return

	# Metodo que armazena na tabela de registro, um novo registro declarado caso ele ainda nao exista
	def addRegistry(self, name_token):
		try:
			# Verifica o novo registro ja existe
			check = self.__st_registry[ name_token["token"] ]
			print("[ERROR: linha " + name_token["linha"] + "] Erro semantico: registro \"" + name_token["token"] + "\" ja existe.")
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
			print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta sendo declarado mais de uma vez.")
			return
		except Exception as e:
			if(atr_type["token"] == "vazio" or atr_type["sigla"] == "IDE"):
				print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo invalido para atributos em elementos compostos.")
				print("Esperado tipo: \"inteiro\", \"real\", \"booleano\", \"cadeia\", \"char\".")
			else:
				# Caso nao exista, dá seguimento à analise
				if(isVM == False): # Nao e vetor ou matriz
					# Armazena na tabela o novo atributo
					registry[atr_name["token"]]       = {"type": atr_type["token"], "dimensao": None}
					self.__st_registry[name["token"]] = registry
					print(self.__st_registry)
				elif(isVM == True): # E vetor ou matriz
					size = lexema["dimensao"].split("x")
					if(len(size) == 1): # E vetor
						try:
							linha = int(size[0])
							if(len(linha.split(".")) > 1):  # Verifica se o valor e um inteiro
								print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento.")
								print("Esperado um valor numerico do tipo: \"inteiro\".")								
							else:
								# Armazena na tabela o novo atributo
								registry[atr_name["token"]]		  = {"type": atr_type["token"], "dimensao": linha}
								self.__st_registry[name["token"]] = registry
								print(self.__st_registry)
						except Exception as e:
							print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento.")
							print("Esperado um valor numerico do tipo: \"inteiro\".")
					elif(len(size) == 2): # E matriz
						try:
							linha  = int(size[0])
							coluna = int(size[1])
							if(len(linha.split(".")) > 1 or len(coluna.split(".")) > 1):  # Verifica se os valores sao inteiros
								print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento.")
								print("Esperado um valor numerico do tipo: \"inteiro\".")								
							else: 
								# Armazena na tabela o novo atributo
								registry[atr_name["token"]]       = {"type": atr_type["token"], "dimensao": size}
								self.__st_registry[name["token"]] = registry
								print(self.__st_registry)
						except Exception as e:
							print("[ERROR: linha " + line + "] Erro semantico: atributo \"" + atr_name["token"] + "\" do registro \"" +  name["token"] + "\" esta usando um tipo incorreto para dimensionamento.")
							print("Esperado um valor numerico do tipo: \"inteiro\".")
	# =========================================================================
	# =========================================================================
	# Metodo para analizar semanticamente o lado esquerdo de uma atribuicao
	def left_Assignment(self, linha, lexema):
		# Nome da variavel de atribuicao
		nome = lexema["name"]
		# Busca através do nome na tabela de simbolos para variaveis e constantes.
		check = self.__get_var_const(nome)
		if(check != ""): 
			# Verifica se o identificador pertecente a uma constante
			if(check["categoria"] == "constante"):
				print("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - \"" + nome + "\" e uma constante.")
				return False
			elif(check["categoria"] == "matriz" or check["categoria"] == "array"):
				return self.__access_vector_matrix(nome, check, lexema, linha)
			else:
				return True # Consiste em uma variavel simples.
		else:
			print("[ERROR: linha " + linha + "] Erro semantico: Atribuicao Invalida - \"" + nome + "\" nao foi declarado.")
			return False

	# =========================================================================
	# Metodo que realiza a analise semantica de acesso a vetores e matrizes
	def __access_vector_matrix(self, nome, data, lexema, linha):
		if(lexema["dimensao"] == "composto"):
			print("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\". Elementos compostos nao sao permitidos como index de vetor ou matriz.")
			return False
		elif(lexema["dimensao"] == None): # Verifica se foi passados os index de acesso
			# Nenhum index foi informado.
			print("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\". Nenhum index foi informado.")
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
					print("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\" nao e um vetor.")
					return False
			elif(len(size) == 2): # MATRIZ ===============================================================
				if(data["categoria"] == "matriz"):
					# Realiza analise dos index da matriz
					return self.__analysis_Matrix(nome, size[0], size[1], linha)
				else:
					print("[ERROR: linha " + linha + "] Erro semantico: Acesso Invalido - \"" + nome + "\" nao e uma matriz.")
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
				# Verificar se esse identificador foi declarado.
				test = self.__get_var_const(index["token"])
				if(test != ""):
					if(test["categoria"] == "variavel" or test["categoria"] == "constante"):
						if(test["tipo"] != "inteiro"):
							print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido na matriz - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".")
							result = False
					else:
						print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido na matriz - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".") 
						result = False
				else:
					print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido - \"" + test["token"] + " nao foi declarado.") 
					result = False
			elif(index["sigla"] == "NRO"):
				number = coluna["token"]
				# Verifica se o index recebido e um inteiro
				if(len(number.split(".")) > 1):
					print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso Invalido - na matriz \"" + nome + "\". Esperando index do tipo \"inteiro\".")
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
						print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido no vetor - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".")
						return False
				else:
					print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido no vetor - \"" + nome + "\". Esperando constante ou variavel do tipo \"inteiro\".") 
					return False
			else:
				print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso invalido - \"" + test["token"] + " nao foi declarado.") 
				return False
		elif(coluna["sigla"] == "NRO"):
			number = coluna["token"]
			# Verifica se o index recebido e um inteiro
			if(len(number.split(".")) > 1):
				print("[ERROR: linha " + assignment_line + "] Erro semantico: Acesso Invalido - no vetor \"" + nome + "\". Esperando index do tipo \"inteiro\".")
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
