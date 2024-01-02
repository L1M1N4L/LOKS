from typing import List

# Base class representing a symbol
class Symbol:
    def __init__(self, n: str, t: str = None) -> None:
        """
        Initialize a Symbol object.

        :param n: Name of the symbol.
        :param t: Type of the symbol (default is None).
        """
        self.name: str = n
        self.type: Symbol = t

    def __str__(self) -> str:
        """
        Return a string representation of the symbol.

        :return: String representation of the symbol.
        """
        if self.type is not None:
            return f"<{self.type}:{self.name}>"
        return f"<{self.name}>"

    def __repr__(self) -> str:
        """
        Return a string representation of the symbol for debugging.

        :return: String representation of the symbol.
        """
        return self.__str__()


# Derived class representing a type symbol
class TypeSymbol(Symbol):
    def __init__(self, t: str) -> None:
        """
        Initialize a TypeSymbol object.

        :param t: Type of the symbol.
        """
        super().__init__(t)

# Derived class representing a variable symbol
class VariableSymbol(Symbol):
    def __init__(self, n: str) -> None:
        """
        Initialize a VariableSymbol object.

        :param n: Name of the variable symbol.
        """
        # Call the constructor of the base class (Symbol)
        super().__init__(n, "variable")

    def setType(self, t: TypeSymbol) -> None:
        """
        Set the type of the variable symbol.

        :param t: Type of the variable symbol.
        :return: None
        """
        # Set the type of the variable symbol
        self.type = t


# Derived class representing a function symbol
class FunctionSymbol(Symbol):
    def __init__(self, n: str, b, args: List[Symbol] = []) -> None:
        """
        Initialize a FunctionSymbol object.

        :param n: Name of the function symbol.
        :param b: Block associated with the function symbol.
        :param args: List of symbols representing function arguments (default is an empty list).
        """
        # Call the constructor of the base class (Symbol)
        super().__init__(n, "function")
        # Assign the block associated with the function symbol
        self.block = b
        # Assign the list of symbols representing function arguments
        self.argSymbols: List[Symbol] = args


# Class representing a symbol table
class SymbolTable:
    def __init__(self, n: str) -> None:
        """
        Initialize a SymbolTable object.

        :param n: Name of the symbol table.
        """
        # Assign the name of the symbol table
        self.name: str = n
        # Initialize an empty dictionary to store symbols
        self._table = dict()
        # Initialize the enclosing symbol table to None
        self._enclosingTable: SymbolTable = None

    def get(self, s: str, restrict=False) -> Symbol:
        """
        Get a symbol from the symbol table.

        :param s: Name of the symbol to retrieve.
        :param restrict: Flag to restrict the search to the current table only (default is False).
        :return: The symbol if found, otherwise None.
        """
        # If the search is restricted to the current table only
        if restrict:
            return self._table.get(s)

        # If the symbol is found in the current table, return it
        if self._table.get(s) is not None:
            return self._table.get(s)

        # If the current table does not contain the symbol and there is an enclosing table
        if self._enclosingTable is not None:
            # Recursively search in the enclosing table
            return self._enclosingTable.get(s)

        # If the symbol is not found and there is no enclosing table, return None
        return None

    def add(self, s: Symbol) -> None:
        """
        Add a symbol to the symbol table.

        :param s: The symbol to be added.
        :return: None
        """
        # Add the symbol to the table with its name as the key
        self._table[s.name] = s

    def setEnclosingScope(self, s) -> None:
        """
        Set the enclosing scope of the symbol table.

        :param s: The symbol table to be set as the enclosing scope.
        :return: None
        """
        # Set the given symbol table as the enclosing scope
        self._enclosingTable = s

    def getEnclosingScope(self):
        """
        Get the enclosing scope of the symbol table.

        :return: The enclosing symbol table.
        """
        # Return the enclosing symbol table
        return self._enclosingTable

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the symbol table.

        :return: A string representation of the symbol table.
        """
        # Initialize an empty string to store the output
        output = ""
        
        # Iterate through each element in the table
        for e in self._table:
            # Append the string representation of the symbol and its name to the output
            output += f"{self._table[e]}: {e}\n"

        # Return the final string representation
        return output


    def __repr__(self) -> str:
        """
        Return a string representation of the symbol table for debugging.

        :return: A string representation of the symbol table.
        """
        # Call the __str__ method to get the string representation
        return self.__str__()