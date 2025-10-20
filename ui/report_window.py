from PyQt5 import QtWidgets
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image
from io import BytesIO

def export_pdf(path, rows):
    c = canvas.Canvas(path, pagesize=letter)
    w,h = letter
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, h-50, 'Inventory Report')
    c.setFont('Helvetica', 10)
    c.drawString(40, h-70, f'Generated: {datetime.utcnow().isoformat()} (UTC)')
    y = h-100
    c.setFont('Helvetica-Bold', 9)
    c.drawString(40,y,'ID'); c.drawString(70,y,'Name'); c.drawString(260,y,'Category'); c.drawString(350,y,'Qty'); c.drawString(400,y,'Price'); c.drawString(460,y,'Value')
    y -= 15
    c.setFont('Helvetica', 9)
    total = 0.0
    for r in rows:
        if y < 80:
            c.showPage(); y = h-50
        qty = int(r['quantity'] or 0); price = float(r['price'] or 0.0)
        val = qty*price; total += val
        c.drawString(40,y,str(r['id'])); c.drawString(70,y, str(r['name'])[:28]); c.drawString(260,y,str(r['category'])[:16])
        c.drawRightString(380,y,str(qty)); c.drawRightString(440,y,f"{price:.2f}"); c.drawRightString(520,y,f"{val:.2f}")
        y -= 18
    y -= 10
    c.setFont('Helvetica-Bold', 10)
    c.drawString(40,y, f'Total inventory value: {total:.2f}')
    c.save()

class ReportWindow(QtWidgets.QWidget):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows
        self.setWindowTitle('Reports')
        self.resize(300,100)
        layout = QtWidgets.QVBoxLayout(self)
        btn = QtWidgets.QPushButton('Save PDF Report'); btn.clicked.connect(self.save)
        layout.addWidget(btn)

    def save(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save PDF', 'inventory_report.pdf', 'PDF Files (*.pdf)')
        if path:
            export_pdf(path, self.rows)
            QtWidgets.QMessageBox.information(self, 'Saved', f'PDF saved to {path}')
