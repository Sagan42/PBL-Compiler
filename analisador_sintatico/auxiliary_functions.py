import string

class Auxiliary_Functions():
	"""docstring for Auxiliary_Functions"""
	def __init__(self):
		pass

	# Funcao que verifica se um símbolo terminal pertence ao conjunto seguinte de um nao-terminal da linguagem.
	def Follow(self, non_terminal, token, sigla):
		if(non_terminal == "v_m_access"):
			return self.__follow_v_m_access(token, sigla)
		elif(non_terminal == "vector_matrix"):
			return self.__follow_vector_matrix(token, sigla)
		elif(non_terminal == "exprValorMod"):
			return self.__exprValorMod(token, sigla)
		elif(non_terminal == "exprArt"):
			return self.__follow_exprArt(token, sigla)
		elif(non_terminal == "exprRel"):
			return self.__follow_exprRel(token, sigla)
		elif(non_terminal == "exprNumber"):
			return self.__follow_exprNumber(token, sigla)


	# Funcao que verifica se um símbolo terminal pertence ao conjunto primeiro de um nao-terminal da linguagem.
	def First(self, non_terminal, token, sigla):
		if(non_terminal == "function_body"):
			return self.__function_body(token, sigla)
		elif(non_terminal == "function_body1"):
			return self.__function_body1(token, sigla)
		elif(non_terminal == "function_body2"):
			return self.__function_body2(token, sigla)
		elif(non_terminal == "expressao"):
			return self.__expressao(token, sigla)
		elif(non_terminal == "value_with_expressao"):
			return self.__value_with_expressao(token, sigla)
		elif(non_terminal == "com_retornar"):
			return self.__com_retornar(token,sigla)
		elif(non_terminal == "read_cmd"):
			return self.__read_cmd(token,sigla)
		elif(non_terminal == "write_cmd"):
			return self.__write_cmd(token,sigla)
		elif(non_terminal == "com_para"):
			return self.__com_para(token,sigla)
		elif(non_terminal == "com_enquanto"):
			return self.__com_enquanto(token,sigla)
		elif(non_terminal == "se"):
			return self.__se(token,sigla)
		elif(non_terminal == "senao"):
			return self.__senao(token,sigla)
		elif(non_terminal == "function_declaration1"):
			return self.__function_declaration1(token, sigla)
		elif(non_terminal == "function_declaration2"):
			return self.__function_declaration2(token,sigla)
		elif(non_terminal == "function_parameters"):
			return self.__function_parameters(token, sigla)
		elif(non_terminal == "function_parameters2"):
			return self.__function_parameters2(token, sigla)
		elif(non_terminal == "function_parameters5"):
			return self.__function_parameters5(token, sigla)
		elif(non_terminal == "varList2"):
			return self.__varList2(token, sigla)
		elif(non_terminal == "functionCall"):
			return self.__functionCall(token, sigla)
		elif(non_terminal == "atr"):
			return self.__atr(token, sigla)
		elif(non_terminal == "var_atr"):
			return self.__var_atr(token, sigla)
		elif(non_terminal == "var_atr_1"):
			return self.__var_atr_1(token, sigla)
		elif(non_terminal == "value_with_IDE"):
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
		elif(non_terminal == "operatorSoma"):
			return self.__operatorSoma(token, sigla)
		elif(non_terminal == "operatorAuto0"):
			return self.__operatorAuto0(token, sigla)
		elif(non_terminal == "read_value"):
			return self.__read_value(token, sigla)
		elif(non_terminal == "operatorLog"):
			return self.__operatorLog(token, sigla)
		elif(non_terminal == "operatorMulti"):
			return self.__operatorMulti(token, sigla)
		elif(non_terminal == "operatorRel"):
			return self.__operatorRel(token, sigla)
		else:
			return False


	# == Conjuntos Primeiro ===============================================================================
	def __function_declaration1(self, token, sigla):
		if(token == "algoritmo" or sigla == "IDE"):
			return True
		else:
			return False

	def __function_declaration2(self, token, sigla):
		if(sigla == "IDE"):
			return True
		else:
			return False

	def __function_body(self, token, sigla):
		if(self.__declaration_const(token, sigla) == True or self.__function_body1(token,sigla) == True):
			return True
		else:
			return False

	def __function_body1(self, token, sigla):
		if(self.__declaration_var(token, sigla) == True or self.__function_body2(token,sigla) == True):
			return True
		else:
			return False

	def __function_body2(self, token, sigla):
		if(self.__com_enquanto(token, sigla) == True or self.__com_para(token, sigla) == True or self.__se(token, sigla) == True or self.__write_cmd(token, sigla) == True or self.__read_cmd(token, sigla) == True or sigla == "IDE" or token == "retorno"):
			return True
		else:
			return False

	def __value_with_expressao(self,token,sigla):
		if(self.__expressao(token, sigla) == True or sigla == "CAD" or sigla == "CAR"):
			return True
		else:
			return False

	def __expressao(self,token,sigla):
		if(self.__follow_exprRel(token, sigla) == True or token == "(" or token == "!"):
			return True
		else:
			return False

	def __com_retornar(self,token,sigla):
		if(token == "retorno"):
			return True
		else:
			return False
	def __write_cmd(self, token, sigla):
		if(token == "escreva"):
			return True
		else:
			return False

	def __read_cmd(self, token, sigla):
		if(token == "leia"):
			return True
		else:
			return False

	def __com_enquanto(self, token, sigla):
		if(token == "enquanto"):
			return True
		else:
			return False

	def __com_para(self, token, sigla):
		if(token == "para"):
			return True
		else:
			return False

	def __se(self,token,sigla):
		if(token == "se"):
			return True
		else:
			return False

	def __senao(self,token,sigla):
		if(token == "senao"):
			return True
		else:
			return False

	def __function_parameters(self, token, sigla):
		if(token == "(" ):
			return True
		else:
			return False

	def __function_parameters2(self, token, sigla):
		if(self.__primitive_type(token, sigla) == True or sigla == "IDE"):
			return True
		else:
			return False
	
	def __function_parameters5(self, token, sigla):
		if(token == "," or token == ")" ):
			return True
		else:
			return False

	def  __varList2(self, token, sigla):
		if(token == "," or token == ")" ):
			return True
		else:
			return False

	def  __functionCall(self, token, sigla):
		if(token == "("):
			return True
		else:
			return False
	
	def  __atr(self, token, sigla):
		if(token == "="):
			return True
		else:
			return False

	def  __var_atr(self, token, sigla):
		if(sigla == "IDE"):
			return True
		else:
			return False

	def __var_atr_1(self,token,sigla):
		if(token == "=" or token == "[" or token == "."):
			return True
		else:
			return False

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

	def __operatorSoma(self, token, sigla):
		if(token == "+" or token == "-"):
			return True
		else:
			return False

	def __operatorAuto0(self, token, sigla):
		if(token == "++" or token == "--"):
			return True
		else:
			return False

	def __read_value(self, token, sigla):
		if (sigla == "IDE"):
			return True
		else:
			return False

	def __operatorLog(self, token, sigla):
		if (token == "&&" or token == "||"):
			return True
		else:
			return False

	def __operatorMulti(self, token, sigla):
		if (token == "*" or token == "/"):
			return True
		else:
			return False

	def __operatorRel(self, token, sigla):
		if (token == "==" or token == ">=" or token == "<=" or token == "!=" or token == ">" or token == "<"):
			return True
		else:
			return False
	# == Fim dos Conjuntos Primeiro ==========================================================================

	# ========================================================================================================
	# == Conjuntos Seguinte ==================================================================================
	def __follow_v_m_access(self,token,sigla):
		if(token == "," or token == ";" or token == ")" or token == "." or token == "=" or token == "}"):
			return True
		else:
			return False

	def __follow_vector_matrix(self,token,sigla):
		if(token == "," or token == ";"):
			return True
		else:
			return False

	def __exprValorMod(self, token, sigla):
		if(sigla == "NRO" or token == "++" or sigla == "IDE"):
			return True
		else:
			return False

	def __follow_exprArt(self, token, sigla):
		if(token == "+" or token == "-" or sigla == "NRO" or token == "++" or token == "--" or sigla == "IDE"):
			return True
		else:
			return False

	def __follow_exprRel(self, token, sigla):
		if (token == "+" or token == "-" or sigla == "NRO" or token == "++" or token == "--" or sigla == "IDE" or token == "verdadeiro" or token == "falso"):
			return True
		else:
			return False

	def __follow_exprNumber(self, token, sigla):
		if (token == "("):
			return True
		else:
			return False
	# == Fim dos Conjuntos Seguinte ==========================================================================