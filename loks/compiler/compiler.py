# Importing Type Annotations
from typing import List, Union, Dict

# Importing Custom Modules
from ..parser.abstractSyntaxTree import ASTNode  # Importing ASTNode class from the parser.ast module
from ..nodevisitor import NodeVisitor  # Importing NodeVisitor class from the nodevisitor module
from ..stdlib import builtinFunctionInfo  # Importing builtinFunctionInfo from the stdlib module


class Compiler(NodeVisitor):
    def __init__(self) -> None:
        """
        Initialize a Compiler instance.

        Attributes:
        - _constantPool: List[str] - An empty list to store constant pool values.
        - _functions: Dict[str, str] - A dictionary to store functions with "main" as the default entry.
        - _currentFn: str - The current function, initially set to "main".
        - _globalVars: List[str] - An empty list to store global variables.
        - _labelCtr: int - A counter for generating unique labels, initially set to -1.

        Calls the _initCode() method for additional initialization.
        """
        # Initialize an empty list to store constant pool values
        self._constantPool: List[str] = []

        # Initialize a dictionary to store functions with "main" as the default entry
        self._functions: Dict[str, str] = {"main": ""}

        # Set the current function to "main"
        self._currentFn: str = "main"

        # Initialize an empty list to store global variables
        self._globalVars: List[str] = []

        # Initialize a counter for generating unique labels
        self._labelCtr: int = -1

        # Call the _initCode() method to perform additional initialization
        self._initCode()


    def getCode(self) -> str:
        """
        Get the compiled code.

        This method generates and returns the compiled code, including constant pool and function definitions.

        :return: Compiled code as a string.
        """
        # Initialize a string to represent the constant pool section
        cpStr: str = f"cpc {len(self._constantPool)}\n"
        
        # Append each constant pool value to the string
        for s in self._constantPool:
            cpStr += s + '\n'

        # Initialize the output string with the constant pool section
        output: str = cpStr + '\n'  

        # Append the "END" to the main function
        self._functions["main"] += "    END"

        # Append each function definition to the output string
        for f in self._functions:
            output += self._functions[f] + '\n\n'

        # Return the compiled code
        return output


    def _initCode(self) -> None:
        """
        Initialize the code for the current function.

        This method is called during the initialization of the Compiler class.
        It adds a function header and sets the argument count for the main function.

        :return: None
        """
        self._functions[self._currentFn] += "fn main\nargc 0\n"


    def _emit(self, c: str, fmt: bool = True) -> None:
        """
        Emit code for the current function.

        This method appends the given code (c) to the current function in the Compiler instance.
        If fmt is True, it adds four spaces before the code, indicating proper indentation.

        :param c: The code to be emitted.
        :param fmt: If True, format the emitted code with indentation. Default is True.
        :return: None
        """
        if fmt:
            # Add indented code to the current function
            self._functions[self._currentFn] += f"    {c}\n"
        else:
            # Add non-indented code to the current function
            self._functions[self._currentFn] += f"    {c}\n"


    def _addConstant(self, c: str) -> None:
        """
        Add a constant to the constant pool.

        This method appends the given constant (c) to the constant pool in the Compiler instance.

        :param c: The constant to be added.
        :return: None
        """
        self._constantPool.append(c)


    def _generateLabel(self) -> str:
        """
        Generate a unique label.

        This method increments the label counter and returns a unique label string.

        :return: Unique label string.
        """
        self._labelCtr += 1
        return f"L{self._labelCtr}"


    def visit_ProgramNode(self, node) -> None:
        """
        Visit method for ProgramNode in the abstract syntax tree.

        This method visits the ProgramNode and iteratively visits each declaration in the declaration list.

        :param node: ProgramNode instance representing the entire program.
        :return: None
        """
        for d in node.declarationList:
            self.visit(d)

    def visit_NumberNode(self, node) -> None:
        """
        Visit method for NumberNode in the abstract syntax tree.

        This method processes a NumberNode, handling different cases based on the type and value of the number.

        :param node: NumberNode instance representing a numeric value.
        :return: None
        """
        v: Union[int, float] = node.token.value

        # Check if the number is a float
        if type(v).__name__ == "float":
            # Add the float constant to the constant pool
            self._addConstant(f"d {v}")
            # Emit the corresponding LOAD_CONST instruction
            self._emit(f"LOAD_CONST {len(self._constantPool) - 1}")
            return

        # Check if the number is a small integer (fits in one byte)
        if v < 256:
            # Emit BIPUSH instruction for small integers
            self._emit(f"BIPUSH {v}")
        else:
            # Add the integer constant to the constant pool
            self._addConstant(f"i {v}")
            # Emit the corresponding LOAD_CONST instruction
            self._emit(f"LOAD_CONST {len(self._constantPool) - 1}")

    def visit_StringNode(self, node) -> None:
        """
        Visit method for StringNode in the abstract syntax tree.

        This method processes a StringNode, adds the string constant to the constant pool,
        and emits the corresponding LOAD_CONST instruction.

        :param node: StringNode instance representing a string value.
        :return: None
        """
        # Add the string constant to the constant pool
        self._addConstant(f's "{node.token.value}"')
        # Emit the corresponding LOAD_CONST instruction
        self._emit(f"LOAD_CONST {len(self._constantPool) - 1}")


    def visit_NilNode(self, node) -> None:
        """
        Visit method for NilNode in the abstract syntax tree.

        This method emits the LOAD_NIL instruction.

        :param node: NilNode instance representing the nil value.
        :return: None
        """
        # Emit the LOAD_NIL instruction
        self._emit("LOAD_NIL")


    def visit_TrueNode(self, node) -> None:
        """
        Visit method for TrueNode in the abstract syntax tree.

        This method emits the LOAD_TRUE instruction.

        :param node: TrueNode instance representing the true value.
        :return: None
        """
        # Emit the LOAD_TRUE instruction
        self._emit("LOAD_TRUE")

    def visit_FalseNode(self, node) -> None:
        """
        Visit method for FalseNode in the abstract syntax tree.

        This method emits the LOAD_FALSE instruction.

        :param node: FalseNode instance representing the false value.
        :return: None
        """
        # Emit the LOAD_FALSE instruction
        self._emit("LOAD_FALSE")


    def visit_ArrayNode(self, node) -> None:
        """
        Visit method for ArrayNode in the abstract syntax tree.

        This method visits each element in the array node and emits the BUILD_LIST instruction.

        :param node: ArrayNode instance representing an array.
        :return: None
        """
        # Visit each element in the array node
        for i in node.elements:
            self.visit(i)
        # Emit the BUILD_LIST instruction with the length of the elements
        self._emit(f"BUILD_LIST {len(node.elements)}")


    def visit_IdentifierNode(self, node) -> None:
        """
        Visit method for IdentifierNode in the abstract syntax tree.

        This method emits either LOAD_GLOBAL or LOAD_LOCAL instruction based on
        whether the identifier is in the global variable list (_globalVars).

        :param node: IdentifierNode instance representing an identifier.
        :return: None
        """
        # Check if the identifier is in the global variable list
        if node.token.value in self._globalVars:
            # Emit LOAD_GLOBAL instruction
            self._emit(f"LOAD_GLOBAL {node.token.value}")
        else:
            # Emit LOAD_LOCAL instruction
            self._emit(f"LOAD_LOCAL {node.token.value}")



    def visit_ArrayAccessNode(self, node) -> None:
        """
        Visit method for ArrayAccessNode in the abstract syntax tree.

        This method visits the base and index nodes, then emits the BINARY_SUBSCR instruction.

        :param node: ArrayAccessNode instance representing an array access.
        :return: None
        """
        # Visit the base and index nodes
        self.visit(node.base)
        self.visit(node.index)
        # Emit the BINARY_SUBSCR instruction
        self._emit("BINARY_SUBSCR")


    def visit_NotNode(self, node) -> None:
        """
        Visit method for NotNode in the abstract syntax tree.

        This method visits the child node and emits the UNARY_NOT instruction.

        :param node: NotNode instance representing a logical NOT operation.
        :return: None
        """
        # Visit the child node
        self.visit(node.node)
        # Emit the UNARY_NOT instruction
        self._emit("UNARY_NOT")


    def visit_NegationNode(self, node) -> None:
        """
        Visit method for NegationNode in the abstract syntax tree.

        This method handles negation of numeric values, adding a negated constant to the constant pool
        or emitting the UNARY_NEGATIVE instruction for non-numeric values.

        :param node: NegationNode instance representing a negation operation.
        :return: None
        """
        # Check if the child node is a NumberNode
        if type(node.node).__name__ == "NumberNode":
            # Check if the number is a float
            if type(node.node.token.value).__name__ == "float":
                # Add the negated float constant to the constant pool
                self._addConstant(f"d -{node.node.token.value}")
            else:
                # Add the negated integer constant to the constant pool
                self._addConstant(f"i -{node.node.token.value}")
            # Emit the corresponding LOAD_CONST instruction
            self._emit(f"LOAD_CONST {len(self._constantPool) - 1}")
        else:
            # Visit the child node and emit UNARY_NEGATIVE for non-numeric values
            self.visit(node.node)
            self._emit("UNARY_NEGATIVE")


    def visit_AddNode(self, node) -> None:
        """
        Visit method for AddNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_ADD instruction.

        :param node: AddNode instance representing an addition operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_ADD instruction
        self._emit("BINARY_ADD")


    def visit_SubNode(self, node) -> None:
        """
        Visit method for SubNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_SUBTRACT instruction.

        :param node: SubNode instance representing a subtraction operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_SUBTRACT instruction
        self._emit("BINARY_SUBTRACT")


    def visit_MulNode(self, node) -> None:
        """
        Visit method for MulNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_MULTIPLY instruction.

        :param node: MulNode instance representing a multiplication operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_MULTIPLY instruction
        self._emit("BINARY_MULTIPLY")

    def visit_DivNode(self, node) -> None:
        """
        Visit method for DivNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_DIVIDE instruction.

        :param node: DivNode instance representing a division operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_DIVIDE instruction
        self._emit("BINARY_DIVIDE")


    def visit_ModNode(self, node) -> None:
        """
        Visit method for ModNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_MODULO instruction.

        :param node: ModNode instance representing a modulo operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_MODULO instruction
        self._emit("BINARY_MODULO")

    def visit_VarDeclNode(self, node) -> None:
        """
        Visit method for VarDeclNode in the abstract syntax tree.

        This method processes a variable declaration node, visiting the expression node if present,
        emitting the LOAD_NIL instruction if the expression is not provided, and storing the result in the local variable.

        Additionally, if the variable declaration is within the "main" function, it adds the variable to the global variable list.

        :param node: VarDeclNode instance representing a variable declaration.
        :return: None
        """
        # Visit the expression node if present, otherwise emit LOAD_NIL
        if node.exprNode is not None:
            self.visit(node.exprNode)
        else:
            self._emit("LOAD_NIL")

        # Check if the variable declaration is within the "main" function
        if self._currentFn == "main":
            # Add the variable to the global variable list
            self._globalVars.append(node.id.token.value)

        # Emit the STORE_LOCAL instruction to store the result in the local variable
        self._emit(f"STORE_LOCAL {node.id.token.value}")


    def visit_AssignNode(self, node) -> None:
        """
        Visit method for AssignNode in the abstract syntax tree.

        This method visits the expression node, and based on the type of the left-hand side (lvalue),
        emits the appropriate instruction to store the result.

        For IdentifierNode, it checks if the identifier is in the global variable list and emits STORE_GLOBAL or STORE_LOCAL.
        For ArrayAccessNode, it visits the base and index nodes and emits STORE_SUBSCR.

        :param node: AssignNode instance representing an assignment operation.
        :return: None
        """
        # Visit the expression node
        self.visit(node.exprNode)

        # Check the type of the left-hand side (lvalue)
        if type(node.lvalue).__name__ == "IdentifierNode":
            n: str = node.lvalue.token.value
            # Check if the identifier is in the global variable list
            if n in self._globalVars:
                # Emit STORE_GLOBAL instruction
                self._emit(f"STORE_GLOBAL {n}")
            else:
                # Emit STORE_LOCAL instruction
                self._emit(f"STORE_LOCAL {n}")
        elif type(node.lvalue).__name__ == "ArrayAccessNode":
            # Visit the base and index nodes and emit STORE_SUBSCR
            self.visit(node.lvalue.base)
            self.visit(node.lvalue.index)
            self._emit("STORE_SUBSCR")


    def visit_BlockNode(self, node, startLabl: str = None, endLabl: str = None) -> None:
        """
        Visit method for BlockNode in the abstract syntax tree.

        This method iterates through the statement list of the block node and visits each statement.
        It handles special cases like ContinueNode, BreakNode, and IfNode with optional startLabl and endLabl.

        :param node: BlockNode instance representing a block of statements.
        :param startLabl: Optional label for the start of the block (used in ContinueNode and IfNode).
        :param endLabl: Optional label for the end of the block (used in BreakNode and IfNode).
        :return: None
        """
        # Iterate through the statement list of the block node
        for s in node.stmtList:
            # Handle special cases
            if type(s).__name__ == "ContinueNode":
                # Emit GOTO instruction to jump to the start label
                self._emit(f"GOTO {startLabl}")
                continue

            if type(s).__name__ == "BreakNode":
                # Emit GOTO instruction to jump to the end label
                self._emit(f"GOTO {endLabl}")
                continue

            if type(s).__name__ == "IfNode":
                # Call the visit_IfNode method for IfNode
                self.visit_IfNode(s, startLabl, endLabl)
            else:
                # Visit other types of statements
                self.visit(s)


    def visit_EqualNode(self, node) -> None:
        """
        Visit method for EqualNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPEQ instruction.

        :param node: EqualNode instance representing an equality comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPEQ instruction
        self._emit("CMPEQ")


    def visit_NotEqualNode(self, node) -> None:
        """
        Visit method for NotEqualNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPNE instruction.

        :param node: NotEqualNode instance representing a not-equal comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPNE instruction
        self._emit("CMPNE")


    def visit_GreaterThanNode(self, node) -> None:
        """
        Visit method for GreaterThanNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPGT instruction.

        :param node: GreaterThanNode instance representing a greater-than comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPGT instruction
        self._emit("CMPGT")

    def visit_LessThanNode(self, node) -> None:
        """
        Visit method for LessThanNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPLT instruction.

        :param node: LessThanNode instance representing a less-than comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPLT instruction
        self._emit("CMPLT")


    def visit_GreaterThanEqualNode(self, node) -> None:
        """
        Visit method for GreaterThanEqualNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPGE instruction.

        :param node: GreaterThanEqualNode instance representing a greater-than-or-equal comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPGE instruction
        self._emit("CMPGE")


    def visit_LessThanEqualNode(self, node) -> None:
        """
        Visit method for LessThanEqualNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the CMPLE instruction.

        :param node: LessThanEqualNode instance representing a less-than-or-equal comparison.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the CMPLE instruction
        self._emit("CMPLE")


    def visit_AndNode(self, node) -> None:
        """
        Visit method for AndNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_AND instruction.

        :param node: AndNode instance representing a logical AND operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_AND instruction
        self._emit("BINARY_AND")

    def visit_OrNode(self, node) -> None:
        """
        Visit method for OrNode in the abstract syntax tree.

        This method visits the left and right nodes, then emits the BINARY_OR instruction.

        :param node: OrNode instance representing a logical OR operation.
        :return: None
        """
        # Visit the left and right nodes
        self.visit(node.left)
        self.visit(node.right)
        # Emit the BINARY_OR instruction
        self._emit("BINARY_OR")

    def visit_ConditionalNode(self, node, startLabl: str = None, endLabl: str = None) -> None:
        """
        Visit method for ConditionalNode in the abstract syntax tree.

        This method visits the condition node, emits a conditional jump instruction (POP_JMP_IF_FALSE),
        and handles special cases like ContinueNode, BreakNode, and BlockNode with optional startLabl and endLabl.

        :param node: ConditionalNode instance representing a conditional statement.
        :param startLabl: Optional label for the start of the block (used in ContinueNode and BlockNode).
        :param endLabl: Optional label for the end of the block (used in BreakNode and BlockNode).
        :return: None
        """
        # Generate a unique label for the next block
        nextLabel: str = self._generateLabel()

        # Visit the condition node and get the result
        conditionResult = self.visit(node.condition)

        # If the condition is falsy, emit a conditional jump instruction
        if not conditionResult:
            self._emit(f"POP_JMP_IF_FALSE {nextLabel}")

        # Handle special cases for ContinueNode, BreakNode, and BlockNode
        if type(node.statement).__name__ == "ContinueNode":
            # Ensure that startLabl is provided for ContinueNode
            assert startLabl is not None
            # Emit a jump to the start label
            self._emit(f"GOTO {startLabl}")
        elif type(node.statement).__name__ == "BreakNode":
            # Ensure that endLabl is provided for BreakNode
            assert endLabl is not None
            # Emit a jump to the end label
            self._emit(f"GOTO {endLabl}")
        elif type(node.statement).__name__ == "BlockNode":
            # Visit the BlockNode with optional startLabl and endLabl
            self.visit_BlockNode(node.statement, startLabl, endLabl)
        else:
            # Visit other types of statements
            self.visit(node.statement)

        # If the condition is truthy, return the result, otherwise return the next label
        return conditionResult if conditionResult else nextLabel


    def visit_IfNode(self, node, startLabl: str = None, endLabl: str = None) -> None:
        """
        Visit method for IfNode in the abstract syntax tree.

        This method processes an if statement, including any elsif and else blocks.
        It generates labels for the end of the if statement and skips to the appropriate block based on the condition.

        :param node: IfNode instance representing the if statement.
        :param startLabl: Optional label for the start of the block (used in ContinueNode and BlockNode).
        :param endLabl: Optional label for the end of the block (used in BreakNode and BlockNode).
        :return: None
        """
        # Generate a unique label for the end of the if statement
        endifLabel: str = self._generateLabel()

        # Visit the if block and get the label to skip if the condition is falsy
        skipIfLabel: str = self.visit_ConditionalNode(node.ifBlock, startLabl, endLabl)

        # Emit a jump to the endif label and the label to skip the if block
        self._emit(f"GOTO {endifLabel}")
        self._emit(f".{skipIfLabel}")

        # Visit each elsif block and emit jumps to the endif label and labels to skip the elsif blocks
        for elsifBlock in node.elsifBlocks:
            skipElsifLabel: str = self.visit_ConditionalNode(elsifBlock, startLabl, endLabl)
            self._emit(f"GOTO {endifLabel}")
            self._emit(f".{skipElsifLabel}")

        # Visit the else block if present
        if node.elseBlock:
            # Handle special cases for ContinueNode, BreakNode, and BlockNode in the else block
            if type(node.elseBlock).__name__ == "ContinueNode":
                assert startLabl is not None
                self._emit(f"GOTO {startLabl}")
            elif type(node.elseBlock).__name__ == "BreakNode":
                assert endLabl is not None
                self._emit(f"GOTO {endLabl}")
            elif type(node.elseBlock).__name__ == "BlockNode":
                # Visit the BlockNode with optional startLabl and endLabl
                self.visit_BlockNode(node.elseBlock, startLabl, endLabl)
            else:
                # Visit other types of statements in the else block
                self.visit(node.elseBlock)

        # Emit the label for the end of the if statement
        self._emit(f".{endifLabel}")


    def visit_WhileNode(self, node) -> None:
        """
        Visit method for WhileNode in the abstract syntax tree.

        This method processes a while loop, generating labels for the loop and its end.
        It emits instructions for the loop condition, jump instructions, and visits the loop body.

        :param node: WhileNode instance representing the while loop.
        :return: None
        """
        # Generate unique labels for the while loop and its end
        loopLabel: str = self._generateLabel()
        endLoopLabel: str = self._generateLabel()

        # Emit the label for the start of the while loop
        self._emit(f".{loopLabel}")

        # Visit the condition node and emit a conditional jump instruction
        self.visit(node.condition)
        self._emit(f"POP_JMP_IF_FALSE {endLoopLabel}")

        # Visit the loop body, handling special cases for BlockNode and IfNode
        if type(node.statement).__name__ in ["BlockNode", "IfNode"]:
            self.visit_BlockNode(node.statement, loopLabel, endLoopLabel)
        else:
            self.visit(node.statement)

        # Emit a jump back to the start of the while loop
        self._emit(f"GOTO {loopLabel}")

        # Emit the label for the end of the while loop
        self._emit(f".{endLoopLabel}")

    def visit_ReturnNode(self, node) -> None:
        """
        Visit method for ReturnNode in the abstract syntax tree.

        This method visits the expression node within a return statement and emits the RETURN_VALUE instruction.

        :param node: ReturnNode instance representing a return statement.
        :return: None
        """
        # Visit the expression node within the return statement
        self.visit(node.expr)
        # Emit the RETURN_VALUE instruction
        self._emit("RETURN_VALUE")


    def visit_FunDeclNode(self, node) -> None:
        """
        Visit method for FunDeclNode in the abstract syntax tree.

        This method processes a function declaration, updating the current function,
        initializing the function signature, visiting parameter nodes, and visiting the block node.

        :param node: FunDeclNode instance representing a function declaration.
        :return: None
        """
        # Save the current function name and update it with the new function name
        oldFn: str = self._currentFn
        self._currentFn = node.id.token.value

        # Initialize the function signature in the functions dictionary
        self._functions[self._currentFn] = f"fn {self._currentFn}\nargc {len(node.paramList)}\n"

        # Visit parameter nodes and emit STORE_LOCAL instructions
        for param in node.paramList:
            self._emit(f"STORE_LOCAL {param.value}")

        # Visit the block node of the function
        self.visit(node.blockNode)

        # If there is no explicit return statement in the function, emit a default RETURN_VALUE instruction
        if "RETURN_VALUE" not in self._functions[self._currentFn]:
            self._emit("LOAD_NIL")
            self._emit("RETURN_VALUE")

        # Restore the original current function name
        self._currentFn = oldFn

    def visit_FunctionCallNode(self, node) -> None:
        """
        Visit method for FunctionCallNode in the abstract syntax tree.

        This method processes a function call, visiting argument nodes, and emitting instructions
        to call either a native function (if it is a built-in function) or a user-defined function.

        :param node: FunctionCallNode instance representing a function call.
        :return: None
        """
        # Visit argument nodes in the function call
        for arg in node.argList:
            self.visit(arg)

        # Check if the function is a built-in function
        if str(node.nameNode) in builtinFunctionInfo:
            # Emit CALL_NATIVE instruction for built-in functions
            self._emit(f"CALL_NATIVE {builtinFunctionInfo[node.nameNode.token.value][0]}")
            return

        # Emit CALL_FUNCTION instruction for user-defined functions
        self._emit(f"CALL_FUNCTION {node.nameNode.token.value}")
