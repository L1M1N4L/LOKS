# Import statement for relative package, assuming directory structure is correctly set up
from ..lexerOrScanner.token import Token
from typing import List, Union

# Base class for all nodes in the abstract syntax tree (AST)
class ASTNode:
    def __repr__(self) -> str:
        # Create a string representation of the object for debugging purposes
        return f"{self.__class__.__name__}()"

# Class representing the top-level structure of the AST
class ProgramNode(ASTNode):
    def __init__(self, declList: List[ASTNode]) -> None:
        # Constructor for ProgramNode, initializing with a list of declaration nodes
        self.declarationList: List[ASTNode] = declList

    def __str__(self) -> str:
        # Create a string representation of the ProgramNode
        return "\n".join(map(str, self.declarationList))
    
class BlockNode(ASTNode):
    def __init__(self, stmtlist: List[ASTNode]) -> None:
        # Constructor for BlockNode, initializing with a list of statement nodes
        self.stmtList: List[ASTNode] = stmtlist

    def __str__(self) -> str:
        # Create a string representation of the BlockNode
        output: str = '{\n'
        for s in self.stmtList:
            output += str(s) + '\n'
        output += '}'
        return output
    
# Declaration Nodes

class VarDeclNode(ASTNode):
    def __init__(self, id: Token, exprNode: ASTNode=None) -> None:
        # Constructor for VarDeclNode, initializing with an identifier token and an optional expression node
        self.id: IdentifierNode = id
        self.exprNode: ASTNode = exprNode

    def __str__(self) -> str:
        # Create a string representation of the VarDeclNode
        return f"vardecl: {str(self.id)} = {str(self.exprNode)}"

class FunDeclNode(ASTNode):
    def __init(self, id: Token, pList: List[Token], blk: BlockNode) -> None:
        # Constructor for FunDeclNode, initializing with an identifier token, a list of parameter tokens, and a BlockNode
        self.id: IdentifierNode = id
        self.paramList: List[Token] = pList
        self.blockNode: BlockNode = blk

    def __str__(self) -> str:
        # Create a string representation of the FunDeclNode
        output = f"func {self.id}("
        for p in self.paramList:
            output += str(p.value) + ','
        output += ')' + str(self.blockNode)
        return output

# Statement Nodes

class AssignNode(ASTNode):
    def __init__(self, id: Token, exprNode: ASTNode) -> None:
        # Constructor for AssignNode, initializing with an lvalue (either IdentifierNode or ArrayAccessNode) and an expression node
        self.lvalue: Union[IdentifierNode, ArrayAccessNode] = id
        self.exprNode: ASTNode = exprNode

    def __str__(self) -> str:
        # Create a string representation of the AssignNode
        return f"assign: {str(self.lvalue)} = {str(self.exprNode)}"

class ConditionalNode(ASTNode):
    def __init__(self, cond: ASTNode, stmt: ASTNode) -> None:
        # Constructor for ConditionalNode, initializing with a condition node and a statement node
        self.condition: ASTNode =  cond
        self.statement: ASTNode = stmt

    def __str__(self) -> str:
        # Create a string representation of the ConditionalNode
        return f"{str(self.condition)} {str(self.statement)}"

class IfNode(ASTNode):
    def __init__(self, ifBlock: ConditionalNode, elsifBlocks: List[ConditionalNode], elseBlock: ASTNode) -> None:
        # Constructor for IfNode, initializing with an if block, a list of elsif blocks, and an else block
        self.ifBlock: ConditionalNode = ifBlock
        self.elsifBlocks: List[ConditionalNode] = elsifBlocks
        self.elseBlock: ASTNode = elseBlock

    def __str__(self) -> str:
        # Create a string representation of the IfNode
        output = f"if{str(self.ifBlock)}\n"
        for e in self.elsifBlocks:
            output += "elsif" + str(e) + '\n'
        output += f"else {str(self.elseBlock)}"
        return output
    
class ReturnNode(ASTNode):
    def __init__(self, exprNode: ASTNode, l: int) -> None:
        # Constructor for ReturnNode, initializing with an expression node and a line number
        self.expr: ASTNode = exprNode
        self.line: int = l

    def __str__(self) -> str:
        # Create a string representation of the ReturnNode
        return f"return: {str(self.expr)}"

class ContinueNode(ASTNode):
    def __init__(self, t: Token) -> None:
        # Constructor for ContinueNode, initializing with a token
        self.tok = t

    def __str__(self) -> str:
        # Create a string representation for the 'continue' statement
        return "continue"

class BreakNode(ASTNode):
    def __init__(self, t: Token) -> None:
        # Constructor for BreakNode, initializing with a token
        self.tok = t

    def __str__(self) -> str:
        # Create a string representation for the 'break' statement
        return "break"

class WhileNode(ConditionalNode):
    def __init__(self, cond: ASTNode, stmt: ASTNode) -> None:
        # Constructor for WhileNode, initializing with a condition and statement
        super().__init__(cond, stmt)

    def __str__(self) -> str:
        # Create a string representation of the WhileNode
        return "while:" + super().__str__()

# Binary operation nodes
class BinOpNode(ASTNode):
    def __init__(self, op: str, l: ASTNode, r: ASTNode):
        # Constructor for BinOpNode, initializing with an operator, left, and right operands
        self.op: str = op
        self.left: ASTNode = l
        self.right: ASTNode = r

    def __str__(self):
        # Create a string representation of the binary operation
        return f"({str(self.left)} {self.op} {str(self.right)})"

class OrNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for OrNode, initializing with left and right operands and setting the operator to 'or'
        super().__init__('or', l, r)

class AndNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for AndNode, initializing with left and right operands and setting the operator to 'and'
        super().__init__('and', l, r)

class EqualNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for EqualNode, initializing with left and right operands and setting the operator to '=='
        super().__init('==', l, r)

class NotEqualNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for NotEqualNode, initializing with left and right operands and setting the operator to '!='
        super().__init('!=', l, r)

class GreaterThanNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for GreaterThanNode, initializing with left and right operands and setting the operator to '>'
        super().__init('>', l, r)

class GreaterThanEqualNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for GreaterThanEqualNode, initializing with left and right operands and setting the operator to '>='
        super().__init('>=', l, r)

class LessThanNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for LessThanNode, initializing with left and right operands and setting the operator to '<'
        super().__init('<', l, r)

class LessThanEqualNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for LessThanEqualNode, initializing with left and right operands and setting the operator to '<='
        super().__init('<=', l, r)

class AddNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for AddNode, initializing with left and right operands and setting the operator to '+'
        super().__init('+', l, r)

class SubNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for SubNode, initializing with left and right operands and setting the operator to '-'
        super().__init('-', l, r)

class MulNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for MulNode, initializing with left and right operands and setting the operator to '*'
        super().__init('*', l, r)

class DivNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for DivNode, initializing with left and right operands and setting the operator to '/'
        super().__init('/', l, r)

class ModNode(BinOpNode):
    def __init__(self, l: ASTNode, r: ASTNode):
        # Constructor for ModNode, initializing with left and right operands and setting the operator to '%'
        super().__init('%', l, r)

# unary operation nodes
class UnaryOpNode(ASTNode):
    def __init__(self, op: str, n: ASTNode) -> None:
        # Constructor for UnaryOpNode, initializing with an operator and an operand
        self.op: str = op
        self.node: ASTNode = n

    def __str__(self):
        # Create a string representation of the unary operation
        return f"({self.op} {str(self.node)})"

class NotNode(UnaryOpNode):
    def __init__(self, n: ASTNode) -> None:
        # Constructor for NotNode, initializing with an operand and setting the operator to '!'
        super().__init('!', n)

class NegationNode(UnaryOpNode):
    def __init__(self, n: ASTNode) -> None:
        # Constructor for NegationNode, initializing with an operand and setting the operator to '-'
        super().__init('-', n)

# function call
class FunctionCallNode(ASTNode):
    def __init__(self, name: ASTNode, arg: List[ASTNode]) -> None:
        # Constructor for FunctionCallNode, initializing with the function name node and a list of argument nodes
        self.nameNode: ASTNode = name
        self.argList: List[ASTNode] = arg

    def __str__(self) -> str:
        # Create a string representation of the function call
        output = f"call: {str(self.nameNode)} "
        for a in self.argList:
            output += str(a) + ' '
        return output
# Primary nodes

class PrimaryNode(ASTNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for PrimaryNode, initializing with a token.
        self.token: Token = tok

    def __str__(self) -> str:
        # Create a string representation of the primary node, which is the value of the token.
        return f"{self.token.value}"

class TrueNode(PrimaryNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for TrueNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        TrueNode represents the 'true' boolean value in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode. 
        '''

class FalseNode(PrimaryNode):
    def __init(self, tok: Token) -> None:
        # Constructor for FalseNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        FalseNode represents the 'false' boolean value in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode.
        '''

class NilNode(PrimaryNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for NilNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        NilNode represents the 'nil' value in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode.
        '''

class NumberNode(PrimaryNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for NumberNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        NumberNode represents a numeric value in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode.
        '''
class StringNode(PrimaryNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for StringNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        StringNode represents a string value in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode.
        '''

class IdentifierNode(PrimaryNode):
    def __init__(self, tok: Token) -> None:
        # Constructor for IdentifierNode, inheriting from PrimaryNode and initializing with a token.
        super().__init__(tok)
        '''
        IdentifierNode represents an identifier (variable name) in the abstract syntax tree (AST). 
        It is a specific instance of a primary node and inherits the behavior of PrimaryNode.
        '''

class ArrayNode(ASTNode):
    def __init__(self, l: List[ASTNode]) -> None:
        # Constructor for ArrayNode, initializing with a list of elements.
        self.elements: List[ASTNode] = l

    def __str__(self) -> str:
        # Create a string representation of the array node.
        output = f"arr: ["
        for a in self.elements:
            output += str(a) + ', '
        output = output.strip()[:-1]
        output += ']'
        return output
        '''
        ArrayNode represents an array in the abstract syntax tree (AST). It contains a list of elements and provides a string representation of the array's contents.
        '''

class ArrayAccessNode(ASTNode):
    def __init__(self, b: ASTNode, idx: ASTNode) -> None:
        # Constructor for ArrayAccessNode, initializing with a base node and an index node.
        self.base: ASTNode = b
        self.index: ASTNode = idx

    def __str__(self) -> str:
        # Create a string representation of the array access node.
        return f"(aac: {str(self.base)}[{str(self.index)}])"
        '''
        ArrayAccessNode represents an array access operation in the abstract syntax tree (AST). It has a base node representing the array and an index node representing the accessed element's index. The string representation demonstrates the format of an array access operation.
        '''
