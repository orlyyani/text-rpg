import random
from flask import session

class Event:
    def apply(self, character):
        pass

class FindItemEvent(Event):
    def apply(self, character):
        items = ['sword', 'shield', 'potion', 'gold']
        item = random.choice(items)
        character.add_item(item)
        session['message'] = f'{character.name} found a {item}!'

class BattleEvent(Event):
    def apply(self, character):
        outcome = random.choice(['win', 'lose'])
        if outcome == 'win':
            exp_gain = random.randint(5, 20)
            character.gain_experience(exp_gain)
            session['message'] = f'{character.name} won the battle and gained {exp_gain} experience!'
        else:
            health_loss = random.randint(5, 20)
            character.lose_health(health_loss)
            session['message'] = f'{character.name} lost the battle and lost {health_loss} health!'

class NothingHappensEvent(Event):
    def apply(self, character):
        session['message'] = f'{character.name} travels safely without incident.'
