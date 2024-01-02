from ..nodevisitor import NodeVisitor
from ..parser import abstractSyntaxTree

class VisualizeAST(NodeVisitor):
    """
    VisualizeAST class for generating a textual representation of an abstract syntax tree (AST).

    This class inherits from NodeVisitor and provides methods to emit code for visualization purposes.

    Attributes:
        _pre (str): Prefix for indentation in the generated code.
        _outputCode (str): Accumulated code representing the AST.
        _ctr (int): Counter for generating unique numbers in the AST.

    Methods:
        __init__: Constructor method initializing attributes.
        _emit: Helper method to append code to the output.
        _genUniqueNumber: Helper method to generate unique numbers for nodes in the AST.
    """
    def __init__(self) -> None:
        """
        Constructor method for VisualizeAST.

        Initializes attributes for code generation and unique number tracking.
        """
        self._pre = ''
        self._outputCode = ''
        self._ctr = 0

    def _emit(self, s: str) -> None:
        """
        Helper method to append code to the output.

        :param s: Code to be appended.
        :return: None
        """
        self._outputCode += s + '\n'

    def _genUniqueNumber(self) -> int:
        """
        Helper method to generate unique numbers for nodes in the AST.

        :return: Unique number.
        """
        self._ctr += 1
        return self._ctr    

    def getDot(self) -> str:
        """
        Generate a DOT language representation for visualization of the abstract syntax tree (AST).

        This method constructs DOT language code with specific formatting for nodes and edges in the AST.

        :return: DOT language code representing the AST.
        """
        conf = "digraph G{\n"  # Initialize DOT language configuration with graph properties
        conf += "nodesep=1.0\n"  # Set the node separation
        conf += "node [color=Red,fontname=Courier,shape=circle]\n"  # Set node properties
        conf += "edge [color=Blue]\n"  # Set edge properties
        return conf + self._pre + '\n' + self._outputCode + '}'  # Combine configuration, prefix, and AST code


    def visit_ProgramNode(self, node: abstractSyntaxTree.ProgramNode) -> None:
        """
        Visit method for ProgramNode in the abstract syntax tree.

        This method generates DOT language code for the ProgramNode and its declarations.

        :param node: ProgramNode instance representing the program.
        :return: None
        """
        for s in node.declarationList:
            self._emit(f"ProgramNode -> {self.visit(s)}")  # Emit edge from ProgramNode to each declaration


    def visit_BlockNode(self, node: abstractSyntaxTree.BlockNode) -> None:
        """
        Visit method for BlockNode in the abstract syntax tree.

        This method generates DOT language code for the BlockNode and its statements.

        :param node: BlockNode instance representing a block of statements.
        :return: Unique label representing the BlockNode.
        """
        l: str = f'block{self._genUniqueNumber()}'  # Generate a unique label for the BlockNode
        self._pre += f'{l} [label="block"];\n'  # Add node properties to the prefix
        for s in node.stmtList:
            self._emit(f"{l} -> {self.visit(s)}")  # Emit edge from BlockNode to each statement
        return l

    def visit_FalseNode(self, node) -> str:
        """
        Visit method for FalseNode in the abstract syntax tree.

        This method generates a DOT language code for a FalseNode and returns a unique label.

        :param node: FalseNode instance representing the 'false' value.
        :return: Unique label representing the FalseNode.
        """
        return self._visitPrimary(node, "false", "false")


    def visit_NilNode(self, node) -> str:
        """
        Visit method for NilNode in the abstract syntax tree.

        This method generates a DOT language code for a NilNode and returns a unique label.

        :param node: NilNode instance representing the 'nil' value.
        :return: Unique label representing the NilNode.
        """
        return self._visitPrimary(node, "nil", "nil")


    def visit_StringNode(self, node) -> str:
        """
        Visit method for StringNode in the abstract syntax tree.

        This method generates a DOT language code for a StringNode and returns a unique label.

        :param node: StringNode instance representing a string literal.
        :return: Unique label representing the StringNode.
        """
        return self._visitPrimary(node, "str", str(node))


    def visit_IdentifierNode(self, node) -> str:
        """
        Visit method for IdentifierNode in the abstract syntax tree.

        This method generates a DOT language code for an IdentifierNode and returns a unique label.

        :param node: IdentifierNode instance representing an identifier.
        :return: Unique label representing the IdentifierNode.
        """
        return self._visitPrimary(node, "id", str(node))


    def visit_ArrayNode(self, node) -> str:
        """
        Visit method for ArrayNode in the abstract syntax tree.

        This method generates a DOT language code for an ArrayNode and returns a unique label.

        :param node: ArrayNode instance representing an array.
        :return: Unique label representing the ArrayNode.
        """
        l: str = f'arr{self._genUniqueNumber()}'
        self._pre += f'{l} [label="array"];\n'

        for e in node.elements:
            self._emit(f'{l} -> {self.visit(e)}')

        return l


    def visit_ArrayAccessNode(self, node) -> str:
        """
        Visit method for ArrayAccessNode in the abstract syntax tree.

        This method generates a DOT language code for an ArrayAccessNode and returns a unique label.

        :param node: ArrayAccessNode instance representing an array access.
        :return: Unique label representing the ArrayAccessNode.
        """
        return f'{self.visit(node.base)} -> {self.visit(node.index)}'


    def _visitBinOpNode(self, node, name: str) -> str:
        """
        Helper method for visiting binary operation nodes in the abstract syntax tree.

        This method generates a DOT language code for a binary operation node and returns a unique label.

        :param node: Binary operation node.
        :param name: Name representing the binary operation.
        :return: Unique label representing the binary operation node.
        """
        l: str = f'"{name}{self._genUniqueNumber()}"'
        self._pre += f'{l} [label="{name}"];\n'
        return f'{l} -> {self.visit(node.left)}\n{l} -> {self.visit(node.right)}'


    def visit_IdentifierNode(self, node) -> str:
        """
        Visit method for IdentifierNode in the abstract syntax tree.

        This method generates a DOT language code for an IdentifierNode and returns a unique label.

        :param node: IdentifierNode instance representing an identifier.
        :return: Unique label representing the IdentifierNode.
        """
        return self._visitPrimary(node, "id", str(node))


    def visit_ArrayNode(self, node) -> str:
        """
        Visit method for ArrayNode in the abstract syntax tree.

        This method generates a DOT language code for an ArrayNode and returns a unique label.

        :param node: ArrayNode instance representing an array.
        :return: Unique label representing the ArrayNode.
        """
        l: str = f'arr{self._genUniqueNumber()}'
        self._pre += f'{l} [label="array"];\n'

        for e in node.elements:
            self._emit(f'{l} -> {self.visit(e)}')

        return l


    def visit_ArrayAccessNode(self, node) -> str:
        """
        Visit method for ArrayAccessNode in the abstract syntax tree.

        This method generates a DOT language code for an ArrayAccessNode and returns a unique label.

        :param node: ArrayAccessNode instance representing an array access.
        :return: Unique label representing the ArrayAccessNode.
        """
        return f'{self.visit(node.base)} -> {self.visit(node.index)}'


    def _visitBinOpNode(self, node, name: str) -> str:
        """
        Helper method for visiting binary operation nodes in the abstract syntax tree.

        This method generates a DOT language code for a binary operation node and returns a unique label.

        :param node: Binary operation node.
        :param name: Name representing the binary operation.
        :return: Unique label representing the binary operation node.
        """
        l: str = f'"{name}{self._genUniqueNumber()}"'
        self._pre += f'{l} [label="{name}"];\n'
        return f'{l} -> {self.visit(node.left)}\n{l} -> {self.visit(node.right)}'

    def visit_ModNode(self, node) -> str:
        """
        Visit method for ModNode in the abstract syntax tree.

        This method generates a DOT language code for a ModNode and returns a unique label.

        :param node: ModNode instance representing a modulo operation.
        :return: Unique label representing the ModNode.
        """
        return self._visitBinOpNode(node, "%")


    def visit_EqualNode(self, node) -> str:
        """
        Visit method for EqualNode in the abstract syntax tree.

        This method generates a DOT language code for an EqualNode and returns a unique label.

        :param node: EqualNode instance representing an equality comparison.
        :return: Unique label representing the EqualNode.
        """
        return self._visitBinOpNode(node, "==")


    def visit_NotEqualNode(self, node) -> str:
        """
        Visit method for NotEqualNode in the abstract syntax tree.

        This method generates a DOT language code for a NotEqualNode and returns a unique label.

        :param node: NotEqualNode instance representing a non-equality comparison.
        :return: Unique label representing the NotEqualNode.
        """
        return self._visitBinOpNode(node, "!=")


    def visit_GreaterThanNode(self, node) -> str:
        """
        Visit method for GreaterThanNode in the abstract syntax tree.

        This method generates a DOT language code for a GreaterThanNode and returns a unique label.

        :param node: GreaterThanNode instance representing a greater than comparison.
        :return: Unique label representing the GreaterThanNode.
        """
        return self._visitBinOpNode(node, ">")


    def visit_LessThanNode(self, node) -> str:
        """
        Visit method for LessThanNode in the abstract syntax tree.

        This method generates a DOT language code for a LessThanNode and returns a unique label.

        :param node: LessThanNode instance representing a less than comparison.
        :return: Unique label representing the LessThanNode.
        """
        return self._visitBinOpNode(node, "<")

    def visit_GreaterThanEqualNode(self, node) -> str:
        """
        Visit method for GreaterThanEqualNode in the abstract syntax tree.

        This method generates a DOT language code for a GreaterThanEqualNode and returns a unique label.

        :param node: GreaterThanEqualNode instance representing a greater than or equal to comparison.
        :return: Unique label representing the GreaterThanEqualNode.
        """
        return self._visitBinOpNode(node, ">=")


    def visit_LessThanEqualNode(self, node) -> str:
        """
        Visit method for LessThanEqualNode in the abstract syntax tree.

        This method generates a DOT language code for a LessThanEqualNode and returns a unique label.

        :param node: LessThanEqualNode instance representing a less than or equal to comparison.
        :return: Unique label representing the LessThanEqualNode.
        """
        return self._visitBinOpNode(node, "<=")


    def visit_AndNode(self, node) -> str:
        """
        Visit method for AndNode in the abstract syntax tree.

        This method generates a DOT language code for an AndNode and returns a unique label.

        :param node: AndNode instance representing a logical AND operation.
        :return: Unique label representing the AndNode.
        """
        return self._visitBinOpNode(node, "and")


    def visit_OrNode(self, node) -> str:
        """
        Visit method for OrNode in the abstract syntax tree.

        This method generates a DOT language code for an OrNode and returns a unique label.

        :param node: OrNode instance representing a logical OR operation.
        :return: Unique label representing the OrNode.
        """
        return self._visitBinOpNode(node, "or")


    def visit_VarDeclNode(self, node: abstractSyntaxTree.VarDeclNode) -> str:
        """
        Visit method for VarDeclNode in the abstract syntax tree.

        This method generates a DOT language code for a VarDeclNode and returns a unique label.

        :param node: VarDeclNode instance representing a variable declaration.
        :return: Unique label representing the VarDeclNode.
        """
        # Create a unique label for the VarDeclNode
        labl: str = f"vardec{self._genUniqueNumber()}"
        # Add a DOT language code for the VarDeclNode to the _pre attribute
        self._pre += f'{labl} [label="VarDecl"];\n'
        # Return DOT language code connecting VarDeclNode components
        return f'{labl} -> {self.visit(node.id)}\n{labl} -> {self.visit(node.exprNode)}'


    def visit_AssignNode(self, node: abstractSyntaxTree.VarDeclNode) -> str:
        """
        Visit method for AssignNode in the abstract syntax tree.

        This method generates a DOT language code for an AssignNode and returns a unique label.

        :param node: AssignNode instance representing an assignment.
        :return: Unique label representing the AssignNode.
        """
        # Create a unique label for the AssignNode
        labl: str = f"assign{self._genUniqueNumber()}"
        # Add a DOT language code for the AssignNode to the _pre attribute
        self._pre += f'{labl} [label="Assign"];\n'
        # Return DOT language code connecting AssignNode components
        return f'{labl} -> {self.visit(node.lvalue)}\n{labl} -> {self.visit(node.exprNode)}'


    def visit_FunDeclNode(self, node: abstractSyntaxTree.FunDeclNode) -> str:
        """
        Visit method for FunDeclNode in the abstract syntax tree.

        This method generates a DOT language code for a FunDeclNode and returns a unique label.

        :param node: FunDeclNode instance representing a function declaration.
        :return: Unique label representing the FunDeclNode.
        """
        # Create a unique label for the FunDeclNode
        fnName: str = f'Function{self._genUniqueNumber()}'
        # Add a DOT language code for the FunDeclNode to the _pre attribute
        self._pre += f'{fnName} [label="Function {str(node.id)}"];\n'
        # Add DOT language code connecting FunDeclNode components
        for s in node.blockNode.stmtList:
            self._emit(f'"{fnName}" -> {self.visit(s)}')
        # Return the unique label for the FunDeclNode
        return f'{fnName}'

    def visit_FunctionCallNode(self, node: abstractSyntaxTree.FunctionCallNode) -> str:
        """
        Visit method for FunctionCallNode in the abstract syntax tree.

        This method generates a DOT language code for a FunctionCallNode and returns a unique label.

        :param node: FunctionCallNode instance representing a function call.
        :return: Unique label representing the FunctionCallNode.
        """
        # Create a unique label for the FunctionCallNode
        callN: str = f'call{self._genUniqueNumber()}'
        # Add a DOT language code for the FunctionCallNode to the _pre attribute
        self._pre += f'{callN} [label="call"];\n'
        # Generate DOT language code connecting FunctionCallNode components
        output = f'{callN} -> {self.visit(node.nameNode)} -> '
        for a in node.argList:
            output += self.visit(a) + ','
        output = output[:-1]
        # Return the generated DOT language code
        return output


    def visit_ReturnNode(self, node: abstractSyntaxTree.ReturnNode) -> str:
        """
        Visit method for ReturnNode in the abstract syntax tree.

        This method generates a DOT language code for a ReturnNode and returns a unique label.

        :param node: ReturnNode instance representing a return statement.
        :return: Unique label representing the ReturnNode.
        """
        # Create a unique label for the ReturnNode
        labl: str = f'return{self._genUniqueNumber()}'
        # Add a DOT language code for the ReturnNode to the _pre attribute
        self._pre += f'{labl} [label="return"];\n'
        # Return DOT language code connecting ReturnNode components
        return f'{labl} -> {self.visit(node.expr)}'


    def visit_ContinueNode(self, node: abstractSyntaxTree.ContinueNode) -> str:
        """
        Visit method for ContinueNode in the abstract syntax tree.

        This method generates a DOT language code for a ContinueNode and returns a unique label.

        :param node: ContinueNode instance representing a continue statement.
        :return: Unique label representing the ContinueNode.
        """
        # Create a unique label for the ContinueNode
        labl: str = f'continue{self._genUniqueNumber()}'
        # Add a DOT language code for the ContinueNode to the _pre attribute
        self._pre += f'{labl} [label="continue"];\n'
        # Return the unique label for the ContinueNode
        return labl

    def visit_BreakNode(self, node: abstractSyntaxTree.BreakNode) -> str:
        """
        Visit method for BreakNode in the abstract syntax tree.

        This method generates a DOT language code for a BreakNode and returns a unique label.

        :param node: BreakNode instance representing a break statement.
        :return: Unique label representing the BreakNode.
        """
        # Create a unique label for the BreakNode
        labl: str = f'br{self._genUniqueNumber()}'
        # Add a DOT language code for the BreakNode to the _pre attribute
        self._pre += f'{labl} [label="break"];\n'
        # Return the unique label for the BreakNode
        return labl

    def visit_IfNode(self, node: abstractSyntaxTree.IfNode) -> str:
        """
        Visit method for IfNode in the abstract syntax tree.

        This method generates a DOT language code for an IfNode and returns a unique label.

        :param node: IfNode instance representing an if statement.
        :return: Unique label representing the IfNode.
        """
        # Create a unique label for the IfNode
        lif: str = f'if{self._genUniqueNumber()}'
        # Add a DOT language code for the IfNode to the _pre attribute
        self._pre += f'{lif} [label="if"];\n'

        # Create a unique label for the condition block
        lcond: str = f'cond{self._genUniqueNumber()}'
        # Add a DOT language code for the condition block to the _pre attribute
        self._pre += f'{lcond} [label="condition"];\n'

        # Generate DOT language code connecting IfNode components for the condition
        output = f'{lif}->{lcond}->{self.visit(node.ifBlock.condition)}\n'
        # Generate DOT language code connecting IfNode components for the statement
        self._emit(f'{lif}->{self.visit(node.ifBlock.statement)}')

        # Iterate over each elsif block in the IfNode
        for e in node.elsifBlocks:
            # Create a unique label for the elsif block
            lelif: str = f'elif{self._genUniqueNumber()}'
            # Add a DOT language code for the elsif block to the _pre attribute
            self._pre += f'{lelif} [label="elsif"];\n'

            # Create a unique label for the elsif condition block
            lcond: str = f'cond{self._genUniqueNumber()}'
            # Add a DOT language code for the elsif condition block to the _pre attribute
            self._pre += f'{lcond} [label="condition"];\n'

            # Generate DOT language code connecting elsif components for the condition
            output += f'{lelif}->{lcond}->{self.visit(e.condition)}\n'
            # Generate DOT language code connecting elsif components for the statement
            self._emit(f'{lif}->{lelif}->{self.visit(e.statement)}')

        # Check for the presence of an else block in the IfNode
        if node.elseBlock:
            # Create a unique label for the else block
            lelse: str = f'else{self._genUniqueNumber()}'
            # Add a DOT language code for the else block to the _pre attribute
            self._pre += f'{lelse} [label="else"];\n'

            # Generate DOT language code connecting IfNode components for the else block
            self._emit(f'{lif}->{lelse}->{self.visit(node.elseBlock)}')

        # Return the generated DOT language code
        return output

    def visit_ConditionalNode(self, node: abstractSyntaxTree.IfNode) -> str:
        """
        Visit method for ConditionalNode in the abstract syntax tree.

        This method generates a DOT language code for a ConditionalNode and returns a unique label.

        :param node: IfNode instance representing a conditional statement.
        :return: Unique label representing the ConditionalNode.
        """
        # Create a unique label for the condition block
        lcond: str = f'cond{self._genUniqueNumber()}'
        # Add a DOT language code for the condition block to the _pre attribute
        self._pre += f'{lcond} [label="condition"];\n'

        # Return the unique label for the condition block
        return lcond


    def visit_WhileNode(self, node: abstractSyntaxTree.IfNode) -> str:
        """
        Visit method for WhileNode in the abstract syntax tree.

        This method generates a DOT language code for a WhileNode and returns a unique label.

        :param node: IfNode instance representing a while loop.
        :return: Unique label representing the WhileNode.
        """
        # Create a unique label for the while loop
        lwhile: str = f'while{self._genUniqueNumber()}'
        # Add a DOT language code for the while loop to the _pre attribute
        self._pre += f'{lwhile} [label="while"];\n'

        # Create a unique label for the condition block
        lcond: str = f'cond{self._genUniqueNumber()}'
        # Add a DOT language code for the condition block to the _pre attribute
        self._pre += f'{lcond} [label="condition"];\n'

        # Generate DOT language code connecting WhileNode components for the condition
        output = f'{lwhile}->{lcond}->{self.visit(node.condition)}\n'
        # Generate DOT language code connecting WhileNode components for the statement
        self._emit(f'{lwhile}->{self.visit(node.statement)}')

        # Return the generated DOT language code
        return output