import os
import random
from flask import Flask, render_template, request, redirect, url_for, session
from game import Character, create_event
from game.events import BattleEvent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Required for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        character = Character(name)
        session['character'] = character.__dict__
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
        return redirect(url_for('battle'))

    session['character'] = character.__dict__
    return redirect(url_for('status'))

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)

    if request.method == 'POST':
        action = request.form['action']
        if action == 'attack':
            message = character.attack()
        elif action == 'defend':
            message = character.defend()
        elif action.startswith('use '):
            item = action.split(' ', 1)[1]
            message = character.use_item(item)
        session['message'] = message

        if session['enemy_health'] <= 0:
            exp_gain = random.randint(5, 20)
            character.gain_experience(exp_gain)
            session['message'] += f' {character.name} won the battle and gained {exp_gain} experience!'
            session.pop('enemy_health', None)
            session['character'] = character.__dict__
            return redirect(url_for('status'))

        # Enemy attacks
        enemy_damage = random.randint(5, 15)
        character.lose_health(enemy_damage)
        session['message'] += f' The enemy attacks {character.name} for {enemy_damage} damage!'

        if character.health <= 0:
            session['message'] += ' You have been defeated in battle!'
            session['character'] = character.__dict__
            return redirect(url_for('status'))

        session['character'] = character.__dict__

    return render_template('battle.html', character=character, enemy_health=session.get('enemy_health'))

@app.route('/status')
def status():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    message = session.pop('message', '')
    return render_template('status.html', character=character, message=message)

if __name__ == '__main__':
    app.run(debug=True)
