from riotwatcher import LolWatcher 
import os
lol_watcher = LolWatcher(os.environ.get('RIOT_API'))
region = 'na1'

#The code below takes champion data from DataDragon API and places champion
#name and respective id in a dict format {id, championName}
champions = lol_watcher.data_dragon.champions(version='10.5.1')['data']
champ_names = champions.keys()
champ_id = {}
for name in champ_names:
       champ_id[name] = champions[name]['key']
champ_code = {}
for key, value in champ_id.items():
    champ_code[value] = key 

class Summoner:
    
    def __init__(self, region, name):
        self.region = region
        self.name = lol_watcher.summoner.by_name(region, name)['name']
        self.summ_id = lol_watcher.summoner.by_name(region, name)['id']
        self.account_id = lol_watcher.summoner.by_name(region, name)['accountId']
        self.level = lol_watcher.summoner.by_name(region, name)['summonerLevel']

    def get_rank(self):
        data = lol_watcher.league.by_summoner(self.region,self.summ_id)[0]
        tier = data['tier']
        rank = data['rank']
        lp = data['leaguePoints']
        return tier, rank, lp

    def get_stats(self):
        match_list = lol_watcher.match.matchlist_by_account(
        self.region,
        self.account_id,
        begin_index=0,end_index=5)
        game_list = []
        for match in match_list['matches']:
            game_list.append(match['gameId'])

        matches = [lol_watcher.match.by_id(self.region,game) for game in game_list]
        stats_data= []
        for match in matches:
            identities = match['participantIdentities']
            pair = {}
            for identity in identities:
                pair.update({identity['player']['summonerName']:identity['participantId']})
            pid = pair[self.name]
            stat = {}
            for player in match['participants']:
                if player['participantId'] == pid:
                    stat.update({'championId':player['championId']})
                    stat.update(player['stats'])
            stats_data.append(stat)
        kills = []
        deaths = []
        assists = []
        gold = [] 
        for data in stats_data:
            kills.append(data['kills'])
            deaths.append(data['deaths'])
            assists.append(data['assists'])
            gold.append(data['goldEarned'])
        avg_kills = (sum(kills)/len(kills))
        avg_deaths = (sum(deaths)/len(deaths))
        avg_assists = (sum(assists)/len(assists))
        avg_gold = (sum(gold)/len(gold))
        return avg_kills, avg_deaths, avg_assists, avg_gold 
    
    def get_champs(self):
        match_list = lol_watcher.match.matchlist_by_account(
        self.region,
        self.account_id,
        begin_index=0,end_index=20)
        game_list = []
        for match in match_list['matches']:
            game_list.append(match['gameId'])

        matches = [lol_watcher.match.by_id(self.region,game) for game in game_list]
        champs = []
        wins = []
        champions = []
        for match in matches:
            identities = match['participantIdentities']
            pair = {}
            for identity in identities:
                pair.update({identity['player']['summonerName']:identity['participantId']})
            pid = pair[self.name]
            for player in match['participants']:
                if player['participantId'] == pid:
                    champs.append({'championId':player['championId']})
                    wins.append(player['stats']['win'])
        for champ in champs:
            for code in champ_code:
                if str(champ['championId'])==code:
                    champions.append(champ_code.get(code))
        return wins, champions


