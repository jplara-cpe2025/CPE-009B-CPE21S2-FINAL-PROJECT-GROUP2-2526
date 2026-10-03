import sys
import os
import ctypes
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtGui import QIcon, QMovie, QGuiApplication

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('lab4.pyqt6.gui')
except Exception:
    pass


class App(QWidget):
    def center_window(self):
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width) // 2 + screen_geometry.left()
        y = (screen_geometry.height() - self.height) // 2 + screen_geometry.top()

        self.move(x, y)

    def __init__(self):
        super().__init__()
        self.title = "PyQt Labels"
        self.x = 200
        self.y = 200
        self.width = 300
        self.height = 300
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.center_window()

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Window Icon
        icon_path = os.path.join(script_dir, 'pythonico.ico')
        self.setWindowIcon(QIcon(icon_path))

        # GIF Integration
        gif_path = os.path.join(script_dir, 'giphy.gif')
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(100, 160, 100, 100)
        self.movie = QMovie(gif_path)
        self.gif_label.setMovie(self.movie)
        self.gif_label.setScaledContents(True)
        self.movie.start()

        # Labels
        self.textboxlbl = QLabel("Hello World!", self)
        self.textboxlbl.move(110, 50)
        self.sublbl = QLabel("This program is written in Visual Studio", self)
        self.sublbl.move(35, 90)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())