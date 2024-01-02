# Importing necessary modules and types

# Import the 'Token' class from the 'token' module within the 'lexer' package
from ..lexerOrScanner.token import Token

# Import the 'TokenType' enumeration from the 'token' module
from ..lexerOrScanner.token import TokenType

# Import the 'SyntaxErr' class from the 'error' module
from ..error import SyntaxErr

# Import all classes and types from the 'ast' module in the current package
from .abstractSyntaxTree import *

# Import the 'List' type hint from the 'typing' module
from typing import List

#
# Parser class for generating an Abstract Syntax Tree (AST) from a list of tokens.
#
class Parser:
    def __init__(self, tokList: List[Token]) -> None:
        """
        Initializes a new Parser instance with a list of tokens.

        :param tokList: List of tokens to parse.
        """
        # Store the list of tokens in the instance variable.
        self._tokList: List[Token] = tokList

        # Initialize the index of the current token being processed.
        self._idx: int = 0

        # Set the current token to the first token in the list.
        self._curToken: Token = tokList[0]

        # Flag to indicate whether any syntax errors have occurred during parsing.
        self.hadError: bool = False

        # List to store syntax error objects if any are encountered during parsing.
        self._errList: List[SyntaxErr] = []
            # Main parser method that returns the constructed AST.
   
    def getAST(self) -> ASTNode:
        """
        This method initiates the parsing process by invoking the '_program' method.

        :return: The root node of the constructed Abstract Syntax Tree (AST).
        """
        return self._program()

    # Move forward by 'advBy' steps in the token list.
    def _advance(self, advBy: int = 1) -> None:
        """
        Advances the parser's current token index by 'advBy' steps.

        :param advBy: The number of steps to advance. Default is 1.
        """
        self._idx += advBy

        # Check if the index has gone beyond the end of the token list.
        if self._idx >= len(self._tokList):
            self._curToken = self._tokList[-1]
            return

        # Update the current token to the token at the new index.
        self._curToken = self._tokList[self._idx]
        
    
    # Get the next token without advancing the index.
    def _peek(self) -> Token:
        """
        Returns the next token in the token list without advancing the parser's index.

        :return: The next token.
        """
        if self._idx + 1 >= len(self._tokList):
            return self._tokList[-1]
        return self._tokList[self._idx + 1]

    # Get the previous token.
    def _prevToken(self) -> Token:
        """
        Returns the previous token in the token list.

        :return: The previous token.
        """
        return self._tokList[self._idx - 1]

    # Adds an error to the error list and synchronizes the parser.
    def _error(self, msg: str) -> None:
        """
        Records a syntax error in the error list, sets the 'hadError' flag, and synchronizes the parser.

        :param msg: The error message to be added.
        """
        # Set the 'hadError' flag to indicate that an error has occurred.
        self.hadError = True

        # Create a SyntaxErr object and add it to the error list.
        self._errList.append(
            SyntaxErr(msg, self._curToken.line, self._curToken.position)
        )

        # Synchronize the parser to continue parsing.
        self._sync()

    # Synchronize the parser by discarding tokens until a known recovery point.
    def _sync(self) -> None:
        """
        Synchronizes the parser by discarding tokens until a known recovery point is reached.
        This helps the parser continue parsing and potentially report more errors at once.

        Recovery points are specific token types that the parser can safely advance to.
        """
        while self._curToken.type not in [
            TokenType.SEMI,
            TokenType.EOF,
            TokenType.VAR,
            TokenType.FUNCTION,
            TokenType.R_PAREN,
            TokenType.R_CURLY,
            TokenType.RETURN
        ]:
            # Continue advancing until a recovery point is reached.
            self._advance()

    # 'Consumes' the current token, adds an error if the token is not of type 'tt'.
    def _consume(self, tt: TokenType) -> None:
        """
        Consumes the current token and adds an error if it does not match the expected 'tt' type.

        :param tt: The expected token type.
        """
        if self._curToken.type != tt:
            self.hadError = True

            # Missing semicolon error
            if tt == TokenType.SEMI:
                self._errList.append(
                    SyntaxErr(f"Expected ';'", self._prevToken().line, self._prevToken().position)
                )

            # Unexpected token error
            else:
                if self._curToken.value != '':
                    self._errList.append(
                        SyntaxErr(f"Expected {tt.value}, got '{self._curToken.value}'", self._curToken.line, self._curToken.position)
                    )
                else:
                    self._errList.append(
                        SyntaxErr(f"Expected {tt.value}", self._curToken.line, self._curToken.position)
                    )
            self._sync()

        # Advance to the next token after consuming or encountering an error.
        self._advance()

    # Get the list of syntax errors.
    def getError(self) -> List[SyntaxErr]:
        """
        Returns the list of syntax error objects recorded during parsing.

        :return: List of syntax error objects.
        """
        return self._errList
    

    # Methods that construct the AST #
    #  based on grammar defined in loks/specification/grammar.txt #

    def _program(self) -> ProgramNode:
        """
        Parses a program by constructing an Abstract Syntax Tree (AST) based on the defined grammar.

        A program is represented as a sequence of declarations.

        :return: A ProgramNode containing a list of AST nodes representing declarations.
        """
        # Initialize an empty list to store declarations.
        declList: List[ASTNode] = []

        # Continue parsing declarations until the end of the input is reached.
        while self._curToken.type != TokenType.EOF:
            # Parse a declaration and append it to the list of declarations.
            declList.append(self._declaration())

        # Create and return a ProgramNode, encapsulating the list of declarations.
        return ProgramNode(declList)
    
    
    #Declarations#

    def _declaration(self) -> ASTNode:
        """
        Parses a declaration, which can be a variable declaration, function declaration, or a statement.

        A declaration is the top-level construct in the grammar and represents a single statement or definition.

        :return: An ASTNode representing the parsed declaration.
        """
        if self._curToken.type == TokenType.VAR:
            # If the current token is 'VAR', it's a variable declaration.
            return self._varDecl()
        elif self._curToken.type == TokenType.FUNCTION:
            # If the current token is 'FUNCTION', it's a function declaration.
            return self._funDecl()
        else:
            # Otherwise, it's a statement (e.g., assignment, if statement).
            return self._statement()

    
    def _varDecl(self) -> ASTNode:
        """
        Parses a variable declaration.

        A variable declaration can take the form:
        VAR identifier (ASSIGN expression)? SEMI

        This method handles the parsing of variable declarations.

        :return: An ASTNode representing the parsed variable declaration.
        """
        # Consume the 'VAR' token.
        self._consume(TokenType.VAR)
        
        # Get the identifier token for the variable.
        id: Token = self._curToken
        exprNode: ASTNode = None
        
        # Consume the identifier token.
        self._consume(TokenType.ID)

        # Check if there is an assignment operator.
        if self._curToken.type == TokenType.ASSIGN:
            # Consume the assignment operator.
            self._consume(TokenType.ASSIGN)
            
            # Parse the expression on the right-hand side of the assignment.
            exprNode = self._expression()
        
        # Consume the semicolon at the end of the declaration.
        self._consume(TokenType.SEMI)

        # Return a VarDeclNode representing the variable declaration.
        return VarDeclNode(IdentifierNode(id), exprNode)
    
    def _funDecl(self) -> ASTNode:
        """
        Parses a function declaration.

        A function declaration consists of the following components:
        FUNCTION identifier ( L_PAREN (parameters)? R_PAREN ) block

        :return: An ASTNode representing the parsed function declaration.
        """
        # Consume the 'FUNCTION' keyword.
        self._consume(TokenType.FUNCTION)

        # Get the identifier token for the function.
        id: Token = self._curToken

        # Consume the identifier token.
        self._consume(TokenType.ID)

        # Consume the left parenthesis for the parameter list.
        self._consume(TokenType.L_PAREN)

        # Initialize an empty list to store parameters.
        params: List[Token] = []

        # Check if there are parameters inside the parenthesis.
        if self._curToken.type != TokenType.R_PAREN:
            # Parse the parameters if present.
            params = self._parameters()

        # Consume the right parenthesis to close the parameter list.
        self._consume(TokenType.R_PAREN)

        # Parse the function's block.
        bl: BlockNode = self._block()

        # Return a FunDeclNode representing the function declaration.
        return FunDeclNode(IdentifierNode(id), params, bl)
    
    #Statements#

    def _statement(self) -> ASTNode:
        """
        Parses a statement, which can be an assignment statement, expression statement,
        if statement, block statement, return statement, continue statement, break statement,
        while loop, for loop, or a simple expression statement.

        :return: An ASTNode representing the parsed statement.
        """
        if self._curToken.type == TokenType.ID:
            stmt: ASTNode = None
            # Check if the current token is an assignment or an array index (L_SQUARE).
            if self._peek().type in [TokenType.ASSIGN,  TokenType.L_SQUARE]:
                stmt = self._assignStmt()
            else:
                stmt = self._exprStmt()
            return stmt

        elif self._curToken.type == TokenType.IF:
            # Parse an if statement.
            return self._ifStmt()

        elif self._curToken.type == TokenType.L_CURLY:
            # Parse a block statement.
            return self._block()

        elif self._curToken.type == TokenType.RETURN:
            # Parse a return statement.
            return self._return()

        elif self._curToken.type == TokenType.CONTINUE:
            # Parse a continue statement.
            return self._continue()

        elif self._curToken.type == TokenType.BREAK:
            # Parse a break statement.
            return self._break()

        elif self._curToken.type == TokenType.WHILE:
            # Parse a while loop.
            return self._while()

        elif self._curToken.type == TokenType.FOR:
            # Parse a for loop.
            return self._for()

        else:
            # If none of the above cases match, treat it as a simple expression statement.
            return self._exprStmt()

    def _exprStmt(self) -> ASTNode:
        """
        Parses an expression statement, ending with a semicolon.

        An expression statement is typically used to evaluate an expression and discard its result.

        :return: An ASTNode representing the parsed expression statement.
        """
        stmt: ASTNode = self._expression()

        # Consume the semicolon at the end of the expression statement.
        self._consume(TokenType.SEMI)
        
        return stmt

    def _assignStmt(self) -> AssignNode:
        """
        Parses an assignment statement, which assigns a value to a variable or an array element.

        An assignment statement can be of the form:
        identifier ('[' expression ']')? ASSIGN expression SEMI

        :return: An AssignNode representing the parsed assignment statement.
        """
        # Get the identifier token.
        id: Token = self._curToken

        # Check for subscript (array access).
        aac: ArrayAccessNode = None
        if self._peek().type == TokenType.L_SQUARE:
            aac = self._array_access()
        else:
            # Consume the identifier token.
            self._consume(TokenType.ID)

        # Consume the assignment operator.
        self._consume(TokenType.ASSIGN)

        # Parse the right-hand side expression.
        exprNode: ASTNode = self._expression()

        # Consume the semicolon at the end of the assignment statement.
        self._consume(TokenType.SEMI)

        # Create an AssignNode representing the assignment statement.
        if aac != None:
            return AssignNode(aac, exprNode)
        return AssignNode(IdentifierNode(id), exprNode)

    def _ifStmt(self) -> IfNode:
        """
        Parses an if statement, which may include multiple conditional branches (if, elseif, and else).

        An if statement has the following structure:
        IF (expression) statement (ELSEIF (expression) statement)* (ELSE statement)?

        :return: An IfNode representing the parsed if statement with its conditional branches.
        """
        # Parse the 'IF' keyword and the opening parenthesis.
        self._consume(TokenType.IF)
        self._consume(TokenType.L_PAREN)

        # Parse the condition for the 'IF' branch.
        ifCond: ASTNode = self._expression()

        # Consume the closing parenthesis.
        self._consume(TokenType.R_PAREN)

        # Parse the statement block for the 'IF' branch.
        ifBlk: BlockNode = self._statement()
        ifst: ConditionalNode = ConditionalNode(ifCond, ifBlk)

        # Initialize a list to store 'ELSEIF' branches.
        elsifArr: List[ConditionalNode] = []

        # Parse 'ELSEIF' branches if they exist.
        while self._curToken.type == TokenType.ELSEIF:
            # Consume 'ELSEIF' and the opening parenthesis.
            self._consume(TokenType.ELSEIF)
            self._consume(TokenType.L_PAREN)

            # Parse the condition for the 'ELSEIF' branch.
            elifCond = self._expression()

            # Consume the closing parenthesis.
            self._consume(TokenType.R_PAREN)

            # Parse the statement block for the 'ELSEIF' branch.
            elifBlk: BlockNode = self._statement()
            elsifArr.append(ConditionalNode(elifCond, elifBlk))

        # Initialize a variable for the 'ELSE' branch.
        elseSt: BlockNode = None

        # Parse the 'ELSE' branch if it exists.
        if self._curToken.type == TokenType.ELSE:
            # Consume 'ELSE' and parse the 'ELSE' statement.
            self._consume(TokenType.ELSE)
            elseSt = self._statement()

        # Create and return an IfNode representing the if statement with its branches.
        return IfNode(ifst, elsifArr, elseSt)

        
    def _return(self) -> ReturnNode:
        """
        Parses a return statement, which may include an optional expression to be returned.

        A return statement allows a function to return a value. It has the following structure:
        RETURN (expression)? SEMI

        - The 'RETURN' keyword signifies the start of the return statement.
        - An optional expression can follow 'RETURN' to specify the value to be returned.
        - The statement is terminated by a semicolon ('SEMI').

        :return: A ReturnNode representing the parsed return statement.
        """
        # Get the current token, which is 'RETURN'.
        t: Token = self._curToken

        # Consume the 'RETURN' keyword to indicate the start of the return statement.
        self._consume(TokenType.RETURN)

        # Initialize a variable to store the expression (if any).
        expr: ASTNode = None

        # Check if there is an expression following 'RETURN' (if not, it's a void return).
        if self._curToken.type != TokenType.SEMI:
            # Parse the expression to determine the value to be returned.
            expr = self._expression()

        # Consume the semicolon at the end of the return statement to mark its completion.
        self._consume(TokenType.SEMI)

        # If no expression was provided, create a NilNode to represent a void return.
        if expr is None:
            expr = NilNode(t)

        # Create and return a ReturnNode representing the parsed return statement,
        # including the returned expression and the line where the 'RETURN' keyword appeared.
        return ReturnNode(expr, t.line)

    def _continue(self) -> ContinueNode:
        """
        Parses a 'continue' statement, which is used to exit the current loop iteration and continue to the next iteration.

        A 'continue' statement has the following structure:
        CONTINUE SEMI

        :return: A ContinueNode representing the parsed 'continue' statement.
        """
        # Get the current token, which is 'CONTINUE'.
        t: Token = self._curToken

        # Consume the 'CONTINUE' keyword to indicate the start of the 'continue' statement.
        self._consume(TokenType.CONTINUE)

        # Consume the semicolon at the end of the 'continue' statement to mark its completion.
        self._consume(TokenType.SEMI)

        # Create and return a ContinueNode representing the parsed 'continue' statement.
        return ContinueNode(t)

    def _break(self) -> BreakNode:
        """
        Parses a 'break' statement, which is used to exit the current loop.

        A 'break' statement has the following structure:
        BREAK SEMI

        :return: A BreakNode representing the parsed 'break' statement.
        """
        # Get the current token, which is 'BREAK'.
        t: Token = self._curToken

        # Consume the 'BREAK' keyword to indicate the start of the 'break' statement.
        self._consume(TokenType.BREAK)

        # Consume the semicolon at the end of the 'break' statement to mark its completion.
        self._consume(TokenType.SEMI)

        # Create and return a BreakNode representing the parsed 'break' statement.
        return BreakNode(t)

    def _while(self) -> WhileNode:
        """
        Parses a 'while' loop statement, which represents a loop that continues while a given condition is true.

        A 'while' loop statement has the following structure:
        WHILE (expression) statement

        :return: A WhileNode representing the parsed 'while' loop statement.
        """
        # Consume the 'WHILE' keyword to indicate the start of the 'while' loop.
        self._consume(TokenType.WHILE)
        
        # Consume the opening parenthesis to mark the start of the loop condition.
        self._consume(TokenType.L_PAREN)

        # Parse the loop condition, which is an expression.
        cond = self._expression()

        # Consume the closing parenthesis to indicate the end of the loop condition.
        self._consume(TokenType.R_PAREN)

        # Parse the statement block associated with the 'while' loop.
        blk: ASTNode = self._statement()

        # Create and return a WhileNode representing the parsed 'while' loop statement,
        # including the loop condition and the statement block.
        return WhileNode(cond, blk)

    def _for(self) -> BlockNode:
        """
        Parses a 'for' loop statement, which is syntactic sugar for a 'while' loop with a counter.

        A 'for' loop statement has the following structure:
        FOR (first-statement; condition; third-statement) statement

        This comment describes the first part of the '_for' method, which handles the initialization of the 'for' loop.

        :return: A BlockNode representing the parsed 'for' loop statement desugared into a 'while' loop.
        """
        # Consume the 'FOR' keyword to indicate the start of the 'for' loop.
        self._consume(TokenType.FOR)

        # Consume the opening parenthesis to mark the start of the loop control expressions.
        self._consume(TokenType.L_PAREN)

        # Parse the first statement or declaration inside the 'for' loop parentheses.
        decl: ASTNode = None

        # Check the type of the current token to determine the type of first statement.
        if self._curToken.type == TokenType.VAR:
            # Parse a variable declaration statement.
            decl = self._varDecl()
        elif self._curToken.type == TokenType.SEMI:
            # If the current token is a semicolon, simply advance to the next token.
            self._advance()
        elif self._curToken.type == TokenType.ID:
            # Parse an assignment statement.
            decl = self._assignStmt()
        else:
            # If none of the above cases match, assume it's an expression statement.
            decl = self._exprStmt()

        # Parse the second statement inside the 'for' loop parentheses, which represents the loop condition.
        cond: ASTNode = None

        # Check if the current token is not a semicolon, indicating the presence of a second statement.
        if self._curToken.type != TokenType.SEMI:
            # Parse the second statement, which typically evaluates the loop condition.
            cond = self._expression()

        # Consume the semicolon to separate the second statement from the third statement.
        self._consume(TokenType.SEMI)

        # Initialize a variable to store the third statement inside the 'for' loop parentheses.
        update: ASTNode = None

        # Check if the current token is not a closing parenthesis, indicating the presence of a third statement.
        if self._curToken.type != TokenType.R_PAREN:
            # Parse the third statement, which is an assignment statement to update loop variables.
            id = self._curToken
            self._consume(TokenType.ID)
            self._consume(TokenType.ASSIGN)
            expr = self._expression()
            update = AssignNode(IdentifierNode(id), expr)

        # Consume the closing parenthesis to indicate the end of the loop control expressions.
        self._consume(TokenType.R_PAREN)
        
        # Desugar the 'for' loop into a 'while' loop.
        stmtlist: List[ASTNode] = []

        # If there was a first statement (declaration or assignment), add it to the list of statements.
        if decl != None:
            stmtlist.append(decl)

        # Parse the statement block associated with the 'for' loop.
        blk: ASTNode = self._statement()

        # If there's a third statement (loop update), add it to the statement block.
        if update != None:
            # Check if the statement block is a BlockNode; if it is, append the update statement.
            if isinstance(blk, BlockNode):
                blk.stmtList.append(update)
            else:
                # If the statement block is not a BlockNode, create one with the original statement and the update.
                blk = BlockNode([blk, update])

        # Create a 'while' loop node to represent the desugared loop.
        w: WhileNode = None

        # Check if there is a loop condition (second statement inside the 'for' loop parentheses).
        if cond != None:
            w = WhileNode(cond, blk)
        else:
            # If there is no condition, create a 'while' loop with a true condition (infinite loop).
            dummyTrue: TrueNode = TrueNode(Token(TokenType.TRUE, "true", 0, 0))
            w = WhileNode(dummyTrue, blk)

        # Add the 'while' loop node to the list of statements.
        stmtlist.append(w)

        # Create and return a BlockNode representing the desugared 'for' loop as a 'while' loop.
        return BlockNode(stmtlist)

    def _parameters(self) -> List[Token]:
        """
        Parses a list of function parameters.

        Function parameters are a comma-separated list of identifiers.

        :return: A list of Token objects representing the parsed function parameters.
        """
        # Initialize a list to store the function parameters, starting with the current token.
        paramList: List[Token] = [self._curToken]

        # Consume the current token, which is the first parameter.
        self._consume(TokenType.ID)

        # Continue parsing additional parameters while there are commas.
        while self._curToken.type == TokenType.COMMA:
            # Advance to the next token (the comma).
            self._advance()

            # Add the current token (the identifier) to the parameter list.
            paramList.append(self._curToken)

            # Consume the identifier token.
            self._consume(TokenType.ID)

        # Return the list of parsed function parameters.
        return paramList

    def _block(self) -> BlockNode:
        """
        Parses a block of statements enclosed within curly braces.

        A block is a sequence of declarations and statements enclosed within curly braces.

        :return: A BlockNode representing the parsed block of statements.
        """
        # Consume the opening curly brace to mark the beginning of the block.
        self._consume(TokenType.L_CURLY)

        # Initialize an empty list to store the statements in the block.
        stmtList: List[ASTNode] = []

        # Continue parsing declarations and statements until a closing curly brace or the end of the file.
        while self._curToken.type not in [TokenType.R_CURLY, TokenType.EOF]:
            stmtList.append(self._declaration())

        # Consume the closing curly brace to indicate the end of the block.
        self._consume(TokenType.R_CURLY)

        # Create and return a BlockNode containing the parsed statements.
        return BlockNode(stmtList)
    
    
    #Expressions#

    def _expression(self) -> ASTNode:
        """
        Parses an expression, starting with the lowest precedence operator (logical OR).

        This method serves as the entry point for parsing expressions and handles the logical OR operator.

        :return: An ASTNode representing the parsed expression.
        """
        return self._logicOr()

    def _logicOr(self) -> ASTNode:
        """
        Parses logical OR expressions.

        Logical OR expressions are formed by logical AND expressions separated by 'or' operators.

        :return: An ASTNode representing the parsed logical OR expression.
        """
        # Parse the left-hand side of the logical OR expression.
        l: ASTNode = self._logicAnd()

        # Continue parsing logical OR expressions while encountering 'or' operators.
        while self._curToken.type == TokenType.OR:
            # Advance to the 'or' operator.
            self._advance()

            # Parse the right-hand side of the logical OR expression.
            r: ASTNode = self._logicAnd()

            # Create an OrNode to represent the logical OR operation.
            l = OrNode(l, r)

        # Return the parsed logical OR expression.
        return l

    def _logicAnd(self) -> ASTNode:
        """
        Parses logical AND expressions.

        Logical AND expressions are formed by equality expressions separated by 'and' operators.

        :return: An ASTNode representing the parsed logical AND expression.
        """
        # Parse the left-hand side of the logical AND expression.
        l: ASTNode = self._equality()

        # Continue parsing logical AND expressions while encountering 'and' operators.
        while self._curToken.type == TokenType.AND:
            # Advance to the 'and' operator.
            self._advance()

            # Parse the right-hand side of the logical AND expression.
            r: ASTNode = self._equality()

            # Create an AndNode to represent the logical AND operation.
            l = AndNode(l, r)

        # Return the parsed logical AND expression.
        return l
    
    def _equality(self) -> ASTNode:
        """
        Parses equality expressions.

        Equality expressions are formed by comparison expressions separated by '==' or '!=' operators.

        :return: An ASTNode representing the parsed equality expression.
        """
        # Parse the left-hand side of the equality expression.
        l: ASTNode = self._comparison()

        # Continue parsing equality expressions while encountering '==' or '!=' operators.
        while self._curToken.type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            # Store the type of the operator (either '==' or '!=').
            opType = self._curToken.type

            # Advance to the operator token.
            self._advance()

            # Parse the right-hand side of the equality expression.
            r: ASTNode = self._comparison()

            # Create an EqualNode or a NotEqualNode based on the operator type.
            if opType == TokenType.EQUAL:
                l = EqualNode(l, r)
            elif opType == TokenType.NOT_EQUAL:
                l = NotEqualNode(l, r)

        # Return the parsed equality expression.
        return l

    def _comparison(self) -> ASTNode:
        """
        Parses comparison expressions.

        Comparison expressions are formed by term expressions separated by comparison operators,
        which include '<', '<=', '>', and '>='.

        :return: An ASTNode representing the parsed comparison expression.
        """
        # Parse the left-hand side of the comparison expression.
        l: ASTNode = self._term()

        # Continue parsing comparison expressions while encountering comparison operators.
        while self._curToken.type in [
            TokenType.GREATER_THAN,
            TokenType.GREATER_THAN_EQ,
            TokenType.LESS_THAN,
            TokenType.LESS_THAN_EQ
        ]:
            # Store the type of the comparison operator.
            opType = self._curToken.type

            # Advance to the operator token.
            self._advance()

            # Parse the right-hand side of the comparison expression.
            r: ASTNode = self._term()

            # Create a specific comparison node based on the operator type.
            if opType == TokenType.GREATER_THAN:
                l = GreaterThanNode(l, r)
            elif opType == TokenType.GREATER_THAN_EQ:
                l = GreaterThanEqualNode(l, r)
            elif opType == TokenType.LESS_THAN:
                l = LessThanNode(l, r)
            elif opType == TokenType.LESS_THAN_EQ:
                l = LessThanEqualNode(l, r)

        # Return the parsed comparison expression.
        return l


    def _term(self) -> ASTNode:
        """
        Parses term expressions, which involve addition and subtraction operations on factors.

        Term expressions are part of the grammar and handle mathematical operations involving addition and subtraction.

        :return: An ASTNode representing the parsed term expression.
        """
        # Parse the left-hand side of the term expression, which is a factor.
        l: ASTNode = self._factor()

        # Continue parsing term expressions while encountering addition or subtraction operators.
        while self._curToken.type in [TokenType.PLUS, TokenType.MINUS]:
            # Store the type of the operator (either '+' or '-').
            opType = self._curToken.type

            # Advance to the operator token.
            self._advance()

            # Parse the right-hand side of the term expression.
            r: ASTNode = self._factor()

            # Create an AddNode or SubNode based on the operator type.
            if opType == TokenType.PLUS:
                l = AddNode(l, r)
            elif opType == TokenType.MINUS:
                l = SubNode(l, r)

        # Return the parsed term expression.
        return l

    def _factor(self) -> ASTNode:
        """
        Parses factor expressions, which involve multiplication, division, and modulo operations on unary expressions.

        Factor expressions are part of the grammar and handle mathematical operations involving multiplication, division, and modulo.

        :return: An ASTNode representing the parsed factor expression.
        """
        # Parse the left-hand side of the factor expression, which is a unary expression.
        l: ASTNode = self._unary()

        # Continue parsing factor expressions while encountering multiplication, division, or modulo operators.
        while self._curToken.type in [TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            # Store the type of the operator (either '*', '/', or '%').
            opType = self._curToken.type

            # Advance to the operator token.
            self._advance()

            # Parse the right-hand side of the factor expression.
            r: ASTNode = self._unary()

            # Create a MulNode, DivNode, or ModNode based on the operator type.
            if opType == TokenType.MUL:
                l = MulNode(l, r)
            elif opType == TokenType.DIV:
                l = DivNode(l, r)
            elif opType == TokenType.MOD:
                l = ModNode(l, r)

        # Return the parsed factor expression.
        return l

    def _unary(self) -> ASTNode:
        """
        Parses unary expressions, including logical negation and arithmetic negation (negation).

        Unary expressions involve applying a unary operator, such as 'not' or '-', to a subexpression, which can be an array access or another unary expression.

        :return: An ASTNode representing the parsed unary expression.
        """
        # Initialize a variable to store the resulting unary expression.
        n: ASTNode = None

        # Check for logical negation using the 'not' operator.
        if self._curToken.type == TokenType.NOT:
            # Advance to the 'not' operator token.
            self._advance()

            # Parse the subexpression and create a NotNode to represent the logical negation.
            n = NotNode(self._unary())
        # Check for arithmetic negation (negation) using the '-' operator.
        elif self._curToken.type == TokenType.MINUS:
            # Advance to the '-' operator token.
            self._advance()

            # Parse the subexpression and create a NegationNode to represent the arithmetic negation.
            n = NegationNode(self._unary())
        else:
            # If no unary operator is present, parse an array access or another unary expression.
            n = self._array_access()

        # Return the parsed unary expression, which may involve a negation or logical negation operation.
        return n
    
    def _array_access(self) -> ASTNode:
        """
        Parses array access expressions, allowing access to elements within an array.

        Array access expressions involve accessing elements within an array using square brackets.

        :return: An ASTNode representing the parsed array access expression.
        """
        # Parse the primary expression, which can be a function call or another expression.
        p: ASTNode = self._call()

        # Continue parsing array access expressions while encountering square brackets.
        while self._curToken.type == TokenType.L_SQUARE:
            # Advance to the left square bracket token.
            self._advance()

            # Parse the expression inside the square brackets to specify the element index.
            expr = self._expression()

            # Consume the right square bracket token.
            self._consume(TokenType.R_SQUARE)

            # Create an ArrayAccessNode to represent the array access operation.
            p = ArrayAccessNode(p, expr)

        # Return the parsed array access expression, which may involve multiple access operations.
        return p
   

    def _call(self) -> ASTNode:
        """
        Parses function or method call expressions, allowing the invocation of functions or methods with arguments.

        Call expressions involve invoking a function or method with optional arguments enclosed in parentheses.

        :return: An ASTNode representing the parsed call expression, which can be a function call or another primary expression.
        """
        # Parse the primary expression, which can be a variable, a literal, or another primary expression.
        p: ASTNode = self._primary()

        # Check if the current token is an open parenthesis, indicating a function or method call.
        if self._curToken.type == TokenType.L_PAREN:
            # Advance to the left parenthesis token.
            self._advance()

            # Initialize a list to store the function call arguments.
            arg: List[ASTNode] = []

            # Check if there are any arguments specified within the parentheses.
            if self._curToken.type != TokenType.R_PAREN:
                # Parse and gather the arguments.
                arg = self._arguments()

            # Consume the right parenthesis token, closing the argument list.
            self._consume(TokenType.R_PAREN)

            # Create a FunctionCallNode to represent the function or method call with arguments.
            p = FunctionCallNode(p, arg)

        # Return the parsed call expression, which may involve a function or method call.
        return p


    def _primary(self) -> ASTNode:
        """
        Parses primary expressions, which can be literals or identifiers.

        Primary expressions handle literals such as 'true,' 'false,' and 'nil,' as well as identifiers.

        :return: An ASTNode representing the parsed primary expression, which can be a literal node (TrueNode, FalseNode, NilNode) or an identifier node (IdentifierNode).
        """
        # Check if the current token is 'true,' representing a boolean true literal.
        if self._curToken.type == TokenType.TRUE:
            # Get the current token representing 'true.'
            t: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return a TrueNode representing the 'true' literal.
            return TrueNode(t)

        # Check if the current token is 'false,' representing a boolean false literal.
        elif self._curToken.type == TokenType.FALSE:
            # Get the current token representing 'false.'
            t: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return a FalseNode representing the 'false' literal.
            return FalseNode(t)

        # Check if the current token is 'nil,' representing a null value.
        elif self._curToken.type == TokenType.NIL:
            # Get the current token representing 'nil.'
            t: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return a NilNode representing the 'nil' literal.
            return NilNode(t)

        # Check if the current token is a numeric literal (e.g., an integer or floating-point number).
        elif self._curToken.type == TokenType.NUMBER:
            # Get the current token representing a numeric literal.
            t: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return a NumberNode representing the parsed numeric literal.
            return NumberNode(t)

        # Check if the current token is a string literal.
        elif self._curToken.type == TokenType.STRING:
            # Get the current token representing a string literal.
            t: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return a StringNode representing the parsed string literal.
            return StringNode(t)

        # Check if the current token is an identifier (variable or function name).
        elif self._curToken.type == TokenType.ID:
            # Get the current token representing an identifier.
            id: Token = self._curToken

            # Advance to the next token.
            self._advance()

            # Create and return an IdentifierNode representing the parsed identifier.
            return IdentifierNode(id)

        # Check if the current token is an open parenthesis, indicating the start of an expression within parentheses.
        elif self._curToken.type == TokenType.L_PAREN:
            # Advance to the left parenthesis token.
            self._advance()

            # Parse the expression inside the parentheses.
            exp = self._expression()

            # Consume the right parenthesis token, closing the expression.
            self._consume(TokenType.R_PAREN)

            # Return the parsed expression.
            return exp

        # Check if the current token is an open square bracket, indicating the start of an array literal.
        elif self._curToken.type == TokenType.L_SQUARE:
            # Advance to the left square bracket token.
            self._advance()

            # Check if the array literal is empty (no elements).
            if self._curToken.type == TokenType.R_SQUARE:
                # Consume the right square bracket token and return an empty ArrayNode.
                self._consume(TokenType.R_SQUARE)
                return ArrayNode([])

            # Parse the elements of the array and create an ArrayNode to represent the array literal.
            a = ArrayNode(self._arguments())

            # Consume the right square bracket token, closing the array literal.
            self._consume(TokenType.R_SQUARE)

            # Return the parsed array literal.
            return a
        
        # If none of the recognized primary expression patterns are matched, report an error.
        else:
            # Signal a syntax error indicating that an expression was expected but not found.
            self._error("Expected expression")

    def _arguments(self) -> List[ASTNode]:
        """
        Parses a comma-separated list of arguments, such as function call arguments.

        This method handles the parsing of multiple expressions separated by commas.

        :return: A list of ASTNodes representing the parsed arguments.
        """
        # Initialize a list to store the parsed arguments, starting with the first expression.
        argList: List[ASTNode] = [self._expression()]

        # Check for additional arguments separated by commas.
        while self._curToken.type == TokenType.COMMA:
            # Advance to the next token, skipping the comma.
            self._advance()

            # Parse and add the next expression to the argument list.
            argList.append(self._expression())

        # Return the list of parsed arguments.
        return argList
