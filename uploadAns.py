from time import sleep
from SDUOJ_Manager import SDUOJ_Manager


if __name__ == "__main__":
    oj = SDUOJ_Manager()
    oj.login_to_sduoj()
    idx = int(input("请输入题目编号: "))
    idx -= 1
    code = input("请输入代码文件: ")
    with open(code, "r", encoding="utf-8") as f:
        code = f.read()
    ans_id = oj.answerProblem("71", 0, idx, code, 6)["data"]
    print(f"Answer id: {ans_id}")
    print("Waiting for result...")
    sleep(5)
    print(oj.getSubmissionInfo("71", 0, idx, ans_id))
