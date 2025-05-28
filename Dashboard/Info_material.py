class Estocado:
    def __init__(self, nomenclatura):
        self.nomenclatura = nomenclatura
        self.localizacao = "Prateleira 1"

    def detalhes(self):
        print(f"PN: {self.nomenclatura}.")
        print(f"Localizacao: {self.localizacao}.")
    
    def localizar(self):
        print(f"Localizacao: {self.localizacao}.")