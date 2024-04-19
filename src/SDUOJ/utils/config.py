import os
from .FileHandler import read_json_file as read_json, write_json_file as write_json


def get_loacl_config():
    '''
    获取上次的配置 ， if any
    '''
    if not os.path.exists("config.json"):
        return None
    return read_json("config.json")

def generate_config(groupId, PSETorContest=0, PSETLabel="", psid="", ContestId=""):
    config = {
        "groupId": groupId,
        "PSETorContest": PSETorContest,
        "PSETLabel": PSETLabel,
        "psid": psid,
        "ContestId": ContestId
    }
    write_json("config.json", config)