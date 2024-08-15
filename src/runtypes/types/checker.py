import typing

from runtypes.utilities import _assert, _assert_isinstance


class TypeChecker(object):

    def __init__(self, caster, checker=None, arguments=None, name=None) -> None:

        # Make sure the caster is callable
        _assert(callable(caster), "Caster must be callable")

        # Make sure the checker is a callable if defined
        if checker is not None:
            _assert(callable(checker), "Checker must be callable")

        # Make sure arguments are a list or none
        if arguments:
            _assert_isinstance(arguments, list)

        # Decide the name
        self._name = name or caster.__name__

        # Set internal checker and caster
        self._caster = caster
        self._checker = checker
        self._arguments = arguments or list()

    def __instancecheck__(self, value: typing.Any) -> bool:
        try:
            # Try type-checking
            self.check(value)

            # Type-checking passed
            return True
        except:
            # Type-checking failed
            return False

    def cast(self, value: typing.Any) -> typing.Any:
        # Use the caster to cast the value
        return self._caster(value, *self._arguments)

    def check(self, value: typing.Any) -> None:
        # If the type checker is defined, execute it
        if self._checker:
            # Execute type checker with arguments
            self._checker(value, *self._arguments)

            # Nothing more to do
            return
        
        # Check using the type caster
        if value != self.cast(value):
            raise TypeError(f"Casted value does not equal given value")


    def __getitem__(self, argument):
        # Make sure object is not already subscripted
        if self._arguments is not None:
            raise NotImplementedError(f"Cannot subscript an already subscripted type {self!r}")
        
        # Convert index into list
        if isinstance(argument, tuple):
            arguments = list(argument)
        else:
            arguments = [argument]

        # Return a subscripted validator
        return self.__class__(self._caster, self._checker, arguments, self._name)

    def __call__(self, value: typing.Any) -> typing.Any:
        # Try casting the value
        return self.cast(value)

    def __repr__(self) -> str:
        # Create initial representation
        representation = self._name

        # If there are any arguments, add them to the representation
        if self._arguments is not None:
            representation += repr(self._arguments)

        # Return the generated representation
        return representation


# Create lower-case name for ease-of-use
typechecker = TypeChecker
