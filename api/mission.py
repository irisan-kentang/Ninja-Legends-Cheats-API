import json
import hashlib
from enemy import Enemy
from client import Client
from character import Character 

class Mission:
    __missions = []
    __enemy: Enemy
    __client: Client
    __character: Character

    def __init__(self, enemy, client, character) -> None:
        missionFile = open("missions.json", "r")
        self.__missions = json.load(missionFile)['data']
        self.__enemy = enemy
        self.__client = client
        self.__character = character

    def __get_mission(self, mission_id):
        for mission in self.__missions:
            if mission['msn_id'] == f"msn_{mission_id}":
                return mission

    def __get_mission_level(self, mission_id):
        return self.__get_mission(mission_id)['msn_level']
    
    def total_ene_hp(self, mission_id):
        enemies = self.__get_mission(mission_id)['msn_enemy']
        return self.__enemy.get_hp(enemies, self.__get_mission_level(mission_id))

    def instant_mission(self, uid, mission_id):
        # start mission
        r_msg = self.__client.send_remoting_amf(
            target="BattleSystem.startMission", 
            body=[[uid, f"msn_{mission_id}"]]
        )

        battle_code = r_msg.bodies[0][1].body

        # finish mission
        total_ene_hp = self.total_ene_hp(mission_id)
        h = hashlib.sha256(f"msn_{mission_id}{uid}{battle_code}{total_ene_hp}".encode())
        r_msg = self.__client.send_remoting_amf(
            target="BattleSystem.finishMission", 
            body=[[uid, f"msn_{mission_id}", battle_code, h.hexdigest(), total_ene_hp, self.__character.session_key]]
        )

        return r_msg.bodies[0][1].body
