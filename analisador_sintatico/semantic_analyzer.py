class Semantic_Analyzer(object):
	"""docstring for Semantic_Analyzer"""
	def __init__(self):
		# st = simbol table
		# Tabela de simbolos para variaveis e constantes
		self.__st_var_const = {}

	def Print_st_var_const(self):
		print("===================================================================================")
		print("[INFO] Tabela de simbolos para variaveis e constantes. ============================")
		a = list(self.__st_var_const.items())
		for x in range(len(a)):
			print(a[x])
			print("\n")
		print("===================================================================================")

	# Funcao para realizar a analise semantica da declaracao de variaveis e constantes.
	def analyzer_var_const(self, linha, lexema, table):
		# == Primeira verificacao: analise dos nomes. ========================================
		try:
			check = self.__st_var_const[ table["nome"] ]
			if((check["categoria"] == "variavel" and table["categoria"] == "variavel") or (check["categoria"] == "constante" and table["categoria"] == "constante")):
				if(check["escopo"] == "local" and table["escopo"] == "local"):
					# erro de declaracao de variaveis locais redeclaracadas.
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
				elif(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de declaracao de variaveis locais com o mesmo nome de uma global.
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma " + check["categoria"] + " global.")
					elif(table["escopo"] == "global"):
						# erro de declaracao de variaveis globais redeclaracadas.
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" está sendo declarada mais de uma vez.")
			if( (check["categoria"] == "variavel" and table["categoria"] == "constante") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel global com o mesmo nome de uma constante local
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
			if( (check["categoria"] == "constante" and table["categoria"] == "variavel") ):
				if(check["escopo"] == "global"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante global.
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")
					elif(table["escopo"] == "global"):
						# erro de variavel global com o mesmo nome de uma constante global.
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(global) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (global).")				
				elif(check["escopo"] == "local"):
					if(table["escopo"] == "local"):
						# erro de variavel local com o mesmo nome de uma constante local.
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(local) " + " \"" + table["nome"] + "\" com o mesmo nome de uma constante (local).")
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
		if(table["tipo"] == "vazio"):
			print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" está usando vazio como tipo.")
			print("Esperado tipo: inteiro, real, char, cadeia, booleano.\n")
		elif(table["init"] == True):            # variavel/constante foi inicializada.
			valor = lexema["valor"]             # Pega o token utilizado na inicializacao
			tipo  = lexema["tipo"]              # Pega o token utilizado no tipo da constante/variavel
			if(tipo["token"] == "inteiro"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 1): # Verifica se o valor e um inteiro
						return
					else:
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "real"):
				if(valor["sigla"] == "NRO"):    # Verifica se o valor de inicializacao e um numero
					v = str(valor["token"])     # converte para string
					if(len(v.split(".")) == 2): # Verifica se o valor e um real
						return
					else:
						print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
						print("Esperado um valor do tipo: " + tipo["token"] + "\n")
						return
				else:
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "booleano"):
				if(valor["token"] == "verdadeiro" or valor["token"] == "falso"):  # Verifica se o valor de inicializacao e um booleano.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "char"):
				if(valor["sigla"] == "CAR"):  # Verifica se o valor de inicializacao e um char.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
			if(tipo["token"] == "cadeia"):
				if(valor["sigla"] == "CAD"): # Verifica se o valor de inicializacao e uma cadeia de caracteres.
					return
				else:
					print("[ERROR: linha " + linha + "] Erro semântico: " + table["categoria"] + "(" + table["escopo"] + ") \"" + table["nome"] + "\" usando tipo incorreto para inicializacao.")
					print("Esperado um valor do tipo: " + tipo["token"] + "\n")
					return
		# == Fim da Segunda Verificacao ==========================================
		