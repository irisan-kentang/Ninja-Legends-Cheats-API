import json
from .character import Character

class Enemy:
    __enemies = []
    __character: Character

    def __init__(self, character) -> None:
        enemyFile = open("enemies.json", "r")
        self.__enemies = json.load(enemyFile)['data']
        self.__character = character

    def __get_stat(self, enemy_id, mission_level):
        for enemy in self.__enemies:
            if enemy['enemy_id'] == enemy_id:
                if enemy['enemy_level'] == 99:
                    return {
                        'hp' : int(self.__character.data.character_level) * 50,
                        'cp' : int(self.__character.data.character_level) * 50,
                        'agility': 11 + int(self.__character.data.character_level),
                    }
                elif enemy['enemy_hp'] == 0:
                    return {
                        'hp': 30 + (int(mission_level) * 15),
                        'cp': 30 + (int(mission_level) * 15),
                        'agility': 11 + int(mission_level),
                    }
                else:
                    return {
                        'hp': 1,
                        'cp': 1,
                        'agility': 1,
                    }
    
    def get_hp(self, enemy_ids, mission_level):
        hp = 0
        for enemy_id in enemy_ids:
            hp += self.__get_stat(enemy_id, mission_level)['hp']
        return hp
