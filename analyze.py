import sys
import urllib2

from bs4 import BeautifulSoup

league_id = sys.argv[1]

base_rosters_url = 'http://games.espn.go.com/fba/leaguerosters?leagueId='
base_standings_url_1 = 'http://games.espn.go.com/fba/standings?leagueId='
base_standings_url_2 = '&seasonId=2013'
base_scoreboard_url_1 = 'http://games.espn.go.com/fba/scoreboard?leagueId='
base_scoreboard_url_2 = '&seasonId=2013'
base_player_ratings_url_1 = 'http://games.espn.go.com/fba/playerrater?leagueId='
base_player_ratings_url_2 = '&teamId=1&startIndex='

teams = []
rosters = {}
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

def get_rosters(league_id):
    rosters_dom = curl(build_rosters_url(league_id))
    teams_dom = rosters_dom.find_all('table', class_='playerTableTable')
    for team_dom in teams_dom:
        team_name = team_dom.find(class_='playerTableBgRowHead').a.string
        teams.append(team_name)
        players_dom = team_dom.find_all('td', class_='playertablePlayerName')
        players_list = []
        for player_dom in players_dom:
            player_name = player_dom.a.string
            player_id = int(player_dom.a['playerid'])
            team_pos_string = player_dom.contents[1].string #TODO: parse string to get NBA team and position eligibility
            players_list.append((player_name, player_id))
        rosters[team_name] = players_list

if __name__ == "__main__":
    build_player_ratings(500)
    get_rosters(league_id)
    for team in teams:
        roster = rosters.get(team)
        team_rating = sum(v for k,v in player_ratings.iteritems() if k in [player[1] for player in roster])
        print "{0} ({1} total rating)".format(team, team_rating)
        for player in roster:
            print "  {0} ({1})".format(player[0], float(player_ratings.get(player[1]) or 0))
