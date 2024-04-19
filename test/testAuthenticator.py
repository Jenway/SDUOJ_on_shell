import xml.dom.minidom
from SDUOJ.utils.Authenticator import Authenticator
import httpx

class Tester:
    '''
    test class
    '''

    def __init__(self):
        self.auth = Authenticator()

    def get_user_name_and_id(self):
        '''
        Return user name and id
        '''
        service = "https://service.sdu.edu.cn/tp_up/view?m=up"
        sTicket = self.auth.get_sTicket(_content=f"service={service}")
        user_data = xml.dom.minidom.parseString(httpx.get(
            f"https://pass.sdu.edu.cn/cas/serviceValidate",
            params={"ticket": sTicket, "service": service}
        ).text)

        # log the user_data into a file
        # with open("user_data.xml", "w") as f:
        #     f.write(user_data.toprettyxml()) 

        name = user_data.getElementsByTagName("cas:USER_NAME")[0].childNodes[0].data
        student_id = user_data.getElementsByTagName("sso:user")[0].childNodes[0].data
        return name, student_id

    # 添加功能
    # Login class 中已经有了 username, password, sTicket, base_url
    # 通过 httpx.get() 获取 user_data