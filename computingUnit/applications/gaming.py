#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
# Command pattern reference : https://sourcemaking.com/design_patterns/command/python/1
#
import subprocess

league_path = 'C:\\Riot Games\\League of Legends\\LeagueClient'


class GamingControl:

    def __init__(self):
        pass

    def start_gaming(self):
        print("General gaming started")

    def start_LOL(self):
        subprocess.call(league_path)

    def stop_gaming(self):
        pass

    def start_furmark(self):
        pass

