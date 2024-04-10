import json
from operator import ge
from SDUOJ_Manager import SDUOJ_Manager
from entity import Group, ProblemSet
from utils.FileHandler import create_file, read_json_file
from config import get_loacl_config, generate_config

def getGroups() -> list:
    return [Group(row=group) for group in oj.getGroupList()["data"]["rows"]]

def getLabelList(gpId: str) -> list:
    return [label for label in oj.getProblemSetLabel(gpId)["data"]["label"]]

def getProblemSet(gpId: str, label: str) -> list:
    return [ProblemSet(row) for row in oj.searchProblemSet(gpId, label)["data"]["rows"]]

def getProblemSetInfo(psid: str):
    return oj.getProblemSetInfo(psid)


def dealWithPset(psid: str):

    psInfo = getProblemSetInfo(psid)

    for problem in psInfo["data"]["groupInfo"][0]["problemInfo"]:
        print(f"{problem['index']} : {problem['name']}")

    while True:
        pIdx = input("请输入题目编号: ")
        problem = oj.getProblemInfo(psid, 0, pIdx)
        title = problem["data"]["problemTitle"]
        description = problem["data"]["problemDescriptionDTO"]["markdownDescription"]

        judgeTemplates = problem["data"]["judgeTemplates"]
        # for idx, template in enumerate(judgeTemplates):
        #     print(f"{template}")
        print(title)
        print(description)
        # if not exist  create
        create_file(pIdx, title, description)

def getContestList(gpId: str) -> list:
    return [contest for contest in oj.searchContest(gpId)["data"]["rows"]]

def dealWithContest():
    print("懒得写了 = =")
    print("如果你想使用的话，只需要调用 SDUOJ_Manager.py 中的 接口即可 :)")


def get_pset():
    PSETLabel = input("请输入label: ")
    psid = input("请输入psid: ")
    ContestId = input("请输入ContestId: ")
    return PSETLabel, psid, ContestId

def get_contest():
    # 在这里添加获取比赛信息的代码
    pass

def get_config_via_input():
    groups = getGroups()
    for group in groups:
        print(f"groupId: {group.groupId} title: {group.title}")
    groupId = input("请输入groupId: ")

    PSETorContest = input("输入 1 获取题单，输入 2 获取比赛: ")
    if PSETorContest == "1":
        for label in getLabelList(groupId):
            print(label + " ", end="")
        print()
        psetLabel = input("请输入label: ")
        psets = getProblemSet(groupId, psetLabel)
        for pset in psets:
            print(f"psid: {pset.psid} name: {pset.name}")
        psid = input("请输入psid: ")
        config = {
            "groupId": groupId,
            "PSETorContest": 0,
            "psid": psid,
        }
    else:
        print("懒得写了 = =")
        print("如果你想使用的话，只需要调用 SDUOJ_Manager.py 中的 接口即可 :)")
        config = {
            "groupId": groupId,
            "PSETorContest": 1,
        }
    generate_config(groupId=groupId, PSETorContest=0, PSETLabel=psetLabel, psid=psid)
    print(f"配置文件已生成，内容为: {config}")
    return config

def get_config() -> dict:
    exist_config = get_loacl_config()
    if exist_config is not None:
        choice = input("是否使用上次的配置？(y/n): ")
        if choice == "y":
            return exist_config
        else:
            return get_config_via_input()
    else:
        print("没有找到配置文件，将使用输入的配置")
        return get_config_via_input()

def mainLoop(config):
    if config["PSETorContest"] == 0:
        dealWithPset(config["psid"])
    else:
        dealWithContest()

if __name__ == "__main__":
    oj = SDUOJ_Manager()
    config = get_config()
    mainLoop(config)