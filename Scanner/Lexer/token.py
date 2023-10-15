# Import required modules for the code
from enum import Enum          # Allows creating custom enumerations (TokenType is an example)
from typing import Any, List  # Provides type hinting for variables, function parameters, and return values

'''
 Define the TokenType enumeration
 This enumeration represents different types of tokens used in parsing or lexing code.
 It includes identifiers, numbers, strings, punctuation symbols, operators, and keywords.
 To add a new keyword, simply add an entry at the end of the enumeration.
'''
class TokenType(Enum):
    # Token types for identifiers, numbers, and strings
    ID = "identifier"
    NUMBER = "number"
    STRING = "string"
    EOF = None  # Represents the end of the token stream

    # Punctuation tokens
    L_PAREN = '('
    R_PAREN = ')'
    L_SQUARE = '['
    R_SQUARE = ']'
    L_CURLY = '{'
    R_CURLY = '}'
    SEMI = ';'
    COMMA = ','
    QUOTE = '"'
    S_QUOTE = "'"

    # Operator tokens
    LESS_THAN = '<'
    GREATER_THAN = '>'
    LESS_THAN_EQ = '<='
    GREATER_THAN_EQ = '>='
    EQUAL = '=='
    NOT_EQUAL = '!='
    NOT = '!'

    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    ASSIGN = '='

    # Keywords
    VAR = "var"
    FUNCTION = "fun"
    IF = "if"
    ELSE = "else"
    ELSEIF = "elsif"
    WHILE = "while"
    FOR = "for"
    RETURN = "return"
    CONTINUE = "continue"
    BREAK = "break"
    AND = "and"
    OR = "or"
    TRUE = "true"
    FALSE = "false"
    NIL = "nil"

# Convert the TokenType enum into a dictionary (excluding keywords)
def makeTokenDict() -> dict:
    d = dict()
    
    # Get a list of all enum members from the TokenType enumeration
    kList: List[TokenType] = list(TokenType)
    
    # Find the index of the last non-keyword token
    endIdx: int = kList.index(TokenType.VAR)
    
    # Create a dictionary where the key is the token value, and the value is the corresponding TokenType
    for i in range(0, endIdx):
        d[kList[i].value] = kList[i]
    
    return d

# Create a keyword dictionary from the TokenType enum
def makeKeywordDict() -> dict:
    d = dict()
    
    # Get a list of all enum members from the TokenType enumeration
    kList: List[TokenType] = list(TokenType)
    
    # Find the index of the first keyword token
    startIdx: int = kList.index(TokenType.VAR)
    
    # Determine the total number of TokenType enum members
    l: int = len(kList)
    
    # Create a dictionary where the key is the keyword value, and the value is the corresponding TokenType
    for i in range(startIdx, l):
        d[kList[i].value] = kList[i]
    
    return d

# Define the Token class to represent tokens in the lexer
class Token:
    def __init__(self, t: TokenType, v: Any, l: int, pos: int) -> None:
        # Initialize a Token instance with type, value, line, and position attributes
        self.type: TokenType = t
        self.value: Any = v
        self.line: int = l
        self.position: int = pos

    def __str__(self) -> str:
        # Define a string representation for Token objects
        return f"({self.line}:{self.position}){self.type}: {self.value}"

    def __repr__(self) -> str:
        # Provide a human-readable representation for Token objects
        return self.__str__()

    def __eq__(self, o) -> bool:
        # Implement equality comparison for Token objects
        return (
            self.type.value == o.type.value and
            self.value == o.value and
            self.line == o.line and
            self.position == o.position
        )

# Create dictionaries for token types and keywords using helper functions
tokenDict: dict = makeTokenDict()  # A dictionary for mapping token values to TokenType enums (excluding keywords)
keywordDict: dict = makeKeywordDict()  # A dictionary for mapping keyword values to TokenType enums

