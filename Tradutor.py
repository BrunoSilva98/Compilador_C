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

    def setAssemblyExpressao(self, contador, variavel_atribuindo=None):
        pass

    def setAssemblyAtribuicao(self, contador):
        contadorExpressao = contador
        variavel_atribuindo = self.tokens[contador][1]
        contador += 2

        while (self.tokens[contador][1] != ';'):
            
            if (self.tokens[contador][2] == "Identificador") and (self.tokens[contador+1][1] == ';'):
                self.traducao.append("CRVL " + self.tokens[contador][1])
                self.traducao.append("ARMZ " + variavel_atribuindo)

            elif (self.tokens[contador][2] == "Constante Numerica") and (self.tokens[contador+1][1] == ';'):
                self.traducao.append("CRCT " + self.tokens[contador][1])
                self.traducao.append("ARMZ " + variavel_atribuindo)

            elif (self.tokens[contador][2] == "Operador"):
                self.setAssemblyExpressao(contadorExpressao, variavel_atribuindo)
            contador += 1
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
            
            if (contador >= len(self.tokens)) and (self.tokens[len(self.tokens) - 1][1] == '}'):
                contador = self.setAssemblyFinalizacao()

            contador += 1

    def printAssembly(self):
        for element in self.traducao:
            print(element)

    
if __name__ == "__main__":
    assembly = Tradutor(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")
    assembly.code_parser()
    assembly.printAssembly()

        