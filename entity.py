
class Profile:
    def __init__(self, data):
        self.data = data
        self.username = data['username']
        self.nickname = data['nickname']
        self.email = data['email']
        self.phone = data['phone']
        self.gender = data['gender']
        self.studentId = data['studentId']
        self.roles = data['roles']
        self.sduId = data['sduId']
        self.groups = data['groups']
        self.ipv4 = data['ipv4']
        self.userAgent = data['userAgent']
    
    def __str__(self):
        return f"username: {self.username}\nnickname: {self.nickname}\nemail: {self.email}\nphone: {self.phone}\ngender: {self.gender}\nstudentId: {self.studentId}\nroles: {self.roles}\nsduId: {self.sduId}\ngroups: {self.groups}\nipv4: {self.ipv4}\nuserAgent: {self.userAgent}"

class Group:
    def __init__(self,row):
        self.groupId = row['groupId']
        self.gmtCreate = row['gmtCreate']
        self.openness = row['openness']
        self.title = row['title']
        self.memberNum = row['memberNum']
        self.description = row['description']
        self.userId = row['userId']
        self.status = row['status']
        self.owner = row['owner']


class ProblemSet:
    def __init__(self, row):
        self.psid = row['psid']
        self.description = row['description']
        self.global_score = row['global_score']
        self.tm_end = row['tm_end']
        self.manageGroupId = row['manageGroupId']
        self.tag = row['tag']
        self.name = row['name']
        self.type = row['type']
        self.tm_start = row['tm_start']
        self.username = row['username']
        self.groupId = row['groupId']
