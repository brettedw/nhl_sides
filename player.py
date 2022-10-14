import requests
import json
import pandas as pd
import pickle
import os

SEASON = '20222023'
LAST_SEASON = '20212022'

BASE_URL = "https://statsapi.web.nhl.com"
TEAMS_URL = f"{BASE_URL}/api/v1/teams/"


class Player:
    def __init__(self, owner, player_name):
        self.owner = owner
        self.player_name = player_name
        self.player_id = None
        self.games = 0
        self.points = 0
        self.Fpts = 0
        self.ppg = '-'
        self.apg = '-'
        self.pts_last_szn = 0
        self.pts_differential = 0

    def __repr__(self):
        return f"{self.player_name}; {self.player_id}; {self.Fpts}"

    def set_player_name_id(self, player_id_dict):
        for player, pid in player_id_dict.items():
            if self.player_name in player:
                self.player_name = player
                self.player_id = pid

    def set_player_stats(self, season=SEASON):
        stats_url = f'{BASE_URL}/api/v1/people/{self.player_id}/stats?stats=statsSingleSeason&season={season}'
        stats = requests.get(stats_url)
        try:
            stats_json = json.loads(stats.content)['stats'][0]['splits'][0]['stat']
        except:
            return None

        self.__dict__.update(stats_json)

        self.set_ppg()

    def set_last_season_points(self):
        stats_url = f'{BASE_URL}/api/v1/people/{self.player_id}/stats?stats=statsSingleSeason&season={LAST_SEASON}'
        stats = requests.get(stats_url)
        try:
            stats_json = json.loads(stats.content)['stats'][0]['splits'][0]['stat']
            self.pts_last_szn = stats_json['points']
            self.pts_differential = self.points - self.pts_last_szn
        except:
            return None

    def set_fantrax_points(self):
        try:
            self.Fpts = (self.wins + self.shutouts) * 2
        except:
            self.Fpts = self.points

    def set_ppg(self):
        try:
            self.ppg = round(self.points / self.games, 2)
        except:
            self.pgg = '-'

    def set_apg(self):
        try:
            self.apg = round(self.assists / self.games, 2)
        except:
            self.apg = '-'


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
    player_ids = get_player_ids()
