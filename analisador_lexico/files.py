import os

class Files():
	def __init__(self):
		self.__absolute_Path = "/home/gabriel/Documents/livros/MI-Compiladores/analisador_lexico"
		self.__inputPath     = "/input"
		self.__outputPath    = "/output"    #
		self.__inputFile_ID  = 0 	 # identificador do arquivo de entrada atual.
		self.__indexFile     = 0 	 # Index atual do vetor de arquivos de entrada.
		self.__files         = []    # Lista com os nomes de todos os arquivos de entrada.
		self.__lines         = []    # Atributo com todas as linhas do arquivo que sera processador.  

	def set_inputFiles(self):
		path = self.__absolute_Path + self.__inputPath
		# Busca todos os nomes dos arquivos de entrada.
		self.__files = name_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
		if( len(self.__files) == 0):
			# Não existem arquivos de entrada
			return False
		else:
			# Seta o primeiro arquivo a ser lido
			name                = self.__files[0]
			name = name.replace(".txt","")
			self.__inputFile_ID = name[7:]
			self.__indexFile += 1
			# Busca e ler o primeiro arquivo a ser analisado
			file_path = self.__absolute_Path + self.__inputPath + "/" + self.__files[0]
			with open(file_path, 'r') as f:
				# Ler todas as linhas do arquivo
				self.__lines = f.readlines()
			f.close()
			return True

	def set_nextFile(self):
		size = len(self.__files)
		if(self.__indexFile < size):
			# Busca e ler o proximo arquivo a ser analisado
			file_path = self.__absolute_Path + self.__inputPath + "/" + self.__files[self.__indexFile]
			with open(file_path, 'r') as f:
				# Ler todas as linhas do arquivo
				self.__lines = f.readlines()
			f.close()
			# Atualiza o ID para o arquivo atual
			name                = self.__files[self.__indexFile]
			name = name.replace(".txt","")
			self.__inputFile_ID = name[7:]
			# Atualiza o index para o proximo arquivo
			self.__indexFile += 1
			return True
		else:
			# Todos os arquivos ja foram processados
			return False

	def write_in_file(self, data):
		# Monta o caminho de escrita do arquivo de saída.
		path = self.__absolute_Path + self.__outputPath + "/saida" + str(self.__inputFile_ID) + ".txt" 
		# Verifica se o arquivo existe
		if not os.path.exists(path):
			"""Creates the output file"""
			with open(path, 'w') as f:
				f.write(data)
			f.close()
		else:
			with open(path, 'a') as f:
				f.write(data)
			f.close()

	def getContent(self):
		return self.__lines

