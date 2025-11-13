from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QCalendarWidget, QListWidget, QInputDialog, QLabel, QFrame, QMessageBox,
    QLineEdit
)
from PyQt5.QtCore import QDate, pyqtSignal
import sys
from system import DutyManagementSystem

class Dashboard(QMainWindow):
    logged_out = pyqtSignal()
    
    def __init__(self, system, current_user):
        super().__init__()
        
        self.system = system
        self.user = current_user
        
        self.setWindowTitle(f"Duty Management System - {self.user.name} ({self.user.role})")
        self.setGeometry(200, 100, 900, 500)

        main_layout = QHBoxLayout()

        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("background-color: #B71C1C; color: white;")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(20)

        self.btnAddEvent = QPushButton("Add Event")
        self.btnDutyHours = QPushButton("Duty Hours")
        self.btnLogout = QPushButton("Logout")

        for btn in [self.btnAddEvent, self.btnDutyHours, self.btnLogout]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #D32F2F; color: white;
                    border-radius: 8px; padding: 8px; font-weight: bold;
                }
                QPushButton:hover { background-color: #E53935; }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        main_content = QWidget()
        content_layout = QVBoxLayout()

        header = QLabel(" Duty Calendar")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.show_events)

        self.event_list = QListWidget()
        self.event_list.setStyleSheet("background-color: #f8f8f8; border-radius: 6px;")

        self.btnAddEvent.clicked.connect(self.add_event)
        self.btnLogout.clicked.connect(self.logout_action)
        self.btnDutyHours.clicked.connect(self.view_duty_hours)

        content_layout.addWidget(header)
        content_layout.addWidget(self.calendar)
        content_layout.addWidget(QLabel("Events for selected date:"))
        content_layout.addWidget(self.event_list)
        main_content.setLayout(content_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(main_content)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.apply_role_permissions()
        self.show_events()

    def show_events(self):
        selected_date = self.calendar.selectedDate()
        self.event_list.clear()
        
        events_from_db = self.system.get_events(selected_date)
        
        if events_from_db:
            for event_tuple in events_from_db:
                self.event_list.addItem(event_tuple[0])
        else:
            self.event_list.addItem("No events for this day.")

    def add_event(self):
        selected_date = self.calendar.selectedDate()
        text, ok = QInputDialog.getText(self, "Add Event", "Enter event name:")
        
        if ok and text:
            self.system.add_event(selected_date, text)
            self.show_events()

    def logout_action(self):
        print(f"Logging out {self.user.name}...")
        self.logged_out.emit()

    def view_duty_hours(self):
        msg = QMessageBox()
        msg.setWindowTitle("Duty Hours Summary")
        msg.setIcon(QMessageBox.Information)
        
        if self.user.role == "Member":
            total_hours = self.user.duty_hours
            msg.setText(f"You have rendered a total of {total_hours} duty hours.")
            msg.setInformativeText("Detailed event list is coming soon.")
        else:
            msg.setText("Duty hour tracking is available for Members.")
        
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def apply_role_permissions(self):
        if self.user.role == "Member":
            self.btnAddEvent.hide()
            
        if self.user.role == "Administrator":
            self.btnDutyHours.hide()
            
        if self.user.role == "Team Leader":
            self.btnDutyHours.hide()


class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(DutyManagementSystem, object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duty Management System - Login")
        self.setGeometry(400, 200, 300, 250)
        self.system = DutyManagementSystem()

        self.central = QWidget()
        self.layout = QVBoxLayout()

        self.label = QLabel("Login to your account")
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("Student ID")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton("Login")
        self.signup_btn = QPushButton("Sign Up")

        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.open_signup)

        for w in [self.label, self.student_id, self.password, self.login_btn, self.signup_btn]:
            self.layout.addWidget(w)

        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

    def login(self):
        student_id = self.student_id.text().strip()
        password = self.password.text().strip()
        if self.system.login(student_id, password):
            self.login_successful.emit(self.system, self.system.current_user)
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid Student ID or Password")

    def open_signup(self):
        self.signup_window = SignupWindow(self.system)
        self.signup_window.show()


class SignupWindow(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.setWindowTitle("Sign Up - Duty Management System")
        self.setGeometry(420, 220, 350, 400)

        self.central = QWidget()
        self.layout = QVBoxLayout()

        self.name = QLineEdit(); self.name.setPlaceholderText("Full Name")
        self.student_id = QLineEdit(); self.student_id.setPlaceholderText("Student ID")
        self.course = QLineEdit(); self.course.setPlaceholderText("Course and Year")
        self.contact = QLineEdit(); self.contact.setPlaceholderText("Contact Number")
        self.password = QLineEdit(); self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QLineEdit(); self.role.setPlaceholderText("Role (1=Member, 2=Leader, 3=Admin)")

        self.signup_btn = QPushButton("Register")
        self.signup_btn.clicked.connect(self.signup_user)

        for w in [self.name, self.student_id, self.course, self.contact, self.password, self.role, self.signup_btn]:
            self.layout.addWidget(w)

        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

    def signup_user(self):
        if self.system.signup(
            self.student_id.text().strip(),
            self.name.text().strip(),
            self.course.text().strip(),
            self.contact.text().strip(),
            self.password.text().strip(),
            self.role.text().strip()
        ):
            QMessageBox.information(self, "Success", "Signup successful! You can now log in.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Signup failed. Try again.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login_win = LoginWindow()
    main_window = None

    def show_dashboard(system_obj, user_obj):
        global main_window
        main_window = Dashboard(system_obj, user_obj)
        main_window.logged_out.connect(show_login)
        main_window.show()

    def show_login():
        if main_window:
            main_window.close()
        login_win.show()

    login_win.login_successful.connect(show_dashboard)
    login_win.show()
    
    sys.exit(app.exec_())