from SDUOJ_Manager import SDUOJ_Manager
from entity import Group,ProblemSet

if __name__ == "__main__":
    oj = SDUOJ_Manager()
    oj.login_to_sduoj()

    gl = oj.getGroupList()
    groupList = []
    for row in gl['data']['rows']:
        groupList.append(Group(row))
    
    for group in groupList:
        print(f"groupId: {group.groupId} title: {group.title}")
    gpId = input("请输入groupId: ")

    for label in oj.getProblemSet(gpId)['data']['label']:
        print(label + " ", end="")
    print()

    psLabel = input("请输入label: ")
    # print(oj.searchProblemSet(gpId, psLabel))
    psLst = oj.searchProblemSet(gpId, psLabel)['data']['rows']
    psetList = []
    for row in psLst:
        psetList.append(ProblemSet(row))
    for pset in psetList:
        print(f"psid: {pset.psid} name: {pset.name}")

    psid = input("请输入psid: ")
    psInfo = oj.getProblemSetInfo(psid)
    for problem in psInfo['data']['groupInfo'][0]['problemInfo']:
            print(f"{problem['index']} : {problem['name']}")


    pIdx = input("请输入题目编号: ")
    problem = oj.getProblemSetProInfo(psid, 0, pIdx)
    # data->problemDescriptionDTO->markdownDescription
    title = problem['data']['problemTitle']
    description = problem['data']['problemDescriptionDTO']['markdownDescription']
    judgeTemplates = problem['data']['judgeTemplates']
    print(title)
    print(description)
    for template in judgeTemplates:
        print(f"id: {template['id']} name: {template['title']}")
    templateId = input("请输入模板编号: ")
    exit(0)
    ans = "print(5)"

    print(oj.answerProblem(psid, 0, pIdx, ans, 13))