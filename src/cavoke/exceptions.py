class GameError(Exception):
    "Base exception used by this module."
    pass


class GameWarning(Warning):
    "Base warning used by this module."
    pass


class NoGameWarning(GameWarning):
    "Warning raised when unit is used without a game."
    pass


class UnitGameOverrideWarning(GameWarning):
    "Warning raised when unit with already configured game gets added to another game"
    def __init__(self, unit, newGame):
        self.message = repr(newGame) + " was attempted to be linked to " + repr(unit) + " already linked to a game."

    def __repr__(self):
        return self.message


class GameUnitsCountExceededWarning(GameWarning):
    "Warning raised when there are too many units in one game"
    pass


class GameUnitsArrayTypeWarning(GameWarning):
    "Warning raised when there is a non-UnitInfo object in Game units storage"
    pass


class GameAddUnitDepthExceededWarning(GameWarning):
    "Warning raised when depth of added unit-list is too big"
    pass


class GameCreatorFunctionIncorrectReturnTypeError(GameError):
    "Exception raised when creator-written function returns the type that differs from expected one"

    def __init__(self, result, expected_type: str):
        self.message = "Expected type: " + expected_type + ", got: " + repr(result) + " - which type is " +\
                       repr(type(result).__name__) + " (" + repr(type(result))

    def __repr__(self):
        return self.message


class UnitNotFoundError(GameError):
    "Exception raised when no unit matches search parameters in a game."
    pass
