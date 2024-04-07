import json
import os
from Authenticator import Authenticator
import httpx

class SDUOJ_Manager:
    def __init__(self):
        self.auth = Authenticator()
        self.base_url = "https://oj.qd.sdu.edu.cn/"
        self.cookie_file = "sduoj_cookie.json"

    @staticmethod
    def request_get(url, cookies, params={}, verify=False):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": "https://oj.qd.sdu.edu.cn/"
        }
        return httpx.get(url, headers=headers, params=params, cookies=cookies, verify=verify)

    @staticmethod
    def request_post(url, cookies, json, verify=False):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": "https://oj.qd.sdu.edu.cn/"
        }
        return httpx.post(url, headers=headers, json=json, cookies=cookies, verify=verify)


    def get_cookie(self):
        service = f"{self.base_url}v2/thirdPartyLogin?thirdParty=SDUCAS"
        sTicket = self.auth.get_sTicket(_content=f"service={service}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": self.base_url
        }
        params = {"thirdParty": "SDUCAS", "ticket": sTicket}
        response = httpx.get(f"{self.base_url}api/user/thirdPartyLogin", headers=headers, params=params, verify=False)
        return response.headers["Set-Cookie"].split("=")[1].split(";")[0]

    def if_cookie_expired(self, cookie):
        """
        Check if the cookie has expired
        """
        response = self.request_get(
            "https://oj.qd.sdu.edu.cn/api/user/getProfile",
            cookies={"SESSION": cookie},
            verify=False
        )
        if response.status_code == 401:
            print("Cookie has expired.")
            return True
        # print data-username and nickname
        print(f"Hello, {response.json()['data']['nickname']}! Your username is {response.json()['data']['username']}.")
        return False

    def load_cookie_from_file(self):
        if self.cookie_file in os.listdir():
            with open(self.cookie_file, "r") as f:
                return json.load(f)["cookie"]
        return None

    def save_cookie_to_file(self, cookie):
        with open(self.cookie_file, "w") as f:
            json.dump({"cookie": cookie}, f)

    def login_to_sduoj(self):
        existing_cookie = self.load_cookie_from_file()
        if existing_cookie and not self.if_cookie_expired(existing_cookie):
            self.sduoj_cookie = existing_cookie
        else:
            self.sduoj_cookie = self.get_cookie()
            self.save_cookie_to_file(self.sduoj_cookie)
    
    def getProfile(self):
        response = self.request_get(
            "https://oj.qd.sdu.edu.cn/api/user/getProfile",
            cookies={"SESSION": self.sduoj_cookie},
            verify=False
        )
        return response.json()
    
    def getGroupList(self):
        # https://oj.qd.sdu.edu.cn/api/group/page?pageNow=1&pageSize=12&isParticipating=1
        response = self.request_get(
            "https://oj.qd.sdu.edu.cn/api/group/page",
            cookies={"SESSION": self.sduoj_cookie},
            params={"pageNow": 1, "pageSize": 12, "isParticipating": 1},
            verify=False
        )
        return response.json()

    # 	https://oj.qd.sdu.edu.cn/api/ps/problem_set/key
    def getProblemSet(self, groupId):
        # json {"groupId": "57"}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/ps/problem_set/key",
            cookies={"SESSION": self.sduoj_cookie},
            json={"groupId": groupId},
            verify=False
        )
        return response.json()

    # 	https://oj.qd.sdu.edu.cn/api/contest/list?pageNow=1&pageSize=15&groupId=30
    def searchContest(self, groupId, pageNow=1, pageSize=15):
        # json {"pageNow":1,"pageSize":15,"groupId":"30"}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/contest/list",
            cookies={"SESSION": self.sduoj_cookie},
            json={"pageNow": pageNow, "pageSize": pageSize, "groupId": groupId},
            verify=False
        )
        return response.json()

    # /api/ps/problem_set/search
    def searchProblemSet(self, groupId, tag, pageNow=1, pageSize=20):
        # json {"pageNow":1,"pageSize":20,"groupId":"57","tag":"CSPT3模测"}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/ps/problem_set/search",
            cookies={"SESSION": self.sduoj_cookie},
            json={"pageNow": pageNow, "pageSize": pageSize, "groupId": groupId, "tag": tag},
            verify=False
        )
        return response.json()
    
    # /api/ps/problem_set/info_c
    def getProblemSetInfo(self, problemSetId):
        # json {"psid":59}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/ps/problem_set/info_c",
            cookies={"SESSION": self.sduoj_cookie},
            json={"psid": problemSetId},
            verify=False
        )
        return response.json()
    
    # https://oj.qd.sdu.edu.cn/api/ps/problem_set/pro_info
    def getProblemSetProInfo(self, problemSetId, gid, pid):
        # json {"router":{"psid":"63","gid":"0","pid":"3"}}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/ps/problem_set/pro_info",
            cookies={"SESSION": self.sduoj_cookie},
            json={"router": {"psid": problemSetId, "gid": gid, "pid": pid}},
            verify=False
        )
        return response.json()


    # /api/ps/answer_sheet/answer
    def answerProblem(self, problemSetId, gid, pid, code, judgeTemplateId):
        # json {"data":{"judgeTemplateId":"13","code":"print(5)","problemSetId":"71"},"router":{"psid":"71","gid":"0","pid":"0"}}
        response = self.request_post(
            "https://oj.qd.sdu.edu.cn/api/ps/answer_sheet/answer",
            cookies={"SESSION": self.sduoj_cookie},
            json={"data": {"judgeTemplateId": judgeTemplateId, "code": code, "problemSetId": problemSetId}, "router": {"psid": problemSetId, "gid": gid, "pid": pid}},
            verify=False
        )
        return response.json()