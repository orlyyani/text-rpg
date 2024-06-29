from .item import Item

class Shield(Item):
    def use(self, character):
        character.defending = True
        return f"{character.name} is now defending with {self.name}!"
