# Import necessary type hints from the typing module
from typing import Union, List

# Define a base class named LObject
class LObject:
    # Method to return a string representation of the object
    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
        - A string representation of the object.
        """
        return self.__str__()

# Define a class named Number that inherits from LObject
class Number(LObject):
    # Constructor method, initializes a Number object with a numeric value
    def __init__(self, val: Union[int, float]) -> None:
        """
        Initializes a Number object with the specified numeric value.

        Parameters:
        - val: The numeric value (either int or float).
        """
        self.value = val

    # Method to return a string representation of the Number object
    def __str__(self) -> str:
        """
        Returns a string representation of the Number object.

        Returns:
        - A string representation of the Number object.
        """
        return f"{self.value}"

# Define a class named Nil that inherits from LObject
class Nil(LObject):
    # Constructor method, initializes a Nil object
    def __init__(self) -> None:
        """
        Initializes a Nil object.
        """
        self.value = "nil"

    # Method to return a string representation of the Nil object
    def __str__(self) -> str:
        """
        Returns a string representation of the Nil object.

        Returns:
        - A string representation of the Nil object.
        """
        return "nil"
# Define a class named Boolean that inherits from LObject
class Boolean(LObject):
    # Constructor method, initializes a Boolean object with a string value
    def __init__(self, val: str) -> None:
        """
        Initializes a Boolean object with the specified string value.

        Parameters:
        - val: The string value representing a boolean.
        """
        self.value = val

    # Method to return a string representation of the Boolean object
    def __str__(self) -> str:
        """
        Returns a string representation of the Boolean object.

        Returns:
        - A string representation of the Boolean object.
        """
        return f"{self.value}"

# Define a class named String that inherits from LObject
class String(LObject):
    # Constructor method, initializes a String object with a string value
    def __init__(self, val: str) -> None:
        """
        Initializes a String object with the specified string value.

        Parameters:
        - val: The string value.
        """
        self.value = val

    # Method to return a string representation of the String object
    def __str__(self) -> str:
        """
        Returns a string representation of the String object.

        Returns:
        - A string representation of the String object, enclosed in double quotes.
        """
        return f'"{self.value}"'

# Define a class named Array that inherits from LObject
class Array(LObject):
    # Constructor method, initializes an Array object with an empty list
    def __init__(self) -> None:
        """
        Initializes an Array object with an empty list.
        """
        self._arr: List[LObject] = []

    # Method to add an element to the end of the array
    def addEl(self, el: LObject) -> None:
        """
        Adds an element to the end of the array.

        Parameters:
        - el: The element to be added to the array.
        """
        self._arr.append(el)

    # Method to set an element at a specific index in the array
    def setEL(self, el: LObject, idx: int) -> None:
        """
        Sets the element at the specified index in the array.

        Parameters:
        - el: The element to be set at the specified index.
        - idx: The index where the element should be set.
        """
        self._arr[idx] = el

    # Method to retrieve an element from a specific index in the array
    def getEL(self, idx: int) -> None:
        """
        Retrieves the element at the specified index in the array.

        Parameters:
        - idx: The index from which to retrieve the element.

        Returns:
        - The element at the specified index.
        """
        return self._arr[idx]

    # Method to get the length of the array
    def getLen(self) -> int:
        """
        Returns the length of the array.

        Returns:
        - The length of the array.
        """
        return len(self._arr)

    # Method to return a string representation of the Array object
    def __str__(self) -> str:
        """
        Returns a string representation of the Array object.

        Returns:
        - A string representation of the Array object, including its elements.
        """
        # Initialize an empty string 'output' with '['
        output: str = '['
        
        # Iterate through each element 'i' in the array
        for i in self._arr:
            # Concatenate the string representation of 'i' and a comma to 'output'
            output += str(i) + ", "
        
        # Remove the trailing comma and space by excluding the last two characters
        output = output[:-2]
        
        # Append ']' to complete the string representation
        output += ']'
        
        # Return the final string representation of the Array object
        return output
    
# Define a class named Function that inherits from LObject
class Function(LObject):
    # Constructor method, initializes a Function object with a name, list of arguments, and a block
    def __init__(self, n: str, args: list, b) -> None:
        """
        Initializes a Function object with a name, list of arguments, and a block.

        Parameters:
        - n: The name of the function.
        - args: The list of arguments for the function.
        - b: The block associated with the function.
        """
        self.name = n
        self.args = args
        self.block = b

    # Method to return a string representation of the Function object
    def __str__(self) -> str:
        """
        Returns a string representation of the Function object.

        Returns:
        - A string representation of the Function object, including its name and arguments.
        """
        # Initialize a string 'output' with the function name and an opening angle bracket
        output = f"<function {self.name}: "

        # Iterate through each argument 'a' in the list of arguments
        for a in self.args:
            # Concatenate the string representation of 'a' and a comma to 'output'
            output += str(a) + ', '

        # Remove the trailing comma and space by excluding the last two characters
        output = output[:-2]

        # Append a closing angle bracket to complete the string representation
        output += '>'
        
        # Return the final string representation of the Function object
        return output