from typing import Any

class Stack:
    def __init__(self):
        # Initialize an empty list to represent the stack.
        self._list = []

    def push(self, e: Any) -> None:
        """
        Push an element onto the stack.

        Args:
            e (Any): Element to be pushed onto the stack.
        Returns:
            None
        """
        self._list.append(e)  # Append the element to the list.

    def pop(self) -> Any:
        """
        Pop an element from the stack.

        Returns:
            Any: Element popped from the stack.
        """
        return self._list.pop()  # Pop and return the last element from the list.

    def peek(self) -> Any:
        """
        Peek at the top element of the stack without removing it.

        Returns:
            Any: Top element of the stack.
        """
        if len(self._list) == 0:
            return None  # Return None if the stack is empty.
        return self._list[-1]  # Return the last element of the list.
