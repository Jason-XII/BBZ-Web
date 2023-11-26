from flask import Flask, render_template, request, make_response
from game import GameAI
import json

app = Flask(__name__)
#game = GameAI()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newgame")
def create_new_game():
    return json.dumps({"enabled":[1, 1, 0, 0, 1, 0, 0, 0]})

@app.route("/act", methods=['GET', 'POST'])
def player_acts():
    resp = request.get_json()
    action = int(resp['action'])
    game = GameAI()
    game.e1 = int(resp['e1'])
    game.e2 = int(resp['e2'])
    machine_act = game.act(action)
    return_dict = {"a": action, "ma": machine_act, "over":game.over, "e1":game.e1, "e2":game.e2, 
                    "text1":game.text[action], "text2":game.text[machine_act], "winner": game.winner}
    enabled = []
    for i in range(1, 9):
        if (game.e1 >= game.requires[i]):
            enabled.append(1)
        else:
            enabled.append(0)
    return_dict['enabled'] = enabled
    return json.dumps(return_dict)

app.run()
