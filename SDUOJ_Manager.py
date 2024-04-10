from email import header
import json
import os
from Authenticator import Authenticator
import httpx
from utils.FileHandler import debugprint

class SDUOJ_Manager:
    def __init__(self):
        self.auth = Authenticator()
        self.sduoj_cookie = self.login_to_sduoj()

    base_url = "https://oj.qd.sdu.edu.cn/"
    cookie_file = "sduoj_cookie.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": ""
    }

    def request_get(self, url, params={}, verify=False):
        return httpx.get(
            f"{self.base_url}{url}",
            headers=self.headers,
            params=params,
            cookies={"SESSION": self.sduoj_cookie},
            verify=verify
        )
    def request_post(self, url, json, verify=False):
        return httpx.post(
            f"{self.base_url}{url}",
            headers=self.headers,
            json=json,
            cookies={"SESSION": self.sduoj_cookie},
            verify=verify
        )

    def login_to_sduoj(self) -> str:
        def load_cookie_from_file():
            if self.cookie_file in os.listdir():
                with open(self.cookie_file, "r") as f:
                    return json.load(f)["cookie"]
            return None

        def save_cookie_to_file(cookie):
            with open(self.cookie_file, "w") as f:
                json.dump({"cookie": cookie}, f)

        def getAndSaveCookie():
            cookie = self.get_cookie()
            save_cookie_to_file(cookie)
            return cookie

        exist_cookie = load_cookie_from_file()
        if exist_cookie and not SDUOJ_Manager.if_cookie_expired(exist_cookie):
            return exist_cookie
        else:
            return getAndSaveCookie()

    def get_cookie(self)->str:
        service = f"{self.base_url}v2/thirdPartyLogin?thirdParty=SDUCAS"
        sTicket = self.auth.get_sTicket(_content=f"service={service}")
        params = {"thirdParty": "SDUCAS", "ticket": sTicket}

        try:
            response = httpx.get(f"{self.base_url}api/user/thirdPartyLogin", headers=self.headers, params=params, verify=False)
        except Exception as e:
            print("Error in getting cookie: ", e)
            exit(1)
        finally:
            if response.status_code != 200 or "Set-Cookie" not in response.headers:
                print(f"Error in getting cookie: {response.status_code}")
                exit(1)
        return response.headers["Set-Cookie"].split("=")[1].split(";")[0]

    @staticmethod
    def if_cookie_expired(cookie):
        """
        Check if the cookie has expired
        """
        response = httpx.get(
            f"{SDUOJ_Manager.base_url}api/user/getProfile",
            headers=SDUOJ_Manager.headers,
            cookies={"SESSION": cookie},
            verify=False
        )
        if response.status_code == 401:
            print("Cookie has expired.")
            return True
        if response.status_code != 200:
            print(f"Error in checking cookie: {response.status_code}")
            return True
        # print data-username and nickname
        print(f"Hello, {response.json()['data']['nickname']}! Your username is {response.json()['data']['username']}.")
        return False


    def getProfile(self):
        response = self.request_get(
            "api/user/getProfile",
        )
        return response.json()
    
    def getGroupList(self):
        response = self.request_get(
            "api/group/page",
            params={"pageNow": 1, "pageSize": 12, "isParticipating": 1},
        )
        return response.json()

    def getProblemSetLabel(self, groupId):
        response = self.request_post(
            "api/ps/problem_set/key",
            json={"groupId": groupId},
        )
        return response.json()
    
    def searchProblemSet(self, groupId, label, pageNow=1, pageSize=20):
        response = self.request_post(
            "api/ps/problem_set/search",
            json={"pageNow": pageNow, "pageSize": pageSize, "groupId": groupId, "tag": label},
        )
        return response.json()
    
    def getProblemSetInfo(self, problemSetId):
        response = self.request_post(
            "api/ps/problem_set/info_c",
            json={"psid": problemSetId},
        )
        return response.json()
    
    def getProblemInfo(self, problemSetId, gid, pid):
        response = self.request_post(
            "api/ps/problem_set/pro_info",
            json={"router": {"psid": problemSetId, "gid": gid, "pid": pid}},
        )
        return response.json()


    # /api/ps/answer_sheet/answer
    def answerProblem(self, problemSetId, gid, pid, code, judgeTemplateId):
        # json {"data":{"judgeTemplateId":"13","code":"print(5)","problemSetId":"71"},"router":{"psid":"71","gid":"0","pid":"0"}}
        response = self.request_post(
            "api/ps/answer_sheet/answer",
            json={"data": {"judgeTemplateId": judgeTemplateId, "code": code, "problemSetId": problemSetId}, "router": {"psid": problemSetId, "gid": gid, "pid": pid}},

        )
        return response.json()
    
    # /api/ps/answer_sheet/answer
    def answerProblemMD(self, problemSetId, gid, pid, code):
        # {"data":[],"router":{"psid":"71","gid":"1","pid":"3"}}
        response = self.request_post(
            "api/ps/answer_sheet/answer",
            json={"data": [code], "router": {"psid": problemSetId, "gid": gid, "pid": pid}},
        )
        return response.json()


    # api/ps/answer_sheet/submissionInfo
    # {psid: "71", gid: "0", pid: "1", submissionId: "7d71c5057403c8a"}

    def getSubmissionInfo(self, problemSetId, gid, pid, submissionId):
        response = self.request_post(
            "api/ps/answer_sheet/submissionInfo",
            json={"psid": problemSetId, "gid": gid, "pid": pid, "submissionId": submissionId},

        )
        return response.json()["data"]["judgeScore"]
    
    # 	api/contest/list?pageNow=1&pageSize=15&groupId=30
    def searchContest(self, groupId, pageNow=1, pageSize=15):
        # json {"pageNow":1,"pageSize":15,"groupId":"30"}
        response = self.request_get(
            "api/contest/list",
            params={"pageNow": pageNow, "pageSize": pageSize, "groupId": groupId},
        )
        return response.json()
    
    def getContestList(self, contestId):
        # api/contest/query?contestId=318
        response = self.request_get(
            "api/contest/query",
            params={"contestId": contestId},
        )
        return response.json()
    
    # api/contest/queryProblem?contestId=318&problemCode=1
    def getContestProblem(self, contestId, problemCode):
        response = self.request_get(
            "api/contest/queryProblem",
            params={"contestId": contestId, "problemCode": problemCode},
        )
        return response.json()
    
    # api/contest/createSubmission
    def createContestSubmission(self, code, problemCode, contestId, judgeTemplateId):
        # {"judgeTemplateId":"6","code":"","problemCode":"1","contestId":"318"}
        response = self.request_post(
            "api/contest/createSubmission",
            json={"judgeTemplateId": judgeTemplateId, "code": code, "problemCode": problemCode, "contestId": contestId},
        )
        return response.json()
    
    # api/contest/querySubmission?contestId=318&submissionId=7d96654970032be
    def getContestSubmission(self, contestId, submissionId):
        response = self.request_get(
            "api/contest/querySubmission",
            params={"contestId": contestId, "submissionId": submissionId},
        )
        return response.json()