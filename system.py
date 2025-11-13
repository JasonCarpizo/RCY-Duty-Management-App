import hashlib
import inspect
from db import get_connection, initialize_db
from user import Member, TeamLeader, Administrator

class DutyManagementSystem:
    def __init__(self):
        self.current_user = None
        initialize_db()

    def signup(self, student_id, name, course, contact_num, password, role_choice):
        conn = get_connection()
        cursor = conn.cursor()

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM Users WHERE studentIDNumber = ?", (student_id,))
        if cursor.fetchone():
            print("Error: A user with this ID already exists.")
            conn.close()
            return False

        role = {'1': "Member", '2': "Team Leader", '3': "Administrator"}.get(role_choice)
        if not role:
            print("Invalid role choice.")
            conn.close()
            return False

        cursor.execute("""
        INSERT INTO Users (studentIDNumber, name, course, contactNumber, password, userRole)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, course, contact_num, hashed_pw, role))
        conn.commit()
        conn.close()
        print(f"Sign up successful! Welcome, {name}. Your role is {role}.")
        return True

    def login(self, student_id, password):
        conn = get_connection()
        cursor = conn.cursor()

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM Users WHERE studentIDNumber = ? AND password = ?", (student_id, hashed_pw))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            student_id, name, course, contact, pw, role = user_data
            
            if role == "Member":
                self.current_user = Member(student_id, name, course, contact)
            elif role == "Team Leader":
                self.current_user = TeamLeader(student_id, name, course, contact)
            else:
                self.current_user = Administrator(student_id, name, course, contact)
            
            print(f"Welcome, {self.current_user.name}! You are logged in as {self.current_user.role}.")
            return True
        else:
            print("Invalid credentials.")
            return False

    def add_event(self, date, name):
        conn = get_connection()
        cursor = conn.cursor()
        date_str = date.toString("yyyy-MM-dd")
        cursor.execute("""
        INSERT INTO Events (eventDate, eventName) VALUES (?, ?)
        """, (date_str, name))
        conn.commit()
        conn.close()
        print(f"Event '{name}' added for {date_str}")

    def get_events(self, date):
        conn = get_connection()
        cursor = conn.cursor()
        date_str = date.toString("yyyy-MM-dd")
        cursor.execute("SELECT eventName FROM Events WHERE eventDate = ?", (date_str,))
        events = cursor.fetchall()
        conn.close()
        return events