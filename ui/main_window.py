from PyQt5 import QtWidgets, QtCore
from db import fetch_products, add_product, update_product, delete_product
from ui.add_product_dialog import AddProductDialog
from ui.report_window import ReportWindow
from ui.dashboard_window import DashboardWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f'Inventory - Logged in: {user["username"]} ({user["role"]})')
        self.resize(1000,600)
        central = QtWidgets.QWidget(); self.setCentralWidget(central)
        v = QtWidgets.QVBoxLayout(central)
        top = QtWidgets.QHBoxLayout()
        self.search = QtWidgets.QLineEdit(); self.search.setPlaceholderText('Search...'); self.search.returnPressed.connect(self.refresh)
        top.addWidget(self.search)
        self.search_btn = QtWidgets.QPushButton('Search'); self.search_btn.clicked.connect(self.refresh); top.addWidget(self.search_btn)
        self.add_btn = QtWidgets.QPushButton('Add'); self.add_btn.clicked.connect(self.add_item); top.addWidget(self.add_btn)
        self.edit_btn = QtWidgets.QPushButton('Edit'); self.edit_btn.clicked.connect(self.edit_item); top.addWidget(self.edit_btn)
        self.del_btn = QtWidgets.QPushButton('Delete'); self.del_btn.clicked.connect(self.delete_item); top.addWidget(self.del_btn)
        self.report_btn = QtWidgets.QPushButton('Report'); self.report_btn.clicked.connect(self.open_report); top.addWidget(self.report_btn)
        if self.user['role'] == 'admin':
            self.dashboard_btn = QtWidgets.QPushButton('Admin Dashboard'); self.dashboard_btn.clicked.connect(self.open_dashboard); top.addWidget(self.dashboard_btn)
        v.addLayout(top)

        self.table = QtWidgets.QTableWidget(0,9); self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setHorizontalHeaderLabels(['ID','Name','SKU','Category','Qty','Price','Value','Supplier','Image'])
        v.addWidget(self.table)
        self.status = QtWidgets.QLabel(''); v.addWidget(self.status)
        self.apply_role(); self.refresh()

    def apply_role(self):
        if self.user['role'] != 'admin':
            self.add_btn.setEnabled(False); self.edit_btn.setEnabled(False); self.del_btn.setEnabled(False)
        else:
            self.add_btn.setEnabled(True); self.edit_btn.setEnabled(True); self.del_btn.setEnabled(True)

    def refresh(self):
        text = self.search.text().strip()
        rows = fetch_products(text or None)
        self.table.setRowCount(0)
        total_items = 0; total_value = 0.0
        for r in rows:
            idx = self.table.rowCount(); self.table.insertRow(idx)
            qty = int(r['quantity'] or 0); price = float(r['price'] or 0.0)
            total_items += qty; total_value += qty*price
            self.table.setItem(idx,0, QtWidgets.QTableWidgetItem(str(r['id'])))
            self.table.setItem(idx,1, QtWidgets.QTableWidgetItem(r['name'] or ''))
            self.table.setItem(idx,2, QtWidgets.QTableWidgetItem(r['sku'] or ''))
            self.table.setItem(idx,3, QtWidgets.QTableWidgetItem(r['category'] or ''))
            self.table.setItem(idx,4, QtWidgets.QTableWidgetItem(str(qty)))
            self.table.setItem(idx,5, QtWidgets.QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(idx,6, QtWidgets.QTableWidgetItem(f"{qty*price:.2f}"))
            self.table.setItem(idx,7, QtWidgets.QTableWidgetItem(r['supplier'] or ''))
            self.table.setItem(idx,8, QtWidgets.QTableWidgetItem(r['image_path'] or ''))
        self.status.setText(f'Total items: {total_items}    Total value: {total_value:.2f}')

    def get_selected_id(self):
        sel = self.table.selectedItems()
        if not sel: return None
        row = sel[0].row(); return int(self.table.item(row,0).text())

    def add_item(self):
        dlg = AddProductDialog(self)
        if dlg.exec_():
            data = dlg.get_data(); add_product(data); QtWidgets.QMessageBox.information(self, 'Added','Product added'); self.refresh()

    def edit_item(self):
        pid = self.get_selected_id()
        if not pid: QtWidgets.QMessageBox.information(self, 'Select','Select a product'); return
        from db import get_connection
        conn = get_connection(); cur = conn.cursor(); cur.execute('SELECT * FROM products WHERE id=?', (pid,)); row = cur.fetchone(); conn.close()
        dlg = AddProductDialog(self, product=dict(row))
        if dlg.exec_():
            update_product(pid, dlg.get_data()); QtWidgets.QMessageBox.information(self, 'Updated','Product updated'); self.refresh()

    def delete_item(self):
        pid = self.get_selected_id()
        if not pid: QtWidgets.QMessageBox.information(self, 'Select','Select a product'); return
        ok = QtWidgets.QMessageBox.question(self, 'Confirm', 'Delete selected product?')
        if ok == QtWidgets.QMessageBox.StandardButton.Yes:
            delete_product(pid); QtWidgets.QMessageBox.information(self, 'Deleted','Product deleted'); self.refresh()

    def open_report(self):
        rows = fetch_products()
        self.report_window = ReportWindow(rows); self.report_window.show()

    def open_dashboard(self):
        self.dashboard = DashboardWindow(); self.dashboard.show()
