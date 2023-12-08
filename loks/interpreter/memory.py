# Import the Enum class from the enum module
from enum import Enum

# Define a class named CallStack
class CallStack:
    # Constructor method, initializes an empty list 'stack'
    def __init__(self):
        self.stack = []

    # Method to push an item 'ar' onto the stack
    def push(self, ar):
        """
        Pushes the provided item onto the call stack.

        Parameters:
        - ar: The item to be pushed onto the stack.
        """
        self.stack.append(ar)

    # Method to pop and return the top item from the stack
    def pop(self):
        """
        Pops and returns the top item from the call stack.

        Returns:
        - The top item from the stack.
        """
        return self.stack.pop()

    # Method to peek and return the top item from the stack without removing it
    def peek(self):
        """
        Returns the top item from the call stack without removing it.

        Returns:
        - The top item from the stack.
        """
        return self.stack[-1]

    # Custom representation of the CallStack for easy debugging
    def __repr__(self):
        """
        Returns a string representation of the call stack for debugging purposes.

        Returns:
        - A string containing the representation of the call stack.
        """
        # Create a string 'output' as the representation header
        output = 'CALL STACK:\n'
        # Iterate through each item 'a' in the stack and append its string representation to 'output'
        for a in self.stack:
            output += str(a) + '\n'
        # Return the final representation of the CallStack
        return output

# Define a class named Environment
class Environment:
    # Constructor method, initializes an environment with an optional enclosing environment
    def __init__(self, enclosing=None) -> None:
        """
        Initializes an environment.

        Parameters:
        - enclosing: An optional enclosing environment (default is None).
        """
        self._members = dict()
        self.enclosingEnv = enclosing

    # Method to retrieve the value associated with a given name
    def get(self, name):
        """
        Retrieves the value associated with the given name from the environment.

        Parameters:
        - name: The name of the variable.

        Returns:
        - The value associated with the given name.
        """
        if self.enclosingEnv is None:
            return self._members.get(name)

        if self._members.get(name) is not None:
            return self._members.get(name)

        return self.enclosingEnv.get(name)

    # Overloaded method to retrieve the value associated with a key
    def __getitem__(self, key):
        """
        Overloaded method to retrieve the value associated with a key using the square bracket notation.

        Parameters:
        - key: The key (variable name) to retrieve the value for.

        Returns:
        - The value associated with the given key.
        """
        return self._members[key]

    # Overloaded method to set the value associated with a key
    def __setitem__(self, key, value):
        """
        Overloaded method to set the value associated with a key using the square bracket notation.

        Parameters:
        - key: The key (variable name) to set the value for.
        - value: The value to be associated with the given key.
        """
        self._members[key] = value

    # Custom string representation for easy debugging
    def __str__(self) -> str:
        """
        Returns a string representation of the environment for debugging purposes.

        Returns:
        - A string containing the representation of the environment.
        """
        output = ''
        for v in self._members:
            output += f"{v} : {self._members[v]}\n"
        return output

# Import the Enum class from the enum module
from enum import Enum

# Define an enumeration class named ARType
class ARType(Enum):
    # Method to convert the enumeration value to a string
    def __str__(self) -> str:
        """
        Returns the string representation of the enumeration value.

        Returns:
        - A string representing the value of the enumeration.
        """
        return str(self.value)

    # Enumeration values for different activation record types
    MAIN = 'main'
    FUNCTION = 'function'
    BLOCK = 'block'


# Define a class named ActivationRecord
class ActivationRecord:
    # Constructor method, initializes an activation record with a given type
    def __init__(self, typ: ARType):
        """
        Initializes an activation record with the specified type.

        Parameters:
        - typ: The type of the activation record (from the ARType enumeration).
        """
        self.name: str = str(typ)
        self.members: Environment = Environment()
        self.type: ARType = typ

    # Method to retrieve the value associated with a given name
    def get(self, name):
        """
        Retrieves the value associated with the given name from the activation record.

        Parameters:
        - name: The name of the variable.

        Returns:
        - The value associated with the given name.
        """
        return self.members.get(name)

    # Overloaded method to retrieve the value associated with a key
    def __getitem__(self, key):
        """
        Overloaded method to retrieve the value associated with a key using the square bracket notation.

        Parameters:
        - key: The key (variable name) to retrieve the value for.

        Returns:
        - The value associated with the given key.
        """
        return self.members[key]

    # Overloaded method to set the value associated with a key
    def __setitem__(self, key, value):
        """
        Overloaded method to set the value associated with a key using the square bracket notation.

        Parameters:
        - key: The key (variable name) to set the value for.
        - value: The value to be associated with the given key.
        """
        self.members[key] = value

    # Method to set the enclosing environment for the activation record
    def setEnclosingEnv(self, env: Environment) -> None:
        """
        Sets the enclosing environment for the activation record.

        Parameters:
        - env: The enclosing environment.
        """
        self.members.enclosingEnv = env

    # Custom string representation for easy debugging
    def __repr__(self):
        """
        Returns a string representation of the activation record for debugging purposes.

        Returns:
        - A string containing the representation of the activation record.
        """
        output = f"AR {self.name}:\n{str(self.members)}"
        return output

    # String representation (calls __repr__) for ease of use
    def __str__(self):
        return self.__repr__()