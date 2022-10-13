import requests
import json
from collections import defaultdict
from flask import Flask, render_template
from player import get_player_ids, Player
import os
import pickle
import EvQ

PLAYER_IDS = get_player_ids()

app = Flask(__name__)


def get_bet_players(bet_dict, set_last_season=False):
    bet_players = defaultdict(list)

    for owner, players in bet_dict.items():
        for player in players:
            player = Player(owner=owner, player_name=player)
            player.set_player_name_id(PLAYER_IDS)
            player.set_player_stats()
            player.set_fantrax_points()

            if set_last_season:
                player.set_last_season_points()

            bet_players[owner].append(player)

    return bet_players


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/EddieVQuinn')
def EddieVQuinn():
    bet1_teams = get_bet_players(EvQ.bet1)
    bet2_teams = get_bet_players(EvQ.bet2)
    bet3_teams = get_bet_players(EvQ.bet3, set_last_season=True)

    return render_template(
        'EvQ_bet_tables.html', bet1_teams=bet1_teams, bet2_teams=bet2_teams, bet3_teams=bet3_teams)


@app.route('/EddieVMarc')
def EddieVMarc():
    pass


@app.route('/MarcVQuinn')
def MarcVQuinn():
    pass


@app.route('/MitchVQuinn')
def MitchVQuinn():
    pass


if __name__ == '__main__':
    # x = get_bet_players(EvQ.bet2)
    # for key, value in x.items():
    #     print(value)
    app.run(debug=True)
