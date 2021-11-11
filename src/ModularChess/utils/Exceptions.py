class ModularChessException(Exception):
    pass


class InvalidMoveException(ModularChessException):
    pass


class InvalidPositionError(ModularChessException, IndexError):
    pass


class InvalidArgumentsError(ModularChessException, ValueError):
    pass


class TimerError(ModularChessException):
    pass


class InvalidPathException(ModularChessException):
    pass
