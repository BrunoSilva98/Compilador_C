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
                return contador + 1
            contador += 1

    def setAssemblyDeclaracao(self, contador):
        enderecoVariaveis = 0
        quantidadeVariaveis = 0
        while(self.tokens[contador][1] != ';'):
            if(self.tokens[contador][2] == "Identificador"):
                self.enderecoIdentificadores.append([self.tokens[contador][1], enderecoVariaveis])
                enderecoVariaveis += 1
                quantidadeVariaveis += 1
            contador += 1
        self.traducao.append("AMEM " + str(quantidadeVariaveis))
        return contador + 1

    def code_parser(self):
        contador = self.setAssemblyMain()
        while contador < len(self.tokens):
            if (self.tokens[contador][1] == "int"):
                self.setAssemblyDeclaracao(contador)
                break
            contador += 1

    def printAssembly(self):
        for element in self.traducao:
            print(element)

    
if __name__ == "__main__":
    assembly = Tradutor(r"C:\Users\bruno\Desktop\Projetos\Compilador\codigo.txt")
    assembly.code_parser()
    assembly.printAssembly()

        