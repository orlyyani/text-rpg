import random
from flask import session

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.experience = 0
        self.level = 1
        self.inventory = []

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.health = data.get('health', self.health)
        self.experience = data.get('experience', self.experience)
        self.level = data.get('level', self.level)
        self.inventory = data.get('inventory', self.inventory)

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.health = min(self.health + 20, 100)

    def lose_health(self, amount):
        self.health -= amount

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        if item in self.inventory:
            if item == 'potion':
                self.health = min(self.health + 30, 100)
            self.inventory.remove(item)
            return f"{self.name} used a {item}!"
        return f"{item} not found in inventory!"

    def attack(self):
        damage = random.randint(10, 20)
        session['enemy_health'] -= damage
        return f"{self.name} attacks the enemy for {damage} damage!"

    def defend(self):
        self.health = min(self.health + 10, 100)
        return f"{self.name} defends and gains 10 health!"
