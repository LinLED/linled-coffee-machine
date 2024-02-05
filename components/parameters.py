class Parameter:
    def __init__(self, state=False, display_name=""):
        self.state = state
        self.display_name = display_name


class GlobalParameters:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instantiation already exists!")

    def addParameter(self, key, state=False, display_name=""):
        setattr(self, key, Parameter(state, display_name))
