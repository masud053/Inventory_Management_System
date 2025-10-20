from PyQt5 import QtWidgets
from db import fetch_products, fetch_users
import matplotlib.pyplot as plt

class DashboardWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Dashboard')
        self.resize(800,400)
        layout = QtWidgets.QVBoxLayout(self)
        stats_layout = QtWidgets.QHBoxLayout()
        self.total_products_lbl = QtWidgets.QLabel('Products: 0')
        self.total_value_lbl = QtWidgets.QLabel('Total Value: 0.00')
        self.user_count_lbl = QtWidgets.QLabel('Users: 0')
        stats_layout.addWidget(self.total_products_lbl); stats_layout.addWidget(self.total_value_lbl); stats_layout.addWidget(self.user_count_lbl)
        layout.addLayout(stats_layout)

        btns = QtWidgets.QHBoxLayout()
        self.refresh_btn = QtWidgets.QPushButton('Refresh'); self.refresh_btn.clicked.connect(self.refresh)
        self.users_btn = QtWidgets.QPushButton('Manage Users'); self.users_btn.clicked.connect(self.manage_users)
        self.chart_btn = QtWidgets.QPushButton('Show Category Chart'); self.chart_btn.clicked.connect(self.show_chart)
        btns.addWidget(self.refresh_btn); btns.addWidget(self.users_btn); btns.addWidget(self.chart_btn)
        layout.addLayout(btns)

        self.users_table = QtWidgets.QTableWidget(0,3)
        self.users_table.setHorizontalHeaderLabels(['ID','Username','Role'])
        layout.addWidget(self.users_table)
        self.refresh()

    def refresh(self):
        rows = fetch_products()
        total_items = 0; total_value = 0.0
        for r in rows:
            total_items += int(r['quantity'] or 0)
            total_value += int(r['quantity'] or 0) * float(r['price'] or 0.0)
        users = fetch_users()
        self.total_products_lbl.setText(f'Products: {len(rows)}')
        self.total_value_lbl.setText(f'Total Value: {total_value:.2f}')
        self.user_count_lbl.setText(f'Users: {len(users)}')

        # populate users table
        self.users_table.setRowCount(0)
        for r in users:
            idx = self.users_table.rowCount(); self.users_table.insertRow(idx)
            self.users_table.setItem(idx,0, QtWidgets.QTableWidgetItem(str(r['id'])))
            self.users_table.setItem(idx,1, QtWidgets.QTableWidgetItem(str(r['username'])))
            self.users_table.setItem(idx,2, QtWidgets.QTableWidgetItem(str(r['role'])))

    def manage_users(self):
        # simple role toggle for selected user
        sel = self.users_table.selectedItems()
        if not sel:
            QtWidgets.QMessageBox.information(self, 'Select', 'Select a user to toggle role')
            return
        row = sel[0].row()
        user_id = int(self.users_table.item(row,0).text())
        role = self.users_table.item(row,2).text()
        new_role = 'admin' if role != 'admin' else 'user'
        from db import update_user_role
        update_user_role(user_id, new_role)
        QtWidgets.QMessageBox.information(self, 'Updated', f'User role changed to {new_role}')
        self.refresh()

    def show_chart(self):
        rows = fetch_products()
        from collections import defaultdict
        cat = defaultdict(float)
        for r in rows:
            cat[r['category'] or 'Uncategorized'] += int(r['quantity'] or 0) * float(r['price'] or 0.0)
        labels = list(cat.keys()); values = list(cat.values())
        if not labels:
            QtWidgets.QMessageBox.information(self, 'No Data', 'No data to chart')
            return
        plt.figure(figsize=(8,4))
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
