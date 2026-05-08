class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type_name):
        self.symbols[name] = type_name

    def exists(self, name):
        return name in self.symbols

    def get_type(self, name):
        return self.symbols.get(name)

    def clear(self):
        self.symbols.clear()
