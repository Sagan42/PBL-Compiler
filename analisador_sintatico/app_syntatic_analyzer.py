####################################################################
# Instituição: Universidade Estadual de Feira de Santana
# Autores: Gabriel Sá e João Pedro
# Data: -- de -- de 2021
# ##################################################################
from files import Files
files = Files()
def main():
	files.read()
	my_tokens = files.get_tokens()
	print(my_tokens)

if __name__ == "__main__":
	main()
