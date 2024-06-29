import os
from flask import Flask, render_template, request, redirect, url_for, session
from game import Character, create_event
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
    
    session['character'] = character.__dict__
    return redirect(url_for('status'))

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)

    if request.method == 'POST':
        item = request.form['item']
        message = character.use_item(item)
        session['character'] = character.__dict__
        session['message'] = message
        return redirect(url_for('status'))

    return render_template('battle.html', character=character)

@app.route('/status')
def status():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    message = session.pop('message', '')
    return render_template('status.html', character=character, message=message)

if __name__ == '__main__':
    app.run(debug=True)
