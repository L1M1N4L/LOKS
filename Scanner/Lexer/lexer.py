# Import necessary modules and types from the .token module
from .token import TokenType, Token, tokenDict, keywordDict

# Import necessary modules and types from the ..error module, which refers to a module in the parent directory
from ..error import IllegalCharError, SyntaxErr

# Import the 'typing' module for type hints
from typing import Union, List, Tuple

# Define the Lexer class for tokenizing input strings.
class Lexer:
    # Constructor that initializes the Lexer instance with an input string.
    def __init__(self, inpstr: str) -> None:
        # Store the input string in the instance variable _inpstr.
        self._inpstr: str = inpstr

        # Initialize the indices to keep track of the current character position.
        self._curAbsIdx: int = 0  # Index from the beginning of the input string.
        self._curIdx: int = 0  # Index from the beginning of the current line.

        # Initialize the current line number.
        self._curLine: int = 1

        # Initialize the current character. If the input string is empty, set it to an empty string.
        if not len(inpstr) == 0:
            self._curChar: str = inpstr[0]
        else:
            self._curChar: str = ""

        # Initialize lists to store tokens and errors.
        self._tokList: List[Token] = []  # List of tokens.
        self._errList: List[Union[IllegalCharError, SyntaxErr]] = []  # List of errors.

        # Flag to track whether an error has occurred.
        self.hadError: bool = False

        # Flag to track whether a string is currently being processed, preventing newline characters
        # inside strings from incrementing _curLine.
        self._inString: bool = False
