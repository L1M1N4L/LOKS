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


    # Define the classes IllegalCharError and SyntaxErr.
    def getErrorList(self) -> List[Union[IllegalCharError, SyntaxErr]]:
            return self._errList

    # Moves forward by 'advBy' characters, checks for newlines, and  sets the current position accordingly
    def _advance(self, advBy: int = 1) -> None:
        # Increment the absolute index and the relative index by 'advBy'
        self._curAbsIdx += advBy
        self._curIdx += advBy

        # Check if the absolute index is beyond the length of the input string
        if self._curAbsIdx >= len(self._inpstr):
            self._curChar = 'eof'  # Set current character to 'eof' (end of file)
            return

        # Update the current character based on the current absolute index
        self._curChar = self._inpstr[self._curAbsIdx]

        # Check if the current character is a newline and not inside a string
        if self._curChar == '\n' and not self._inString:
            self._curIdx = 0  # Reset relative index to 0 (start of a new line)
            self._curLine += 1  # Increment the line number
    # Check the next character in the input string without advancing the current position

    def _peek(self) -> str:
        # Check if advancing one character would go beyond the input string length
        if self._curAbsIdx + 1 >= len(self._inpstr):
            return 'eof'  # Return 'eof' (end of file) if there are no more characters to peek

        # Return the character at the position one character ahead of the current absolute index
        return self._inpstr[self._curAbsIdx + 1]

    # Main lexer method that returns a list of tokens
    def getTokens(self) -> List[Token]:

        while self._curChar != 'eof':
        
            # Skip comments
            if self._curChar == '/':
                # Single-line comments
                if self._peek() == '/':
                    while not self._curChar == '\n':
                        self._advance()
                    continue
            
                # Multiline comments
                if self._peek() == '*':
                    while True:
                        self._advance()

                        if self._curChar == '*':
                            self._advance()
                            if self._curChar == "/":
                                self._advance()
                                break
            # Tokenizing logic for various token types
            # This code efficiently processes characters in the input string to recognize and tokenize different elements.

            # Skip whitespace characters
            if self._curChar.isspace():
                self._advance()

            # String literals enclosed in single or double quotes
            elif self._curChar in ["'", '"']:
                self._tokList.append(Token(TokenType.STRING, self._getString(), self._curLine, self._curIdx))

            # Two-character long tokens, such as operators or symbols
            elif self._curChar + self._peek() in tokenDict:
                val = self._curChar + self._peek()
                typ = tokenDict[val]
                self._tokList.append(Token(typ, val, self._curLine, self._curIdx))
                self._advance(2)

            # Single character tokens, like individual operators or symbols
            elif self._curChar in tokenDict:
                typ = tokenDict[self._curChar]
                self._tokList.append(Token(typ, self._curChar, self._curLine, self._curIdx))
                self._advance()

            # Numbers
            elif self._curChar.isdigit():
                self._tokList.append(Token(TokenType.NUMBER, self._getNumber(), self._curLine, self._curIdx))
                self._advance()

            # Identifiers, including keywords
            elif self._curChar.isalpha() or self._curChar == '_':
                id = self._getID()
                pos = self._curIdx - len(id)
                if id in keywordDict:
                    self._tokList.append(Token(keywordDict[id], id, self._curLine, pos))
                else:
                    self._tokList.append(Token(TokenType.ID, id, self._curLine, pos))
                
                self._advance()

            # Handling illegal characters
            # When an unexpected character is encountered, it records an error, advances the lexer, and adds an EOF token.

            # If an unexpected character is found, mark an error and record it.
            else:
                self.hadError = True
                self._errList.append(IllegalCharError(
                    f"Unexpected character '{self._curChar}'",
                    self._curLine,
                    self._curIdx
                ))
                self._advance()

            # Add an end-of-file (EOF) token to signify the end of tokenization.
            self._tokList.append(Token(TokenType.EOF, '', self._curLine, self._curIdx))
            return self._tokList
    
        # Process a number. Called when the lexer encounters a digit (0-9)
    def _getNumber(self) -> Union[int, float, None]:
        number: str = ''

        # to check for floats. If the user entered something like 1..2, dot_count will be 2 (which will cause a syntax error)
        dot_count: int = 0

        NUM = '0123456789.'  # legal number characters

        # Consume characters until a character that is not a number or dot is encountered
        while self._curChar in NUM:
            number += self._curChar
            if self._curChar == '.':
                dot_count += 1
            if self._peek() == 'eof':
                break
            if self._peek() not in NUM:
                break
            self._advance()

        if dot_count == 1:
            # Note that '1.' and '.1' are valid floating point numbers in Python, so we are okay as long as
            # dot_count is 1
            return float(number)

        elif dot_count == 0:
            return int(number)

        else:
            # If there is more than one decimal point, mark a syntax error
            self.hadError = True
            self._errList.append(SyntaxErr(
                f"Number contains more than 1 decimal point(s)",
                self._curLine,
                self._curIdx
            ))
    # Process an identifier. Called when the lexer encounters an alphabet [a-zA-Z] or underscore (_)
    def _getID(self) -> str:
        identifier: str = ''

        # Consume characters until a character that is not an alphabet or underscore is encountered
        while self._curChar.isalnum() or self._curChar == '_':
            identifier += self._curChar
            if self._peek() == 'eof':
                break
            if not self._peek().isalnum() and self._peek() != '_':
                break
            self._advance()

        return identifier
    # Process a string. Called when the lexer encounters a double or single quote.
    def _getString(self) -> str:
        # Set a flag to indicate that we are inside a string
        self._inString = True

        # Store the initial position for potential error reporting
        initialPos: Tuple[int, int] = (self._curLine, self._curIdx)
        strn: str = ''

        # Advance past the opening quote
        self._advance()

        # Accumulate characters until a matching closing quote or end of file is found
        while self._curChar not in ["'", '"'] and self._curChar != "eof" :
            strn += self._curChar
            self._advance()

        # If we reached the end of the program without finding a matching closing quote, mark an error
        if self._curChar == "eof":
            self.hadError = True
            self._errList.append(SyntaxErr(
                f"Unmatched Quote",
                initialPos[0],
                initialPos[1]
        ))

        # Advance past the closing quote and reset the string flag
        self._advance()
        self._inString = False
        return strn




                    