import sys
from PyQt6.QtWidgets import QApplication
from gui import MainView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec())
