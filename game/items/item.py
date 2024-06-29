class Item:
    def __init__(self, name):
        self.name = name

    def use(self, character):
        pass

    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name
        }
