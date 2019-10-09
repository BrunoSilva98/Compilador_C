from tabulate import tabulate

class AnalisadorLexico():
    
    def __init__(self, caminho):
        self.codigo = open(caminho, 'r')
        self.char = 0
        self.fonte = self.codigo.readlines()
        self.codigo.close()
        self.contLinhas = 0
        self.ListaCharEspecial = [",", ")", "(", ";", "=", "*", "+", "-", "{", "}", ">", 
                                "<", "[", "]", r"\ ", "/", "%", "!", "#", "|", "&", '"', ':', '.', "'"]

        self.ListaKeys = ["main", "auto", "break", "case", "char", "const", "continue", "default",
                        "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", 
                        "int", "long", "register", "return", "short", "signed", "sizeof", "static", 
                        "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", 
                        "while", "include", "null"]    

        self.ListaNumerica = ['0','1', '2','3','4','5','6','7','8','9']

        self.ListaLetras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']
        
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

    def verificaCharEspecial(self, linha):
        if(linha[self.char] in self.ListaCharEspecial):
            token = linha[self.char]
            self.char += 1

            if ((token == '>') or (token == '<')): #Verifica simbolo de > ou >=
                if (linha[self.char] == '='):
                    token = token + linha[self.char]
                    self.char+=1
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])

            elif ((token == '"')) or (token == "'"): #Verifica caso de string
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
                token = ""
                while((linha[self.char] != '"') and (linha[self.char] != "'")):
                    token = token + linha[self.char]
                    self.char += 1
                self.listaTokens.append([self.contLinhas, token, "String"])    
                token = ""
                token = token + linha[self.char]
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
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
            
            else: #Qualquer outro caractere especial
                self.listaTokens.append([self.contLinhas, token, "Simbolo Especial"])
            return True                
        return False
    
    def verificaNumeros(self, linha):
        token = ""
        if (linha[self.char] in self.ListaNumerica):
            while(linha[self.char] in self.ListaNumerica):
                token = token + linha[self.char]
                self.char += 1

            if (linha[self.char] in self.ListaLetras):
                self.listaTokens.append([self.contLinhas, token, "Token nao reconhecido"])
                self.char += 1
            else:
                self.listaTokens.append([self.contLinhas, token, "Constante Numerica"])
            return True
        return False
        
    def verificaPalavraChave(self, linha): #Verifica se é palavra chave ou identificador
        token = ""
        if (linha[self.char] in self.ListaLetras):
            
            while((self.char < len(linha)) and ((linha[self.char] in self.ListaLetras) or (linha[self.char] in self.ListaNumerica))):
                token = token + linha[self.char]
                self.char += 1
            
            if (token in self.ListaKeys):
                self.listaTokens.append([self.contLinhas, token, "Palavra Reservada"])
            else:
                self.listaTokens.append([self.contLinhas, token, "Identificador"])
            return True
        return False

    def analiseLexica(self):
        for linha in self.fonte:
            linha = self.formataLinha(linha)
            self.contLinhas +=1
            self.char = 0

            while (self.char < len(linha)):

                if ((linha[self.char] != '') and (linha[self.char] != ' ')):
                    """Sempre que entrar em algum caso pode ser dado o break para seguir para o proximo 
                        caractere e economizar processamento"""
                    
                    if (self.verificaDiretivaComentario(linha)):
                        break
                    
                    if (self.verificaCharEspecial(linha)):
                        continue

                    if (self.verificaPalavraChave(linha)):
                        continue
                    
                    if (self.verificaNumeros(linha)):
                        continue
                else:
                    self.char += 1

if __name__ == "__main__":
    analisadorLexico = AnalisadorLexico(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")
    analisadorLexico.analiseLexica()
    print(tabulate(analisadorLexico.listaTokens))


#SEPARAR ASPAS DA STRING, CADA ASPA É UM TOKEN