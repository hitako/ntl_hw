import requests
from pprint import pprint


# url = "https://httpbin.org/get"
# resp = requests.get(url)
# pprint(resp.json())

class SuperHero:
    API_URI = "https://superheroapi.com/api/"

    def __init__(self, token):
        self.token = token

    def get_superhero_id(self, name):
        return requests.get(self.API_URI + self.token + "/search/" + name).json()['results'][0]['id']

    def get_superhero_info(self, hero_id, info):
        return requests.get(self.API_URI + self.token + "/" + hero_id + "/" + info).json()

    def set_superhero_stat(self, heroes_dict, stat):
        for hero in heroes_dict.items():
            hero_id = self.get_superhero_id(hero[0])
            heroes_dict[hero[0]] = int(self.get_superhero_info(hero_id, "powerstats")[stat])
        return heroes_dict

    @staticmethod
    def print_sorted_heroes(heroes_dict, stat):
        for hero_name, hero_stat in sorted(heroes_dict.items(), key=lambda i: i[1], reverse=True):
            print(hero_name + "(" + stat + " = " + str(hero_stat) + ")", sep='\n')


sh = SuperHero("2619421814940190")
heroes_intelligence = {"Hulk": 0, "Captain America": 0, "Thanos": 0}
heroes_intelligence = sh.set_superhero_stat(heroes_intelligence, "intelligence")
sh.print_sorted_heroes(heroes_intelligence, "Intelligence")
