from collections import defaultdict
from flask import Flask, render_template
from player import get_player_ids, Player
from team import Team
import EvQ
import EvM
import MvQ
import MBvQ

PLAYER_IDS = get_player_ids()

app = Flask(__name__)


def get_bet_players(bet_dict, set_last_season=False):
    bet_players = defaultdict(list)

    for owner, players in bet_dict.items():
        for player in players:
            player = Player(player_name=player)
            player.set_player_name_id(PLAYER_IDS)
            player.set_player_stats()
            player.set_fantrax_points()
            player.set_ppg()
            player.set_apg()

            if set_last_season:
                player.set_last_season_points()

            bet_players[owner].append(player)

    return bet_players


def create_teams(bet_dict, set_last_season=False):
    bet_players = get_bet_players(bet_dict, set_last_season=set_last_season)

    teams = []
    for owner, players in bet_players.items():
        team = Team(owner, players)
        teams.append(team)

    return teams


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/EddieVQuinn')
def EddieVQuinn():
    bet1_teams = create_teams(EvQ.bet1)
    bet2_teams = create_teams(EvQ.bet2)
    bet3_teams = create_teams(EvQ.bet3, set_last_season=True)

    return render_template(
        'EvQ_bet_tables.html', bet1_teams=bet1_teams, bet2_teams=bet2_teams, bet3_teams=bet3_teams)


@app.route('/EddieVMarc')
def EddieVMarc():
    bet1_teams = create_teams(EvM.bet1)
    bet2_teams = create_teams(EvM.bet2)
    bet3_teams = create_teams(EvM.bet3)

    return render_template(
        'EvM_bet_tables.html', bet1_teams=bet1_teams, bet2_teams=bet2_teams, bet3_teams=bet3_teams)


@app.route('/MarcVQuinn')
def MarcVQuinn():
    bet1_teams = create_teams(MvQ.bet1)
    bet2_teams = create_teams(MvQ.bet2)
    bet3_teams = create_teams(MvQ.bet3)

    return render_template(
        'QvM_bet_tables.html', bet1_teams=bet1_teams, bet2_teams=bet2_teams, bet3_teams=bet3_teams)


@app.route('/MitchVMarc')
def MitchVMarc():
    bet1_teams = create_teams(MBvQ.bet1)

    return render_template(
        'MBvMS_bet_tables.html', bet1_teams=bet1_teams)


if __name__ == '__main__':
    app.run()
