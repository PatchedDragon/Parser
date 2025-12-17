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


# =======================
# Parser Implementation
# =======================

class Parser:

    def __init__(self, tokens):
        # Convert raw tokens to Token objects for easier handling
        self.tokens = [Token(*t) if len(t) == 4 else Token(t[0], t[1], t[2], 0)
                       for t in tokens]
        self.pos = 0  # Current position in token stream
        self.current_token = self.tokens[0] if self.tokens else None
        self.symbol_table = SymbolTable()
        self.errors = []  # Store syntax errors

    # =======================
    # Token Management
    # =======================

    def advance(self):
        """Move to the next token in the stream"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def peek(self, offset=1):
        """Look ahead at future tokens without consuming them"""
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    def check(self, token_type, lexeme=None):
        if not self.current_token:
            return False
        if self.current_token.type != token_type:
            return False
        if lexeme and self.current_token.lexeme != lexeme:
            return False
        return True

    def match(self, token_type, lexeme=None):
        if self.check(token_type, lexeme):
            token = self.current_token
            self.advance()
            return token
        return None

    def expect(self, token_type, lexeme=None):
        token = self.match(token_type, lexeme)
        if token:
            return token

        # Error detected - report it
        expected = f"{token_type}"
        if lexeme:
            expected += f":'{lexeme}'"
        actual = f"{self.current_token.type}:'{self.current_token.lexeme}'" if self.current_token else "EOF"
        self.report_error(f"Expected {expected}, got {actual}")
        return None

    # =======================
    # Error Handling
    # =======================

    def report_error(self, message):
        """Record a syntax error with position information"""
        if self.current_token:
            line = self.current_token.line
            col = self.current_token.col
            error_msg = f"Syntax Error at {line}:{col} - {message}"
        else:
            error_msg = f"Syntax Error at EOF - {message}"

        self.errors.append(error_msg)
        print(f"❌ {error_msg}")

    def synchronize(self):
        sync_tokens = {'SEMICOLON', 'EOF'}
        sync_keywords = {'int', 'float', 'char', 'if', 'while', 'for', 'return'}

        while self.current_token:
            # Stop at semicolon or EOF
            if self.current_token.type in sync_tokens:
                if self.current_token.type == 'SEMICOLON':
                    self.advance()  # Consume the semicolon
                return

            # Stop at statement-starting keywords
            if (self.current_token.type == 'KEYWORD' and
                    self.current_token.lexeme in sync_keywords):
                return

            self.advance()

    # =======================
    # Grammar Rules (Recursive Descent)
    # =======================

    def parse(self):
        print("🔍 Starting parsing process...")
        print(f"📝 Total tokens received from lexer: {len(self.tokens)}")
        print()

        try:
            ast = self.program()

            if self.errors:
                print(f"\n⚠️  Parsing completed with {len(self.errors)} error(s)")
            else:
                print(f"\n✅ Parsing completed successfully!")

            return ast
        except Exception as e:
            self.report_error(f"Fatal parsing error: {str(e)}")
            return None

    def program(self):
        statements = []

        # Parse statements until EOF
        while self.current_token and self.current_token.type != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)

            # If error occurred, try to recover
            if self.errors and self.current_token and self.current_token.type != 'EOF':
                self.synchronize()

        return Program(statements)

    def statement(self):
        # Check for variable declaration (keyword at start)
        if self.check('KEYWORD'):
            keyword = self.current_token.lexeme
            # Check if it's a type keyword
            if keyword in ['int', 'float', 'double', 'char', 'bool', 'string']:
                return self.declaration()

        # Check for assignment (identifier followed by =)
        if self.check('IDENTIFIER'):
            next_token = self.peek()
            if next_token and next_token.type == 'OPERATOR' and next_token.lexeme == '=':
                return self.assignment()

        # Otherwise, it's an expression statement
        return self.expression_statement()

    def declaration(self):
        # Get type keyword
        type_token = self.expect('KEYWORD')
        if not type_token:
            return None

        var_type = type_token.lexeme
        line, col = type_token.line, type_token.col

        # Get identifier
        id_token = self.expect('IDENTIFIER')
        if not id_token:
            return None

        identifier = id_token.lexeme

        # Check if there's an initialization
        value = None
        if self.match('OPERATOR', '='):
            value = self.expression()

        # Expect semicolon
        self.expect('SEMICOLON')

        # Add to symbol table
        if not self.symbol_table.declare(identifier, var_type, value):
            self.report_error(f"Variable '{identifier}' already declared")

        return VarDeclaration(var_type, identifier, value, line, col)

    def assignment(self):
        # Get identifier
        id_token = self.expect('IDENTIFIER')
        if not id_token:
            return None

        identifier = id_token.lexeme
        line, col = id_token.line, id_token.col

        # Check if variable is declared
        if not self.symbol_table.exists(identifier):
            self.report_error(f"Variable '{identifier}' used before declaration")

        # Expect assignment operator
        if not self.expect('OPERATOR', '='):
            return None

        # Parse the right-hand side expression
        value = self.expression()

        # Expect semicolon
        self.expect('SEMICOLON')

        return Assignment(identifier, value, line, col)

    def expression_statement(self):
        expr = self.expression()
        self.expect('SEMICOLON')
        return expr

    def expression(self):
        left = self.term()

        # Handle left-associative operators
        while self.check('OPERATOR') and self.current_token.lexeme in ['+', '-']:
            op_token = self.current_token
            operator = op_token.lexeme
            line, col = op_token.line, op_token.col
            self.advance()

            right = self.term()
            left = BinaryOp(operator, left, right, line, col)

        return left

    def term(self):
        left = self.factor()

        # Handle left-associative operators
        while self.check('OPERATOR') and self.current_token.lexeme in ['*', '/', '%']:
            op_token = self.current_token
            operator = op_token.lexeme
            line, col = op_token.line, op_token.col
            self.advance()

            right = self.factor()
            left = BinaryOp(operator, left, right, line, col)

        return left

    def factor(self):
        # Number literal
        if self.check('NUMBER'):
            token = self.current_token
            self.advance()
            return Number(token.lexeme, token.line, token.col)

        # Identifier (variable reference)
        elif self.check('IDENTIFIER'):
            token = self.current_token
            identifier = token.lexeme

            # Check if variable is declared
            if not self.symbol_table.exists(identifier):
                self.report_error(f"Undefined variable '{identifier}'")

            self.advance()
            return Identifier(identifier, token.line, token.col)

        # Parenthesized expression
        elif self.check('OPERATOR', '('):
            self.advance()  # consume '('
            expr = self.expression()
            self.expect('OPERATOR', ')')  # expect ')'
            return expr

        else:
            self.report_error(f"Unexpected token: {self.current_token.type}:'{self.current_token.lexeme}'")
            self.advance()  # Skip the problematic token (phrase-level recovery)
            return None


# =======================
# Test Cases
# =======================

def run_test_case_1():
    """Test Case 1: Variable Declaration with Initialization"""
    print("=" * 70)
    print("TEST CASE 1: Variable Declaration with Initialization")
    print("Input: int x = 5;")
    print("=" * 70)

    # Token stream from lexer: int x = 5;
    tokens = [
        ('KEYWORD', 'int', 1, 0),
        ('IDENTIFIER', 'x', 1, 4),
        ('OPERATOR', '=', 1, 6),
        ('NUMBER', '5', 1, 8),
        ('SEMICOLON', ';', 1, 9),
        ('EOF', '', 1, 10)
    ]

    print("\n Tokens received from lexer:")
    for token in tokens[:-1]:  # Skip EOF for display
        print(f"   {token}")
    print()

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n Generated AST:")
    print(f"   {ast}")

    print("\n Symbol Table:")
    print(f"   {parser.symbol_table}")

    print("\n" + "=" * 70 + "\n")
    return ast


def run_test_case_2():
    """Test Case 2: Complex Expression with Operator Precedence"""
    print("=" * 70)
    print("TEST CASE 2: Complex Expression with Operator Precedence")
    print("Input: int result = 10 + 20 * 2;")
    print("=" * 70)

    # Token stream from lexer: int result = 10 + 20 * 2;
    tokens = [
        ('KEYWORD', 'int', 1, 0),
        ('IDENTIFIER', 'result', 1, 4),
        ('OPERATOR', '=', 1, 11),
        ('NUMBER', '10', 1, 13),
        ('OPERATOR', '+', 1, 16),
        ('NUMBER', '20', 1, 18),
        ('OPERATOR', '*', 1, 21),
        ('NUMBER', '2', 1, 23),
        ('SEMICOLON', ';', 1, 24),
        ('EOF', '', 2, 0)
    ]

    print("\n Tokens received from lexer:")
    for token in tokens[:-1]:  # Skip EOF for display
        print(f"   {token}")
    print()

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n Generated AST:")
    print(f"   {ast}")

    print("\n Symbol Table:")
    print(f"   {parser.symbol_table}")

    print("\n Note: Multiplication has higher precedence, so:")
    print("   Expression parsed as: 10 + (20 * 2), not (10 + 20) * 2")

    print("\n" + "=" * 70 + "\n")
    return ast


def run_test_case_3():
    """Test Case 3: Multiple Statements"""
    print("=" * 70)
    print("TEST CASE 3: Multiple Statements")
    print("Input:")
    print("   int x = 5;")
    print("   int y = 10;")
    print("   int sum = x + y;")
    print("=" * 70)

    # Token stream from lexer
    tokens = [
        ('KEYWORD', 'int', 1, 0),
        ('IDENTIFIER', 'x', 1, 4),
        ('OPERATOR', '=', 1, 6),
        ('NUMBER', '5', 1, 8),
        ('SEMICOLON', ';', 1, 9),
        ('KEYWORD', 'int', 2, 0),
        ('IDENTIFIER', 'y', 2, 4),
        ('OPERATOR', '=', 2, 6),
        ('NUMBER', '10', 2, 8),
        ('SEMICOLON', ';', 2, 10),
        ('KEYWORD', 'int', 3, 0),
        ('IDENTIFIER', 'sum', 3, 4),
        ('OPERATOR', '=', 3, 8),
        ('IDENTIFIER', 'x', 3, 10),
        ('OPERATOR', '+', 3, 12),
        ('IDENTIFIER', 'y', 3, 14),
        ('SEMICOLON', ';', 3, 15),
        ('EOF', '', 4, 0)
    ]

    print("\n Tokens received from lexer:")
    for token in tokens[:-1]:  # Skip EOF for display
        print(f"   {token}")
    print()

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n Generated AST:")
    print(f"   {ast}")

    print("\n Symbol Table:")
    for name, symbol in parser.symbol_table.symbols.items():
        print(f"   {symbol}")

    print("\n" + "=" * 70 + "\n")
    return ast


def run_error_test():
    """Test Case 4: Error Detection and Recovery"""
    print("=" * 70)
    print("TEST CASE 4: Error Detection and Recovery")
    print("Input (with errors):")
    print("   int x = 5;")
    print("   y = 10;          // Error: y not declared")
    print("   int z = x + ;    // Error: incomplete expression")
    print("=" * 70)

    # Token stream with errors
    tokens = [
        ('KEYWORD', 'int', 1, 0),
        ('IDENTIFIER', 'x', 1, 4),
        ('OPERATOR', '=', 1, 6),
        ('NUMBER', '5', 1, 8),
        ('SEMICOLON', ';', 1, 9),
        # Error: undeclared variable
        ('IDENTIFIER', 'y', 2, 0),
        ('OPERATOR', '=', 2, 2),
        ('NUMBER', '10', 2, 4),
        ('SEMICOLON', ';', 2, 6),
        # Error: incomplete expression
        ('KEYWORD', 'int', 3, 0),
        ('IDENTIFIER', 'z', 3, 4),
        ('OPERATOR', '=', 3, 6),
        ('IDENTIFIER', 'x', 3, 8),
        ('OPERATOR', '+', 3, 10),
        ('SEMICOLON', ';', 3, 12),  # Missing operand
        ('EOF', '', 4, 0)
    ]

    print("\n Tokens received from lexer:")
    for token in tokens[:-1]:
        print(f"   {token}")
    print()

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n Generated AST (with partial recovery):")
    print(f"   {ast}")

    print("\n Symbol Table:")
    for name, symbol in parser.symbol_table.symbols.items():
        print(f"   {symbol}")

    print("\n Note: Parser detected errors but continued parsing")

    print("\n" + "=" * 70 + "\n")


# =======================
# Main Execution
# =======================

if __name__ == "__main__":
    banner()

    # Run all test cases
    run_test_case_1()
    run_test_case_2()
    run_test_case_3()
    run_error_test()
