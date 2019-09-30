from tabulate import tabulate

class AnalisadorLexico():
    
    def __init__(self, caminho):
        self.codigo = open(caminho, 'r')
        self.char = 0
        self.fonte = self.codigo.readlines()
        self.codigo.close()
        self.contLinhas = 0
        self.ListaCharEspecial = [",", ")", "(", ";", "=", "*", "+", "-", "{", "}", ">", 
                                "<", "[", "]", r"\ ", "/", "%", "!", "#", "|", "&", '"', ':']

        self.ListaKeys = ["main", "auto", "break", "case", "char", "const", "continue", "default",
                        "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", 
                        "int", "long", "register", "return", "short", "signed", "sizeof", "static", 
                        "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", 
                        "while", "include"]    

        self.ListaNumerica = ['0','1', '2','3','4','5','6','7','8','9']

        self.ListaLetras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        self.listaTokens = list()

    def formataLinha(self, linha):
        texto = linha.replace("\n","")
        texto = texto.replace("\r", "")
        texto = texto.replace("\t", "")
        texto = texto.lower()
        return texto

    def verificaDiretivaComentario(self, linha):
        if (linha[self.char] == '#'): #Verifica diretiva de pré-processamento
            token = linha[self.char]
            self.listaTokens.append([self.contLinhas, token, "Diretiva"])
            return True

        elif ((linha[self.char] == '/') and (linha[self.char+1] == '/')): #Verifica comentário na linha
            token = linha[self.char] + linha[self.char+1]
            self.listaTokens.append([self.contLinhas, token, "Comentario"])
            return True
        return False

    def verificaCasoEspecial(self, linha):
        if(linha[self.char] in self.ListaCharEspecial):
            token = linha[self.char]
            self.char += 1

            if ((token == '>') or (token == '<')): #Verifica simbolo de > ou >=
                if (linha[char] == '='):
                    token = token + linha[char]
                    self.char+=1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '"'): #Verifica caso de string, está salvando a string assim como aspa, pode ser separado depois
                while(linha[self.char] != '"'):
                    token = token + linha[self.char]
                    self.char += 1
                token = token + linha[self.char]
                self.listaTokens.append([self.contLinhas, token, "String"])
                self.char += 1

            elif (token == '|'): #Verifica o OR, que são dois símbolos ||
                if (linha[self.char] == '|'):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '&'): #Verifica o AND, que são dois símbolos &&
                if (linha[self.char] == '&'):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '='): #Verifica comparacao ou atribuicao
                if (linha[self.char] == '='):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '!'): #Verica NOT ou Diferente
                if (linha[self.char] == '='):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '+'): #Verifica ++ e +=
                if ((linha[self.char] == '+') or (linha[self.char] == '=')):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
            
            elif (token == '-'): #Verifica -- e -=
                if ((linha[self.char] == '-') or (linha[self.char] == '=')):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])            

            elif (token == '/'): #Verifica /= ou /
                if (linha[self.char] == '='):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif (token == '*'): #Verifica *= ou *
                if (linha[self.char] == '='):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
            
            else:
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
            return True
                
        return False
            

    def analiseLexica(self):
        for linha in self.fonte:
            linha = self.formataLinha(linha)
            self.contLinhas +=1
            self.char = 0
            try:
                while self.char < len(linha):
                    token = ""

                    if ((linha[self.char] != '') or (linha[self.char] != ' ')):
                        """Sempre que entrar em algum caso pode ser dado o break para seguir para o proximo 
                            caractere e economizar processamento"""
                        
                        if (self.verificaDiretivaComentario(linha)):
                            break
                        
                        if (self.verificaCasoEspecial):
                            break

                        elif txtentrada[i] in ListaLetras:
                            while((txtentrada[i] in ListaLetras) or (txtentrada[i] in ListaNumerica)):
                                token = token + txtentrada[i]
                                i += 1

                            if (token in ListaKeys):
                                listaTokens.append([contLinhas, token, "Palavra Reservada"])
                            else:
                                listaTokens.append([contLinhas, token, "Identificador"])

                        elif (txtentrada[i] in ListaNumerica):
                            while(txtentrada[i] in ListaNumerica):
                                token = token + txtentrada[i]
                                i += 1

                            if txtentrada[i] in ListaLetras:
                                listaTokens.append([contLinhas, token, "Token nao reconhecido"])
                                i += 1
                            else:
                                listaTokens.append([contLinhas, token, "Constante Numerica"])
                    else:
                        char += 1

            except IndexError:
                if (token in ListaKeys) or (token in ListaCharEspecial):
                    listaTokens.append([contLinhas, token, "Palavra Reservada"])
                else:
                    listaTokens.append([contLinhas, token, "Identificador"])


print(tabulate(listaTokens))

