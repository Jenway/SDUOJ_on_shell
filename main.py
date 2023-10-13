from login import Login

if __name__ == "__main__":
    login = Login.from_input()
    name, student_id = login.get_user_name_and_id()
    print(f"姓名: {name}\n学号: {student_id}")