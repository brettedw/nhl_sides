import requests
import json
from flask import Flask, render_template
import EvQ, EvM, MvQ, MBvQ


def request_json(player_id):
    request = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20212022'
    response = requests.get(request)
    stats = json.loads(response.text)

    return stats


def get_player_stats(json_stats):
    stats = json_stats['stats'][0]['splits'][0]['stat']

    return stats


def player_bets_string(list_of_bets):
    result = ''
    for bet in list_of_bets:
        for k,v in bet.items():
            resp = request_json(v)
            stats = get_player_stats(resp)

            points = stats['points']
            games = stats['games']
            ppg = points/games

            result += f'{k} -- {points} points in {games} games ({ppg:.2f} PPG)<br>'
        result += '<hr>'
    return result


def player_team_bets_string(list_of_bets):
    result = ''
    for bet in list_of_bets:
        pt_total = 0
        gm_total = 0
        for k,v in bet.items():
            resp = request_json(v)
            stats = get_player_stats(resp)

            points = stats['points']
            games = stats['games']
            ppg = points/games

            pt_total += points
            gm_total += games
            result += f'{k} -- {points} points in {games} games ({ppg:.2f} PPG)<br>'
        result += f'-- Team Total: {pt_total}<br>'
        result += f'-- Team PPG: {pt_total/gm_total:.2f}<hr>'

    return result


def goalie_bets_string(list_of_bets):
    result = ''
    for bet in list_of_bets:
        for k,v in bet.items():
            resp = request_json(v)
            stats = get_player_stats(resp)

            games = stats['games']
            wins = stats['wins']
            shutouts = stats['shutouts']
            ot = stats['ot']

            points = wins*2 + shutouts*2 + ot
            ppg = points/games

            result += f'{k} -- {points} points in {games} games ({ppg:.2f} PPG) -- {wins} wins - {shutouts} shutouts - {ot} OT points<br>'
        result += '<hr>'
    return result


def goalie_team_bets_string(list_of_bets):
    result = ''
    for bet in list_of_bets:
        pt_total = 0
        for k,v in bet.items():
            resp = request_json(v)
            try:
                stats = get_player_stats(resp)

                games = stats['games']
                wins = stats['wins']
                shutouts = stats['shutouts']
                ot = stats['ot']

                points = wins*2 + shutouts*2 + ot
                ppg = points/games
                pt_total += points

                result += f'{k} -- {points} points in {games} games ({ppg:.2f} PPG) -- {wins} wins - {shutouts} shutouts - {ot} OT points<br>'
            except: 
                result += f'{k} has yet to play a game<br>'
        result += f'-- Team Total: {pt_total}<hr>'
    return result


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/EddieVQuinn')
def EddieVQuinn():
    stats = player_bets_string(EvQ.player_bets)
    stats += player_team_bets_string(EvQ.team_bets)
    rules = EvQ.rules

    return render_template('index.html', **locals())


@app.route('/EddieVMarc')
def EddieVMarc():
    stats = player_bets_string(EvM.player_bets)
    stats += player_team_bets_string(EvM.team_bets)
    rules = EvM.rules

    return render_template('index.html', **locals())


@app.route('/MarcVQuinn')
def MarcVQuinn():
    stats = player_bets_string(MvQ.player_bets)
    rules = MvQ.rules

    return render_template('index.html', **locals())

@app.route('/MitchVQuinn')
def MitchVQuinn():
    stats = player_team_bets_string(MBvQ.team_bets)
    rules = MBvQ.rules

    return render_template('index.html', **locals())



if __name__=='__main__':
    app.run()