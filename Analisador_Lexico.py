from tabulate import tabulate

arq = open(r'C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt', 'r')

texto = arq.readlines()
arq.close()

ListaCharEspecial = [",", ")", "(", ";", "=", "*", "+", "-", "{", "}", ">", "<", "[", "]", r"\ ", "/", "%", "!", "#", "|", "&", '"', ':']

ListaKeys = ["main", "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", 
             "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed",
             "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while", "include"]

ListaNumerica = ['0','1', '2','3','4','5','6','7','8','9']
ListaLetras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
listaTokens = []  
contLinhas = 0

for txtentrada in texto:
    txtentrada = txtentrada.replace("\n","")
    txtentrada = txtentrada.replace("\r", "")
    txtentrada = txtentrada.replace("\t", "")
    txtentrada = txtentrada.lower()
    contLinhas +=1
    i=0
    try:
        while i < len(txtentrada):
            token = ""

            if txtentrada[i] == '' or txtentrada[i] == ' ':
                i += 1

            else:
                if txtentrada[i] == '#':
                    token = txtentrada[i]
                    listaTokens.append([contLinhas, token, "Diretiva"])
                    break

                if (txtentrada[i] == '/') and (txtentrada[i+1] == '/'):
                    token = txtentrada[i] + txtentrada[i+1]
                    listaTokens.append([contLinhas, token, "Comentario"])
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

    except IndexError:
        if (token in ListaKeys) or (token in ListaCharEspecial):
            listaTokens.append([contLinhas, token, "Palavra Reservada"])
        else:
            listaTokens.append([contLinhas, token, "Identificador"])


print(tabulate(listaTokens))

