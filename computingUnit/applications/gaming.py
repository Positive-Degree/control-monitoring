#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
# Command pattern reference : https://sourcemaking.com/design_patterns/command/python/1
#
import subprocess

league_path = 'C:\\Riot Games\\League of Legends\\LeagueClient'
steam_path = "C:\\Program Files (x86)\\Steam\\Steam.exe"

steam_kill = 'taskkill /im Steam.exe /F /t'


class GamingControl:

    def __init__(self):
        pass

    def start_LOL(self):
        subprocess.call(league_path)

    def start_steam(self):
        subprocess.call(steam_path)

    def stop_steam(self):
        try:
            subprocess.call(steam_kill)
        except:
            print("Steam was not running.")

    def start_furmark(self):
        pass


if __name__ == "__main__":
    subprocess.call(steam_kill)
