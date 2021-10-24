import string

class Auxiliary_Functions():
	"""docstring for Auxiliary_Functions"""
	def __init__(self):
		pass

	# Funcao que verifica se um símbolo terminal pertence ao conjunto seguinte de um nao-terminal da linguagem.
	def Follow(self, non_terminal, token, sigla):
		if(non_terminal == "v_m_access"):
			return self.__follow_v_m_access(token, sigla)


	# Funcao que verifica se um símbolo terminal pertence ao conjunto primeiro de um nao-terminal da linguagem.
	def First(self, non_terminal, token, sigla):
		if(non_terminal == "value_with_IDE"):
			return self.__value_with_IDE(token,sigla)
		elif(non_terminal == "value_without_IDE"):
			return self.__value(token,sigla)
		elif(non_terminal == "type"):
			return self.__type(token, sigla)
		elif(non_terminal == "value"):
			return self.__value(token, sigla)
		elif(non_terminal == "primitive_type"):
			return self.__primitive_type(token, sigla)
		elif(non_terminal == "declaration_reg"):
			return self.__declaration_reg(token, sigla)
		elif(non_terminal == "declaration_reg1"):
			return self.__declaration_reg1(token, sigla)
		elif(non_terminal == "declaration_reg2"):
			return self.__declaration_reg2(token, sigla)
		elif(non_terminal == "declaration_reg3"):
			return self.__declaration_reg3(token, sigla)
		elif(non_terminal == "declaration_reg4"):
			return self.__declaration_reg4(token, sigla)
		elif(non_terminal == "declaration_reg5"):
			return self.__declaration_reg5(token, sigla)
		elif(non_terminal == "elem_registro"):
			return self.__elem_registro(token, sigla)
		elif(non_terminal == "nested_elem_registro"):
			return self.__nested_elem_registro(token, sigla)
		elif(non_terminal == "nested_elem_registro1"):
			return self.__nested_elem_registro1(token, sigla)
		elif(non_terminal == "v_m_access"):
			return self.__v_m_access(token, sigla)
		elif(non_terminal == "v_m_access1"):
			return self.__v_m_access1(token, sigla)
		elif(non_terminal == "v_m_access2"):
			return self.__v_m_access2(token, sigla)
		elif(non_terminal == "v_m_access3"):
			return self.__v_m_access3(token, sigla)
		elif(non_terminal == "declaration_const"):
			return self.__declaration_const(token, sigla)
		elif(non_terminal == "declaration_const1"):
			return self.__declaration_const1(token, sigla)
		elif(non_terminal == "declaration_const2"):
			return self.__declaration_const2(token, sigla)
		elif(non_terminal == "vector_matrix"):
			return self.__vector_matrix(token, sigla)
		elif(non_terminal == "vector_matrix_1"):
			return self.__vector_matrix_1(token, sigla)
		elif(non_terminal == "vector_matrix_2"):
			return self.__vector_matrix_2(token, sigla)
		elif(non_terminal == "init_matrix"):
			return self.__init_matrix(token, sigla)
		elif(non_terminal == "init_matrix_1"):
			return self.__init_matrix_1(token, sigla)
		elif(non_terminal == "init_matrix_2"):
			return self.__init_matrix_2(token, sigla)
		elif(non_terminal == "init_vector"):
			return self.__init_vector(token, sigla)
		elif(non_terminal == "init_vector_1"):
			return self.__init_vector_1(token, sigla)
		elif(non_terminal == "init_vector_2"):
			return self.__init_vector_2(token, sigla)
		elif(non_terminal == "declaration_var"):
			return self.__declaration_var(token, sigla)
		elif(non_terminal == "declaration_var1"):
			return self.__declaration_var1(token, sigla)
		elif(non_terminal == "declaration_var2"):
			return self.__declaration_var2(token, sigla)
		elif(non_terminal == "declaration_var3"):
			return self.__declaration_var3(token, sigla)
		else:
			return False


	# == Conjuntos Primeiro ===============================================================================
	def __value_with_IDE(self,token,sigla):
		if(self.__value(token,sigla) == True or sigla == "IDE"):
			return True
		else:
			return False

	def __type(self,token,sigla):
		if(self.__primitive_type(token, sigla) == True or sigla == "IDE"):
			return True
		else:
			return False

	def __value(self, token, sigla):
		if(sigla == "NRO" or sigla == "CAD" or sigla == "CAR" or token == "verdadeiro" or token == "falso"):
			return True
		else:
			return False

	def __primitive_type(self, token,sigla):
		if(token == "inteiro" or token == "real" or token == "booleano" or token == "char" or token == "cadeia" or token == "vazio"):
			return True
		else:
			return False

	def __declaration_reg(self, token,sigla):
		if(token == "registro"):
			return True
		else:
			return False

	def __declaration_reg1(self,token, sigla):
		if(token == "inteiro" or token == "real" or token == "booleano" or token == "char" or token == "cadeia" or token == "vazio"):
			return True
		elif(sigla == "IDE"):
			return True
		else:
			return False

	def __declaration_reg2(self,token, sigla):
		if(token == "," or token == ";"):
			return True
		else:
			return False

	def __declaration_reg3(self,token, sigla):
		if(token == "}"):
			return True
		else:
			return False

	def __declaration_reg4(self,token, sigla):
		if(self.__v_m_access(token,sigla) == True or token == "," or token == ";"):
			return True
		else:
			return False

	def __declaration_reg5(self,token, sigla):
		if(self.__declaration_reg1(token, sigla) == True or self.__declaration_reg3(token, sigla) == True):
			return True
		else:
			return False

	def __elem_registro(self,token, sigla):
		if(token == "."):
			return True
		else:
			return False

	def __nested_elem_registro(self,token, sigla):
		if(token == "." or self.__v_m_access(token, sigla) == True):
			return True
		else:
			return False

	def __nested_elem_registro1(self,token, sigla):
		if(self.__elem_registro(token, sigla) == True):
			return True
		else:
			return False

	def __declaration_var(self,token, sigla):
		if(token == "variaveis"):
			return True
		else:
			return False

	def __declaration_var1(self,token, sigla):
		if(sigla == "IDE" or token == "inteiro" or token == "real" or token == "booleano" or token == "char" or token == "cadeia" or token == "vazio"):
			return True
		elif(token == "}"):
			return True
		else:
			return False


	def __declaration_var2(self,token, sigla):
		if(token == "=" or self.__vector_matrix(token, sigla) == True or self.__declaration_var3(token, sigla) == True):
			return True
		else:
			return False


	def __declaration_var3(self,token, sigla):
		if(token == "," or token == ";" ):
			return True
		else:
			return False

	def __vector_matrix(self,token, sigla):
		if(token == "["):
			return True
		else:
			return False

	def __vector_matrix1(self,token, sigla):
		if(token == "[" or token == "=" or self.__declaration_var3(token, sigla) == True):
			return True
		else:
			return False


	def __vector_matrix2(self,token, sigla):
		if(token == "=" or self.__declaration_var3(token, sigla) == True):
			return True
		else:
			return False


	def __init_vector(self,token, sigla):
		if(token == "["):
			return True
		else:
			return False

	def __init_vector_1(self,token, sigla):
		if(sigla == "IDE" or sigla == "NRO" or sigla == "CAD" or sigla == "CAR" or token == "verdadeiro" or token == "falso"):
			return True
		else:
			return False

	def __init_vector_2(self,token, sigla):
		if(token == "," or token == "]"):
			return True
		else:
			return False

	def __init_matrix(self,token, sigla):
		if(token == "["):
			return True
		else:
			return False

	def __init_matrix_1(self,token, sigla):
		if(sigla == "IDE" or sigla == "NRO" or sigla == "CAD" or sigla == "CAR" or token == "verdadeiro" or token == "falso"):
			return True
		else:
			return False

	def __init_matrix_2(self,token, sigla):
		if(token == "," or token == ";" or token == "]"):
			return True
		else:
			return False


	def __declaration_const(self,token, sigla):
		if(token == "constantes"):
			return True
		else:
			return False

	def __declaration_const1(self,token, sigla):
		if(token == "inteiro" or token == "real" or token == "booleano" or token == "char" or token == "cadeia" or token == "vazio"):
			return True
		elif(token == "}"):
			return True
		else:
			return False

	def __declaration_const2(self,token, sigla):
		if(token == "," or token == ";"):
			return True
		else:
			return False


	def __v_m_access(self,token, sigla):
		if(token == "["):
			return True
		else:
			return False

	def __v_m_access1(self,token, sigla):
		if(sigla == "IDE" or sigla == "NRO"):
			return True
		else:
			return False

	def __v_m_access2(self,token, sigla):
		if(self.__elem_registro(token, sigla) == True or token == "["):
			return True
		else:
			return False

	def __v_m_access3(self,token, sigla):
		if(token == "["):
			return True
		else:
			return False
	# == Fim dos Conjuntos Primeiro ==========================================================================


	# == Conjuntos Seguinte ==================================================================================
	def __follow_v_m_access(self,token,sigla):
		if(token == "," or token == ";" or token == ")" or token == "+" or token == "++" or token == "." or token == "=" or token == "}"):
			return True
		else:
			return False
	# == Fim dos Conjuntos Seguinte ==========================================================================