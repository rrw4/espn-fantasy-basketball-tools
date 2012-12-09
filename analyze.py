import sys
import urllib2

from bs4 import BeautifulSoup

league_id = sys.argv[1]

base_rosters_url = 'http://games.espn.go.com/fba/leaguerosters?leagueId='
base_standings_url = 'http://games.espn.go.com/fba/standings?leagueId=47525&seasonId=2013'
base_scoreboard_url = 'http://games.espn.go.com/fba/scoreboard?leagueId=47525&seasonId=2013'
base_player_ratings_url_1 = 'http://games.espn.go.com/fba/playerrater?leagueId='
base_player_ratings_url_2 = '&teamId=1&startIndex='

player_ratings = {}

def build_rosters_url(league_id):
    rosters_url = base_rosters_url + str(league_id)
    return rosters_url

def curl(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return BeautifulSoup(html)

def build_player_ratings_url(league_id, start_index):
    player_ratings_url = base_player_ratings_url_1 + str(league_id) + base_player_ratings_url_2 + str(start_index)
    return player_ratings_url

def build_player_ratings(num_players):
    for start_index in range(0, num_players, 50):
        player_ratings_url = build_player_ratings_url(league_id, start_index)
        player_ratings_dom = curl(player_ratings_url)
        players_dom = player_ratings_dom.find_all('tr', class_='pncPlayerRow')
        for player_dom in players_dom:
            player_id = int(player_dom.find(class_='playertablePlayerName').a['playerid'])
            ratings_dom = player_dom.find_all('td', class_='playertableData')
            try:
                player_rating = float(ratings_dom[-1].string)
            except ValueError:
                player_rating = 0 #temporary
            player_ratings[player_id] = player_rating #TODO: list for rating by each category

class Standings:
    def get_standings(self):
        self.dom = curl(base_url_standings)

class Roster:
    teams = []
    rosters = {}

    def get_rosters(self, league_id):
        self.rosters_dom = curl(build_rosters_url(league_id))
        self.teams_dom = self.rosters_dom.find_all('table', class_='playerTableTable')
        for team_dom in self.teams_dom:
            team_name = team_dom.find(class_='playerTableBgRowHead').a.string
            self.teams.append(team_name)
            players_dom = team_dom.find_all('td', class_='playertablePlayerName')
            players_list = []
            for player_dom in players_dom:
                player_name = player_dom.a.string
                player_id = int(player_dom.a['playerid'])
                team_pos_string = player_dom.contents[1].string #TODO: parse string to get NBA team and position eligibility
                players_list.append((player_name, player_id))
            self.rosters[team_name] = players_list


if __name__ == "__main__":
    build_player_ratings(500)
    r = Roster()
    r.get_rosters(league_id)
    for team in r.teams:
        roster = r.rosters.get(team)
        team_rating = 0
        players_counted = 0
        for player in roster:
            player_rating = player_ratings.get(player[1])
            if player_rating != None and player_rating > 0:
                team_rating += player_rating
                players_counted += 1
        print team
        print team_rating
        print players_counted
