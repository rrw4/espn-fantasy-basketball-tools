import sys
import urllib2

from bs4 import BeautifulSoup


league_id = sys.argv[1]
base_rosters_url = 'http://games.espn.go.com/fba/leaguerosters?leagueId='
base_standings_url = 'http://games.espn.go.com/fba/standings?leagueId=47525&seasonId=2013'
base_scoreboard_url = 'http://games.espn.go.com/fba/scoreboard?leagueId=47525&seasonId=2013'


def build_rosters_url(league_id):
    rosters_url = base_rosters_url + str(league_id)
    return rosters_url

def curl(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return BeautifulSoup(html)


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
    r = Roster()
    r.get_rosters(league_id)
    print r.teams
    print r.rosters
