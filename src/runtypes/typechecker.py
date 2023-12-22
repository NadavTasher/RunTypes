class TypeChecker(object):

    def __init__(self, function, arguments=None):
        # Make sure the function is a callable
        if not callable(function):
            raise TypeError("Function must be callable")

        # Make sure arguments are a list or none
        if arguments and not isinstance(arguments, list):
            raise TypeError("Arguments must be a list")

        # Set the internal target function
        self._target_function = function
        self._target_arguments = arguments or list()

    def __instancecheck__(self, value):
        try:
            # Try type-checking
            self.__call__(value)

            # Type-checking passed
            return True
        except:
            # Type-checking failed
            return False

    def __getitem__(self, argument):
        # Convert index into list
        if isinstance(argument, tuple):
            arguments = list(argument)
        else:
            arguments = [argument]

        # Return a partial validator
        return TypeChecker(self._target_function, self._target_arguments + arguments)

    def __call__(self, value):
        # Call the target function with all required arguments
        return self._target_function(value, *self._target_arguments)

    def __repr__(self):
        # Create initial representation
        representation = self._target_function.__name__

        # If there are any arguments, add them to the representation
        if self._target_arguments:
            representation += repr(self._target_arguments)

        # Return the generated representation
        return representation


# Create lower-case name for ease-of-use
typechecker = TypeChecker
