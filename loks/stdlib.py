# Import necessary classes from other modules
from interpreter.types import Nil, String, Number, Array, Boolean
from .error import TypeErr, ValueErr
from typing import Union

# Define a function named loks_print that takes a list of arguments and returns Nil
def loks_print(argList: list) -> Nil:
    """
    Custom print function for the Loks language.

    Parameters:
    - argList: A list of arguments to be printed.

    Returns:
    - Nil: The result of the print operation.
    """
    # Initialize an empty string 'output' with the string representation of the first argument
    output: str = str(argList[0])

    # Check if the type of the first argument is a String
    if type(argList[0]).__name__ == "String":
        # Remove the quotes from the string representation for better formatting
        output = output[1:-1]

    # Print the formatted output without a newline character
    print(output, end='')

    # Return Nil to indicate the success of the print operation
    return Nil()

# Define a function named loks_println that takes a list of arguments and returns Nil
def loks_println(argList: list) -> Nil:
    """
    Custom println function for the Loks language.

    Parameters:
    - argList: A list of arguments to be printed.

    Returns:
    - Nil: The result of the println operation.
    """
    # Initialize an empty string 'output' with the string representation of the first argument
    output: str = str(argList[0])

    # Check if the type of the first argument is a String
    if type(argList[0]).__name__ == "String":
        # Remove the quotes from the string representation for better formatting
        output = output[1:-1]

    # Print the formatted output with a newline character
    print(output)

    # Return Nil to indicate the success of the println operation
    return Nil()


# Define a function named loks_input that takes a list of arguments and returns a String
def loks_input(argList: list) -> String:
    """
    Custom input function for the Loks language.

    Parameters:
    - argList: A list of arguments, where the first argument is expected to be a String containing the input prompt.

    Returns:
    - String: The result of the input operation.
    """
    # Extract the input prompt string from the first argument
    inpstr = argList[0].value
    
    # Use the input function with the provided prompt and wrap the result in a String object
    return String(input(inpstr))


# Define a function named loks_len that takes a list of arguments and returns a Number
def loks_len(el: list) -> Number:
    """
    Custom len function for the Loks language.

    Parameters:
    - el: A list containing a single argument, which is expected to be either a String or an Array.

    Returns:
    - Number: The result of the len operation.
    """
    # Extract the first element from the argument list
    e: Union[String, Array] = el[0]

    # Check if the type of the element is a String
    if type(e).__name__ == "String":
        # Return a Number object representing the length of the string
        return Number(len(e.value))

    # Check if the type of the element is an Array
    if type(e).__name__ == "Array":
        # Return a Number object representing the length of the array
        return Number(len(e._arr))

    # Raise a TypeErr if the argument type is neither String nor Array
    raise TypeErr(f"Invalid argument type for len, '{type(e).__name__}'")

# Define a function named loks_int that takes a list of arguments and returns a Number
def loks_int(el: list) -> Number:
    """
    Custom int conversion function for the Loks language.

    Parameters:
    - el: A list containing a single argument, which is expected to be a String or Boolean.

    Returns:
    - Number: The result of the int conversion.
    """
    # Extract the value from the first element of the argument list
    s = el[0].value

    # Check if the type of the element is a Boolean
    if type(el[0]).__name__ == "Boolean":
        # Convert "true" to 1 and "false" to 0 for boolean values
        if s == "true":
            s = 1
        if s == "false":
            s = 0

    # Attempt to convert the value to an integer
    try:
        int(s)
    except:
        # Raise a ValueErr if the conversion fails
        raise ValueErr(f"Invalid literal for conversion to int, '{s}'")
    
    # Return a Number object representing the converted integer value
    return Number(int(s))

# Define a function named loks_str that takes a list of arguments and returns a String
def loks_str(el: list) -> String:
    """
    Custom str conversion function for the Loks language.

    Parameters:
    - el: A list containing a single argument.

    Returns:
    - String: The result of the str conversion.
    """
    # Convert the first element of the argument list to a string and return a String object
    return String(str(el[0]))


