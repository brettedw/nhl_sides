
class Team:
    def __init__(self, owner, roster_list):
        self.owner = owner
        self.roster = roster_list
        self.total_games = 0
        self.total_goals = 0
        self.total_assists = 0
        self.total_points = 0
        self.total_wins = 0
        self.total_so = 0
        self.total_Fpts = 0
        self.total_pt_diff = 0
        self.total_pts_last_szn = 0
        self.set_totals()

    def __repr__(self):
        return f'{self.roster}'

    def set_totals(self):
        for player in self.roster:
            self.total_games += player.games
            if hasattr(player, 'goals') or hasattr(player, 'assists'):
                self.total_goals += player.goals
                self.total_assists += player.assists
                self.total_points += player.points
                self.total_Fpts += player.Fpts
                self.total_pts_last_szn += player.pts_last_szn
                self.total_pt_diff += player.pts_differential
            elif hasattr(player, 'wins'):
                self.total_wins += player.wins
                self.total_so += player.shutouts
                self.total_Fpts += player.Fpts
            else:
                pass
