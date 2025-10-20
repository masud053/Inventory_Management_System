from PyQt5 import QtWidgets
from db import add_user, find_user

class RegisterWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Register Account')
        self.resize(360,200)
        layout = QtWidgets.QFormLayout(self)
        self.username = QtWidgets.QLineEdit(); self.pw = QtWidgets.QLineEdit(); self.pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pw2 = QtWidgets.QLineEdit(); self.pw2.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addRow('Username:', self.username); layout.addRow('Password:', self.pw); layout.addRow('Confirm:', self.pw2)
        self.msg = QtWidgets.QLabel('')
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.register); btns.rejected.connect(self.reject)
        layout.addRow(btns); layout.addRow(self.msg)

    def register(self):
        u = self.username.text().strip(); p = self.pw.text().strip(); p2 = self.pw2.text().strip()
        if not u or not p:
            self.msg.setText('Provide username and password'); return
        if p != p2:
            self.msg.setText('Passwords do not match'); return
        if find_user(u):
            self.msg.setText('Username already exists'); return
        add_user(u, p, role='user')
        QtWidgets.QMessageBox.information(self, 'Success', 'Account created. You can now login.')
        self.accept()
