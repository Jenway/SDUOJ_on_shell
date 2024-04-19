import pyinputplus as pyip
import json
import os
from getpass import getpass

class Uhandler:
    @staticmethod
    def get_user_credentials()->tuple:
        try:
            with open("user_data.json", "r") as f:
                user_data = json.load(f)
                # self.username, self.password  = user_data["username"], user_data["password"]
                return user_data["username"], user_data["password"]
        except FileNotFoundError:
            print("未找到用户数据文件，需要重新输入用户名和密码。")
            username, password = Uhandler.get_user_input()
            with open("user_data.json", "w") as f:
                json.dump({"username": username, "password": password}, f)
        
        return username, password


    @staticmethod
    def get_user_input() -> tuple:
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