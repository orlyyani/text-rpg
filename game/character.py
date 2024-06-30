import random
from flask import session
from collections import defaultdict
from game.items.sword import Sword
from game.items.shield import Shield
from game.items.item import Item
from game.resources.gold import Gold

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.experience = 0
        self.level = 1
        self.inventory = []
        self.inventory_counts = defaultdict(int)
        self.defending = False
        self.sword = None
        self.shield = None
        self.equipped_items = {'sword': None, 'shield': None}  # New equipped item list
        self.gold = Gold()
        self.strength = 10

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.health = data.get('health', self.health)
        self.experience = data.get('experience', self.experience)
        self.level = data.get('level', self.level)
        self.inventory = [self.deserialize_item(item) for item in data.get('inventory', [])]
        self.inventory_counts = defaultdict(int)
        for item in self.inventory:
            self.inventory_counts[item.name] += 1
        self.defending = data.get('defending', self.defending)
        sword_data = data.get('sword')
        if sword_data:
            self.sword = self.deserialize_item(sword_data)
            self.equipped_items['sword'] = self.sword
        shield_data = data.get('shield')
        if shield_data:
            self.shield = self.deserialize_item(shield_data)
            self.equipped_items['shield'] = self.shield

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
        self.inventory_counts[item.name] += 1

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                if isinstance(item, Sword):
                    if self.sword:
                        self.inventory.append(self.sword)
                        self.inventory_counts[self.sword.name] += 1
                    self.sword = item
                    self.equipped_items['sword'] = self.sword
                    message = f"{self.name} equips {item.name}!"
                elif isinstance(item, Shield):
                    if self.shield:
                        self.inventory.append(self.shield)
                        self.inventory_counts[self.shield.name] += 1
                    self.shield = item
                    self.equipped_items['shield'] = self.shield
                    message = f"{self.name} equips {item.name}!"
                else:
                    message = item.use(self)
                    if item.name == 'potion':
                        self.inventory_counts[item.name] -= 1
                        if self.inventory_counts[item.name] == 0:
                            del self.inventory_counts[item.name]
                        self.inventory.remove(item)
                return message
        return f"{item_name} not found in inventory!"

    def attack(self):
        if self.sword:
            damage = self.sword.get_damage()
            session['enemy_health'] -= damage
            durability_message = self.sword.decrease_durability()
            if self.sword.durability <= 0:
                if self.sword in self.inventory:
                    self.inventory.remove(self.sword)
                del self.inventory_counts[self.sword.name]
                self.sword = None
                return f"{self.name} attacks the enemy with a broken sword for 0 damage! {durability_message}"
            return f"{self.name} attacks the enemy with {self.sword.name} for {damage} damage! {durability_message}"
        else:
            damage = random.randint(10, 20)
            session['enemy_health'] -= damage
            return f"{self.name} attacks the enemy for {damage} damage!"
    
    def defend(self):
        health_gain = random.randint(5, 15)  # Random health gain between 5 and 15
        self.health = min(self.health + health_gain, 100)
        shield = next((item for item in self.inventory if isinstance(item, Shield)), None)
        if shield and random.random() < 0.5:  # 50% chance of repelling damage
            repel_damage = random.randint(0, shield.repel_damage)
            session['enemy_health'] = max(session['enemy_health'] - repel_damage, 0)
            return f"{self.name} defends and gains {health_gain} health! The shield also repels {repel_damage} damage back to the enemy!"
        elif shield:
            return f"{self.name} defends and gains {health_gain} health! The shield is ready to repel damage next time."
        else:
            return f"{self.name} defends and gains {health_gain} health!"

    def serialize(self):
        return {
            'name': self.name,
            'health': self.health,
            'experience': self.experience,
            'level': self.level,
            'inventory': [item.serialize() for item in self.inventory],
            'defending': self.defending,
            'sword': self.sword.serialize() if self.sword else None,
            'gold': self.gold.amount,
            'shield': self.shield.serialize() if self.shield else None,
            'equipped_items': {k: v.serialize() if v else None for k, v in self.equipped_items.items()}  # Serialize equipped item list
        }
    
    @property
    def max_health(self):
        return self.strength * 10

    @staticmethod
    def deserialize_item(item_data):
        item_type = item_data['type']
        if item_type == 'Sword':
            return Sword(item_data['name'], tuple(item_data['damage_range']), item_data['durability'])
        elif item_type == 'Shield':
            return Shield(item_data['name'], item_data['repel_damage'])
        else:
            return Item(item_data['name'])
