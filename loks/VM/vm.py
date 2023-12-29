from typing import List

# Importing classes and modules from different parts of the interpreter
from .code.codeBuilder import CodeBuilder
from .code.code import Code, func_info, cp_info, Tag
from ..instruction import opcode, opcodeDict
from .stack.frame import Frame
from .stack.stack import Stack

# Importing types and standard library functions
from ..types import LObject, Number, Nil, Array, Boolean, String
from ..stdlib import builtinFunctionIndex, builtinFunctionTable, builtinFunctionInfo
from ..error import TypeErr, ZeroDivErr, IndexErr, SyntaxErr


class VirtualMachine:
    def __init__(self, code: List[int]) -> None:
        # Initialize the VirtualMachine with the given bytecode
        self._code_obj: Code = CodeBuilder(code).getCodeObj()

        # Initialize the current and main frames
        self._cur_frame: Frame = Frame()
        self._main_frame: Frame = Frame("main")

        # Initialize the call stack, instruction pointer, and current instruction
        self._call_stack: Stack = Stack()
        self._ip: int = -1
        self._cur_ins: int = None

        # Enable/disable logging for debugging purposes
        self._LOG: bool = False

    def _advance(self, advance_by=1) -> int:
        """
        Move the instruction pointer forward by the specified amount.

        Parameters:
        - advance_by: Number of instructions to advance (default is 1).

        Returns:
        - The value of the current instruction after advancing.
        """
        # Move the instruction pointer forward by the specified amount
        self._ip += advance_by
        # Get the current instruction from the current frame
        self._cur_ins = self._cur_frame.getInsAtIndex(self._ip)
        return self._cur_ins

    # Jump to the specified index 'idx' of the code of the currently executing function
    def _goto(self, idx: int) -> None:
        """
        Set the instruction pointer to the specified index 'idx' in the code of the current executing function.

        Parameters:
        - idx: The index to jump to.
        """
        # Set the instruction pointer to the specified index
        self._ip = idx
        # Get the current instruction from the current frame
        self._cur_ins = self._cur_frame.getInsAtIndex(self._ip)

    def _pushFrame(self, f: Frame) -> None:
        """
        Push a frame onto the call stack.

        Parameters:
        - f: The frame to push onto the call stack.
        """
        # Push the specified frame onto the call stack
        self._call_stack.push(f)

    def _popFrame(self) -> Frame:
        """
        Pop a frame from the call stack.

        Returns:
        - The frame popped from the call stack.
        """
        # Pop a frame from the call stack
        return self._call_stack.pop()

    def _init_vm(self) -> None:
        """
        Initialize the virtual machine with the main function's code.
        """
        # Get the main function information from the function pool
        main: func_info = self._code_obj.getFromFP(0)
        # Set the code of the main frame to the main function's code
        self._main_frame.setCode(main.code)
        # Set the current frame to the main frame
        self._cur_frame = self._main_frame
        # Advance the instruction pointer to the first instruction
        self._advance()

    def run(self):
        """
        Execute the virtual machine by initializing it and running the instructions in a loop until the END opcode is encountered.
        """
        # Initialize the virtual machine
        self._init_vm()

        # Continue execution until the END opcode is encountered
        while self._cur_ins != opcode.END.value:
            i = self._cur_ins
            # Execute the current instruction
            self.execute(i)
            
            # Advance the instruction pointer unless the current instruction is a control flow instruction
            if i not in [
                opcode.GOTO.value,
                opcode.POP_JMP_IF_TRUE.value,
                opcode.POP_JMP_IF_FALSE.value,
            ]:
                self._advance()

    def _getObjType(self, el: LObject) -> str:
        """
        Get the type of the given LObject.

        Parameters:
        - el: The LObject to determine the type for.

        Returns:
        - The name of the type as a string.
        """
        # Return the name of the type of the given LObject
        return type(el).__name__

    def _isTruthy(self, obj: LObject) -> bool:
        """
        Check if the given LObject is truthy.

        Parameters:
        - obj (LObject): The LObject to check for truthiness.

        Returns:
        - bool: True if the object is truthy, False otherwise.

        This method examines the type of the LObject and determines its truthiness based on the following rules:

        - For Numbers: The object is truthy if its value is non-zero.
        - For Strings: The object is truthy if its length is non-zero.
        - For Nil: The object is always falsy.
        - For Booleans: The object is falsy if its value is "false"; otherwise, it is truthy.
        - For Arrays: The object is truthy if its length is non-zero.

        Note: If the object doesn't fall into any of these categories, it is considered truthy by default.

        Example:
        ```python
        obj = Number(42)
        result = _isTruthy(obj)  # True
        ```
        """

        # Check the type of the object and determine truthiness accordingly
        if self._getObjType(obj) == "Number":
            # For Numbers: The object is truthy if its value is non-zero.
            if obj.value == 0:
                return False
            return True

        elif self._getObjType(obj) == "String":
            # For Strings: The object is truthy if its length is non-zero.
            if len(obj.value) == 0:
                return False
            return True

        elif self._getObjType(obj) == "Nil":
            # For Nil: The object is always falsy.
            return False

        elif self._getObjType(obj) == "Boolean":
            # For Booleans: The object is falsy if its value is "false"; otherwise, it is truthy.
            if obj.value == "false":
                return False
            return True

        elif self._getObjType(obj) == "Array":
            # For Arrays: The object is truthy if its length is non-zero.
            if obj.getLen() == 0:
                return False
            return True

        # Default: Considered truthy if the object doesn't fall into any of the specified categories.
        return True
    
    def execute(self, i: int) -> None:
        # Construct the method name based on the opcode dictionary
        fn_name = f"execute_{opcodeDict[i]}"
        # Get the method reference using getattr, if not found, use _insNotImplemented
        fn = getattr(self, fn_name, self._insNotImplemented)
        # Call the selected method with the opcode
        fn(i)

    def _insNotImplemented(self, i: int) ->  None:
        # Raise an exception indicating that the execution method for the opcode is not implemented
        raise Exception(f"execute_{opcodeDict[i]} method not implemented.")

    def execute_LOAD_NIL(self, i: int) -> None:
        # Implementation for the LOAD_NIL opcode
        # Push a Nil object onto the operand stack of the current frame
        self._cur_frame.pushOpStack(Nil())

    def execute_LOAD_TRUE(self, i: int) -> None:
        # Implementation for the LOAD_TRUE opcode
        # Push a Boolean("true") object onto the operand stack of the current frame
        self._cur_frame.pushOpStack(Boolean("true"))

    def execute_LOAD_FALSE(self, i: int) -> None:
        # Implementation for the LOAD_FALSE opcode
        # Push a Boolean("false") object onto the operand stack of the current frame
        self._cur_frame.pushOpStack(Boolean("false"))

    def execute_LOAD_CONST(self, i: int) -> None:
        # Implementation for the LOAD_CONST opcode
        # Read the constant pool index from the next two bytes of the bytecode
        idx: int = (self._advance() << 8) + self._advance()
        # Retrieve the constant object from the constant pool using the index
        constObj: cp_info = self._code_obj.getFromCP(idx)

        if constObj.tag == Tag.CONSTANT_String:
            # If the constant is a string, push a String object onto the operand stack
            self._cur_frame.pushOpStack(String(constObj.info))
            
        elif constObj.tag == Tag.CONSTANT_Integer:
            # If the constant is an integer, push a Number object onto the operand stack
            self._cur_frame.pushOpStack(Number(constObj.info))
            
        elif constObj.tag == Tag.CONSTANT_Double:
            # If the constant is a double, push a Number object onto the operand stack
            self._cur_frame.pushOpStack(Number(constObj.info))

    def execute_BINARY_ADD(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # String concatenation for '+'
        if self._getObjType(l) == "String":
            if self._getObjType(r) != "String":
                # Raise an error if trying to add a non-String type to a String
                raise TypeErr(f"Cannot add {self._getObjType(r)} to String")
            # Push the result of string concatenation onto the operand stack
            self._cur_frame.pushOpStack(String(l.value + r.value))

        # Check types for numbers
        elif self._getObjType(l) == "Number":
            if self._getObjType(r) != "Number":
                # Raise an error if trying to add a non-Number type to a Number
                raise TypeErr(f"Cannot add {self._getObjType(r)} to Number")
            # Push the result of addition onto the operand stack
            self._cur_frame.pushOpStack(Number(l.value + r.value))
        
        # Addition is not defined for any other type
        else:
            # Raise an error for unsupported types
            raise TypeErr(f"Addition not defined for type '{self._getObjType(l)}'")

        # Log the addition operation if logging is enabled
        if self._LOG: print(f"add {l.value}, {r.value}")


    def execute_BINARY_SUBTRACT(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check if both operands are of type Number
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            # Raise an error if either operand is not a Number
            raise TypeErr(f"Cannot subtract {self._getObjType(r)} from {self._getObjType(l)}")

        # Push the result of subtraction onto the operand stack
        self._cur_frame.pushOpStack(Number(l.value - r.value))

        # Log the subtraction operation if logging is enabled
        if self._LOG: print(f"sub {l.value}, {r.value}")


    def execute_BINARY_MULTIPLY(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check if both operands are of type Number
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            # Raise an error if either operand is not a Number
            raise TypeErr(f"Cannot multiply {self._getObjType(l)} by {self._getObjType(r)}")

        # Push the result of multiplication onto the operand stack
        self._cur_frame.pushOpStack(Number(l.value * r.value))

        # Log the multiplication operation if logging is enabled
        if self._LOG: print(f"mul {l.value}, {r.value}")

    def execute_BINARY_DIVIDE(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check if both operands are of type Number
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            # Raise an error if either operand is not a Number
            raise TypeErr(f"Cannot divide {self._getObjType(l)} by {self._getObjType(r)}")

        # Check for division by zero
        if r.value == 0:
            raise ZeroDivErr()

        # Push the result of division onto the operand stack
        self._cur_frame.pushOpStack(Number(l.value / r.value))

        # Log the division operation if logging is enabled
        if self._LOG: print(f"div {l.value}, {r.value}")


    def execute_BINARY_MODULO(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check if both operands are of type Number
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            # Raise an error if either operand is not a Number
            raise TypeErr(f"Invalid operand type for modulo: {self._getObjType(l)} and {self._getObjType(r)}")

        # Check for division by zero
        if r.value == 0:
            raise ZeroDivErr()

        # Push the result of modulo operation onto the operand stack
        self._cur_frame.pushOpStack(Number(l.value % r.value))

        # Log the modulo operation if logging is enabled
        if self._LOG: print(f"mod {l.value}, {r.value}")

    def execute_BINARY_AND(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Log the AND operation if logging is enabled
        if self._LOG: print(f"and {l.value}, {r.value}")
        
        # Check if the left operand is truthy
        if not self._isTruthy(l):
            # If not truthy, push 'false' onto the operand stack and return
            self._cur_frame.pushOpStack(Boolean("false"))
            return
        
        # Check if the right operand is truthy
        if not self._isTruthy(r):
            # If not truthy, push 'false' onto the operand stack and return
            self._cur_frame.pushOpStack(Boolean("false"))
            return
            
        # Both operands are truthy, push 'true' onto the operand stack
        self._cur_frame.pushOpStack(Boolean("true"))


    def execute_BINARY_OR(self, i: int) -> None:
        # Pop the right and left operands from the operand stack of the current frame
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check if the left operand is truthy
        if self._isTruthy(l):
            # If truthy, push 'true' onto the operand stack
            self._cur_frame.pushOpStack(Boolean("true"))
        elif self._isTruthy(r):
            # If truthy, push 'true' onto the operand stack
            self._cur_frame.pushOpStack(Boolean("true"))
        else:
            # Both operands are not truthy, push 'false' onto the operand stack
            self._cur_frame.pushOpStack(Boolean("false"))

        # Log the OR operation if logging is enabled
        if self._LOG: print(f"or {l.value}, {r.value}")

    def execute_UNARY_NOT(self, i: int) -> None:
        # Pop the operand from the operand stack of the current frame
        op: LObject = self._cur_frame.popOpStack()

        # Check if the operand is truthy
        if self._isTruthy(op):
            # If truthy, push 'false' onto the operand stack
            self._cur_frame.pushOpStack(Boolean("false"))
        else:
            # If not truthy, push 'true' onto the operand stack
            self._cur_frame.pushOpStack(Boolean("true"))


    def execute_UNARY_NEGATIVE(self, i: int) -> None:
        # Pop the operand from the operand stack of the current frame
        op: LObject = self._cur_frame.popOpStack()
        
        # Check if the operand is of type 'Number'
        if not self._getObjType(op) == "Number":
            # If not a number, raise a type error
            raise TypeErr(f"Cannot negate {self._getObjType(op)}")

        # Negate the value of the operand and push the result onto the operand stack
        self._cur_frame.pushOpStack(Number(-(op.value)))


    def execute_STORE_LOCAL(self, i: int) -> None:
        # Store the operand from the operand stack into a local variable at the specified index
        self._cur_frame.setLocalVarAtIndex(
            self._advance(),
            self._cur_frame.popOpStack()
        )

    def execute_STORE_GLOBAL(self, i: int) -> None:
        # Store the operand from the operand stack into a global variable at the specified index
        self._main_frame.setLocalVarAtIndex(
            self._advance(),
            self._cur_frame.popOpStack()
        )


    def execute_BIPUSH(self, i: int) -> None:
        # Push a constant integer onto the operand stack
        self._cur_frame.pushOpStack(Number(self._advance()))


    def execute_LOAD_LOCAL(self, i: int) -> None:
        # Load a local variable onto the operand stack
        self._cur_frame.pushOpStack(self._cur_frame.getLocalVarAtIndex(self._advance()))


    def execute_LOAD_GLOBAL(self, i: int) -> None:
        # Load a global variable onto the operand stack
        self._cur_frame.pushOpStack(self._main_frame.getLocalVarAtIndex(self._advance()))

    def execute_CMPEQ(self, i: int) -> None:
        # Compare if two values on the operand stack are equal
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check the values and push the result onto the operand stack
        if l.value == r.value:
            self._cur_frame.pushOpStack(Boolean("true"))
        else:
            self._cur_frame.pushOpStack(Boolean("false"))

        # Log the operation if enabled
        if self._LOG: print(f"cmpeq {l.value}, {r.value}")


    def execute_CMPNE(self, i: int) -> None:
        # Compare if two values on the operand stack are not equal
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check the values and push the result onto the operand stack
        if l.value != r.value:
            self._cur_frame.pushOpStack(Boolean("true"))
        else:
            self._cur_frame.pushOpStack(Boolean("false"))

        # Log the operation if enabled
        if self._LOG: print(f"cmpne {l.value}, {r.value}")

def execute_CMPGT(self, i: int) -> None:
    """
    Executes the CMPGT (compare greater than) operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Pops the top two elements from the operand stack as the left (l) and right (r) operands.
    2. Checks the operand types for validity (both must be Numbers).
    3. Compares if the value on the left (l) is greater than the value on the right (r).
    4. Pushes the result (Boolean) of the comparison onto the operand stack.
    5. Logs the operation if logging is enabled.

    Raises:
    - TypeErr: If the operand types are invalid for the greater than comparison.
    """
    # Compare if the value on the left is greater than the value on the right
    r: LObject = self._cur_frame.popOpStack()
    l: LObject = self._cur_frame.popOpStack()

    # Check operand types for validity
    if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
        raise TypeErr(f"Invalid operand type for greater than operator: {self._getObjType(l)} and {self._getObjType(r)}")

    # Perform the comparison and push the result onto the operand stack
    if l.value > r.value:
        self._cur_frame.pushOpStack(Boolean("true"))
    else:
        self._cur_frame.pushOpStack(Boolean("false"))

    # Log the operation if enabled
    if self._LOG: print(f"cmpgt {l.value}, {r.value}")


    def execute_CMPLT(self, i: int) -> None:
        """
        Executes the CMPLT (compare less than) operation.

        Parameters:
        - i (int): Instruction index.

        Description:
        1. Pops the top two elements from the operand stack as the left (l) and right (r) operands.
        2. Checks the operand types for validity (both must be Numbers).
        3. Compares if the value on the left (l) is less than the value on the right (r).
        4. Pushes the result (Boolean) of the comparison onto the operand stack.
        5. Logs the operation if logging is enabled.

        Raises:
        - TypeErr: If the operand types are invalid for the less than comparison.
        """
        # Compare if the value on the left is less than the value on the right
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check operand types for validity
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for less than operator: {self._getObjType(l)} and {self._getObjType(r)}")

        # Perform the comparison and push the result onto the operand stack
        if l.value < r.value:
            self._cur_frame.pushOpStack(Boolean("true"))
        else:
            self._cur_frame.pushOpStack(Boolean("false"))

        # Log the operation if enabled
        if self._LOG: print(f"cmplt {l.value}, {r.value}")

    def execute_CMPGE(self, i: int) -> None:
        """
        Executes the CMPGE (compare greater than or equals) operation.

        Parameters:
        - i (int): Instruction index.

        Description:
        1. Pops the top two elements from the operand stack as the left (l) and right (r) operands.
        2. Checks the operand types for validity (both must be Numbers).
        3. Compares if the value on the left (l) is greater than or equal to the value on the right (r).
        4. Pushes the result (Boolean) of the comparison onto the operand stack.
        5. Logs the operation if logging is enabled.

        Raises:
        - TypeErr: If the operand types are invalid for the greater than or equals comparison.
        """
        # Compare if the value on the left is greater than or equal to the value on the right
        r: LObject = self._cur_frame.popOpStack()
        l: LObject = self._cur_frame.popOpStack()

        # Check operand types for validity
        if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
            raise TypeErr(f"Invalid operand type for greater than equals operator: {self._getObjType(l)} and {self._getObjType(r)}")

        # Perform the comparison and push the result onto the operand stack
        if l.value >= r.value:
            self._cur_frame.pushOpStack(Boolean("true"))
        else:
            self._cur_frame.pushOpStack(Boolean("false"))

        # Log the operation if enabled
        if self._LOG: print(f"cmpge {l.value}, {r.value}")

def execute_CMPLE(self, i: int) -> None:
    """
    Executes the CMPLE (compare less than or equals) operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Pops the top two elements from the operand stack as the left (l) and right (r) operands.
    2. Checks the operand types for validity (both must be Numbers).
    3. Compares if the value on the left (l) is less than or equal to the value on the right (r).
    4. Pushes the result (Boolean) of the comparison onto the operand stack.
    5. Logs the operation if logging is enabled.

    Raises:
    - TypeErr: If the operand types are invalid for the less than or equals comparison.
    """
    # Compare if the value on the left is less than or equal to the value on the right
    r: LObject = self._cur_frame.popOpStack()
    l: LObject = self._cur_frame.popOpStack()

    # Check operand types for validity
    if self._getObjType(l) != "Number" or self._getObjType(r) != "Number":
        raise TypeErr(f"Invalid operand type for less than equals operator: {self._getObjType(l)} and {self._getObjType(r)}")

    # Perform the comparison and push the result onto the operand stack
    if l.value <= r.value:
        self._cur_frame.pushOpStack(Boolean("true"))
    else:
        self._cur_frame.pushOpStack(Boolean("false"))

    # Log the operation if enabled
    if self._LOG: print(f"cmple {l.value}, {r.value}")


def execute_GOTO(self, i: int) -> None:
    """
    Executes the GOTO (unconditional jump) operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Reads the 16-bit operand (jump location) from the next two instructions.
    2. Updates the instruction pointer to the specified location in the current code.
    3. Logs the operation if logging is enabled.
    """
    # Read the 16-bit operand (jump location)
    loc: int = (self._advance() << 8) + self._advance()

    # Update the instruction pointer to the specified location in the current code
    self._goto(loc)

def execute_POP_JMP_IF_TRUE(self, i: int) -> None:
    """
    Executes the POP_JMP_IF_TRUE (conditional jump if true) operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Reads the 16-bit operand (jump location) from the next two instructions.
    2. Pops the top element from the operand stack and checks if it is truthy.
    3. If true, updates the instruction pointer to the specified location in the current code.
    4. If false, consumes the second argument by advancing the instruction pointer.
    5. Logs the operation if logging is enabled.
    """
    # Read the 16-bit operand (jump location)
    idx: int = (self._advance() << 8) + self._advance()

    # Check if the top element on the operand stack is truthy
    if self._isTruthy(self._cur_frame.popOpStack()):
        # Update the instruction pointer to the specified location in the current code
        self._goto(idx)
    else:
        # Consume the second argument by advancing the instruction pointer
        self._advance()


def execute_POP_JMP_IF_FALSE(self, i: int) -> None:
    """
    Executes the POP_JMP_IF_FALSE (conditional jump if false) operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Reads the 16-bit operand (jump location) from the next two instructions.
    2. Pops the top element from the operand stack and checks if it is not truthy.
    3. If true, updates the instruction pointer to the specified location in the current code.
    4. If false, consumes the second argument by advancing the instruction pointer.
    5. Logs the operation if logging is enabled.
    """
    # Read the 16-bit operand (jump location)
    idx: int = (self._advance() << 8) + self._advance()

    # Check if the top element on the operand stack is not truthy
    if not self._isTruthy(self._cur_frame.popOpStack()):
        # Update the instruction pointer to the specified location in the current code
        self._goto(idx)
    else:
        # Consume the second argument by advancing the instruction pointer
        self._advance()

def execute_CALL_NATIVE(self, i: int) -> None:
    """
    Executes the CALL_NATIVE operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Reads the index of the native function from the next instruction.
    2. Retrieves the function name from the built-in function index.
    3. Reads the number of arguments expected by the function from the built-in function info.
    4. Collects arguments from the operand stack based on the expected argument count.
    5. Invokes the built-in function with the collected arguments and pushes the result onto the operand stack.
    """
    # Read the index of the native function
    idx: int = self._advance()
    
    # Retrieve the function name from the built-in function index
    fnName = builtinFunctionIndex[idx]

    # Initialize an empty list to store arguments
    args: List[LObject] = []

    # Read the expected argument count from the built-in function info
    argc: int = builtinFunctionInfo[fnName][1]

    # Collect arguments from the operand stack based on the expected argument count
    for _ in range(argc):
        args = [self._cur_frame.popOpStack()] + args

    # Invoke the built-in function with the collected arguments and push the result onto the operand stack
    self._cur_frame.pushOpStack(builtinFunctionTable[fnName](args))


def execute_RETURN_VALUE(self, i: int) -> None:
    """
    Executes the RETURN_VALUE operation.

    Parameters:
    - i (int): Instruction index.

    Description:
    1. Pops the return value from the operand stack.
    2. Attempts to pop the previous frame from the call stack.
    3. Updates the instruction pointer, copies the state of the previous frame to the current frame, and pushes the return value.
    """
    # Pop the return value from the operand stack
    retVal: LObject = self._cur_frame.popOpStack()

    try:
        # Attempt to pop the previous frame from the call stack
        ret_f: Frame = self._popFrame()

        # Update the instruction pointer, copy the state of the previous frame to the current frame, and push the return value
        self._ip = ret_f.getReturnAddress()
        self._cur_frame.copy(ret_f)
        self._cur_frame.pushOpStack(retVal)
    except:
        # Handle the case where there is no previous frame to return to
        pass

    def execute_BUILD_LIST(self, i: int) -> None:
        """
        Executes the BUILD_LIST operation.

        Parameters:
        - i (int): Instruction index.

        Description:
        1. Reads the length of the list from the next two instructions.
        2. Initializes an empty Array object.
        3. Collects elements from the operand stack based on the specified length.
        4. Adds the collected elements to the Array object.
        5. Pushes the Array object onto the operand stack.
        """
        # Read the length of the list from the next two instructions
        length: int = (self._advance() << 8) + self._advance()

        # Initialize an empty Array object
        arrObj: Array = Array()

        # Collect elements from the operand stack based on the specified length
        arrElList: list = []
        for _ in range(length):
            arrElList = [self._cur_frame.popOpStack()] + arrElList

        # Add the collected elements to the Array object
        for e in arrElList:
            arrObj.addEl(e)

        # Push the Array object onto the operand stack
        self._cur_frame.pushOpStack(arrObj)


    def execute_BINARY_SUBSCR(self, i: int) -> None:
        """
        Executes the BINARY_SUBSCR operation.

        Parameters:
        - i (int): Instruction index.

        Description:
        1. Pops the index from the operand stack.
        2. Checks if the index is a valid integer, raising a TypeErr if not.
        3. Pops the array from the operand stack.
        4. Checks if the array is an Array, raising a TypeErr if not.
        5. Retrieves the element at the specified index from the array and pushes it onto the operand stack.
        """
        # Pop the index from the operand stack
        idx: Number = self._cur_frame.popOpStack()

        # Check if the index is a valid integer, raising a TypeErr if not
        if type(idx).__name__ != "Number":
            raise TypeErr(f"Array indices must be integers, not '{type(idx).__name__}'")

        # Check if the index is a float, raising a TypeErr if it is
        if type(idx.value).__name__ == "float":
            raise TypeErr(f"Array indices must be integers, not float")

        # Pop the array from the operand stack
        arr: Array = self._cur_frame.popOpStack()

        # Check if the array is an Array, raising a TypeErr if not
        if self._getObjType(arr) != "Array":
            raise TypeErr(f"Type '{type(arr).__name__}' is not subscriptable")

        # Check if the index is within bounds, raising an IndexErr if not
        if arr.getEL(idx.value) == None:
            raise IndexErr()

        # Retrieve the element at the specified index from the array and push it onto the operand stack
        self._cur_frame.pushOpStack(arr.getEL(idx.value))

    def execute_STORE_SUBSCR(self, i: int) -> None:
        """
        Executes the STORE_SUBSCR operation.

        Parameters:
        - i (int): Instruction index.

        Description:
        1. Pops the index from the operand stack.
        2. Checks if the index is a valid integer, raising a TypeErr if not.
        3. Pops the array from the operand stack.
        4. Checks if the array is an Array, raising a TypeErr if not.
        5. Pops the value to be assigned from the operand stack.
        6. Checks if the index is within bounds, raising an IndexErr if not.
        7. Sets the element at the specified index in the array to the given value.
        8. Pushes the modified array back onto the operand stack.
        """
        # Pop the index from the operand stack
        idx: Number = self._cur_frame.popOpStack()

        # Check if the index is a valid integer, raising a TypeErr if not
        if type(idx).__name__ != "Number":
            raise TypeErr(f"Array indices must be integers, not '{type(idx).__name__}'")

        # Check if the index is a float, raising a TypeErr if it is
        if type(idx.value).__name__ == "float":
            raise TypeErr(f"Array indices must be integers, not float")

        # Pop the array from the operand stack
        arr: Array = self._cur_frame.popOpStack()

        # Check if the array is an Array, raising a TypeErr if not
        if self._getObjType(arr) != "Array":
            raise TypeErr(f"Type '{type(arr).__name__}' is not subscriptable")

        # Pop the value to be assigned from the operand stack
        val: LObject = self._cur_frame.popOpStack()

        # Check if the index is within bounds, raising an IndexErr if not
        if arr.getEL(idx.value) == None:
            raise IndexErr()

        # Set the element at the specified index in the array to the given value
        arr.setEL(val, idx.value)

        # Push the modified array back onto the operand stack
        self._cur_frame.pushOpStack(arr)
