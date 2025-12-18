import sys
import os

##################### TOKENIZER BOILERPLATE BEGINS ############################# 
# Token types enumeration
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}

# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False
    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False
    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False
    return True

# Original boilerplate tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0
    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')
        
        char = source_code[position]
        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue
        
        # Identifier recognition from original boilerplate
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1
            
            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition from original boilerplate
        elif char.isdigit():
            lexeme = char
            position += 1
            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")
                elif not next_char.isdigit():
                    break
                lexeme += next_char
                position += 1
            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition from original boilerplate
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL
        
        tokens.append((token_type, lexeme))
            
    return tokens
########################## TOKENIZER BOILERPLATE ENDS ###########################

# --- Syntactic Analyzer Implementation ---
class Parser:
    """
    A recursive descent parser for the specified grammar.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.operators = {'+', '-', '*', '/', '^', '<', '>', '='}
        self.statement_starters = {TokenType.IDENTIFIER, TokenType.KEYWORD, TokenType.INTEGER, TokenType.FLOAT}

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        token = self.current_token()
        if token is None:
            raise SyntaxError("Syntax Error: Unexpected end of input.")
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Syntax Error: Expected {expected_type} but found {token[0]} ('{token[1]}').")
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f"Syntax Error: Expected '{expected_value}' but found '{token[1]}'.")
        self.pos += 1
        return token

    def parse_x(self):
        """ Rule: x -> R | condy (simplified to Identifier, Integer, Float, or some Keywords) """
        token = self.current_token()
        if token and token[0] in {TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.FLOAT, TokenType.KEYWORD}:
             if token[1] in ['if', 'else']:
                 raise SyntaxError(f"Syntax Error: Unexpected keyword '{token[1]}' in a condition.")
             self.consume()
        else:
            raise SyntaxError(f"Syntax Error: Expected an identifier, number, or keyword but got {token[0] if token else 'nothing'}.")

    def parse_cond(self):
        """ Rule: cond -> x (op1 x)* """
        self.parse_x()
        token = self.current_token()
        while token and token[0] == TokenType.SYMBOL and token[1] in self.operators:
            self.consume() # consume op1
            self.parse_x()
            token = self.current_token()

    def parse_A(self):
        """ Rule: A -> (cond) [then] (statement) [else (statement) [endif]] """
        self.parse_cond()
        
        # Consume optional 'then' identifier
        token = self.current_token()
        if token and token[0] == TokenType.IDENTIFIER and token[1] == 'then':
            self.consume()

        self.parse_statement()

        token = self.current_token()
        if token and token[1] == 'else':
            if token[0] != TokenType.KEYWORD:
                 raise SyntaxError("Syntax Error: 'else' must be a keyword.")
            self.consume(expected_value='else')
            self.parse_statement()

            # Consume optional 'endif' identifier after the else block
            token = self.current_token()
            if token and token[0] == TokenType.IDENTIFIER and token[1] == 'endif':
                self.consume()

    def parse_statement(self):
        """ Rule: statement -> if (A) | y """
        token = self.current_token()
        if not token:
             raise SyntaxError("Syntax Error: Expected a statement but found end of input.")
        
        if token[1] == 'if':
            if token[0] != TokenType.KEYWORD:
                 raise SyntaxError("Syntax Error: 'if' must be a keyword.")
            self.consume(expected_value='if')
            self.parse_A()
        elif token[1] != 'else' and token[0] in self.statement_starters:
            self.consume()
        else:
            raise SyntaxError(f"Syntax Error: Invalid start of a statement with token '{token[1]}'.")

    def parse(self):
        """ Rule: S -> statement+ """
        if not self.tokens:
            return # Empty line is not an error

        while self.current_token() is not None:
            if self.current_token() and self.current_token()[1] == ';':
                self.consume()
                break
            self.parse_statement()

        if self.current_token() is not None:
            raise SyntaxError(f"Syntax Error: Unexpected token '{self.current_token()[1]}' after valid statements.")


def checkGrammar(tokens):
    """
    Wrapper function to run the parser. Raises SyntaxError on failure.
    """
    parser = Parser(tokens)
    parser.parse()


# --- Main I/O Boilerplate ---
if len(sys.argv) != 2:
    print("Usage: python q2.py '<input_path>'")
    sys.exit(1)

input_str = sys.argv[1]

try:
    with open(input_str, "r") as input_file:
        source_code = input_file.read()
except FileNotFoundError:
    print(f"Error: Input file not found at {input_str}")
    sys.exit(1)


lines = []
for line in source_code.splitlines():
    code = line.strip()
    if not code:
        lines.append("No Error\n")
        continue
    try:
        tokens = tokenize(code)
        checkGrammar(tokens)
        lines.append("No Error\n")
    except ValueError:
        lines.append("Lexical Error\n")
    except SyntaxError:
        lines.append("Syntax Error\n")


base, ext = os.path.splitext(input_str)
output_filename = f"{base}_output.txt"
try:
    with open(output_filename, "w") as output_file:
        output_file.writelines(lines)
    print(f"Output written to {output_filename}")
except Exception as e:
    print(f"Error writing to output file: {e}")

