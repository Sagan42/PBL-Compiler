class Syntactic_analyzer:
    def checkRegister (self, token):
        if token == 'registro':
            if token == 'IDE':
                if token == '{':
                    while token != '}':
                        if token == 'PRE':
                            if token == 'IDE':
                                if token == ';':
                                    control = True
                                elif token == '[':
                                    if token == 'IDE':
                                        if token == ']':
                                            if token == ';':
                                                control = True
                                            else:
                                                control = False
                                                print('Esperado um delimitador')
                                        else:
                                            control = False
                                            print('Esperado um delimitador')
                                    else:
                                        control = False
                                        print('Esperado um identificador')
                                else:
                                    control = False
                                    print('Esperado delimitador')
                            else:
                                control = False
                                print('Esperado identificador')
                        else:
                            control = False
                            print('Esperada palavra reservada.')
                else:
                    control = False
                    print('Esperado delimitador.')
            else:
                control = False
                print('Esperado identificador do registro.')
        else:
            control = False
            print('Esperada palavra reservada registro.')
        return control

    def checkConstants (self, token):
        if token == 'constantes':
            if token == '{':
                while token != '}':
                    if token == 'PRE':
                        if token == 'IDE':
                            if token == 'REL':
                                if token == 'NRO':
                                    if token == ';':
                                        control = True
                                    elif token == ',':
                                        while token != ';':
                                            if token == 'IDE':
                                                if token == 'REL':
                                                    if token == 'NRO':
                                                        control = True
                                                    else:
                                                        control = False
                                                        print('Esperado um número')
                                                else:
                                                    control = False
                                                    print('Esperado um operador relacional')
                                            else:
                                                control = False
                                                print('Esperado um identificador')
                                    else:
                                        control = False
                                        print('Esperado um delimitador')
                                else:
                                    control = False
                                    print('Esperado um número')
                            else:
                                control = False
                                print('Esperado um operador relacional')
                        else:
                            control = False
                            print('Esperado identificador')
                    else:
                        control = False
                        print('Esperada palavra reservada')
            else:
                control = False
                print('Esperado delimitador')
        else:
            control = False
            print('Esperada palavra reservada')
        return control