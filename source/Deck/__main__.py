import sys
from PyQt6.QtWidgets import QApplication
from ui import SpotifyDeck

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpotifyDeck()
    window.show()
    sys.exit(app.exec())
