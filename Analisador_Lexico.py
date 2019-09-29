from tabulate import tabulate

class AnalisadorLexico():
    
    def __init__(self, caminho):
        self.codigo = open(caminho, 'r')
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

    def verificaDiretivaComentario(self, linha, char):
        if (linha[char] == '#'):
            token = linha[char]
            self.listaTokens.append([self.contLinhas, token, "Diretiva"])
            return True

        elif ((linha[char] == '/') and (linha[char+1] == '/')):
            token = linha[char] + linha[char+1]
            self.listaTokens.append([self.contLinhas, token, "Comentario"])
            return True
        return False

    def verificaCasoEspecial(self, linha, char):
        
            

    def analiseLexica(self):
        for linha in self.fonte:
            linha = self.formataLinha(linha)
            self.contLinhas +=1
            char = 0
            try:
                while char < len(linha):
                    token = ""

                    if ((linha[char] != '') or (linha[char] != ' ')):

                        if (self.verificaDiretivaComentario):
                            break

                        if txtentrada[i] in ListaCharEspecial:
                            token = txtentrada[i]
                            i += 1
                            
                            if token == '>' or token == '<':
                                if (txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                            
                            elif token == '"':
                                while(txtentrada[i] != '"'):
                                    token = token + txtentrada[i]
                                    i+=1   
                                token = token + txtentrada[i]
                                listaTokens.append([contLinhas, token, "String"])
                                i+=1

                            elif token == '|':
                                if (txtentrada[i] == '|'):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '&':
                                if (txtentrada[i] == '&'):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '=':
                                if (txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '!':
                                if (txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '+':
                                if (txtentrada[i] == '+' or txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '-':
                                if (txtentrada[i] == '-' or txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '/':
                                if (txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            elif token == '*':
                                if (txtentrada[i] == '='):
                                    token = token + txtentrada[i]
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])
                                    i+=1
                                else:
                                    listaTokens.append([contLinhas, token, "Simbolo Especial"])

                            else:
                                listaTokens.append([contLinhas, token, "Simbolo Especial"])

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

