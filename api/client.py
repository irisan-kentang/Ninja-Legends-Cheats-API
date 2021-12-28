import requests
from pyamf import remoting, AMF0

class Client:
    __URL = "https://playninjalegends.com/amf_nl/"
    __client: requests.Session

    def __init__(self) -> None:
        headers = {
            'Referer': 'app:/NinjaLegends.swf',
            'Host': 'playninjalegends.com',
            'Content-Type': 'application/x-amf',
            'User-Agent': 'Mozilla/5.0 (Windows; U; en) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/32.0',
            'x-flash-version': '32,0,0,182',
        }
        self.__client = requests.Session()
        self.__client.headers = headers

    def send_remoting_amf(self, target, body):
        req = remoting.Request(
            target=target, 
            body=body
        )
        ev = remoting.Envelope(AMF0)
        ev["/1"] = req

        bin_msg = remoting.encode(ev)
        r = self.__client.post(self.__URL, data=bin_msg.getvalue())
        return remoting.decode(r.content)