# Define a function named loks_isinteger that takes a list of arguments and returns a Boolean
def loks_isinteger(el: list) -> Boolean:
    """
    Custom isinteger function for the Loks language.

    Parameters:
    - el: A list containing a single argument, which is expected to be a String.

    Returns:
    - Boolean: The result of the isinteger operation.
    """
    # Check if the type of the element is not a String
    if type(el[0]).__name__ != "String":
        # Raise a TypeErr if the argument type is not String
        raise TypeErr("Argument for 'isinteger' must be of type String")

    # Helper function to convert a boolean value to a Boolean object
    def getBoolObj(b) -> Boolean:
        if b:
            return Boolean("true")
        else:
            return Boolean("false")

    # Extract the value from the String object
    s = el[0].value

    # Check if the length of the string is zero
    if len(s) == 0:
        # Return a Boolean object representing false if the string is empty
        return Boolean("false")
    
    # Check if the string starts with '-' or '+'
    if s[0] in ('-', '+'):
        # Return a Boolean object representing whether the rest of the string is a digit
        return getBoolObj(s[1:].isdigit())

    # Return a Boolean object representing whether the entire string is a digit
    return getBoolObj(s.isdigit())

# Dictionary that maps function names to their corresponding built-in functions in the Loks language
builtinFunctionTable = {
    "print": loks_print,          # Function to print without a newline character
    "println": loks_println,      # Function to print with a newline character
    "input": loks_input,          # Function to take user input
    "len": loks_len,              # Function to get the length of a String or Array
    "int": loks_int,              # Function to convert a value to an integer
    "str": loks_str,              # Function to convert a value to a string
    "isinteger": loks_isinteger   # Function to check if a string represents an integer
}

# Dictionary that maps function names to tuples containing index and argument count information
builtinFunctionInfo = {
'''
Index: This represents the position or index of the built-in function in the Loks language. 
       For example, the "print" function has an index of 0, 
       "println" has an index of 1, and so on.

Argument Count: This indicates the number of arguments 
                expected by the corresponding built-in function. 
                For instance, the "print" function expects 1 argument, 
                "input" expects 1 argument, and "len" expects 1 argument.
'''
    "print": (0, 1),         # Index 0, 1 argument
    "println": (1, 1),       # Index 1, 1 argument
    "input": (2, 1),         # Index 2, 1 argument
    "len": (3, 1),           # Index 3, 1 argument
    "int": (4, 1),           # Index 4, 1 argument
    "str": (5, 1),           # Index 5, 1 argument
    "isinteger": (6, 1)      # Index 6, 1 argument
}

# Dictionary that maps function indices to their corresponding names
builtinFunctionIndex = {
    0: "print",        # Index 0 corresponds to the "print" function
    1: "println",      # Index 1 corresponds to the "println" function
    2: "input",        # Index 2 corresponds to the "input" function
    3: "len",          # Index 3 corresponds to the "len" function
    4: "int",          # Index 4 corresponds to the "int" function
    5: "str",          # Index 5 corresponds to the "str" function
    6: "isinteger"     # Index 6 corresponds to the "isinteger" function
}
'''
The `builtinFunctionIndex` dictionary provides a mapping between function indices and their corresponding names in the Loks language. 
This information is useful for the Loks language interpreter when it needs to identify a function by its index, 
especially in scenarios where numerical indices are used to reference built-in functions.

- 0: "print": Index 0 corresponds to the "print" function.
- 1: "println": Index 1 corresponds to the "println" function.
- 2: "input": Index 2 corresponds to the "input" function.
- 3: "len": Index 3 corresponds to the "len" function.
- 4: "int": Index 4 corresponds to the "int" function.
- 5: "str": Index 5 corresponds to the "str" function.
- 6: "isinteger": Index 6 corresponds to the "isinteger" function.
'''
