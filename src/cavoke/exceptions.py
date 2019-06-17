class GameError(Exception):
    "Base exception used by this module."
    pass


class GameWarning(Warning):
    "Base warning used by this module."
    pass


class NoCanvasError(GameError):
    "Exception raised when game is executed without a canvas."
    pass


class NoCanvasWarning(GameWarning):
    "Warning raised when unit is used without a canvas."
    pass


class UnitCanvasOverride(GameWarning):
    "Warning raised when unit with already configured canvas gets added to another canvas"
    def __init__(self, unit, newCanvas):
        self.message = repr(newCanvas) + " was attempted to be linked to " + repr(unit) + " already linked to a canvas."

    def __repr__(self):
        return self.message


class CanvasUnitsCountExceeded(GameWarning):
    "Warning raised when too many units on canvas."
    pass