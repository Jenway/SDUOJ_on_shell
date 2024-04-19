from time import sleep
from .oj.SDUOJ_Manager import SDUOJ_Manager
from .utils.config import get_loacl_config

def oju():
    def getPSets(psid: str, gid:int = 0):
        psInfo = oj.getProblemSetInfo(psid)
        if gid == 0:
            for problem in psInfo["data"]["groupInfo"][gid]["problemInfo"]:
                index = int(problem['index']) + 1
                print(f"{index} : {problem['name']}")
            return
        else:
            for problem in psInfo["data"]["groupInfo"][gid]["problemInfo"]:
                p = oj.getProblemInfo(psid, gid, problem['index'])
                index = int(problem['index']) + 1
                print(f"{index} : {p['data']['description']}")
            return

    def getProblemSubmissionTemplate(psid: str, gid: int, pid: int):
        response = oj.getProblemInfo(psid, gid, pid)
        return response["data"]["judgeTemplates"]
    
    oj = SDUOJ_Manager()
    local_config = get_loacl_config()
    if not local_config:
        print("找不到配置文件，请先运行main.py配置")
        exit(1)
    groupid = local_config["groupId"]
    psid = local_config["psid"]
    gid = input("请输入题目组编号: 0->编程题 1->简答题: ")
    print("题目列表:")
    getPSets(psid, int(gid))
    
    idx = int(input("请输入题目编号: "))
    idx -= 1
    code = input("请输入代码文件: ")
    with open(code, "r", encoding="utf-8") as f:
        code = f.read()
    


    if int(gid) == 0:
        templates = getProblemSubmissionTemplate(psid, int(gid), idx)
        for t in templates:
            print("id:", t["id"], "title:", t["title"])
        print("请选择模板:")
        template_id = int(input())
        print("编程题提交中...")
        oj.answerProblem(str(psid), 0, idx, code, template_id)
    else:
        print("简答题提交中...")
        oj.answerProblemMD(str(psid), 1, idx, code)

