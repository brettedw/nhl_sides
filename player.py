import requests
import json
import pandas as pd
import pickle
from pprint import pprint
import os

SEASON = '20222023'

BASE_URL = "https://statsapi.web.nhl.com"
TEAMS_URL = f"{BASE_URL}/api/v1/teams/"


def get_team_url(team_name):
    teams = requests.get(TEAMS_URL)

    team_content = json.loads(teams.content)
    df = pd.DataFrame(team_content['teams'])
    team_id = df.loc[df['teamName'] == team_name, 'id'].item()

    return TEAMS_URL + str(team_id)


def get_player_name_id(player_name, team_name):
    team_url = get_team_url(team_name)
    roster_url = team_url + '/roster?season=' + SEASON
    roster = requests.get(roster_url)
    roster_json = json.loads(roster.content)

    for player in roster_json['roster']:
        if player_name in player['person']['fullName']:
            return player['person']['fullName'], player['person']['id']


def get_player_stats(player_id, season):
    stats_url = f'{BASE_URL}/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season={season}'
    stats = requests.get(stats_url)
    try:
        stats_json = json.loads(stats.content)['stats'][0]['splits'][0]['stat']
    except:
        return None

    return stats_json


def fill_player_id_db():
    import csv
    id_dict = dict()

    with open('players_2022-2023.csv') as player_csv:
        reader = csv.reader(player_csv)
        for player, team in reader:
            player_name, player_id = get_player_name_id(player, team)
            id_dict[player_name] = player_id

    with open('player_id.pkl', 'wb') as handle:
        pickle.dump(id_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return id_dict


def get_player_ids():
    if os.path.exists('player_id.pkl'):
        with open('player_id.pkl', 'rb') as handle:
            player_dict = pickle.load(handle)
    else:
        player_dict = fill_player_id_db()

    return player_dict


if __name__ == '__main__':
    if os.path.exists('player_id.pkl'):
        with open('player_id.pkl', 'rb') as handle:
            player_dict = pickle.load(handle)
    else:
        player_dict = fill_player_id_db()

    player_stats_dict = dict()
    for player, player_id in player_dict.items():
        stats = get_player_stats(player_id, SEASON)
        player_stats_dict[player] = stats

    pprint(player_stats_dict)
