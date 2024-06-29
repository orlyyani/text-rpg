from flask import Blueprint, request, session
from game.character import Character
from game.items.sword import Sword
from game.items.shield import Shield

game_bp = Blueprint('game', __name__)

@game_bp.route('/create_character', methods=['POST'])
def create_character():
    data = request.json
    character = Character(data['name'])
    session['character'] = character.__dict__
    return {"message": f"Character {character.name} created!"}, 201

@game_bp.route('/use_item', methods=['POST'])
def use_item():
    data = request.json
    item_name = data['item']
    character_data = session.get('character')
    if not character_data:
        return {"message": "Character not found in session"}, 404

    character = Character(character_data['name'])
    character.update_from_dict(character_data)
    result = character.use_item(item_name)
    session['character'] = character.__dict__
    return {"message": result}, 200

@game_bp.route('/attack', methods=['POST'])
def attack():
    character_data = session.get('character')
    if not character_data:
        return {"message": "Character not found in session"}, 404

    character = Character(character_data['name'])
    character.update_from_dict(character_data)
    result = character.attack()
    session['character'] = character.__dict__
    return {"message": result}, 200

@game_bp.route('/defend', methods=['POST'])
def defend():
    character_data = session.get('character')
    if not character_data:
        return {"message": "Character not found in session"}, 404

    character = Character(character_data['name'])
    character.update_from_dict(character_data)
    result = character.defend()
    session['character'] = character.__dict__
    return {"message": result}, 200
