from PyQt5 import QtWidgets
from datetime import datetime

class AddProductDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle('Add Product' if product is None else 'Edit Product')
        self.resize(480,420)
        self.product = product or {}
        layout = QtWidgets.QFormLayout(self)
        self.name = QtWidgets.QLineEdit(self.product.get('name',''))
        self.sku = QtWidgets.QLineEdit(self.product.get('sku',''))
        self.category = QtWidgets.QLineEdit(self.product.get('category',''))
        self.qty = QtWidgets.QSpinBox(); self.qty.setMaximum(10**9); self.qty.setValue(int(self.product.get('quantity',0)))
        self.price = QtWidgets.QDoubleSpinBox(); self.price.setMaximum(10**9); self.price.setDecimals(2); self.price.setValue(float(self.product.get('price',0.0)))
        self.supplier = QtWidgets.QLineEdit(self.product.get('supplier',''))
        self.image = QtWidgets.QLineEdit(self.product.get('image_path',''))
        img_btn = QtWidgets.QPushButton('Browse...'); img_btn.clicked.connect(self.browse)
        h = QtWidgets.QHBoxLayout(); h.addWidget(self.image); h.addWidget(img_btn)
        self.desc = QtWidgets.QPlainTextEdit(self.product.get('description',''))

        layout.addRow('Name:', self.name)
        layout.addRow('SKU:', self.sku)
        layout.addRow('Category:', self.category)
        layout.addRow('Quantity:', self.qty)
        layout.addRow('Price:', self.price)
        layout.addRow('Supplier:', self.supplier)
        layout.addRow('Image:', h)
        layout.addRow('Description:', self.desc)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def browse(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if path:
            self.image.setText(path)

    def get_data(self):
        return {
            'name': self.name.text().strip(),
            'sku': self.sku.text().strip(),
            'category': self.category.text().strip(),
            'quantity': self.qty.value(),
            'price': self.price.value(),
            'supplier': self.supplier.text().strip(),
            'image_path': self.image.text().strip(),
            'description': self.desc.toPlainText().strip(),
            'added_date': datetime.utcnow().isoformat()
        }
