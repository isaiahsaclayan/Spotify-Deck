from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtCore import QSize, Qt
import sys
import os

class SpotifyDeck(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SpotiDeck")
        self.setFixedSize(QSize(320,460))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    # Handle Drags
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

