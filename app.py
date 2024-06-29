from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.experience = 0
        self.inventory = []

    def travel(self):
        event = random.choice(['find_item', 'battle', 'nothing'])
        if event == 'find_item':
            self.find_item()
        elif event == 'battle':
            self.battle()
        elif event == 'nothing':
            self.nothing_happens()

    def find_item(self):
        items = ['sword', 'shield', 'potion', 'gold']
        item = random.choice(items)
        self.inventory.append(item)
        session['message'] = f'{self.name} found a {item}!'

    def battle(self):
        outcome = random.choice(['win', 'lose'])
        if outcome == 'win':
            exp_gain = random.randint(5, 20)
            self.experience += exp_gain
            session['message'] = f'{self.name} won the battle and gained {exp_gain} experience!'
        else:
            health_loss = random.randint(5, 20)
            self.health -= health_loss
            session['message'] = f'{self.name} lost the battle and lost {health_loss} health!'

    def nothing_happens(self):
        session['message'] = f'{self.name} travels safely without incident.'

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.health = data.get('health', self.health)
        self.experience = data.get('experience', self.experience)
        self.inventory = data.get('inventory', self.inventory)

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
    character.travel()
    session['character'] = character.__dict__
    return redirect(url_for('status'))

@app.route('/status')
def status():
    character_data = session.get('character', {})
    character = Character(character_data.get('name', ''))
    character.update_from_dict(character_data)
    message = session.pop('message', '')
    return render_template('status.html', character=character, message=message)

if __name__ == '__main__':
    app.run(debug=True)

