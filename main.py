import json
from random import choice
import subprocess
from SDUOJ_Manager import SDUOJ_Manager
from entity import Group, ProblemSet
import os


def getGroups() -> list:
    gl = oj.getGroupList()
    groupList = []
    for row in gl["data"]["rows"]:
        groupList.append(Group(row))
    return groupList


def getLabelList(gpId: str) -> list:
    return [label for label in oj.getProblemSet(gpId)["data"]["label"]]

def getContestList(gpId: str) -> list:
    return [contest for contest in oj.searchContest(gpId)["data"]["rows"]]

def getProblemSet(gpId: str, label: str) -> list:
    psLst = oj.searchProblemSet(gpId, label)["data"]["rows"]
    psetList = []
    for row in psLst:
        psetList.append(ProblemSet(row))
    return psetList


def getProblemSetInfo(psid: str):
    return oj.getProblemSetInfo(psid)

def create_file(pIdx, title, description):
    pIdx = int(pIdx)
    if not os.path.exists(f"{pIdx + 1}_{title}.md"):
        file = f"{pIdx + 1}_{title}.md"
        with open(file, "w", encoding="utf-8") as f:
            f.write(description)
        print(f"create file {file}")
    else:
        print(f"file already exist")


def appLoop():

    def dealWithPset(gpId: str):
        psLabel = input("请输入label: ")
        # psLabel = "作业"

        for pset in getProblemSet(gpId, psLabel):
            print(f"psid: {pset.psid} name: {pset.name}")

        psid = input("请输入psid: ")
        # psid = "71"

        psInfo = getProblemSetInfo(psid)

        for problem in psInfo["data"]["groupInfo"][0]["problemInfo"]:
            print(f"{problem['index']} : {problem['name']}")

        while True:
            pIdx = input("请输入题目编号: ")
            problem = oj.getProblemSetProInfo(psid, 0, pIdx)
            title = problem["data"]["problemTitle"]
            description = problem["data"]["problemDescriptionDTO"]["markdownDescription"]

            judgeTemplates = problem["data"]["judgeTemplates"]
            # for idx, template in enumerate(judgeTemplates):
            #     print(f"{template}")
            print(title)
            print(description)
            # if not exist  create
            create_file(pIdx, title, description)

    def dealWithContest():
        print("懒得写了 = =")
        print("如果你想使用的话，只需要调用 SDUOJ_Manager.py 中的 接口即可 :)")

    
    for group in getGroups():
        print(f"groupId: {group.groupId} title: {group.title}")

    gpId = input("请输入groupId: ")

    # ! 如果你想要的不是 '题单'，而是 `比赛`，using this
    # choice = input("输入 1 获取题单，输入 2 获取比赛: ")
    choice = "1"
    if choice == "1":
        for label in getLabelList(gpId):
            print(label + " ", end="")
        print()
        dealWithPset(gpId)
    elif choice == "2":
        for contest in getContestList(gpId):
            print(f"contestId: {contest['contestId']} title: {contest['contestTitle']}")
        dealWithContest()
    else :
        print("输入错误")
        return



if __name__ == "__main__":
    oj = SDUOJ_Manager()
    oj.login_to_sduoj()
    appLoop()
