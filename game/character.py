import random
from flask import session
from game.items.sword import Sword
from game.items.shield import Shield
from game.items.item import Item

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.experience = 0
        self.level = 1
        self.inventory = []
        self.defending = False
        self.sword = None

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.health = data.get('health', self.health)
        self.experience = data.get('experience', self.experience)
        self.level = data.get('level', self.level)
        self.inventory = [self.deserialize_item(item) for item in data.get('inventory', [])]
        self.defending = data.get('defending', self.defending)
        sword_data = data.get('sword')
        if sword_data:
            self.sword = self.deserialize_item(sword_data)

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.health = min(self.health + 20, 100)

    def lose_health(self, amount):
        if self.defending:
            amount //= 2
            self.defending = False
        self.health -= amount

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                message = item.use(self)
                self.inventory.remove(item)
                return message
        return f"{item_name} not found in inventory!"

    def attack(self):
        if self.sword:
            damage = self.sword.get_damage()
            session['enemy_health'] -= damage
            durability_message = self.sword.decrease_durability(self)
            return f"{self.name} attacks the enemy with {self.sword.name} for {damage} damage! {durability_message}"
        else:
            damage = random.randint(10, 20)
            session['enemy_health'] -= damage
            return f"{self.name} attacks the enemy for {damage} damage!"

    def defend(self):
        self.health = min(self.health + 10, 100)
        return f"{self.name} defends and gains 10 health!"

    def serialize(self):
        return {
            'name': self.name,
            'health': self.health,
            'experience': self.experience,
            'level': self.level,
            'inventory': [item.serialize() for item in self.inventory],
            'defending': self.defending,
            'sword': self.sword.serialize() if self.sword else None
        }

    @staticmethod
    def deserialize_item(item_data):
        item_type = item_data['type']
        if item_type == 'Sword':
            return Sword(item_data['name'], tuple(item_data['damage_range']), item_data['durability'])
        elif item_type == 'Shield':
            return Shield(item_data['name'])
        else:
            return Item(item_data['name'])
