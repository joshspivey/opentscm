from PyQt5.QtWidgets import QMainWindow

from . import MainWindow_ui


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
