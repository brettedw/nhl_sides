import requests
import json
from flask import Flask, render_template
from pprint import pprint

bet1 = {
    'Elias Lindholm':8477496,
    'Kevin Fiala': 8477942,
}

bet2 = {
    'Shea Theodore': 8477447,
    'Morgan Rielly': 8476853
}

eddie_rookies = {
    'Alexis Lafrenière': 8482109,
    'Nils Hoglander': 8481535,
    'Josh Norris': 8480064
}

quinn_rookies = {
    'Kirill Kaprizov': 8478864,
    'Tim Stützle': 8482116,
    'Gabriel Vilardi': 8480014
}

def request_json(player_id):
    request = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20202021'
    response = requests.get(request)
    stats = json.loads(response.text)

    return stats


def get_points(json_stats):
    points = json_stats['stats'][0]['splits'][0]['stat']['points']

    return points


def get_games(json_stats):
    games = json_stats['stats'][0]['splits'][0]['stat']['games']

    return games


def main():
    result = ''
    bets = [bet1, bet2]
    for bet in bets:
        for k,v in bet.items():
            stats = request_json(v)
            points = get_points(stats)
            games = get_games(stats)
            ppg = points/games
            result += f'{k} has {points} points in {games} games ({ppg:.1f} PPG)<br>'
        result += '<hr>'

    team_bets = [eddie_rookies, quinn_rookies]
    for bet in team_bets:
        pt_total = 0
        for k,v in bet.items():
            stats = request_json(v)
            points = get_points(stats)
            games = get_games(stats)
            ppg = points/games
            pt_total += points
            result += f'{k} has {points} points in {games} games ({ppg:.1f} PPG)<br>'
        result += f'Team Total: {pt_total}<hr>'
    return result


app = Flask(__name__)

@app.route('/')
def index():
    stats = main()

    return render_template('index.html', **locals())

# app.run()
