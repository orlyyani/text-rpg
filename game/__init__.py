from .character import Character
from .events import FindItemEvent, BattleEvent, NothingHappensEvent
import random

def create_event():
    events = [FindItemEvent(), BattleEvent(), NothingHappensEvent()]
    return random.choice(events)
