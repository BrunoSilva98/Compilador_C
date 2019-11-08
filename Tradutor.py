from Analisador_Lexico import AnalisadorLexico
from tabulate import tabulate

class Tradutor:
    def __init__(self, caminho):
        self.AnalisadorLexico = AnalisadorLexico(caminho)
        self.AnalisadorLexico.analiseLexica()
        self.tokens = self.AnalisadorLexico.listaTokens
        self.op_codes = dict()
        self.traducao = list()
        self.enderecoIdentificadores = list()

    def setOp_codes(self):
        self.op_codes["declaracao"] = "000"
        self.op_codes["scanf"] = "001"
        self.op_codes["printf"] = "010"
        self.op_codes["expressao"] = "011"
        self.op_codes["atribuicao"] = "100"
        self.op_codes["if"] = "101"
        self.op_codes["if/else"] = "110"
        self.op_codes["while"] = "111"
    

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

    def verificaExpressaoMatematica(self, contador):
        while (self.tokens[contador][1] != ';'):
            if self.tokens[contador][2] == "Operador":
                return True
            contador += 1
        return False

    def setAssemblyOperador(self, operador):
        if (operador == '+'):
            self.traducao.append("SOMA")
        elif (operador == '-'):
            self.traducao.append("SUBT")
        elif (operador == '*'):
            self.traducao.append("MULT")
        elif (operador == '/'):
            self.traducao.append("DIVI")        

    def setAssemblyExpressao(self, contador):
        operador = self.tokens[contador+1][1]
        qtde_operandos = 0

        while (self.tokens[contador][1] != ';'):
            
            if (self.tokens[contador][2] == "Identificador"):
                self.traducao.append("CRVL " + self.tokens[contador][1])
                qtde_operandos += 1
            
            elif (self.tokens[contador][2] == "Constante Numerica"):
                self.traducao.append("CRCT " + self.tokens[contador][1])
                qtde_operandos += 1

            elif (self.tokens[contador][2] == "Operador"):
                if (qtde_operandos == 2):
                    self.setAssemblyOperador(operador)
                    qtde_operandos = 1
                    operador = self.tokens[contador][1]
            contador += 1

        if (qtde_operandos == 2):
            self.setAssemblyOperador(operador)

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


    def code_parser(self):
        contador = self.setAssemblyMain()
        while contador < len(self.tokens):
            if (self.tokens[contador][1] == "int"):
                contador = self.setAssemblyAlocacao(contador)
                
            if (self.tokens[contador][1] == "scanf"):
                contador = self.setAssemblyScanf(contador)
            
            if (self.tokens[contador][2] == "Identificador") and (self.tokens[contador+1][1] == '='):
                contador = self.setAssemblyAtribuicao(contador)
            
            if (contador >= len(self.tokens)-1) and (self.tokens[len(self.tokens) - 1][1] == '}'):
                contador = self.setAssemblyFinalizacao()

            contador += 1

    def printAssembly(self):
        for element in self.traducao:
            print(element)

    
if __name__ == "__main__":
    assembly = Tradutor(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")
    assembly.code_parser()
    assembly.printAssembly()

        