# Define a class named NodeVisitor
class NodeVisitor:
    # Define a method 'visit' that takes 'self' (instance of the class) and 'node' as parameters
    def visit(self, node):
        # Create a string 'fn_name' containing the method name to be called based on the type of 'node'
        fn_name = f'visit_{type(node).__name__}'
        # Get the method with the name 'fn_name' from the class instance, or call 'no_visit_method' if not found
        fn = getattr(self, fn_name, self.no_visit_method)
        # Call the selected method with the 'node' parameter and return its result
        return fn(node)

    # Define a method 'no_visit_method' that takes 'self' and 'node' as parameters
    def no_visit_method(self, node):
        # Raise an exception indicating that the specific visit method for 'node' type was not found
        raise Exception(f'no visit_{type(node).__name__} method found')
