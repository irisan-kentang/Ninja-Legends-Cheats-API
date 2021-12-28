from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import hashlib
from copy import deepcopy
from client import Client
from character import Character
from enemy import Enemy
from mission import Mission

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['characters'] = {}

def init_nl():
    global characters

    data = request.json
    if data == None or "username" not in data or "password" not in data or "profile_id" not in data:
        return jsonify(
            success = False,
            message = "username, password, and profile_id required"
        )
    if data["username"] == "" or data["password"] == "" or data["profile_id"] == "":
        return jsonify(
            success = False,
            message = "username, password, and profile_id must not empty"
        )

    client = Client()
    if data['username'] in app.config['characters']:
        character = app.config['characters'][data['username']]
        character.set_client(client)
    else:
        character = Character()
        character.set_client(client)
        character.login(data["profile_id"], data["username"], data["password"])
        app.config['characters'][data['username']] = character

    enemy = Enemy(character)
    mission = Mission(enemy, client, character)

    return {
        client: client,
        character: character,
        enemy: enemy,
        mission: mission
    }


@app.route('/instant_mission', methods=['POST'])
@cross_origin()
def instant_mission():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "mission_id" not in data:
        return jsonify(
            success = False,
            message = "mission_id required"
        )
    if data["mission_id"] == "":
        return jsonify(
            success = False,
            message = "mission_id must not empty"
        )

    uid = data['profile_id']
    mission_id = int(data['mission_id'])

    return mission.instant_mission(uid, mission_id)


@app.route('/hunting_house', methods=['POST'])
@cross_origin()
def hunting_house():
    ninja_legends = init_nl()
    if type(ninja_legends) == Response:
        return ninja_legends
    client, character, enemy, mission = ninja_legends.values()

    data = request.json
    if "boss_num" not in data:
        return jsonify(
            success = False,
            message = "boss_num required"
        )
    if data["boss_num"] == "":
        return jsonify(
            success = False,
            message = "boss_num must not empty"
        )

    uid = data['profile_id']
    boss_num = int(data['boss_num'])

    # start hunting house
    r_msg = client.send_remoting_amf(
        target="HuntingHouse.startHunting", 
        body=[[f"{uid}", f"{boss_num}", character.session_key]]
    )

    battle_code = r_msg.bodies[0][1].body

    # finish mission
    h = hashlib.sha256(f"{boss_num}{uid}{battle_code}".encode())
    r_msg = client.send_remoting_amf(
        target="HuntingHouse.finishHunting", 
        body=[[f"{uid}", f"{boss_num}", battle_code, h.hexdigest(), character.session_key]]
    )

    results = r_msg.bodies[0][1].body
    return results

@app.route('/debug', methods=['GET'])
@cross_origin()
def debug():
    return 'debug'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
