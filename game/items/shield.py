from .item import Item

class Shield(Item):
    def __init__(self, name, repel_damage):
        super().__init__(name)
        self.repel_damage = repel_damage

    def use(self, character):
        character.defending = True
        return f"{character.name} is now defending with {self.name}!"

    def serialize(self):
        return {
            'type': 'Shield',
            'name': self.name,
            'repel_damage': self.repel_damage
        }