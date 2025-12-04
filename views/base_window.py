from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class BaseWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
    def create_scroll_area(self, content_widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        return scroll
        
    def create_title(self, text, font_size=20, color="#000000"):
        title = QLabel(text)
        title.setStyleSheet(f"font-size: {font_size}px; font-weight: bold; color: {color};")
        title.setAlignment(Qt.AlignCenter)
        return title