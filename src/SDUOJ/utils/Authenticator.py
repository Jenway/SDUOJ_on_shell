from .UserInputHandler import Uhandler
import httpx

class AuthenticationError(Exception):
    pass

class Authenticator:
    def __init__(self):
        self.username, self.password = Uhandler.get_user_credentials()

    def get_sTicket(self,_content="service=https://service.sdu.edu.cn/tp_up/view?m=up"):
        '''
        params: base_url(str), username(str), password (str)
        return: sTicket (str)
        '''
        ticket = self.get_TGT(self.username, self.password)
        try:
            # 发送第二个请求，获取sTicket
            sTicket = httpx.post(
                f"https://pass.sdu.edu.cn/cas/restlet/tickets/{ticket}",
                content= _content,
                headers={"Content-Type": "text/plain"}
            ).text

            # 检查sTicket是否以ST开头
            if not sTicket.startswith("ST"):
                raise AuthenticationError("sTicket should start with ST")

            return sTicket
        
        except Exception as e:
            print("登录失败，请检查用户名和密码是否正确。")
            # print(e)
            exit(1)
    
    @staticmethod
    def get_TGT(username, password):
        '''
        Return TGT
        params: base_url(str), username(str), password (str)
        return: TGT (str)
        '''
        try:
            # 发送第一个请求，获取ticket
            ticket = httpx.post(
                "https://pass.sdu.edu.cn/cas/restlet/tickets",
                data={"username": username, "password": password, "lt": "LT-1-1-1"},
            ).text
            # 检查ticket是否以TGT开头
            if not ticket.startswith("TGT"):
                # raise AuthenticationError("Ticket should start with TGT. Check your username and password.")
                raise Exception("Ticket should start with TGT. Check your username and password.")
            return ticket
        
        except Exception as e:
            print("登录失败，请检查用户名和密码是否正确。")
            # print(e)
            exit(1)
