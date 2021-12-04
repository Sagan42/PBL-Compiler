####################################################################
# Instituição: Universidade Estadual de Feira de Santana
# Autores: Gabriel Sá e João Pedro
# Data: 31 de agosto de 2021
# ##################################################################
from lexical_analyzer import Lexical_analyzer
from files            import Files
from auxiliary_functions import Auxiliary_functions
# Estados
# 1 = inicial
# 2 = palavras reservadas e identificadores
# 3 = operador relacional "!"
# 4 = operadores lógicos
# 5 = operadores relacionais
# 6 = operadores aritméticos
# 7 = numeros
# 8 = delimitadores
# 9 = caractere
# 10 = simbolo invalido
# 11 = cadeia de caracteres
# 12 = comentario de bloco
#success  = []  # Lista que armazena os resultados de sucesso da analise
failures = []  # Lista que armazena os resultados de falha da analise
tokens   = []
files    = Files()

#def add_success(line, sigla, lexema, success_operation):
#	global success
#	global failures
#	value = ""
#	if(line >= 0 and line < 10):
#		value = "0" + str(line)
#	else:
#		value = str(line)
#	value += " " + sigla + " " + lexema
#	if(success_operation):
#		success.append(value)
#	else:
#		failures.append(value)

#def salve_result():
#	global success
#	global failures
#	size_sucess   = len(success)
#	size_failures = len(failures)
#	if(size_sucess > 0):
#		while(len(success) > 0):
#			data = success.pop(0)       # Retira o primeiro elemento da lista
#			if "\n" in data:
#				data = data.replace("\n","") # Retira o \n para escrita no arquivo de saída
#			files.write_in_file(data)  # Armazena os resultados de sucesso no arquivo de saída correspondente ao arquivo de entrada
#			files.write_in_file("\n")
#	if(size_failures > 0):
#		while(len(failures) > 0):
#			data = failures.pop(0)       # Retira o primeiro elemento da lista
#			if "\n" in data:
#				data = data.replace("\n","") # Retira o \n para escrita no arquivo de saída
#			files.write_in_file("\n")
#			files.write_in_file(data)   # Armazena os resultados de falha no arquivo de saída correspondente ao arquivo de entrada

def add_token(line, sigla, lexema):
	global success
	global failures
	value = ""
	if(line >= 0 and line < 10):
		value = "0" + str(line)
	else:
		value = str(line)
	value += " " + sigla + " " + lexema
	tokens.append(value)

def add_failures_tokens(line, sigla, lexema):
	global success
	global failures
	value = ""
	if(line >= 0 and line < 10):
		value = "0" + str(line)
	else:
		value = str(line)
	value += " " + sigla + " " + lexema
	print("[ERROR] erro lexico" + "[" + sigla + "]: Linha [" + str(line) + "] Lexema: " + lexema)
	failures.append(value)

def salve_result():
	global success
	global failures
	failures = []                            # Limpa a lista de erros lexicos
	size = len(tokens)
	if(size > 0):
		while(len(tokens) > 0):
			data = tokens.pop(0)             # Retira o primeiro elemento da lista
			if "\n" in data:
				data = data.replace("\n","") # Retira o \n para escrita no arquivo de saída
			files.write_in_file(data)        # Armazena os resultados de sucesso no arquivo de saída correspondente ao arquivo de entrada
			files.write_in_file("\n")

def analyze_result(line, result):
	sigla = result[0]
	# Verifica se corresponde a um erro lexico
	if(sigla == "SII" or sigla == "CMF" or sigla == "NMF" or sigla == "CaMF" or sigla == "CoMF" or sigla == "OpMF"):
		add_failures_tokens(line, sigla, result[1])
	add_token(line, sigla, result[1])

