from .client import Client
import json

class Character:
    __client: Client
    uid: str
    pid: str
    session_key: str
    hash: str
    data = None

    def __init__(self, client) -> None:
        self.__client = client

    def login(self, profile_id, username, password):
        r_msg = self.__client.send_remoting_amf(
            target="SystemLogin.loginUser", 
            body=[[username, password]]
        )
        data = r_msg.bodies[0][1].body
        self.uid = data.uid
        self.pid = profile_id
        self.session_key = data.sessionkey
        self.hash = data.hash
        self.parse_character_data()

    def parse_character_data(self):
        r_msg = self.__client.send_remoting_amf(
            target="SystemLogin.getCharacterData", 
            body=[[self.pid, self.session_key]]
        )
        self.data = r_msg.bodies[0][1].body
