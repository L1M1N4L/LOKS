# Import necessary classes and modules
from .code import Code, Tag, func_info, cp_info
from ...error import InvalidBytecodeError

# Class for building a Code object from a given code array
class CodeBuilder:
    def __init__(self, codeArr):
        # Initialize a Code object to store the bytecode and related information
        self._code = Code()
        # Input array containing bytecode instructions
        self._code_array = codeArr

    def getCodeObj(self) -> Code:
        # Initialize the code object, build constant pool, and function pool
        self._initCode()
        self._makeConstPool()
        self._makeFuncPool()
        # Return the constructed Code object with constant pool and function pool
        return self._code

    def _removeFromFront(self, n: int) -> None:
        """
        Remove the first n elements from the code array.

        :param n: Number of elements to remove from the front of the code array.
        """
        self._code_array = self._code_array[n:]

    
    def _initCode(self) -> None:
        """
        Initialize the Code object by extracting the magic number from the code array.
        Raise an InvalidBytecodeError if the magic number is not present or incorrect.
        """
        # Check if there are enough bytes for the magic number
        if len(self._code_array) < 10:
            raise InvalidBytecodeError()

        # Extract the magic number from the code array
        magic: int =                        \
            (self._code_array[0] << 24) +   \
            (self._code_array[1] << 16) +   \
            (self._code_array[2] << 8) +    \
            (self._code_array[3])

        # Check if the extracted magic number matches the expected magic number
        if magic != Code.magic_number:
            raise InvalidBytecodeError()
        
        # Remove the magic number bytes from the front of the code array
        self._removeFromFront(4)

    def _makeConstPool(self) -> None:
        """
        Create the constant pool for the Code object by parsing the bytecode.
        """
        # Extract the constant pool count from the code array
        cp_count: int = (self._code_array[0] << 8) + (self._code_array[1])
        # Remove the constant pool count bytes from the front of the code array
        self._removeFromFront(2)
        
        # Iterate over the constant pool entries
        for _ in range(cp_count):
            # Extract the tag from the code array
            t: Tag = self._code_array[0]
            # Remove the tag byte from the front of the code array
            self._removeFromFront(1)

            # Choose the appropriate method based on the tag
            if t == Tag.CONSTANT_Integer:
                self._makeInteger()
            elif t == Tag.CONSTANT_Double:
                self._makeDouble()
            elif t == Tag.CONSTANT_String:
                self._makeString()

    def _makeInteger(self) -> None:
        """
        Parse an integer from the code array and add it to the constant pool.
        """
        # Extract the eight bytes representing the integer from the code array
        i: int =                            \
            (self._code_array[0] << 56) +   \
            (self._code_array[1] << 48) +   \
            (self._code_array[2] << 40) +   \
            (self._code_array[3] << 32) +   \
            (self._code_array[4] << 24) +   \
            (self._code_array[5] << 16) +   \
            (self._code_array[6] << 8) +    \
            (self._code_array[7])

        # Check the sign bit and adjust the value accordingly
        s_test: int = (i & 0xf000000000000000) >> 60
        if s_test > 7:
            i -= 1  # Subtract 1
            i = i ^ (0xffffffffffffffff)  # Flip bits
            i = -i  # Negate

        # Remove the eight bytes from the front of the code array
        self._removeFromFront(8)
        # Add the integer to the constant pool
        self._code.addToCP(cp_info(Tag.CONSTANT_Integer, i))


    def _makeDouble(self) -> None:
        """
        Parse a double from the code array and add it to the constant pool.
        """
        v = self._code_array

        # Extract sign, exponent, and mantissa from the bytes
        sign: int = (v[0] & 0b10000000) >> 7
        exp: int = (((v[0] << 8) + (v[1])) & 0b0111111111110000) >> 4
        mantissa: int = ((v[1] & 0x0f) << 48) + \
            (v[2] << 40) +    \
            (v[3] << 32) +    \
            (v[4] << 24) +    \
            (v[5] << 16) +    \
            (v[6] << 8) +     \
            (v[7])

        # Calculate the double value using the sign, exponent, and mantissa
        d: float = mantissa/(10**exp)

        # Adjust the sign of the double value
        if sign == 1:
            d = -d

        # Remove the eight bytes from the front of the code array
        self._removeFromFront(8)
        # Add the double to the constant pool
        self._code.addToCP(cp_info(Tag.CONSTANT_Double, d))

    def _makeString(self) -> None:
        """
        Parse a string from the code array and add it to the constant pool.
        """
        s: str = ""

        # Read characters until a null terminator (0x00) is encountered
        while self._code_array[0] != 0x00:
            s += chr(self._code_array[0])
            self._removeFromFront(1)

        # Remove the null terminator byte
        self._removeFromFront(1)
        # Add the string to the constant pool
        self._code.addToCP(cp_info(Tag.CONSTANT_String, s))


    def _makeFuncPool(self) -> None:
        """
        Parse the function pool from the code array and add functions to the function pool.
        """
        fp_count: int = (self._code_array[0] << 8) + (self._code_array[1])
        self._removeFromFront(2)

        # Iterate through the function pool entries
        for _ in range(fp_count):
            # Add a function to the function pool
            self._code.addToFP(self._makeFunc())


    def _makeFunc(self) -> func_info:
        """
        Parse a function entry from the code array and return a func_info object.
        """
        f = func_info()

        # Read the number of arguments for the function
        argc: int = (self._code_array[0] << 8) + (self._code_array[1])
        self._removeFromFront(2)
        f.argc = argc

        # Read the number of code entries for the function
        code_count: int = (self._code_array[0] << 8) + (self._code_array[1])
        self._removeFromFront(2)

        # Iterate through the code entries and add them to the function's code list
        for _ in range(code_count):
            f.code.append(self._code_array[0])
            self._removeFromFront(1)

        return f
