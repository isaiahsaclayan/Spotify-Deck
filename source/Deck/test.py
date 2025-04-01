from PyQt6.QtWidgets import QApplication, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QFontDatabase
import sys

class FontListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Available Fonts")
        self.setGeometry(100, 100, 400, 600)
        
        layout = QVBoxLayout()
        self.fontListWidget = QListWidget()
        layout.addWidget(self.fontListWidget)
        
        self.setLayout(layout)
        self.loadFonts()

    def loadFonts(self):
        fonts = QFontDatabase.families()
        self.fontListWidget.addItems(fonts)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontListApp()
    window.show()
    sys.exit(app.exec())