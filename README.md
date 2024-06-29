# Text-Based RPG Web Application

This is a simple text-based RPG web application built with Flask. Players can create a character, travel to different locations, encounter random events, gain experience, and use items during battles.

## Features

- Character creation with name, health, experience, level, and inventory.
- Random events: find items, battle, and safe travels.
- Leveling system: gain experience, level up, and reset experience.
- Item usage during battles.
- Environment variable support for secret key.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/text_rpg_web.git
    cd text_rpg_web
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project directory and add your secret key:**

    ```plaintext
    SECRET_KEY=your_secret_key
    ```

5. **Run the Flask application:**

    ```sh
    python app.py
    ```

6. **Open your web browser and go to:**

    ```
    http://127.0.0.1:5000/
    ```

## Project Structure

```
text_rpg_web/
├── app.py
├── game/
│ ├── init.py
│ ├── character.py
│ └── events.py
├── templates/
│ ├── index.html
│ ├── status.html
│ └── battle.html
├── .env
├── requirements.txt
└── README.md
```


## Usage

1. **Start the game by entering your character's name.**
2. **Travel to encounter random events:**
    - Find items to add to your inventory.
    - Battle enemies and gain experience or lose health.
    - Travel safely without any incidents.
3. **Level up by gaining experience.**
4. **Use items from your inventory during battles.**

## Dependencies

- Flask
- python-dotenv

## License

This project is licensed under the MIT License.
