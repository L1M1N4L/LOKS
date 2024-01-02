# Importing the NodeVisitor class from the "..nodevisitor" module
from ..nodevisitor import NodeVisitor

# Importing the CallStack, ActivationRecord, and ARType classes, as well as
# LObject, Number, Nil, Array, Boolean, String, Function classes, and
# builtinFunctionTable from their respective modules
from .memory import CallStack, ActivationRecord, ARType
from ..types import LObject, Number, Nil, Array, Boolean, String, Function
from ..stdlib import builtinFunctionTable

# Importing TypeErr, ZeroDivErr, and SyntaxErr classes from the "..error" module
from ..error import TypeErr, ZeroDivErr, SyntaxErr

# Defining the Interpreter class that inherits from NodeVisitor
class Interpeter(NodeVisitor):

     # Constructor method for the Interpreter class
    def __init__(self) -> None:
         # Initializing the current frame and call stack
        self._curFrame: ActivationRecord = None
        self._callStack: CallStack = CallStack()

    # Method to get the type of a variable in the current frame
    def _getVarType(self, el: str) -> str:
        # Returning the name of the type of the variable in the current frame
        return type(self._curFrame[el]).__name__

    # Method to get the type of an LObject  
    def _getObjType(self, el: LObject) -> str:
        return type(el).__name__



    # Check if a LObject is truthy
    def _isTruthy(self, obj: LObject) -> bool:
        # Check if the LObject is of type Number
        if self._getObjType(obj) == "Number":
            # Check if the value of the Number is zero
            if obj.value == 0:
                return False
            # If the value is not zero, consider it truthy
            return True

        # Check if the LObject is of type String
        elif self._getObjType(obj) == "String":
            # Check if the length of the String is zero
            if len(obj.value) == 0:
                return False
             # If the length is not zero, consider it truthy
            return True
        
        # Check if the LObject is of type Nil
        elif self._getObjType(obj) == "Nil":
             # Nil is considered falsy
            return False

        # Check if the LObject is of type Boolean
        elif self._getObjType(obj) == "Boolean":
            # Check if the Boolean value is "false"
            if obj.value == "false":
                return False
            # If the value is not "false", consider it truthy
            return True

        # Check if the LObject is of type Array
        elif self._getObjType(obj) == "Array":
            # Check if the length of the Array is zero
            if obj.getLen() == 0:
                return False
            # If the length is not zero, consider it truthy
            return True

         # Check if the LObject is of type Function
        elif self._getObjType(obj) == "Function":
            # Functions are considered falsy
            return False
        
        # If the LObject is of any other type, consider it truthy
        return True
    

    #
    # Visit methods
    #

    def visit_ProgramNode(self, node) -> None:
        """  
        Visit method for ProgramNode in the abstract syntax tree.

        This method is responsible for executing the code within the ProgramNode.

        :param node: The ProgramNode to be visited.
        :return: None
        """
        # create and push main frame
        mainFarame = ActivationRecord(ARType.MAIN)
        self._callStack.push(mainFarame)
        self._curFrame = mainFarame

         # Execute the code by visiting each declaration in the ProgramNode
        for d in node.declarationList:
            self.visit(d)

         # Done executing the code, pop the main frame from the call stack
        self._callStack.pop()
            
    
    def visit_NumberNode(self, node) -> Number:
        # """
        # Visit method for NumberNode in the abstract syntax tree.

        # This method creates a Number object based on the value of the NumberNode's token.

        # :param node: The NumberNode to be visited.
        # :return: A Number object.
        # """
        return Number(node.token.value)


    def visit_NilNode(self, node) -> Nil:
        # """
        # Visit method for NilNode in the abstract syntax tree.

        # This method creates a Nil object.

        # :param node: The NilNode to be visited.
        # :return: A Nil object.
        # """
        return Nil()


    def visit_TrueNode(self, node) -> Boolean:
        # """
        # Visit method for TrueNode in the abstract syntax tree.

        # This method creates a Boolean object with the value "true".

        # """
        return Boolean("true")


    def visit_FalseNode(self, node) -> Boolean:
        # """
        # Visit method for FalseNode in the abstract syntax tree.

        # This method creates a Boolean object with the value "false".
        # """
        return Boolean("false")


    def visit_StringNode(self, node) -> String:
        # """
        # Visit method for StringNode in the abstract syntax tree.

        # This method creates a String object based on the value of the StringNode's token.

        # """
        return String(node.token.value)


    def visit_ArrayNode(self, node) -> Array:
        # """
        # Visit method for ArrayNode in the abstract syntax tree.

        # This method creates an Array object and populates it with elements by visiting each element node.

        # """
        # Create an empty Array
        arr: Array = Array()

         # Visit each element node and add it to the Array
        for e in node.elements:
            arr.addEl(self.visit(e))

        # Return the populated Array
        return arr


    def visit_ArrayAccessNode(self, node) -> LObject:
        # """
        # Visit method for ArrayAccessNode in the abstract syntax tree.

        # This method retrieves an element from an array based on the provided index.

        # """
        # Visit the base expression to obtain the array object
        arrObj = self.visit(node.base)

        # Check if the variable actually holds an array
        if type(arrObj).__name__ != "Array":
            raise TypeErr(f"Type '{type(arrObj).__name__}' is not subscriptable", node.base.token.line)

         # Visit the index expression to obtain the array index
        idx = self.visit(node.index) 

        # check if index is an integer
        if type(idx).__name__ != "Number":
            raise TypeErr(f"Array indices must be integers, not '{type(idx).__name__}'", node.base.token.line)

        # Check if the index is a float (disallowing float indices)
        if type(idx.value).__name__ == "float":
            raise TypeErr(f"Array indices must be integers, not float", node.base.token.line)

        # Everything is okay, return the accessed element from the arra
        return arrObj.getEL(idx.value)


    def visit_IdentifierNode(self, node) -> LObject:
        # """
        # Visit method for IdentifierNode in the abstract syntax tree.

        # This method retrieves the value associated with the identifier from the current frame.
        # """
        return self._curFrame.get(node.token.value)
    

    def visit_VarDeclNode(self, node) -> None:
        # """
        # Visit method for VarDeclNode in the abstract syntax tree.

        # This method assigns a value to a variable in the current frame.
        # """
        # Visit the expression node (if present) to obtain the value, otherwise set it to Nil
        val = self.visit(node.exprNode) if node.exprNode else Nil()

        # Assign the value to the variable in the current frame
        self._curFrame[node.id.token.value] = val


    def visit_AssignNode(self, node) -> None:
        # """
        # Visit method for AssignNode in the abstract syntax tree.

        # This method assigns a value to an lvalue (either an array element or an identifier).

        # """
        # Visit the expression node to obtain the value
        val = self.visit(node.exprNode)

         # Check if the lvalue is an ArrayAccessNode
        if type(node.lvalue).__name__ == "ArrayAccessNode":
            # Retrieve the array object from the current frame
            arrObj = self._curFrame[node.lvalue.base.token.value]
            # check if variable holds an array
            if type(arrObj).__name__ != "Array":
                raise TypeErr(f"Type '{type(arrObj).__name__}' is not subscriptable", node.lvalue.base.token.line)

            # Visit the index expression to obtain the array index
            idx = self.visit(node.lvalue.index)
            # check if index is an integer
            if type(idx).__name__ != "Number":
                raise TypeErr(f"Array indices must be integers, not '{type(idx).__name__}'", node.lvalue.base.token.line)

            # Check if the index is a float (disallowing float indices)
            if type(idx.value).__name__ == "float":
                raise TypeErr(f"Array indices must be integers, not float", node.base.token.line)
            
            # Set the value to the array element at the specified index
            arrObj.setEL(val, idx.value)

        # Check if the lvalue is an IdentifierNode
        elif type(node.lvalue).__name__ == "IdentifierNode":
             # Set the value to the variable in the current frame
            self._curFrame[node.lvalue.token.value] = val


    # Arithmetic nodes
    def visit_NegationNode(self, node) -> Number:
        # """
        # Visit method for NegationNode in the abstract syntax tree.

        # This method computes the negation of a numeric value.

        # :return: A Number object representing the negated value.
        # """
        # Visit the node to obtain the numeric value
        v = self.visit(node.node)

        # Check if the value is of type Number
        if self._getObjType(v) != "Number":
            raise TypeErr(f"Cannot negate {self._getObjType(v)}", node.node.token.line)

        # Return a Number object representing the negated value
        return Number(-v.value)


    def visit_AddNode(self, node) -> Number:
        # """
        # Visit method for AddNode in the abstract syntax tree.

        # This method computes the sum of two values.

        # :return: A Number object representing the sum of the left and right values, or
        #          a String object representing the concatenation of two strings.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # Concatenate strings if the left operand is a String
        if self._getObjType(l) == "String":
            if self._getObjType(r) != "String":
                raise TypeErr(f"Cannot add {self._getObjType(r)} to String", node.left.token.line)
            return String(l.value + r.value)

       # Perform numeric addition if the left operand is a Number
        elif self._getObjType(l) == "Number":
            # Check if the right operand is also a Number
            if self._getObjType(r) != "Number":
                raise TypeErr(f"Cannot add {self._getObjType(r)} to Number", node.left.token.line)
            return Number(l.value + r.value)
        
        # Raise an error if neither operand is a String or Number
        else:
            raise TypeErr(f"Addition not defined for type '{self._getObjType(l)}'", node.left.token.line)


    def visit_SubNode(self, node) -> Number:
        # """
        # Visit method for SubNode in the abstract syntax tree.

        # This method computes the subtraction of two numeric values.

        # :return: A Number object representing the result of the subtraction.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # check if both l and r are numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Cannot subtract {self._getObjType(r)} from {self._getObjType(l)}", node.left.token.line)

        # Perform numeric subtraction
        return Number(l.value - r.value)


    def visit_DivNode(self, node) -> Number:
        # """
        # Visit method for DivNode in the abstract syntax tree.

        # This method computes the division of two numeric values.

        # :return: A Number object representing the result of the division.
        # """
        l = self.visit(node.left)
        r = self.visit(node.right)

        # check if both l and r are numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Cannot divide {self._getObjType(l)} by {self._getObjType(r)}", node.left.token.line)

        # Check for division by zero
        if r.value == 0:
            raise ZeroDivErr(node.left.token.line)

        # Perform numeric division
        return Number(l.value / r.value)


    def visit_MulNode(self, node) -> Number:
        # """
        # Visit method for MulNode in the abstract syntax tree.

        # This method computes the multiplication of two numeric values.

        # :return: A Number object representing the result of the multiplication.
        # """
         # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        #  Check if both l and r are numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Cannot multiply {self._getObjType(l)} by {self._getObjType(r)}", node.left.token.line)

        # Perform numeric multiplication
        return Number(l.value * r.value)


    def visit_ModNode(self, node) -> Number:
        # """
        # Visit method for ModNode in the abstract syntax tree.

        # This method computes the modulo operation of two numeric values.

        # :return: A Number object representing the result of the modulo operation.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

       # Check if both l and r are numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for modulo: {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        # division by zero
        if r.value == 0:
            raise ZeroDivErr(node.left.token.line)

        return Number(l.value % r.value)


    # comparision nodes
    def visit_GreaterThanNode(self, node) -> Boolean:
        # """
        # Visit method for GreaterThanNode in the abstract syntax tree.

        # This method checks if the left operand is greater than the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # comparision only valid for numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for greater than operator: {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        # Perform the comparison and return a Boolean object
        if l.value > r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_GreaterThanEqualNode(self, node) -> Boolean:
        # """
        # Visit method for LessThanNode in the abstract syntax tree.

        # This method checks if the left operand is less than the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """
         # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # comparision only valid for numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for greater than equals operator: {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        # Perform the comparison and return a Boolean object
        if l.value >= r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_LessThanNode(self, node) -> Boolean:
        # """
        # Visit method for LessThanNode in the abstract syntax tree.

        # This method checks if the left operand is less than the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # comparision only valid for numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for less than operator: {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        if l.value < r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_LessThanEqualNode(self, node) -> Boolean: 
        # """
        # Visit method for LessThanEqualNode in the abstract syntax tree.

        # This method checks if the left operand is less than or equal to the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """
        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        # comparision only valid for numbers
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for less than equals operator: {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        if l.value <= r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_EqualNode(self, node) -> Boolean:
        # """
        # Visit method for EqualNode in the abstract syntax tree.

        # This method checks if the left operand is equal to the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """

        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        allowedTypes = [
            "Nil",
            "Number",
            "Boolean",
            "String",
        ]

        # Check if the types are allowed for comparison
        if self._getObjType(l) not in allowedTypes or self._getObjType(r) not in allowedTypes:
            raise TypeErr(f"Cannot compare {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        # Perform the comparison and return a Boolean object
        if l.value == r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_NotEqualNode(self, node) -> Boolean:
        # """
        # Visit method for NotEqualNode in the abstract syntax tree.

        # This method checks if the left operand is not equal to the right operand.

        # :return: A Boolean object representing the result of the comparison.
        # """

        # Visit the left and right nodes to obtain their values
        l = self.visit(node.left)
        r = self.visit(node.right)

        allowedTypes = [
            "Nil",
            "Number",
            "Boolean",
            "String",
        ]

        # Check if the types are allowed for comparison
        if self._getObjType(l) not in allowedTypes or self._getObjType(r) not in allowedTypes:
            raise TypeErr(f"Cannot compare {self._getObjType(l)} and {self._getObjType(r)}", node.left.token.line)

        # Perform the comparison and return a Boolean object
        if l.value != r.value:
            return Boolean("true")

        return Boolean("false")


    def visit_NotNode(self, node) -> Boolean:
        # """
        # Visit method for NotNode in the abstract syntax tree.

        # This method performs the logical NOT operation on a boolean value.

        # :return: A Boolean object representing the result of the logical NOT operation.
        # """
         # Visit the inner node to obtain its boolean value
        val = self.visit(node.node)

         # Perform the logical NOT operation and return a Boolean object
        if self._isTruthy(val):
            return Boolean("false")

        return Boolean("true")


    def visit_AndNode(self, node) -> Boolean:
        # """
        # Visit method for AndNode in the abstract syntax tree.

        # This method performs the logical AND operation on two boolean values.

        # :return: A Boolean object representing the result of the logical AND operation.
        # """
         # Evaluate the left operand and check its truthiness
        l = self._isTruthy(self.visit(node.left))
        if not l:
            return Boolean("false")

        # Evaluate the right operand and check its truthiness
        r = self._isTruthy(self.visit(node.right))
        if not r:
            return Boolean("false")

        # Return a Boolean object representing the result of the logical AND operation
        return Boolean("true")


    def visit_OrNode(self, node) -> Boolean:
        # """
        # Visit method for OrNode in the abstract syntax tree.

        # This method performs the logical OR operation on two boolean values.

        # :return: A Boolean object representing the result of the logical OR operation.
        # """
        # Evaluate the left operand and check its truthiness
        l = self._isTruthy(self.visit(node.left))
        if l:
            return Boolean("true")

        # Evaluate the right operand and check its truthiness
        r = self._isTruthy(self.visit(node.right))
        if r:
            return Boolean("true")
        
        # Return a Boolean object representing the result of the logical AND operation
        return Boolean("false")


    def visit_BlockNode(self, node) -> Nil:
        # """
        # Visit method for BlockNode in the abstract syntax tree.

        # This method iterates through a block of statements and returns the result of the last executed statement.

        # :return: A Nil object indicating the end of the block.
        # """
        for s in node.stmtList:
            v = self.visit(s)

             # Check for control flow statements
            if v == "continue":
                return "continue"
            if v == "break":
                return "break"
             # Return a non-nil value if a return statement is encountered   
            if v != None and str(v) != "nil":
                return v

            if type(s).__name__ == "ReturnNode":
                return v
            # Continue iterating through the block

        # Return a Nil object indicating the end of the block
        return Nil()


    def visit_ContinueNode(self, node) -> str:
        # """
        # Visit method for ContinueNode in the abstract syntax tree.

        # This method returns a string indicating a "continue" statement.

        # :return: A string indicating a "continue" statement.
        # """
        return "continue"



    def visit_BreakNode(self, node) -> str:
        # """
        # Visit method for BreakNode in the abstract syntax tree.

        # This method returns a string indicating a "break" statement.

        # :return: A string indicating a "break" statement.
        # """
        return "break"


    def visit_ConditionalNode(self, node) -> bool:
        # """
        # Visit method for ConditionalNode in the abstract syntax tree.

        # This method evaluates a conditional expression and executes the corresponding statement if the condition is truthy.

        # :return: True if the condition is truthy and the statement is executed, False otherwise.
        # """
        # Evaluate the condition
        cond: LObject = self.visit(node.condition)

        # Check if the condition is truthy
        if self._isTruthy(cond):
              # Visit and execute the statement
            r = self.visit(node.statement)

            # Check for control flow statements within the statement
            if r == "continue":
                return "continue"

            if r == "break":
                return "break"
            
            # Return a non-nil value if a return statement is encountered
            if type(node.statement).__name__ == "ReturnNode":
                return r
                
            if r != None and str(r) != "nil":
                return r
             # Continue executing the block

            # Return True indicating the condition is truthy and the statement is executed

            return True

        return False


    def visit_IfNode(self, node) -> bool:
        # """
        # Visit method for IfNode in the abstract syntax tree.

        # This method evaluates an if statement, including any elsif and else blocks.

        # :return: True if any if or elsif block is executed, False if all conditions are falsy and there is no else block.
        #          Returns the result of the executed block if a return statement is encountered.
        # """
         # Evaluate the if block
        res: bool = self.visit(node.ifBlock)

        # Check if the if block is executed
        if not res:
            # Evaluate any elsif blocks
            for b in node.elsifBloks:
                res = self.visit(b)
                # Break if an elsif block is executed
                if res == True:
                    break

                # Return the result if a return statement is encountered
                if bool(res):
                    return res
        # If no blocks are executed and there is an else block, evaluate it
        if not res and node.elseBlock:
            res = self.visit(node.elseBlock)

        # Return the result of the executed block
        if res not in [True, False]:
            return res

    
    def visit_WhileNode(self, node) -> LObject:
        # """
        # Visit method for WhileNode in the abstract syntax tree.

        # This method evaluates a while loop, repeatedly executing the statement block while the condition is truthy.

        # :return: The result of the last executed statement block, or None if the loop is not executed.
        # """
        # Evaluate the condition
        cond: LObject = self.visit(node.condition)

        # Continue looping while the condition is truthy
        while self._isTruthy(cond):
             # Visit and execute the statement block
            res: LObject = self.visit(node.statement)
            cond = self.visit(node.condition)

            # Return the result if it is non-nil and not a "continue" statement
            if str(res) not in ["nil", "continue"] and bool(res):
                return res
    

    def visit_ReturnNode(self, node) -> LObject:
        # """
        # Visit method for ReturnNode in the abstract syntax tree.

        # This method processes a return statement within a function.

        # :return: The result of the expression specified in the return statement.
        # """
        # Check if the return statement is within a function
        if self._curFrame.type != ARType.FUNCTION:
            raise SyntaxErr("'return' outside function", node.line)
        # Visit and return the result of the expression in the return statement
        return self.visit(node.expr)


    def visit_FunDeclNode(self, node) -> None:
        # """
        # Visit method for FunDeclNode in the abstract syntax tree.

        # This method processes a function declaration, creating a Function object and adding it to the current frame.

        # :return: None.
        # """
        # Create a Function object with the function's name, parameters, and block
        funObj = Function(
            node.id.token.value,
            [a.value for a in node.paramList],
            node.blockNode
        )

        # Add the function object to the current frame
        self._curFrame[node.id.token.value] = funObj


    def visit_FunctionCallNode(self, node) -> LObject:
#         """
#         Visit method for FunctionCallNode in the abstract syntax tree.

#         This method processes a function call, either invoking a built-in function or executing a user-defined function.
# .
#         :return: The result of the function call.
#         """
        # check builtin function
        if str(node.nameNode) in builtinFunctionTable:
            argList = []
            for a in node.argList:
                argList.append(self.visit(a))
            
            # Invoke the built-in function and return the result
            return builtinFunctionTable[str(node.nameNode)](argList)

        # Create a new frame for the function call
        newFrame = ActivationRecord(ARType.FUNCTION)
        newFrame.setEnclosingEnv(self._curFrame)
        
         # Add parameters to the new frame as local variables
        funObj = self._curFrame.get(node.nameNode.token.value)
        for a,f in zip(funObj.args, node.argList):
            newFrame[a] = self.visit(f)

        # Push the new frame to the call stack
        self._callStack.push(newFrame)
        self._curFrame = self._callStack.peek()

        # execute the function
        retval = self.visit(funObj.block)

        # pop frame
        self._callStack.pop()
        self._curFrame = self._callStack.peek()
        
         # Return the result of the function execution
        return retval

