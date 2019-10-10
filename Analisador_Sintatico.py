class AnalisadorSintatico:
    def __init__(self, gramatica):
        self.gramatica = gramatica





if __name__ == "__main__":
    gramatica = {
                    'E': [['T','S']],
                    'T': [['F', 'G']],
                    'S': [['+', 'T', 'S'], ['-', 'T', 'S'], ['']],
                    'G': [['*', 'F', 'G'], ['/', 'F', 'G'], ['']],
                    'F': [['id'], ['num'], ['(', 'E', ')']]
                }
    
    primeiros = {
                    
                }

    analisadorSintatico = AnalisadorSintatico(gramatica)