from .item import Item
import random

class Sword(Item):
    def __init__(self, name, damage_range, durability):
        super().__init__(name)
        self.damage_range = damage_range
        self.durability = durability

    def get_damage(self):
        return random.randint(*self.damage_range)

    def use(self, character):
        character.sword = self
        return f"{character.name} equipped {self.name}!"

    def decrease_durability(self, character):
        self.durability -= 1
        if self.durability <= 0:
            character.inventory.remove(self)
            character.sword = None
            return f"{self.name} broke and was removed from the inventory!"
        return f"{self.name} durability decreased to {self.durability}."

    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'damage_range': self.damage_range,
            'durability': self.durability
        }
