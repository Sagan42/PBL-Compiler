import os

class Files():
    def __init__(self):
        self.__tokens = []
        self.__absolute_Path = os.path.abspath("../")
        self.__inputPath = "/analisador_lexico/output"
        self.__outputPath     = "/analisador_sintatico/output"
        self.__nameOutputFile = "saida"
        self.__counterFile = 0
        self.__inputFile_ID = 0  # identificador do arquivo de entrada atual.
        self.__indexFile = 0  # Index atual do vetor de arquivos de entrada.
        self.__files = []  # Lista com os nomes de todos os arquivos de entrada.
        self.__lines = []  # Atributo com todas as linhas do arquivo que sera processador.

    def read(self):
        path = self.__absolute_Path + self.__inputPath
        # Busca todos os nomes dos arquivos de entrada.
        self.__files = name_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        self.__sort_file()
        if (len(self.__files) == 0):
            # Não existem arquivos de entrada
            return False
        else:
            # Seta o primeiro arquivo a ser lido
            name = self.__files[0]
            name = name.replace(".txt", "")
            self.__inputFile_ID = name[5:]
            self.__nameOutputFile = "saida" + self.__inputFile_ID + ".txt"
            self.__indexFile += 1
            # Busca e ler o primeiro arquivo a ser analisado
            file_path = self.__absolute_Path + self.__inputPath + "/" + self.__files[0]
            with open(file_path, 'r') as f:
                # Ler linha a linha do arquivo
                for lines in f:
                    line = lines.split(' ')
                    token = line[2].replace("\n","")
                    sigla = line[1].replace("\n","")
                    linha = line[0].replace("\n","")
                    dict = {"token": token, "sigla": sigla, "linha": linha}
                    self.__tokens.append(dict)
            f.close()
            return True

    def set_nextFile(self):
        size = len(self.__files)
        if (self.__indexFile < size):
            # Busca e ler o proximo arquivo a ser analisado
            file_path = self.__absolute_Path + self.__inputPath + "/" + self.__files[self.__indexFile]
            # Limpa o dicionario de tokens atuais.
            self.__tokens.clear()
            with open(file_path, 'r') as f:
                # Ler todas as linhas do arquivo
                for lines in f:
                    line = lines.split(' ')
                    token = line[2].replace("\n","")
                    sigla = line[1].replace("\n","")
                    linha = line[0].replace("\n","")
                    dict = {"token": token, "sigla": sigla, "linha": linha}
                    self.__tokens.append(dict)
            f.close()
            # Atualiza o ID para o arquivo atual
            name = self.__files[self.__indexFile]
            name = name.replace(".txt", "")
            self.__inputFile_ID = name[5:]
            self.__nameOutputFile = "saida" + self.__inputFile_ID + ".txt"
            # Atualiza o index para o proximo arquivo
            self.__indexFile += 1
            return True
        else:
            # Todos os arquivos ja foram processados
            return False

    def __sort_file(self):
        """Algoritmo de ordenacao por selecao"""
        for j in range(1, len(self.__files)):
            chave = self.__files[j]
            name = self.__files[j]
            name = name.replace("saida", "")
            x = int(name.replace(".txt", ""))
            i = j - 1
            name_i = self.__files[i]
            name_i = name_i.replace("saida", "")
            y = int(name_i.replace(".txt", ""))
            while i >= 0 and y > x:
                self.__files[i + 1] = self.__files[i]
                i -= 1
                name_i = self.__files[i]
                name_i = name_i.replace("saida", "")
                y = int(name_i.replace(".txt", ""))
            else:
                self.__files[i + 1] = chave

    def get_tokens(self):
        return self.__tokens

    def write_in_file(self, linha, token_atual, waiting):
        expected_tokens = ""
        expected_tokens = "\"" + str(waiting[0]) + "\""
        for x in range(1,len(waiting)):
            expected_tokens = expected_tokens + ",\"" + str(waiting[x]) + "\""
        out = "linha " + str(linha) + "[erro sintatico: token lido " + "\"" + str(token_atual) + "\"], tokens esperados [" + expected_tokens + "]\n"   
        # Monta o caminho de escrita do arquivo de saída.
        path = self.__absolute_Path + self.__outputPath + "/" + self.__nameOutputFile
        # Verifica se o arquivo existe
        if not os.path.exists(path):
            """Creates the output file"""
            with open(path, 'w') as f:
                f.write(out)
            f.close()
        else:
            with open(path, 'a') as f:
                f.write(out)
            f.close()