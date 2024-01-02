from enum import Enum

class opcode(Enum):
    END = 0xff

    # Load constants
    LOAD_NIL = 0x01
    LOAD_TRUE = 0x02
    LOAD_FALSE = 0x03
    LOAD_CONST = 0x64  # arg = u8 x2

    # Binary operations
    BINARY_ADD = 0x17
    BINARY_SUBTRACT = 0x18
    BINARY_MULTIPLY = 0x14
    BINARY_DIVIDE = 0x15
    BINARY_MODULO = 0x16
    BINARY_AND = 0x40
    BINARY_OR = 0x42

    # Unary operations
    UNARY_NOT = 0x0c
    UNARY_NEGATIVE = 0x0b
    
    # Store operations
    STORE_LOCAL = 0x5a  # arg = u8
    STORE_GLOBAL = 0x61

    # Push constant onto the stack
    BIPUSH = 0x10  # arg = u8

    # Load variable onto the stack
    LOAD_LOCAL = 0x52   # arg = u8
    LOAD_GLOBAL = 0x74   # arg = u8

    # List operations
    BUILD_LIST = 0x67  # arg = u8 x2
    BINARY_SUBSCR = 0x19
    STORE_SUBSCR = 0x3c

    # Comparison operations
    CMPEQ = 0x9f
    CMPNE = 0xa0
    CMPGT = 0xa3
    CMPLT = 0xa1
    CMPGE = 0xa2
    CMPLE = 0xa4

    # Jump and conditional jump operations
    POP_JMP_IF_TRUE = 0x70  # arg = u8 x2
    POP_JMP_IF_FALSE = 0x6f  # arg = u8 x2
    GOTO = 0xa7

    # Function call and return
    CALL_FUNCTION = 0x83  # arg = u8
    CALL_NATIVE = 0x84  # arg = u8
    RETURN_VALUE = 0x53

def makeOpcodeDict():
    """
    Create a dictionary mapping opcode values to their corresponding names.

    :return: Dictionary mapping opcode values to their names.
    """
    d = {}

    # Iterate over each opcode in the enumeration
    for o in list(opcode):
        # Map the opcode value to its name
        d[o.value] = o.name

    return d

def makeOpcodeNameDict():
    """
    Create a dictionary mapping opcode names to their corresponding values.

    :return: Dictionary mapping opcode names to their values.
    """
    d = {}

    # Iterate over each opcode in the enumeration
    for o in opcode:
        # Map the opcode name to its value
        d[o.name] = o.value

    return d

# Create a dictionary mapping opcode values to their corresponding names
opcodeDict = makeOpcodeDict()

# Create a dictionary mapping opcode names to their corresponding values
opcodeNameDict = makeOpcodeNameDict()

# Create a dictionary mapping opcode names to their sizes (in bytes) in the bytecode
opcodeSizeDict = {
    "END" : 1,
    "LOAD_NIL" : 1,
    "LOAD_TRUE" : 1,
    "LOAD_FALSE" : 1,
    "LOAD_CONST" : 3,  # arg: u8 x2

    "BINARY_ADD" : 1,
    "BINARY_SUBTRACT" : 1,
    "BINARY_MULTIPLY" : 1,
    "BINARY_DIVIDE" : 1,
    "BINARY_MODULO" : 1,
    "UNARY_NOT": 1,
    "UNARY_NEGATIVE": 1,
    "BINARY_AND": 1,
    "BINARY_OR": 1,
    
    # arg: u8
    "STORE_LOCAL" : 2,
    "STORE_GLOBAL" : 2,

    "BIPUSH" : 2 ,  # arg: u8
    "LOAD_LOCAL" : 2,   # arg: u8
    "LOAD_GLOBAL" : 2,   # arg: u8

    "BUILD_LIST" : 3,  # arg: u8 x2
    "BINARY_SUBSCR" : 1,  # arg: u8 x2
    "STORE_SUBSCR": 1,

    "CMPEQ" : 1,
    "CMPNE" : 1,
    "CMPGT" : 1,
    "CMPLT" : 1,
    "CMPGE" : 1,
    "CMPLE" : 1,

    # arg: u8 x2
    "POP_JMP_IF_TRUE" : 3,
    "POP_JMP_IF_FALSE" : 3,
    "GOTO" : 3,

    "CALL_FUNCTION" : 2,  # arg: u8
    "CALL_NATIVE": 2,
    "RETURN_VALUE" : 1,
}