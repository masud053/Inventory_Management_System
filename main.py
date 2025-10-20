import sys
from PyQt5 import QtWidgets
from db import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

def on_login(user):
    # close login and open main window
    app.login_win.close()
    app.main_win = MainWindow(user)
    app.main_win.show()

if __name__ == '__main__':
    init_db()
    app = QtWidgets.QApplication(sys.argv)
    app.login_win = LoginWindow(); app.login_win.callback = on_login
    app.login_win.show()
    sys.exit(app.exec_())
