import httpx
import xml.dom.minidom
import getpass
import pyinputplus as pyip

class AuthenticationError(Exception):
    pass

class Login:
    '''
    Login class
    '''

    @classmethod
    def from_input(cls):
        '''
        Return a Login object from user input

        params: None
        Input: input username and password
        return: Login object
        '''

        try:
            username = pyip.inputRegex(r'\d{12}', prompt='请输入学号：', limit=3)
        except pyip.RetryLimitException:
            print("输入错误次数过多，程序退出。")
            exit(1)
        
        password = getpass.getpass("请输入密码：")
        sTicket = Login.get_sTicket("https://pass.sdu.edu.cn/", username, password)
        return cls(username, password, sTicket)
    
    def __init__(self, username, password, sTicket):
        self.username, self.password, self.sTicket = username, password, sTicket
        self.base_url = "https://pass.sdu.edu.cn/"


    def get_user_name_and_id(self):
        '''
        Return user name and id
        '''
        user_data = xml.dom.minidom.parseString(httpx.get(
            f"{self.base_url}cas/serviceValidate",
            params={"ticket": self.sTicket, "service": "https://service.sdu.edu.cn/tp_up/view?m=up"},
        ).text)

        # log the user_data into a file
        # with open("user_data.xml", "w") as f:
        #     f.write(user_data.toprettyxml()) 

        name = user_data.getElementsByTagName("cas:USER_NAME")[0].childNodes[0].data
        student_id = user_data.getElementsByTagName("sso:user")[0].childNodes[0].data
        return name, student_id
    
    


    @staticmethod
    def get_sTicket(base_url, username, password):
        '''
        Return sTicket

        params: base_url(str), username(str), password (str)
        return: sTicket (str)
        '''
        try:
            # 发送第一个请求，获取ticket
            ticket = httpx.post(
                f"{base_url}cas/restlet/tickets",
                data={"username": username, "password": password, "lt": "LT-1-1-1"},
            ).text

            # 检查ticket是否以TGT开头
            if not ticket.startswith("TGT"):
                # raise AuthenticationError("Ticket should start with TGT. Check your username and password.")
                raise Exception("Ticket should start with TGT. Check your username and password.")
            # 发送第二个请求，获取sTicket
            sTicket = httpx.post(
                f"{base_url}cas/restlet/tickets/{ticket}",
                content="service=https://service.sdu.edu.cn/tp_up/view?m=up",
                headers={"Content-Type": "text/plain"}
            ).text

            # 检查sTicket是否以ST开头
            if not sTicket.startswith("ST"):
                raise AuthenticationError("sTicket should start with ST")
            
            # 这里假定sTicket获取成功，将 姓名、学号 写入文件
            # with open("user_data.json", "w") as f:
            #     f.write(f"{{\"username\": \"{username}\", \"password\": \"{password}\"}}")

            return sTicket
        
        except Exception as e:
            print("登录失败，请检查用户名和密码是否正确。")
            # print(e)
            exit(1)
