from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QGridLayout, QComboBox, QTextEdit, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFont

class DienteWidget(QWidget):
    dienteClicked = pyqtSignal(int, str)

    def __init__(self, numero):
        super().__init__()
        self.numero = numero
        self.estados = {}
        self.setFixedSize(80, 100)
        self.setCursor(Qt.PointingHandCursor)

        # Coordenadas exactas de cada cara (x, y, ancho, alto)
        self.caras_rect = {
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
        for cara, rect in self.caras_rect.items():
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

    def mousePressEvent(self, event):
        for cara, rect in self.caras_rect.items():
            if rect.contains(event.pos()):
                self.dienteClicked.emit(self.numero, cara)
                return

    def actualizar_estado(self, cara, estado):
        self.estados[cara] = estado
        self.update()
        
class OdontogramaWidget(QWidget):
    def __init__(self, consulta_id, db):
        super().__init__()
        self.consulta_id = consulta_id  # Usar consulta_id en lugar de paciente_id
        self.db = db
        self.dientes = {}
        self.diente_actual = None
        self.cara_actual = None
        self.setup_ui()
        self.cargar_odontograma()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        titulo = QLabel("🦷 ODONTOGRAMA INTERACTIVO")
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

        for i in range(1, 33):
            diente = DienteWidget(i)
            diente.dienteClicked.connect(self.on_diente_clicked)
            dientes_layout.addWidget(diente, (i-1)//8, (i-1)%8)
            self.dientes[i] = diente

        layout.addWidget(scroll)

        # Panel lateral
        self.lbl_seleccion = QLabel("Seleccione un diente")
        self.lbl_seleccion.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_seleccion)

        self.combo_estado = QComboBox()
        estados = [("sano","🦷 Sano"),("cariado","🔴 Cariado"),("obturado","🟡 Obturado"),
                   ("corona","⚪ Corona"),("extraccion","🟤 Extracción"),("implante","🟢 Implante"),
                   ("protesis","🟣 Prótesis"),("ausente","⚫ Ausente")]
        for val, text in estados:
            self.combo_estado.addItem(text, val)
        layout.addWidget(self.combo_estado)

        self.input_procedimiento = QTextEdit()
        self.input_procedimiento.setPlaceholderText("Procedimiento...")
        layout.addWidget(self.input_procedimiento)

        self.input_observaciones = QTextEdit()
        self.input_observaciones.setPlaceholderText("Observaciones...")
        layout.addWidget(self.input_observaciones)

        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("💾 Guardar")
        btn_guardar.clicked.connect(self.guardar_cambios)
        btn_layout.addWidget(btn_guardar)
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_cara)
        btn_layout.addWidget(btn_limpiar)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_diente_clicked(self, numero, cara):
        self.diente_actual = numero
        self.cara_actual = cara
        self.lbl_seleccion.setText(f"Diente {numero} - Cara {cara}")
        self.cargar_datos_cara()

    def cargar_datos_cara(self):
        if not self.diente_actual or not self.cara_actual: 
            return
        
        registros = self.db.obtener_odontograma_consulta(self.consulta_id)
        for num, cara, estado, proc, obs, fecha in registros:
            if num == self.diente_actual and cara == self.cara_actual:
                idx = self.combo_estado.findData(estado)
                if idx >= 0: 
                    self.combo_estado.setCurrentIndex(idx)
                self.input_procedimiento.setPlainText(proc or "")
                self.input_observaciones.setPlainText(obs or "")
                return
        
        # Si no existe, establecer valores por defecto
        self.combo_estado.setCurrentIndex(0)
        self.input_procedimiento.clear()
        self.input_observaciones.clear()

    def guardar_cambios(self):
        if not self.diente_actual or not self.cara_actual:
            QMessageBox.warning(self, "Error", "Seleccione un diente")
            return
        
        estado = self.combo_estado.currentData()
        proc = self.input_procedimiento.toPlainText()
        obs = self.input_observaciones.toPlainText()
        
        success = self.db.guardar_odontograma(
            self.consulta_id,  # Usar consulta_id
            self.diente_actual, 
            self.cara_actual,
            estado, 
            proc, 
            obs
        )
        
        if success:
            self.dientes[self.diente_actual].actualizar_estado(self.cara_actual, estado)
            QMessageBox.information(self, "Éxito", "Cambios guardados")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar")

    def limpiar_cara(self):
        if not self.diente_actual or not self.cara_actual:
            QMessageBox.warning(self, "Error", "Seleccione un diente")
            return
        
        success = self.db.eliminar_registro_odontograma(self.consulta_id, self.diente_actual, self.cara_actual)
        if success:
            self.dientes[self.diente_actual].actualizar_estado(self.cara_actual, "sano")
            self.input_procedimiento.clear()
            self.input_observaciones.clear()
            self.combo_estado.setCurrentIndex(0)
            QMessageBox.information(self, "Éxito", "Cara limpiada")
        else:
            QMessageBox.critical(self, "Error", "No se pudo limpiar")

    def cargar_odontograma(self):
        registros = self.db.obtener_odontograma_consulta(self.consulta_id)
        for num, cara, estado, proc, obs, fecha in registros:
            if num in self.dientes:
                self.dientes[num].actualizar_estado(cara, estado)