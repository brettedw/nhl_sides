import bets
import json
import requests

def request_json(player_id):
    request = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20202021'
    response = requests.get(request)
    stats = json.loads(response.text)

    return stats

def get_player_stats(json_stats):
    stats = json_stats['stats'][0]['splits'][0]['stat']

    return stats


bet_list = [bets.QB1, bets.QB2, bets.QB3]

all_player_bets = []
all_team_bets = []

for bet in bet_list:
    player_bet = []
    team_bet = []

    if isinstance(bet, dict):
        for k,v in bet.items():
            player_results = {}

            resp = request_json(v)
            stats = get_player_stats(resp)

            player_results['player'] = k
            player_results['GP'] = stats['games']
            player_results['P'] = stats['points']

            player_bet.append(player_results)


    if isinstance(bet, list):
        for team in bet:
            team_results = []
            for k,v in team.items():
                player_results = {}

                resp = request_json(v)
                stats = get_player_stats(resp)

                player_results['player'] = k
                player_results['GP'] = stats['games']
                player_results['P'] = stats['points']

                team_results.append(player_results)
            team_bet.append(team_results)

    all_player_bets.append(player_bet)
    all_team_bets.append(team_bet)

    
all_player_bets = [bet for bet in all_player_bets if bet]

for bet in all_player_bets:
    print(bet)

for bet in all_team_bets:
    print(bet)
            
            
