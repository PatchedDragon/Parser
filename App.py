from time import sleep

from colorama import Fore, Style, init
init(autoreset=True)

def banner():
    logo = f"""{Fore.RED}
    ██████   █████  ██████  ███████ ███████ ██████  
    ██   ██ ██   ██ ██   ██ ██      ██      ██   ██ 
    ██████  ███████ ██████  ███████ █████   ██████  
    ██      ██   ██ ██   ██      ██ ██      ██   ██ 
    ██      ██   ██ ██   ██ ███████ ███████ ██   ██ 
    """

    info = f"""
    {Fore.CYAN}Creator{Style.DIM}: ALI Raza
    {Fore.CYAN}Github{Style.DIM}: https://github.com/PatchedDragon/Parser
    {Fore.CYAN}Status{Style.DIM}: Under Development
    """

    print(logo + info)

#=============================================================
#                          AST Nodes
#=============================================================
#Base/Parent class for all nodes
class ASTNode:
    def __init__(self, line=None, col=None):
        self.line = line
        self.col = col

#root node representing the entire program
class Program(ASTNode):
    def __init__(self, statement):
        super().__init__()
        self.statement = statement

    def __repr__(self):
        return f"program(statement={self.statement})"

#to represent numeric literal
class Number(ASTNode):
    def __init__(self, value, line=None, col=None):
        super().__init__(line, col)
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

#representing identifier in AST
class Identifier(ASTNode):
    def __init__(self, name, line=None, col=None):
        super().__init__(line, col)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

#respresnts binary operations( +, -, /, * )
class BinaryOp(ASTNode):
    def __init__(self, operator, left, right, line=None, col=None):
        super().__init__(line=None, col=None)
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp('{self.operator}', {self.left}, {self.right})"

#representing variable declaration e.g int x = 5;
class VarDeclaration(ASTNode):
    def __init__(self,var_type , identifier, value, line=None, col=None):
        super().__init__(line, col)
        self.var_type = var_type
        self.identifier = identifier
        self.value = value
        
    def __repr__(self):
        return f"VarDeclaration(type='{self.var_type}', id='{self.identifier}', value={self.value}"
    
#represent assignment e.g x=5;
class Assignment(ASTNode):
    def __init__(self, identifier, value, line=None, col=None):
        super().__init__(line, col)
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"Assignment(identifier='{self.identifier}', value={self.value})"

#=============================================================
#                          Symbol Table
#=============================================================
class Symbol:
    def __init__(self, name, symbol_type, value=None):
        self.name = name
        self.type = symbol_type
        self.value = value

    def __repr__(self):
        return f"Symbol(name='{self.name}', type={self.type}"

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, symbol_type, value=None):
        """adding symbol in symbol table if not exist"""
        if name in self.symbols:
            return False
        self.symbols[name] = Symbol(name, symbol_type, value)
        return True

    def lookup(self, name):
        """To look-up a symbol in table"""
        return self.symbols.get(name)

    def exists(self, name):
        return name in self.symbols

    def __repr__(self):
        return f"SymbolTable({self.symbols})"

#=============================================================
#                          Token Class
#=============================================================
class Token:
    def __init__(self, token_type, lexeme, line, col):
        self.type = token_type
        self.lexeme = lexeme
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme}, {self.line}, {self.col})"

#During development tests
#myProgram = Program("hello")
#print(myProgram)

if __name__ == '__main__':
    print("█" * 60)
    banner()
    print("█" * 60)
