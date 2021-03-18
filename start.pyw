from design import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import algorithm


app = QApplication(sys.argv)
window = MainWindow()
window.saving_sgl.connect(algorithm.make_prescription)
window.show()
sys.exit(app.exec_())
