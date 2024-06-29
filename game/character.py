import random
from flask import session

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
        if self.defending:
            amount //= 2
            self.defending = False
        self.health -= amount

    def add_item(self, item):
        self.inventory.append(item)

    def use_item(self, item):
        if item in self.inventory:
            if item == 'potion':
                self.health = min(self.health + 30, 100)
            elif item == 'shield':
                self.defending = True
            elif item.startswith('sword'):
                self.sword = item
            self.inventory.remove(item)
            return f"{self.name} used a {item}!"
        return f"{item} not found in inventory!"

    def attack(self):
        if self.sword:
            damage = self.get_sword_damage()
            session['enemy_health'] -= damage
            self.sword_durability -= 1  # Decrease sword durability
            if self.sword_durability <= 0:
                self.inventory.remove(self.sword)  # Remove sword from inventory if durability reaches 0
                self.sword = None
            return f"{self.name} attacks the enemy with {self.sword} for {damage} damage!"
        else:
            damage = random.randint(10, 20)
            session['enemy_health'] -= damage
            return f"{self.name} attacks the enemy for {damage} damage!"

    def defend(self):
        self.health = min(self.health + 10, 100)
        return f"{self.name} defends and gains 10 health!"

    def get_sword_damage(self):
        if self.sword == 'sword_of_light':
            return random.randint(15, 25)
        elif self.sword == 'sword_of_fire':
            return random.randint(20, 30)
        elif self.sword == 'sword_of_ice':
            return random.randint(25, 35)
        else:
            return random.randint(10, 20)

    def add_sword(self, sword):
        self.inventory.append(sword)
        if sword == 'sword_of_light':
            self.sword_durability = 10
        elif sword == 'sword_of_fire':
            self.sword_durability = 8
        elif sword == 'sword_of_ice':
            self.sword_durability = 6
