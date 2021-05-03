from design import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
app.setStyle('Fusion')
with open(r'stylesheet.qss') as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()
sys.exit(app.exec_())
