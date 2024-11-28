from flask import Flask, request, session, redirect, render_template_string
import random

# Create Flask app
app = Flask(__name__)
app.secret_key = "secret_key"  # Required for session management

# Words for the game and their clues
WORD_CLUES = {
    "python": ["It's a programming language.", "It is named after a snake.", "Used for web development, AI, and more."],
    "flask": ["A Python web framework.", "Lightweight and easy to use.", "Often compared to Django."],
    "developer": ["A person who writes code.", "Another term for programmer.", "They build software or apps."],
    "algorithm": ["A step-by-step process.", "Used in programming and problem-solving.", "Basis for many computer operations."],
    "programming": ["The act of writing code.", "Involves logic and problem-solving.", "A key skill for developers."]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session or "reset" in request.args:
        word = random.choice(list(WORD_CLUES.keys()))  # Randomly pick a word
        session["word"] = word
        session["clues"] = WORD_CLUES[word]  # Assign clues for the word
        session["guesses"] = []  # Correct guesses
        session["wrong_guesses"] = []  # Incorrect guesses
        session["attempts"] = 6  # Number of tries left
        session["game_over"] = False

    # Handle the player's guess
    if request.method == "POST":
        guess = request.form["guess"].lower()

        if session["game_over"]:
            return redirect("/")  # Restart game if it's already over

        # Validate the guess
        if guess.isalpha():
            if guess == session["word"]:  # User guessed the entire word correctly
                session["guesses"] = list(session["word"])  # Reveal the full word
                session["game_over"] = "win"
            else:
                # If it's a single letter, handle as a character guess
                if len(guess) == 1:
                    if guess in session["word"]:
                        if guess not in session["guesses"]:
                            session["guesses"].append(guess)
                    else:
                        if guess not in session["wrong_guesses"]:
                            session["wrong_guesses"].append(guess)
                            session["attempts"] -= 1
                else:
                    # For incorrect word guesses
                    session["wrong_guesses"].append(guess)
                    session["attempts"] -= 1

        # Check win/lose conditions
        if all(letter in session["guesses"] for letter in session["word"]):
            session["game_over"] = "win"
        elif session["attempts"] <= 0:
            session["game_over"] = "lose"

        return redirect("/")  # Refresh the page after guessing

    # Display the word with guessed letters revealed
    masked_word = " ".join([letter if letter in session["guesses"] else "_" for letter in session["word"]])

    # Ensure the "clues" key exists in the session
    if "clues" in session:
        clue_index = len(session["wrong_guesses"]) - 1
        current_clue = (
            session["clues"][clue_index]
            if clue_index >= 0 and clue_index < len(session["clues"])
            else "No more clues available!"
        )
    else:
        current_clue = "No clues available!"

    # HTML Template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Word Guessing Game</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #343a40;
            }
            .word {
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 5px;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                padding: 10px;
                font-size: 16px;
                width: 100px;
                text-align: center;
                margin-right: 10px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                color: #ffffff;
                background: #007bff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
            h2 {
                color: #28a745;
            }
            h2 + a {
                text-decoration: none;
                color: #007bff;
            }
            h2 + a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Word Guessing Game</h1>
            <p>Word: <span class="word">{{ masked_word }}</span></p>
            <p>Attempts Remaining: {{ attempts }}</p>
            <p>Wrong Guesses: {{ wrong_guesses|join(", ") }}</p>
            <p>Clue: {{ current_clue }}</p>

            {% if game_over == "win" %}
                <h2>🎉 You Win! The word was "{{ correct_word }}"</h2>
                <a href="/?reset=1">Play Again</a>
            {% elif game_over == "lose" %}
                <h2>😢 You Lost! The word was "{{ correct_word }}"</h2>
                <a href="/?reset=1">Try Again</a>
            {% else %}
                <form method="POST">
                    <label for="guess">Enter a Letter or Word:</label>
                    <input type="text" id="guess" name="guess" required>
                    <button type="submit">Guess</button>
                </form>
            {% endif %}
        </div>
    </body>
    </html>
    """

    # Render the HTML with variables
    return render_template_string(
        html_template,
        masked_word=masked_word,
        attempts=session["attempts"],
        wrong_guesses=session["wrong_guesses"],
        current_clue=current_clue,
        game_over=session["game_over"],
        correct_word=session["word"]
    )
    # Start a new game if the session doesn't have a word or user resets
    if "word" not in session or "reset" in request.args:
        word = random.choice(list(WORD_CLUES.keys()))  # Randomly pick a word
        session["word"] = word
        session["clues"] = WORD_CLUES[word]  # Assign clues for the word
        session["guesses"] = []  # Correct guesses
        session["wrong_guesses"] = []  # Incorrect guesses
        session["attempts"] = 6  # Number of tries left
        session["game_over"] = False

    # Handle the player's guess
    if request.method == "POST":
        guess = request.form["guess"].lower()

        if session["game_over"]:
            return redirect("/")  # Restart game if it's already over

        # Validate the guess
        if guess.isalpha():
            if guess == session["word"]:  # User guessed the entire word correctly
                session["guesses"] = list(session["word"])  # Reveal the full word
                session["game_over"] = "win"
            else:
                # If it's a single letter, handle as a character guess
                if len(guess) == 1:
                    if guess in session["word"]:
                        if guess not in session["guesses"]:
                            session["guesses"].append(guess)
                    else:
                        if guess not in session["wrong_guesses"]:
                            session["wrong_guesses"].append(guess)
                            session["attempts"] -= 1
                else:
                    # For incorrect word guesses
                    session["wrong_guesses"].append(guess)
                    session["attempts"] -= 1

        # Check win/lose conditions
        if all(letter in session["guesses"] for letter in session["word"]):
            session["game_over"] = "win"
        elif session["attempts"] <= 0:
            session["game_over"] = "lose"

        return redirect("/")  # Refresh the page after guessing

    # Display the word with guessed letters revealed
    masked_word = " ".join([letter if letter in session["guesses"] else "_" for letter in session["word"]])

    # Determine the current clue to show
    clue_index = len(session["wrong_guesses"]) - 1
    current_clue = session["clues"][clue_index] if clue_index >= 0 and clue_index < len(session["clues"]) else "No more clues available!"

    # HTML Template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Word Guessing Game</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #343a40;
            }
            .word {
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 5px;
            }
            form {
                margin-top: 20px;
            }
            input[type="text"] {
                padding: 10px;
                font-size: 16px;
                width: 100px;
                text-align: center;
                margin-right: 10px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                color: #ffffff;
                background: #007bff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
            h2 {
                color: #28a745;
            }
            h2 + a {
                text-decoration: none;
                color: #007bff;
            }
            h2 + a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Word Guessing Game</h1>
            <p>Word: <span class="word">{{ masked_word }}</span></p>
            <p>Attempts Remaining: {{ attempts }}</p>
            <p>Wrong Guesses: {{ wrong_guesses|join(", ") }}</p>
            <p>Clue: {{ current_clue }}</p>

            {% if game_over == "win" %}
                <h2>🎉 You Win! The word was "{{ correct_word }}"</h2>
                <a href="/?reset=1">Play Again</a>
            {% elif game_over == "lose" %}
                <h2>😢 You Lost! The word was "{{ correct_word }}"</h2>
                <a href="/?reset=1">Try Again</a>
            {% else %}
                <form method="POST">
                    <label for="guess">Enter a Letter or Word:</label>
                    <input type="text" id="guess" name="guess" required>
                    <button type="submit">Guess</button>
                </form>
            {% endif %}
        </div>
    </body>
    </html>
    """

    # Render the HTML with variables
    return render_template_string(
        html_template,
        masked_word=masked_word,
        attempts=session["attempts"],
        wrong_guesses=session["wrong_guesses"],
        current_clue=current_clue,
        game_over=session["game_over"],
        correct_word=session["word"]
    )

if __name__ == "__main__":
    app.run(debug=True)
