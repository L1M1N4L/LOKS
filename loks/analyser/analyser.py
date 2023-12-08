# Importing type hints for use in function signatures and variable annotations
from typing import List, Union, Tuple

# Importing the NodeVisitor class from a module in the parent directory
from ..nodevisitor import NodeVisitor

# Importing error classes (NameErr, TypeErr, SyntaxErr) for handling different types of errors
from ..error import NameErr, TypeErr, SyntaxErr

# Importing the Token and TokenType classes for lexical analysis
from ..lexerOrScanner.token import Token, TokenType

# Importing the SymbolTable class from the current directory for symbol management
from .symboltable import SymbolTable

# Importing specific symbol-related classes (TypeSymbol, VariableSymbol, FunctionSymbol) from the current directory
from .symboltable import TypeSymbol, VariableSymbol, FunctionSymbol

# SemanticAnalyzer class performs static analysis, checks for defined names, and minimal type checking
# Inherits from the NodeVisitor class, which is defined in locks/nodevisitor.py
class SemanticAnalyzer(NodeVisitor):
    def __init__(self) -> None:
        """
        Initialize the SemanticAnalyzer.

        This method sets up the initial state of the SemanticAnalyzer, including SymbolTables,
        temporary storage for function arguments, error flags, and error lists.

        :return: None
        """
        # SymbolTable for the main scope
        self._mainST: SymbolTable = None
        # SymbolTable for the current scope
        self._currentST: SymbolTable = None

        # Temporary list to store function arguments during analysis
        self._tempArgs = []

        # Flag indicating whether an error has occurred during analysis
        self.hadError: bool = False
        # List to store error objects (NameErr, TypeErr, SyntaxErr)
        self._errList: List[Union[NameErr, TypeErr, SyntaxErr]] = []

        # Flag to check if 'break' and 'continue' statements are outside a loop
        self._inLoop: bool = False

    # add builtin symbols to global symbol table
    def _initMainST(self) -> None:
        """
        Initialize the main symbol table with built-in symbols.

        This method adds built-in types (int, float, double, string) and functions (print, println, input, len,
        int, str, isinteger) to the global symbol table.

        :return: None
        """
        # Add built-in types to the global symbol table
        self._mainST.add(TypeSymbol("int"))      # Add integer type
        self._mainST.add(TypeSymbol("float"))    # Add float type
        self._mainST.add(TypeSymbol("double"))   # Add double type
        self._mainST.add(TypeSymbol("string"))   # Add string type

        # List of built-in functions
        builtinFunctions: List[str] = [
            "print", "println", "input",
            "len",
            "int", "str",
            "isinteger"
        ]

        # Add built-in functions to the global symbol table
        for f in builtinFunctions:
            # FunctionSymbol takes the function name, return type (None for functions with no return type),
            # and a list of parameters (in this case, a single parameter 's' for all functions)
            self._mainST.add(FunctionSymbol(f, None, [VariableSymbol("s")]))
            # Note: The loop above adds each built-in function to the symbol table with a placeholder parameter 's'.
            # In a more complete implementation, you would define the actual parameters for each function.


    def visit_ProgramNode(self, node) -> None:
        """
        Visit ProgramNode and perform static analysis.

        This method initializes the main symbol table, sets it as the current symbol table,
        initializes the main symbol table with built-in symbols, and then visits each declaration
        in the program.

        :param node: The ProgramNode to visit.
        :return: None
        """
        # Initialize the main symbol table
        self._mainST = SymbolTable("main")

        # Set the current symbol table to the main symbol table
        self._currentST = self._mainST

        # Initialize the main symbol table with built-in symbols
        self._initMainST()

        # Visit each declaration in the program
        for d in node.declarationList:
            self.visit(d)


    def visit_VarDeclNode(self, node) -> None:
        """
        Visit VarDeclNode and perform static analysis.

        This method checks for duplicate variable definitions, adds the variable symbol to the
        current symbol table, and checks if the assigned expression is a function (which is not allowed).

        :param node: The VarDeclNode to visit.
        :return: None
        """
        # Check for duplicate variable definitions
        if self._currentST.get(node.id.token.value, True) is not None:
            self._error('n', f"duplicate definition of name '{node.id.token.value}'", node.id.token)
            return

        # Add the variable symbol to the current symbol table
        self._currentST.add(VariableSymbol(node.id.token.value))

        # Check if there is an assigned expression
        if node.exprNode is not None:
            # Get the type and token of the expression
            typ, tok = self.visit(node.exprNode)
            # Check if the assigned expression is a function (which is not allowed)
            if typ == "function":
                self._error('t', f"cannot assign function {tok.value} to variable", tok)

    def visit_AssignNode(self, node) -> None:
        """
        Visit AssignNode and perform static analysis.

        This method visits the left-hand side (lvalue) and right-hand side (exprNode) of an assignment,
        checking for any issues such as assigning a function to a variable.

        :param node: The AssignNode to visit.
        :return: None
        """
        # Visit the left-hand side (lvalue) of the assignment
        self.visit(node.lvalue)

        # Get the type and token of the right-hand side (exprNode) of the assignment
        typ, tok = self.visit(node.exprNode)

        # Check if the right-hand side is a function (which is not allowed)
        if typ == "function":
            self._error('t', f"cannot assign function '{tok.value}' to variable", tok)


    def visit_IdentifierNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit IdentifierNode and perform static analysis.

        This method checks if the identifier is declared in the current symbol table and returns its type.

        :param node: The IdentifierNode to visit.
        :return: A tuple containing the identifier type and the identifier token.
        """
        # Check if the identifier is not declared in the current symbol table
        if self._currentST.get(node.token.value) is None:
            self._error('n', f"name '{node.token.value}' not declared", node.token)
            return "identifier", node.token

        # Return the type of the identifier from the current symbol table and the identifier token
        return self._currentST.get(node.token.value).type, node.token

    def visit_ArrayNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit ArrayNode and perform static analysis.

        This method visits each element in the array and returns the type of the array.

        :param node: The ArrayNode to visit.
        :return: A tuple containing the array type and the token of the last element.
        """
        # Initialize token to None
        tok = None
        # Visit each element in the array
        for e in node.elements:
            # Get the type and token of the element
            typ, tok = self.visit(e)

        # Return the array type and the token of the last element
        return "array", tok


    def visit_ArrayAccessNode(self, node) -> Tuple[str, str]:
        """
        Visit ArrayAccessNode and perform static analysis.

        This method checks if the base (array or variable) is subscriptable and visits the index.

        :param node: The ArrayAccessNode to visit.
        :return: A tuple containing the variable type and an empty string (no specific token needed).
        """
        # Get the type and token of the base (array or variable)
        typ, tok = self.visit(node.base)

        # Check if the base is not an array or a variable
        if typ != "array" and typ != "variable":
            self._error('t', f"Type '{typ}' is not subscriptable", tok)

        # Visit the index
        self.visit(node.index)

        # Return the variable type and an empty string (no specific token needed)
        return "variable", ""
    def visit_NumberNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit NumberNode and perform static analysis.

        This method returns the type and token of the numeric value.

        :param node: The NumberNode to visit.
        :return: A tuple containing the type ("number") and the token of the numeric value.
        """
        # Return the type ("number") and the token of the numeric value
        return "number", node.token


    def visit_TrueNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit TrueNode and perform static analysis.

        This method returns the type ("boolean") and the token for the 'True' value.

        :param node: The TrueNode to visit.
        :return: A tuple containing the type ("boolean") and the token for the 'True' value.
        """
        # Return the type ("boolean") and the token for the 'True' value
        return "boolean", node.token


    def visit_FalseNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit FalseNode and perform static analysis.

        This method returns the type ("boolean") and the token for the 'False' value.

        :param node: The FalseNode to visit.
        :return: A tuple containing the type ("boolean") and the token for the 'False' value.
        """
        # Return the type ("boolean") and the token for the 'False' value
        return "boolean", node.token

    def visit_NilNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit NilNode and perform static analysis.

        This method returns the type ("nil") and the token for the 'nil' value.

        :param node: The NilNode to visit.
        :return: A tuple containing the type ("nil") and the token for the 'nil' value.
        """
        # Return the type ("nil") and the token for the 'nil' value
        return "nil", node.token


    def visit_StringNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit StringNode and perform static analysis.

        This method returns the type ("string") and the token of the string value.

        :param node: The StringNode to visit.
        :return: A tuple containing the type ("string") and the token of the string value.
        """
        # Return the type ("string") and the token of the string value
        return "string", node.token


    def visit_AddNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit AddNode and perform static analysis.

        This method visits the left and right expressions of an addition, checking if they are compatible types.

        :param node: The AddNode to visit.
        :return: A tuple containing the common type and the token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        typr, tokr = self.visit(node.right)

        # Check if both expressions are not variables or function calls
        if typl not in ["variable", "call"] and typr not in ["variable", "call"]:
            # Check if the types are incompatible for addition
            if typr != typl:
                self._error('t', f"cannot add '{typl}' to '{typr}'", tokl)

        # Return the common type and the token of the left expression
        return typl, tokl
    

    def visit_SubNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit SubNode and perform static analysis.

        This method visits the left and right expressions of a subtraction, checking if they are compatible types.

        :param node: The SubNode to visit.
        :return: A tuple containing the common type and the token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        typr, tokr = self.visit(node.right)

        # Check if both expressions are not variables
        if typl != "variable" and typr != "variable":
            # Check if the types are incompatible for subtraction
            if typr != typl:
                self._error('t', f"cannot subtract '{typr}' from '{typl}'", tokl)

        # Return the common type and the token of the left expression
        return typl, tokl


    def visit_MulNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit MulNode and perform static analysis.

        This method visits the left and right expressions of a multiplication, checking if they are compatible types.

        :param node: The MulNode to visit.
        :return: A tuple containing the common type and the token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        typr, tokr = self.visit(node.right)

        # Check if both expressions are not variables
        if typl != "variable" and typr != "variable":
            # Check if the types are incompatible for multiplication
            if typr != typl:
                self._error('t', f"cannot multiply '{typl}' by '{typr}'", tokl)

        # Return the common type and the token of the left expression
        return typl, tokl


    def visit_DivNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit DivNode and perform static analysis.

        This method visits the left and right expressions of a division, checking if they are compatible types.

        :param node: The DivNode to visit.
        :return: A tuple containing the common type and the token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        typr, tokr = self.visit(node.right)

        # Check if both expressions are not variables
        if typl != "variable" and typr != "variable":
            # Check if the types are incompatible for division
            if typr != typl:
                self._error('t', f"cannot divide '{typl}' by '{typr}'", tokl)

        # Return the common type and the token of the left expression
        return typl, tokl


    def visit_ModNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit ModNode and perform static analysis.

        This method visits the left and right expressions of a modulo operation, checking if they are compatible types.

        :param node: The ModNode to visit.
        :return: A tuple containing the common type and the token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        typr, tokr = self.visit(node.right)

        # Check if both expressions are not variables
        if typl != "variable" and typr != "variable":
            # Check if the types are incompatible for modulo operation
            if typr != typl:
                self._error('t', f"cannot modulo '{typl}' by '{typr}'", tokl)

        # Return the common type and the token of the left expression
        return typl, tokl
    def visit_EqualNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit EqualNode and perform static analysis.

        This method visits the left and right expressions of an equality comparison.

        :param node: The EqualNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_NotEqualNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit NotEqualNode and perform static analysis.

        This method visits the left and right expressions of a non-equality comparison.

        :param node: The NotEqualNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_GreaterThanNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit GreaterThanNode and perform static analysis.

        This method visits the left and right expressions of a greater-than comparison.

        :param node: The GreaterThanNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl

    def visit_LessThanNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit LessThanNode and perform static analysis.

        This method visits the left and right expressions of a less-than comparison.

        :param node: The LessThanNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_GreaterThanEqualNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit GreaterThanEqualNode and perform static analysis.

        This method visits the left and right expressions of a greater-than-or-equal comparison.

        :param node: The GreaterThanEqualNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_LessThanEqualNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit LessThanEqualNode and perform static analysis.

        This method visits the left and right expressions of a less-than-or-equal comparison.

        :param node: The LessThanEqualNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl

    def visit_AndNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit AndNode and perform static analysis.

        This method visits the left and right expressions of a logical AND operation.

        :param node: The AndNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_OrNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit OrNode and perform static analysis.

        This method visits the left and right expressions of a logical OR operation.

        :param node: The OrNode to visit.
        :return: A tuple containing the type and token of the left expression.
        """
        # Visit the left expression
        typl, tokl = self.visit(node.left)
        # Visit the right expression
        self.visit(node.right)

        # Return the type and token of the left expression
        return typl, tokl


    def visit_NegationNode(self, node) -> Tuple[TokenType, TokenType]:
        """
        Visit NegationNode and perform static analysis.

        This method visits the expression being negated.

        :param node: The NegationNode to visit.
        :return: A tuple containing the type and token of the expression being negated.
        """
        # Visit the expression being negated
        typ, tok = self.visit(node.node)

        # Return the type and token of the expression being negated
        return typ, tok

    def visit_WhileNode(self, node) -> None:
        """
        Visit WhileNode and perform static analysis.

        This method sets a flag indicating that the code is inside a loop, visits the condition and statement of
        the while loop, and then resets the loop flag.

        :param node: The WhileNode to visit.
        :return: None
        """
        # Set the flag indicating that the code is inside a loop
        self._inLoop = True
        # Visit the condition of the while loop
        self.visit(node.condition)
        # Visit the statement inside the while loop
        self.visit(node.statement)
        # Reset the loop flag
        self._inLoop = False


    def visit_BlockNode(self, node, isFunction=False) -> None:
        """
        Visit BlockNode and perform static analysis.

        This method visits the statements in a block. If it's a function block, it creates a new symbol table,
        adds temporary arguments to it, and updates the current symbol table accordingly.

        :param node: The BlockNode to visit.
        :param isFunction: A boolean indicating if it's a function block (default is False).
        :return: None
        """
        # If it's a function block
        if isFunction:
            # Create a new symbol table for the block
            s: SymbolTable = SymbolTable("block")
            # Set the enclosing scope of the new symbol table to the current symbol table
            s.setEnclosingScope(self._currentST)

            # Add temporary arguments to the new symbol table
            for a in self._tempArgs:
                s.add(a)

            # Reset the temporary arguments list
            self._tempArgs = []
            # Update the current symbol table to the new symbol table
            self._currentST = s

            # Visit each statement in the block
            for st in node.stmtList:
                self.visit(st)

            # Reset the current symbol table to its enclosing scope
            self._currentST = s.getEnclosingScope()
        else:
            # If it's not a function block, visit each statement in the block
            for st in node.stmtList:
                self.visit(st)


    def visit_ReturnNode(self, node) -> None:
        """
        Visit ReturnNode and perform static analysis.

        This method visits the expression in a return statement and checks if it returns a function, generating an error.

        :param node: The ReturnNode to visit.
        :return: None
        """
        # Visit the expression in the return statement
        typ, tok = self.visit(node.expr)

        # Check if the expression returns a function, generating an error
        if typ == "function":
            self._error('t', f"Cannot return function '{tok.value}' from function", tok)

    def visit_ContinueNode(self, node) -> None:
        """
        Visit ContinueNode and perform static analysis.

        This method checks if a 'continue' statement is inside a loop. If not, it generates an error.

        :param node: The ContinueNode to visit.
        :return: None
        """
        # Check if the 'continue' statement is inside a loop
        if not self._inLoop:
            # Generate an error for 'continue' outside a loop
            self._error('s', "'continue' outside loop", node.tok)


    def visit_BreakNode(self, node) -> None:
        """
        Visit BreakNode and perform static analysis.

        This method checks if a 'break' statement is inside a loop. If not, it generates an error.

        :param node: The BreakNode to visit.
        :return: None
        """
        # Check if the 'break' statement is inside a loop
        if not self._inLoop:
            # Generate an error for 'break' outside a loop
            self._error('s', "'break' outside loop", node.tok)

    def visit_FunDeclNode(self, node) -> None:
        """
        Visit FunDeclNode and perform static analysis.

        This method checks for duplicate function definitions, processes function parameters, and adds the function
        symbol to the symbol table. It then visits the block node inside the function.

        :param node: The FunDeclNode to visit.
        :return: None
        """
        # Check for duplicate function definitions
        if self._currentST.get(node.id.token.value) is not None:
            self._error('n', f"duplicate definition of name '{node.id.token.value}'", node.id.token)
            return

        # Process function parameters and add them to temporary arguments
        for a in node.paramList:
            self._tempArgs.append(VariableSymbol(a.value))

        # Add the function symbol to the symbol table
        self._currentST.add(FunctionSymbol(node.id.token.value, node.blockNode, self._tempArgs))

        # Visit the block node inside the function, indicating that it's a function block
        self.visit_BlockNode(node.blockNode, True)


    def visit_FunctionCallNode(self, node) -> Tuple[str, TokenType]:
        """
        Visit FunctionCallNode and perform static analysis.

        This method checks if the symbol being called is a function, verifies the number of arguments,
        and checks for argument count mismatches.

        :param node: The FunctionCallNode to visit.
        :return: A tuple containing the type ("call") and the token of the function being called.
        """
        # Get the type and token of the symbol being called
        t, tok = self.visit(node.nameNode)

        # Check if the symbol is callable (a function)
        if t != "function":
            self._error('t', f"Symbol '{tok.value}' of type '{t}' is not callable", tok)
            return "call", tok

        # Count the number of arguments
        argc: int = 0
        for a in node.argList:
            self.visit(a)
            argc += 1

        # Assert that the nameNode is an IdentifierNode
        assert type(node.nameNode).__name__ == "IdentifierNode"

        # Get the expected number of positional arguments for the function
        count: int = len(self._currentST.get(node.nameNode.token.value).argSymbols)

        # Check for argument count mismatches
        if count != argc:
            self._error('t', f"Expected {count} positional argument(s) for '{tok.value}', got {argc}", tok)

        # Return the type ("call") and the token of the function being called
        return "call", tok
