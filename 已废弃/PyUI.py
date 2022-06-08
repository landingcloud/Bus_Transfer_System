import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui_main import Ui_MainWindow

class UiMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(UiMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UiMainWindow()
    win.show()
    sys.exit(app.exec_())
