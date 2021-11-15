####################################################################
# Instituição: Universidade Estadual de Feira de Santana
# Autores: Gabriel Sá e João Pedro
# Data: -- de -- de 2021
# ##################################################################
from syntatic_analyzer import Syntatic_analyzer
from files            import Files

files = Files()
def main():
	result    = files.set_inputFiles()
	if(result == False):
		print("[INFO] Não existem arquivos para análise. ==================")
		return
	else:
		# Exclue todos os arquivos de saida para iniciar uma nova analise
		files.delete_out_files()
		while(result):
			my_tokens = files.get_tokens()
			syntatic_analyzer = Syntatic_analyzer(my_tokens, files)
			print("==================================================================")
			print("[INFO] Análise Sintática e Semântica Iniciada.")
			print("[INFO] ARQUIVO: " + files.get_number_of_input())
			print("==================================================================")
			syntatic_analyzer.Program()
			print("==================================================================")
			print("[INFO] Análise Sintática e Semântica do arquivo " + files.get_number_of_input() + " encerrada.")
			print("[INFO] ERROS: " + str(syntatic_analyzer.get_erros()))
			print("==================================================================\n")
			if(files.set_nextFile() == True):
				my_tokens = []
				my_tokens = files.get_tokens()
			else:
				print("[INFO] Todos os arquivos foram processados. ======================")
				result = False

if __name__ == "__main__":
	main()