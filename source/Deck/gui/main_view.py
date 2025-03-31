from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget
from PyQt6.QtCore import QSize, Qt
import sys
import os
from .login_view import LoginView
from .player_view import PlayerView

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SpotiDeck")
        self.setFixedSize(QSize(320,460))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.stacked_widgets = QStackedWidget()
        self.login_view = LoginView()
        self.player_view = PlayerView()
        
        self.stacked_widgets.addWidget(self.login_view)
        self.stacked_widgets.addWidget(self.player_view)

        self.setCentralWidget(self.stacked_widgets)
        
    # Handle Drags
    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def switch_player_view(self):
        self.stacked_widgets.setCurrentIndex(1)

