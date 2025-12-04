from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont

class DienteWidget(QWidget):
    def __init__(self, numero):
        super().__init__()
        self.numero = numero
        self.estados = {}  # {"V": "sano", "O": "cariado", ...}
        self.tooltips = {}  # {"V": "Procedimiento/Obs", ...}
        self.setFixedSize(80, 100)

        # Definimos las posiciones de cada cara
        self.caras = {
            "V": QRect(15, 30, 20, 15),
            "O": QRect(45, 30, 20, 15),
            "L": QRect(15, 60, 20, 15),
            "P": QRect(45, 60, 20, 15),
            "M": QRect(30, 45, 20, 15),
            "D": QRect(50, 45, 20, 15)
        }

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Diente redondeado
        painter.setBrush(QBrush(QColor(248, 249, 250)))
        painter.setPen(QPen(QColor(52, 152, 219), 2))
        painter.drawRoundedRect(0, 0, self.width()-2, self.height()-2, 15, 15)

        # Número del diente
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignHCenter, str(self.numero))

        # Caras
        for cara, rect in self.caras.items():
            painter.setBrush(QBrush(self.obtener_color_estado(cara)))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawEllipse(rect)
            painter.setFont(QFont("Arial", 8, QFont.Bold))
            painter.drawText(rect.x()+5, rect.y()+12, cara)

    def obtener_color_estado(self, cara):
        estado = self.estados.get(cara, "sano")
        colores = {
            "sano": QColor(240, 248, 255),
            "cariado": QColor(220, 20, 60),
            "obturado": QColor(255, 215, 0),
            "corona": QColor(192, 192, 192),
            "extraccion": QColor(139, 0, 0),
            "implante": QColor(0, 100, 0),
            "protesis": QColor(138, 43, 226),
            "ausente": QColor(105, 105, 105)
        }
        return colores.get(estado, QColor(240, 248, 255))

    def actualizar_estado(self, cara, estado, tooltip=""):
        self.estados[cara] = estado
        self.tooltips[cara] = tooltip
        self.update()

    def mousePressEvent(self, event):
        click_pos = event.pos()
        for cara, rect in self.caras.items():
            if rect.contains(click_pos):
                info = self.tooltips.get(cara, "")
                if info:
                    QMessageBox.information(self, f"Diente {self.numero} - {cara}", info)
                break

class OdontogramaViewWidget(QWidget):
    def __init__(self, paciente_id, db):
        super().__init__()
        self.paciente_id = paciente_id
        self.db = db
        self.dientes = {}
        self.setup_ui()
        self.cargar_odontograma()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        titulo = QLabel("🦷 Odontograma - Vista")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size:16px;font-weight:bold;color:#2c3e50;padding:10px;")
        layout.addWidget(titulo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        dientes_layout = QGridLayout(content)
        dientes_layout.setSpacing(10)
        dientes_layout.setContentsMargins(10,10,10,10)

        # Crear dientes
        for i in range(1, 33):
            diente = DienteWidget(i)
            dientes_layout.addWidget(diente, (i-1)//8, (i-1)%8)
            self.dientes[i] = diente

        layout.addWidget(scroll)
        self.setLayout(layout)

    def cargar_odontograma(self):
        try:
            registros = self.db.obtener_odontograma_paciente(self.paciente_id)
            for num, cara, estado, procedimiento, observaciones, fecha in registros:
                if num in self.dientes:
                    tooltip = f"Procedimiento: {procedimiento or ''}\nObservaciones: {observaciones or ''}"
                    self.dientes[num].actualizar_estado(cara, estado, tooltip)
        except Exception as e:
            print(f"Error cargando odontograma: {e}")