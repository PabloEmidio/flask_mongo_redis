class DatabaseNotVoid(Exception):
    def __init__(self, msg: str=None):
        msg = msg or 'Your database is not void'
        super().__init__(msg)

class CollectionNotVoid(Exception):
    def __init__(self, msg: str=None):
        msg = msg or 'Your collection is not void'
        super().__init__(msg)

class BadTestPracticeError(Exception):
    def __init__(self, msg: str=None):
        msg = msg or 'You are not following project test rules'
        super().__init__(msg)