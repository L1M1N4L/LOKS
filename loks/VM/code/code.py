from typing import List, Any

# Class defining constants for different tag values
class Tag:
    CONSTANT_Integer = 0x3
    CONSTANT_Double = 0x6
    CONSTANT_String = 0x8

# Class defining information about a function
class func_info:
    def __init__(self):
        # Number of arguments for the function
        self.argc: int = 0
        # List to store the code for the function
        self.code: List[int] = []

    def __str__(self):
        # Convert the code list to a formatted string with hexadecimal representation
        code = " ".join(hex(i) for i in self.code)
        return f"{self.argc}-{code}"

    def __repr__(self):
        # Return the string representation of the func_info object
        return self.__str__()


# Class representing constant pool information
class cp_info:
    def __init__(self, t: int, v: Any):
        # Type tag for the constant pool entry
        self.tag: int = t
        # Information associated with the constant pool entry
        self.info: Any = v

    def __str__(self):
        # String representation of the constant pool entry
        return f"{hex(self.tag)}: {self.info}"

    def __repr__(self):
        # Return the string representation of the cp_info object
        return self.__str__()

# Class representing code information
class Code:
    # Magic number for the code
    magic_number: int = 0x4d69686f

    def __init__(self):
        # List to store constant pool entries
        self.const_pool: List[cp_info] = []
        # List to store function pool entries
        self.func_pool: List[func_info] = []

    def addToCP(self, c: cp_info) -> None:
        # Add a constant pool entry to the const_pool list
        self.const_pool.append(c)

    def getFromCP(self, idx: int) -> cp_info:
        # Retrieve a constant pool entry from the const_pool list based on index
        return self.const_pool[idx]

    def addToFP(self, c: func_info) -> None:
        # Add a function pool entry to the func_pool list
        self.func_pool.append(c)

    def getFromFP(self, idx: int) -> func_info:
        # Retrieve a function pool entry from the func_pool list based on index
        return self.func_pool[idx]
