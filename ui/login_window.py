from PyQt5 import QtWidgets
from utils.auth import check_password
from db import find_user

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login - Inventory')
        self.resize(360, 140)
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        self.user = QtWidgets.QLineEdit(); self.pw = QtWidgets.QLineEdit(); self.pw.setEchoMode(QtWidgets.QLineEdit.Password)
        form.addRow('Username:', self.user); form.addRow('Password:', self.pw)
        layout.addLayout(form)
        btns = QtWidgets.QHBoxLayout()
        self.login_btn = QtWidgets.QPushButton('Login'); self.login_btn.clicked.connect(self.attempt_login)
        self.register_btn = QtWidgets.QPushButton('Register'); self.register_btn.clicked.connect(self.open_register)
        btns.addWidget(self.login_btn); btns.addWidget(self.register_btn)
        layout.addLayout(btns)
        self.message = QtWidgets.QLabel('')
        layout.addWidget(self.message)
        self.callback = None  # to be set by caller

    def attempt_login(self):
        username = self.user.text().strip(); pw = self.pw.text().strip()
        if not username or not pw:
            self.message.setText('Enter username and password')
            return
        row = find_user(username)
        if not row:
            self.message.setText('User not found')
            return
        # row['password'] is bytes stored in sqlite; PySQLite returns as bytes object
        if check_password(pw, row['password']):
            # login success
            if self.callback:
                self.callback(dict(row))
        else:
            self.message.setText('Invalid credentials')

    def open_register(self):
        from ui.register_window import RegisterWindow
        dlg = RegisterWindow(self)
        dlg.exec_()
