from runtypes.typechecker import TypeChecker


class TypeCaster(TypeChecker):

    def __instancecheck__(self, value):
        try:
            # Try type-checking
            result = self.__call__(value)

            # Check whether the result equals the value
            return result == value
        except:
            # Type-checking failed
            return False


# Create lower-case name for ease-of-use
typecaster = TypeCaster
