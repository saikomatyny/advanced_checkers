class TemplateException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class BoardExceptions:
    class MinimumSize(TemplateException):
        pass

    class MaxCountCheckers(TemplateException):
        pass

    class InvalidAmount(TemplateException):
        pass

class MoveExceptions:
    class OutOfBoundaries(Exception):
        def __init__(self, move):
            super().__init__(f"{move} is move out of boundaries")

    class InvalidMoveValue(Exception):
        def __init__(self, move):
            super().__init__(f"{move} is invalid. UR, UL, DL, DR is only valid values")
