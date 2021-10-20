####################################################################
# Instituição: Universidade Estadual de Feira de Santana
# Autores: Gabriel Sá e João Pedro
# Data: -- de -- de 2021
# ##################################################################
from syntatic_analyzer import Syntatic_analyzer
from files            import Files


files = Files()
def main():
	files.read()
	my_tokens = files.get_tokens()
	#print(my_tokens)
	syntatic_analyzer = Syntatic_analyzer(my_tokens)
	if( syntatic_analyzer.number_of_tokens() > 0):
		print("[INFO] Análise Sintática Iniciada.")
		syntatic_analyzer.Program()
		print("[INFO] Análise Sintática Encerrada.")

if __name__ == "__main__":
	main()