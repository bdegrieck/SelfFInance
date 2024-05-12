class TickerDoesNotExist(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EnterTickerInstead(Exception):
    def __init__(self, message:str):
        super().__init__(message)


class SameTickers(Exception):
    def __init__(self, message:str):
        super().__init__(message)


class InsufficientData(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EmptyInput(Exception):
    def __init__(self, message:str):
        super().__init__(message)
