from .character import Character
from .events import FindItemEvent, BattleEvent, NothingHappensEvent, RestEvent
import random

def create_event():
    events = [FindItemEvent(), BattleEvent(), NothingHappensEvent(), RestEvent()]
    return random.choice(events)