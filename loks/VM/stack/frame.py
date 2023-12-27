from typing import List
from .stack import Stack
from ...interpreter.types import LObject, Nil

# Class representing a frame in the interpreter's call stack
class Frame:
    def __init__(self, n: str = None):
        # Initialize a new frame with a given name (optional).
        self.name = n
        self._operand_stack = Stack()  # Operand stack for the frame
        self._local_vars: List[LObject] = [Nil()] * 256  # Local variables array
        self._code: List[int] = []  # Code representing the frame's execution
        self._ret_address: int = 0  # Return address for function calls

    def pushOpStack(self, e: LObject) -> None:
        """Push an element onto the operand stack."""
        self._operand_stack.push(e)

    def popOpStack(self) -> LObject:
        """Pop an element from the operand stack."""
        return self._operand_stack.pop()

    def setReturnAddress(self, a: int) -> None:
        """Set the return address of the frame."""
        self._ret_address = a

    def getReturnAddress(self) -> int:
        """Get the return address of the frame."""
        return self._ret_address

    def getLocalVarAtIndex(self, i: int) -> LObject:
        """Get the local variable at the specified index."""
        return self._local_vars[i]

    def setLocalVarAtIndex(self, i: int, e: LObject) -> None:
        """Set the local variable at the specified index."""
        self._local_vars[i] = e

    def setCode(self, c: List[int]) -> None:
        """Set the code for the frame."""
        self._code = c
    
    def getInsAtIndex(self, i: int) -> int:
        """Get the instruction at the specified index."""
        return self._code[i]

    def reset(self) -> None:
        """Reset the frame to its initial state."""
        self.__init__()
    # Copy the contents of another frame to this frame.
    def copy(self, f) -> None:
        """
        Copies the contents of another frame to the current frame.

        Args:
            f: Another frame to copy from.
        Returns:
            None
        """
        self.name = f.name  # Copy the name of the frame
        self._operand_stack = f._operand_stack  # Copy the operand stack
        self._local_vars = f._local_vars  # Copy the local variables
        self._code = f._code  # Copy the code
        self._ret_address = f._ret_address  # Copy the return address

    # String representation of the frame.
    def __str__(self) -> str:
        """
        Returns a string representation of the frame.

        Returns:
            str: String representation of the frame.
        """
        output = "Locals:\n"
        ctr = 0
        for i in self._local_vars:
            output += str(i) + '\n'
            ctr += 1
            if ctr == 10:
                break
        return output

    # String representation for debugging.
    def __repr__(self) -> str:
        """
        Returns a string representation for debugging.

        Returns:
            str: String representation for debugging.
        """
        return self.__str__()