def main():
	functions = Auxiliary_functions()
	analyser  = Lexical_analyzer()
	state     = 1                   # Estado inicial
	current_line = 0                # Linha inicial de um arquivo.
	result = files.set_inputFiles() # Verifica todos os arquivos de entrada e seta o primeiro arquivo a ser lido.
	files.delete_out_files()        # Exclue todos os arquivos de saida para iniciar uma nova analise
	if(result):                     # Inicia o processamento dos arquivos de entrada.
		state = 1                   # Estado inicial
		while(True):                # Loop para analise de todos os arquivos de entrada.
			content      = files.getContent()           # Captura o conteudo do arquivo atual que esta sendo analisado.
			current_line = 0
			print("==================================================================")
			print("[INFO] Análise Léxica Iniciada.")
			print("[INFO] ARQUIVO: " + files.get_number_of_input())
			while(current_line < (len(content)) ):  # Loop para analise do arquivo atual
				nextLine         = content[current_line]
				initial_position = 0
				while(initial_position < len(nextLine)):  # Loop para analise da linha atual
					if(state == 1):                       # ESTADO INICIAL
						c = nextLine[initial_position]    # Pega o primeiro caractere a ser analisado
						if(functions.isLetter(c)):
							state = 2	                  # Estado de palavras reservadas e identificadores
						elif(functions.isDelimiter(c)):
							if(c == "%"):
								break                     # Comentario de linha
							elif(ord(c) == 32 or ord(c) == 9 or c == "\n"): # " " ou \t
								state = 1
								initial_position +=1
							elif(c == "{" and nextLine[initial_position + 1] == "#"):
								state = 12                # Estado para comentário de bloco
							else:
								state = 8
						elif(c == "%"):                   # Comentário de linha
							break                         # Ignora o restante da linha
						elif(c == '!'):
							state = 3                     # Estado para operador ! ou !=
							initial_position +=1
						elif(functions.isOperatorRelational(c)):
							state = 5                     # Estado para os outros operadores relacionais >= > <= < = ==
						elif(functions.isArithmeticOperators(c)):
							state = 6                     # Estado para os operadores aritméticos.
						elif(functions.isLogicalOperators(c)):
							state = 4                     # Estado para os operadores logicos
						elif(functions.isDigit(c)):
							state = 7
						elif(c == "\'"): # inicio de um caractere
							state = 9
						elif(functions.isSymbol(c) == True or functions.invalid_symbol(c) == True):
							state = 10                    # Estado para reconhecimento de simbolos invalidos
						elif(c == "\""):                  # Estado para reconhecimento de uma cadeia de caracteres
							state = 11
						else:
							state = 1
							initial_position += 1
					elif(state == 2):
						auto_result = analyser.auto_keywords_identifier(nextLine, initial_position)
						initial_position = auto_result[2]  # Atualiza a posição para leitura do próximo caractere.
						analyze_result(current_line + 1, auto_result)
						state = 1                           # Volta ao estado inicial
					elif(state == 3):
						char = nextLine[initial_position]
						if(char == '>' or char == '<' or char == '='):
							initial_position -= 1
							auto_result       = analyser.auto_relational_operators(nextLine, initial_position)
							initial_position  = auto_result[2]  # Atualiza a posição para leitura do próximo caractere.
							analyze_result(current_line + 1, auto_result)
							state = 1
						else:
							initial_position -= 1
							auto_result       = analyser.auto_logical_operators(nextLine, initial_position)
							initial_position  = auto_result[2]  # Atualiza a posição para leitura do próximo caractere.
							analyze_result(current_line + 1, auto_result)
							state = 1
					elif(state == 4):
							auto_result       = analyser.auto_logical_operators(nextLine, initial_position)
							initial_position  = auto_result[2]  # Atualiza a posição para leitura do próximo caractere.
							analyze_result(current_line + 1, auto_result)
							state = 1
					elif(state == 5):
						auto_result       = analyser.auto_relational_operators(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 6):
						auto_result       = analyser.auto_arithmetic_operators(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 7):
						auto_result       = analyser.auto_numbers(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 8):
						auto_result       = ["DEL", c]
						initial_position += 1
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 9):
						auto_result       = analyser.auto_character(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 10):
						auto_result       = analyser.auto_symbol(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 11):
						auto_result       = analyser.auto_string(nextLine, initial_position)
						initial_position  = auto_result[2]     # Atualiza a posição para leitura do próximo caractere.
						state = 1
						analyze_result(current_line + 1, auto_result)
					elif(state == 12):
						auto_result       = analyser.auto_comment(content, current_line, initial_position) # Envia como parâmetro todo o restante do arquivo para verificar até onde o comentário se extende.
						initial_position  = auto_result[1]        # Atualiza a posição inicial.
						current_line      = auto_result[0]        # Atualiza linha atual.
						state             = 1
						if(auto_result[2] == False): # Erro no comentario de bloco
							analyze_result(auto_result[3] + 1, ["CoMF", auto_result[4]])
							break
						else:
							nextLine  = content[current_line] # Atualiza o vetor que contém a linha atual.
				current_line += 1                           # Finalizou uma linha e inicia a analise de outra.
			print("==================================================================")
			print("[INFO] Análise Léxica do arquivo " + files.get_number_of_input() + " encerrada.")
			if(len(failures) > 0):
				print("[INFO] " + files.getCurrent_File_Name() + ": " + str(len(failures)) + " erros.")
			else:
				print("[INFO] " + files.getCurrent_File_Name() + ": sem erros.")
			print("==================================================================\n")
			salve_result()     # Salva os possíveis resultados de falha e sucesso da analise do arquivo atual.
			result = files.set_nextFile()
			if(result == False):
				print("[INFO] Analise Finalizada.")
				break

	else:
		print("[INFO] Não existem arquivos a serem processados.")

if __name__ == "__main__":
	main()