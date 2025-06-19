class BoardExceptions:
    class TemplateException(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    class MinimumSize(TemplateException):
        pass

    class MaxCountCheckers(TemplateException):
        pass

    class InvalidAmount(TemplateException):
        pass
