from Analisador_Lexico import AnalisadorLexico
class Tradutor:
    def __init__(self, caminho):
        self.AnalisadorLexico = AnalisadorLexico(caminho)
        self.AnalisadorLexico.analiseLexica()
        self.tokens = self.AnalisadorLexico.listaTokens
        self.traducao = list()
        self.enderecoIdentificadores = list()
        self.operadores_logicos = ['>', '>=', '<', '<=', '&&', '||', '==', '!=']
        self.label_count = 1

    def setAssemblyMain(self):
        contador = 0
        while contador < len(self.tokens):
            if (self.tokens[contador][1] == "main"):
                self.traducao.append("INPP")
                return contador
            contador += 1

    def setAssemblyAlocacao(self, contador):
        quantidadeVariaveis = 0
        while(self.tokens[contador][1] != ';'):
            if(self.tokens[contador][2] == "Identificador"):
                self.enderecoIdentificadores.append(self.tokens[contador][1])
                quantidadeVariaveis += 1
            contador += 1
        self.traducao.append("AMEM " + str(quantidadeVariaveis))
        return contador

    def setAssemblyLiberacao(self):
        self.traducao.append("DMEM " + str(len(self.enderecoIdentificadores)))
    
    def setAssemblyFinalizacao(self):
        self.setAssemblyLiberacao()
        self.traducao.append("PARA")
        return len(self.tokens)

    def setAssemblyScanf(self, contador):
        self.traducao.append("LEIT")
        while (self.tokens[contador][1] != ';'):
            if self.tokens[contador][2] == "Identificador":
                try:
                    endereco = self.enderecoIdentificadores.index(self.tokens[contador][1])
                except ValueError:
                    raise Exception("Identificador {0} inexistente".format(self.tokens[contador][1]))
            contador += 1
        self.traducao.append("ARMZ " + str(endereco))
        return contador

    def verificaExpressaoMatematica(self, contador, condicao_parada=';'):
        while ((self.tokens[contador][1] != condicao_parada) and\
               (contador < len(self.tokens)-1) and\
               (self.tokens[contador][1] not in self.operadores_logicos)):

            if self.tokens[contador][2] == "Operador":
                return True

            contador += 1

        return False

    def setAssemblyOperadorMatematico(self, operador):
        if (operador == '+'):
            self.traducao.append("SOMA")
        elif (operador == '-'):
            self.traducao.append("SUBT")
        elif (operador == '*'):
            self.traducao.append("MULT")
        elif (operador == '/'):
            self.traducao.append("DIVI") 

    def setAssemblyOperadorLogico(self, operador):
        if (operador == '&&'):
            self.traducao.append("CONJ")
        elif (operador == '||'):
            self.traducao.append("DISJ")
        elif (operador == '<'):
            self.traducao.append("CMME")
        elif (operador == '>'):
            self.traducao.append("CMMA")
        elif (operador == '=='):
            self.traducao.append("CMIG")
        elif (operador == '!='):
            self.traducao.append("CMDG")
        elif (operador == '<='):
            self.traducao.append("CMEG")
        elif (operador == '>='):
            self.traducao.append("CMAG")
        elif (operador == '!'):
            self.traducao.append("NEGA")


    def setAssemblyExpressao(self, contador, condicao_parada=None):
        operador = self.tokens[contador+1][1]
        qtde_operandos = 0

        while ((self.tokens[contador][1] != condicao_parada) and\
               (self.tokens[contador][1] != ';') and\
               (self.tokens[contador][1] not in self.operadores_logicos)):

            if (self.tokens[contador][2] == "Identificador"):
                self.traducao.append("CRVL " + self.tokens[contador][1])
                qtde_operandos += 1
            
            elif (self.tokens[contador][2] == "Constante Numerica"):
                self.traducao.append("CRCT " + self.tokens[contador][1])
                qtde_operandos += 1

            elif (self.tokens[contador][2] == "Operador"):
                if (qtde_operandos == 2):
                    self.setAssemblyOperadorMatematico(operador)
                    qtde_operandos = 1
                    operador = self.tokens[contador][1]
            contador += 1

        if (qtde_operandos == 2):
            self.setAssemblyOperadorMatematico(operador)

        return contador

    def setAssemblyComparacao(self, contador, condicao_parada=None):
        qtde_operandos = 0
        contador2 = contador
        linha_comparacao = self.tokens[contador][0]

        while (self.tokens[contador2][1] not in self.operadores_logicos):
            contador2 += 1
        operador = self.tokens[contador2][1]

        while ((self.tokens[contador][2] != "Identificador") and\
               (self.tokens[contador][2] != "Constante Numerica")):
            contador += 1

        while (self.tokens[contador][0] == linha_comparacao):

            if (self.verificaExpressaoMatematica(contador,'{')):
                contador = self.setAssemblyExpressao(contador,'{')
                qtde_operandos += 1

            elif (self.tokens[contador][2] == "Identificador"):
                self.traducao.append("CRVL " + self.tokens[contador][1])
                qtde_operandos += 1
            
            elif (self.tokens[contador][2] == "Constante Numerica"):
                self.traducao.append("CRCT " + self.tokens[contador][1])
                qtde_operandos += 1
            
            if (self.tokens[contador][1] in self.operadores_logicos):
                if (qtde_operandos == 2):
                    self.setAssemblyOperadorLogico(operador)
                    operador = self.tokens[contador][1]
                    qtde_operandos = 1

            contador += 1

        if (qtde_operandos == 2):
            self.setAssemblyOperadorLogico(operador)

        return contador

    def setAssemblyAtribuicao(self, contador):
        variavel_atribuindo = self.tokens[contador][1]
        contador += 2
        if (not self.verificaExpressaoMatematica(contador)):
            while (self.tokens[contador][1] != ';'):
                
                if (self.tokens[contador][2] == "Identificador") and (self.tokens[contador+1][1] == ';'):
                    self.traducao.append("CRVL " + self.tokens[contador][1])

                elif (self.tokens[contador][2] == "Constante Numerica") and (self.tokens[contador+1][1] == ';'):
                    self.traducao.append("CRCT " + self.tokens[contador][1])
                contador += 1

            self.traducao.append("ARMZ " + variavel_atribuindo)
            return contador

        else:
            contador = self.setAssemblyExpressao(contador)
            self.traducao.append("ARMZ " + variavel_atribuindo)
            return contador

    def getQtdeParametros(self, string):
        contador = 0
        qtde_parametros = 0
        while contador < len(string):
            if string[contador] == '%' and string[contador+1] == 'd':
                qtde_parametros += 1
            contador += 1
        return qtde_parametros

    def setAssemblyPrintf(self, contador):
            while self.tokens[contador][2] != "String":
                contador += 1
            qtde_parametros = self.getQtdeParametros(self.tokens[contador][1])
            
            if qtde_parametros > 0:
                while self.tokens[contador][1] != ';':
                    if (self.tokens[contador][2] == "Identificador") or (self.tokens[contador][2] == "Constante Numerica"):
                        if self.verificaExpressaoMatematica(contador, ','):
                            contador = self.setAssemblyExpressao(contador,',') - 1
                            
                        else:
                            if self.tokens[contador][2] == "Constante Numerica":
                                self.traducao.append("CRCT " + self.tokens[contador][1])
                            else:
                                self.traducao.append("CRVL " + self.tokens[contador][1])
                        
                        self.traducao.append("IMPR")

                    contador += 1
                return contador
            else:
                self.traducao.append("IMPR")
                return contador + 1
    
    def verificaFimBloco(self, contador):
        linha_fim = 0
        pilha_abertura = list()

        pilha_abertura.append(self.tokens[contador][1])
        contador += 1

        while (contador < len(self.tokens)-1):
            if (self.tokens[contador][1] == '{'):
                pilha_abertura.insert(0, self.tokens[contador][1])
            
            elif (self.tokens[contador][1] == '}'):
                pilha_abertura.pop(0)
                linha_fim = self.tokens[contador][0]
            
            if (len(pilha_abertura) == 0):
                return linha_fim

            contador += 1

    def setAssemblyWhile(self, contador):
        self.traducao.append("L" + str(self.label_count) + " INICIO_WHILE")
        label = self.label_count
        self.label_count += 1
        contador = self.setAssemblyComparacao(contador)
        index = len(self.traducao)
        fim_while = self.verificaFimBloco(contador)
        contador = self.code_parser(contador, 0, fim_while)
        self.traducao.append("DSVS L" + str(label))
        self.traducao.append("L" + str(self.label_count) + " FIM_WHILE")
        self.traducao.insert(index, "DSVF L" + str(self.label_count))
        self.label_count += 1
        return contador

    def verificaElse(self, contador):
        pilha = list()
        pilha.append("if")
        contador += 1

        while(contador < len(self.tokens)-1):
            if (self.tokens[contador][1] == "if"):
                pilha.insert(0, self.tokens[contador][1])
            
            elif (self.tokens[contador][1] == "else"):
                pilha.pop(0)
            
            if (len(pilha) == 0):
                return True
                
            contador += 1
        return False     

    def setAssemblyIf(self, contador):
        label = self.label_count
        self.label_count += 1
        contador = self.setAssemblyComparacao(contador)
        index = len(self.traducao)
        fim_if = self.verificaFimBloco(contador)
        tem_else = self.verificaElse(contador)

        contador = self.code_parser(contador, 0, fim_if)

        if (not tem_else):
            self.traducao.append("L" + str(label) + " FALSO")
            self.traducao.insert(index, "DSVF L" + str(label))

        else:
            self.traducao.insert(index, "DSVF L" + str(label))
            self.traducao.append("DSVS L" + str(self.label_count))
            self.traducao.append("L" + str(label) + " FALSO")
            label = self.label_count
            self.label_count += 1
            contador += 2
            fim_else = self.verificaFimBloco(contador)
            contador = self.code_parser(contador, 0, fim_else)            
            self.traducao.append("L" + str(label) + " FIM IF/ELSE")

        return contador

    def code_parser(self, contador, index_cond_parada=1, condicao_parada=None):
        while ((contador < len(self.tokens)) and\
               (self.tokens[contador][index_cond_parada] != condicao_parada)):

            if (self.tokens[contador][1] == "int"):
                contador = self.setAssemblyAlocacao(contador)
                
            if (self.tokens[contador][1] == "scanf"):
                contador = self.setAssemblyScanf(contador)
            
            if (self.tokens[contador][2] == "Identificador") and (self.tokens[contador+1][1] == '='):
                contador = self.setAssemblyAtribuicao(contador)
            
            if (self.tokens[contador][1] == "printf"):
                contador = self.setAssemblyPrintf(contador)
            
            if (self.tokens[contador][1] == "while"):
                contador = self.setAssemblyWhile(contador)

            if (self.tokens[contador][1] == "if"):
                contador = self.setAssemblyIf(contador)
            
            if (contador >= len(self.tokens)-1) and (self.tokens[len(self.tokens) - 1][1] == '}'):
                contador = self.setAssemblyFinalizacao()

            contador += 1
        return contador

    def printAssembly(self):
        for element in self.traducao:
            print(element)

    
if __name__ == "__main__":
    assembly = Tradutor(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")
    contador = assembly.setAssemblyMain()
    assembly.code_parser(contador)
    assembly.printAssembly()