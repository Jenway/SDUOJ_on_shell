import pyinputplus as pyip
from getpass import getpass

class UserInputHandler:
    @staticmethod
    def get_user_credentials():
        # get and return user credentials
        try:
            username = pyip.inputRegex(r'\d{12}', prompt='请输入学号：', limit=3)
        except pyip.RetryLimitException:
            print("输入错误次数过多，程序退出。")
            exit(1)
        password = getpass("请输入密码：")
        return username, password

    @staticmethod
    def validate_input(input):
        # validate the input and return True or False
        pass
