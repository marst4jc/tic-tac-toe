"""Stub implementations of Django model classes."""

class Field:
    """Base placeholder for model fields."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class BigAutoField(Field):
    """Placeholder for BigAutoField used in AppConfig."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
