from flask import Flask, render_template, request
import random

db = {}
app = Flask(__name__)

if 'game_start' not in db:
  db['game_start'] = False

if 'player_score' not in db:
    db['player_score'] = 0

if 'choices' not in db:
    db['choices'] = ''

if 'result' not in db:
    db['result'] = ''

@app.route('/')
def index():
    return render_template('index.html', 
                           game_start= db['game_start'], 
                           choices = db['choices'],
                           player_score=db['player_score'], 
                           result=db['result'])
    
@app.route('/play', methods=['POST'])
def play():
    
    db['game_start'] = True
    player_choice = request.args['choice']
    computer_choice = get_computer_choice()
    score = caluculate_result(player_choice, computer_choice)
    db['result'] = get_result(score)
    db['choices'] = f"👨 {player_choice} 🤖 {computer_choice}"
    db['player_score'] += score
     
    return render_template('index.html', 
                           game_start= db['game_start'], 
                           choices = db['choices'],
                           player_score=db['player_score'], 
                           result=db['result'])


def get_computer_choice():
    return random.choice(['rock','paper','scissors'])

def caluculate_result(player_choice, computer_choice):
    # Create a variable called `score` and set it's value to None
    score = None

    # All situations where human draws, set `score` to 0
    if player_choice == computer_choice:
        score = 0

    # All situations where human wins, set `score` to 1
    # make sure to use elifs here
    elif player_choice == 'rock' and computer_choice == 'scissors':
        score = 1

    elif player_choice == 'paper' and computer_choice == 'pock':
        score = 1

    elif player_choice == 'scissors' and computer_choice == 'paper':
        score = 1

    # Otherwise human loses (aka set score to -1)
    else:
        score = -1

    # return score
    return score
 
def get_result(score):
    score_text = None

    if score == 1:
        score_text = 'You Win!'

    elif score == 0:
        score_text = "It's a Draw!"

    elif score == -1:
        score_text = 'You Lose!'

    return score_text

@app.route('/end')
def end_game():
    db['game_start'] = False
    db['player_score'] = 0
    db['choices'] = ''
    db['result'] = ''

    return render_template('index.html', 
                           game_start=db['game_start'],
                           player_score=db['player_score'],
                           choices=db['choices'],
                           result=db['result'])     
app.run()