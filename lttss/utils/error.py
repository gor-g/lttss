


class PlaceholderMethodError(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = "This is a placeholder method and must be implemented by a subclass."
        else:
            self.message = message

    def __str__(self):
        return self.message
