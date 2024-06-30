import os
import random
from flask import Flask, render_template, request, redirect, url_for, session
from game.character import Character
from game.events import create_event, BattleEvent, RestEvent
from controllers.game_controller import game_bp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Required for session management

# Register the game blueprint
app.register_blueprint(game_bp, url_prefix='/game')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        character = Character(name)
        session['character'] = character.serialize()
        return redirect(url_for('status'))
    return render_template('index.html')

@app.route('/travel')
def travel():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    
    event = create_event()
    event.apply(character)
    
    if isinstance(event, BattleEvent):
        session['enemy_health'] = 100  # Initialize enemy health
        return redirect(url_for('battle'))
    elif isinstance(event, RestEvent):
        return redirect(url_for('status'))  # Go back to status page after resting
    session['character'] = character.serialize()
    return redirect(url_for('status'))

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)

    if 'battle_log' not in session:
        session['battle_log'] = ['Prepare for battle!']

    if request.method == 'POST':
        action = request.form['action']
        if action == 'attack':
            message = character.attack()
        elif action == 'defend':
            message = character.defend()
        elif action.startswith('use '):
            item = action.split(' ', 1)[1]
            message = character.use_item(item)
        session['battle_log'].append(f'{character.name} {message}')

        if session['enemy_health'] <= 0:
            exp_gain = random.randint(5, 20)
            character.gain_experience(exp_gain)
            session['battle_log'].append(f'{character.name} won the battle and gained {exp_gain} experience!')
            session['message'] = f'{character.name} won the battle and gained {exp_gain} experience!'
            session.pop('enemy_health', None)
            session['character'] = character.serialize()
            session['battle_log'] = []
            return redirect(url_for('status'))

        # Enemy attacks
        enemy_damage = random.randint(5, 15)
        character.lose_health(enemy_damage)
        session['battle_log'].append(f'The enemy attacks {character.name} for {enemy_damage} damage!')

        if character.health <= 0:
            session['battle_log'].append('You have been defeated in battle!')
            session['character'] = character.serialize()
            return redirect(url_for('status'))

        session['character'] = character.serialize()

    return render_template('battle.html', character=character, enemy_health=session.get('enemy_health'), battle_log=session['battle_log'])

@app.route('/status')
def status():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    message = session.pop('message', '')
    return render_template('status.html', character=character, message=message)

@app.route('/rest')
def rest():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    
    event = RestEvent()
    event.apply(character)
    
    session['character'] = character.serialize()
    return redirect(url_for('status'))

if __name__ == '__main__':
    app.run(debug=True)
