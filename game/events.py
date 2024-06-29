import random
from flask import session

class Event:
    def apply(self, character):
        pass

class FindItemEvent(Event):
    def apply(self, character):
        items = ['sword_of_light', 'sword_of_fire', 'sword_of_ice', 'shield', 'potion', 'gold']
        item = random.choice(items)
        character.add_item(item)
        session['message'] = f'{character.name} found a {item}!'

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