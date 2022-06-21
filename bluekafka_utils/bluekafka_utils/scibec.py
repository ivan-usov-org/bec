import requests
import json


class SciBec:
    url = "http://[::1]:3030"

    def get_current_session(self):
        # for now, let's just assume there is only one session
        # after implementing the authorization, we can check if Kafka's current session can be loaded
        params = {"filter": '{"include":[{"relation": "devices"}]}'}
        headers = {"Content-type": "application/json"}
        res = requests.get(self.url + "/sessions", headers=headers, params=params, verify=False)
        return json.loads(res.content)

    # def send_run_request(self):
