class Tradutor:
    def __init__(self, codigo):
        self.codigo = codigo
        self.op_codes = dict()
        self.assembly = list()

    def __setOp_codes__(self):
        self.op_codes["declaracao"] = "000"
        self.op_codes["scanf"] = "001"
        self.op_codes["printf"] = "010"
        self.op_codes["expressao"] = "011"
        self.op_codes["atribuicao"] = "100"
        self.op_codes["if"] = "101"
        self.op_codes["if/else"] = "110"
        self.op_codes["while"] = "111"

    def __setAssembly__(self):
        self.assembly.append([self.op_codes.get("declaracao")])
        self.assembly.append([self.op_codes.get("scanf")])
        self.assembly.append([self.op_codes.get("printf")])
        self.assembly.append([self.op_codes.get("expressao")])
        self.assembly.append([self.op_codes.get("atribuicao")])
        self.assembly.append([self.op_codes.get("if")])
        self.assembly.append([self.op_codes.get("if/else")])
        self.assembly.append([self.op_codes.get("while")])

    



        