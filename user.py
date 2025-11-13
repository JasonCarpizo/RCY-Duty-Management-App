class User:
    def __init__(self, student_id, name, course, contact_num, role):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.contact_num = contact_num
        self.role = role 
        self._is_logged_in = True
    
    def display_profile(self):
        print(f"\n--- User Profile ---")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Role: {self.role}")
        print(f"Course: {self.course}")
        print("--------------------")

    def logout(self):
        self._is_logged_in = False
        print(f"\n{self.name} has been logged out.")


class Member(User):
    def __init__(self, student_id, name, course, contact_num):
        super().__init__(student_id, name, course, contact_num, role="Member")
        self.duty_hours = 0
        self.attended_events = []

class TeamLeader(User):
    def __init__(self, student_id, name, course, contact_num):
        super().__init__(student_id, name, course, contact_num, role="Team Leader")

class Administrator(User):
    def __init__(self, student_id, name, course, contact_num):
        super().__init__(student_id, name, course, contact_num, role="Administrator")