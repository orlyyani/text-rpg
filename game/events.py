import random
from flask import session
from game.items.sword import Sword
from game.items.shield import Shield
from game.items.item import Item

class Event:
    def apply(self, character):
        pass

class FindItemEvent(Event):
    def apply(self, character):
        items = [
            Sword('sword_of_light', (15, 25), 10),
            Sword('sword_of_fire', (20, 30), 8),
            Sword('sword_of_ice', (25, 35), 6),
            Shield('shield'),
            Item('potion'),
            Item('gold')
        ]
        item = random.choice(items)
        character.add_item(item)
        session['message'] = f'{character.name} found a {item.name}!'

class BattleEvent(Event):
    def apply(self, character):
        # Initialize battle state
        session['enemy_health'] = 100
        session['message'] = f'{character.name} encountered an enemy! Prepare for battle.'

class NothingHappensEvent(Event):
    def apply(self, character):
        session['message'] = f'{character.name} travels safely without incident.'

class RestEvent(Event):
    def apply(self, character):
        character.health = min(character.health + 50, 100)  # Regain health
        session['message'] = f'{character.name} rested in a nearby town and regained health!'

def create_event():
    events = [FindItemEvent(), BattleEvent(), NothingHappensEvent(), RestEvent()]
    return random.choice(events)
