from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from config.license_manager import generar_id_instalacion, activar_licencia

class VentanaActivacion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activación del Sistema")
        self.resize(500, 350)
        self.setModal(True)
        
        self.id_instalacion = generar_id_instalacion()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        titulo = QLabel("🔐 Activación Requerida")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        instrucciones = QLabel(
            "Para utilizar el sistema, es necesario activarlo con una licencia válida.\n\n"
            "Por favor, contacte al desarrollador y proporcione el siguiente\n"
            "código de identificación para obtener su clave de activación:"
        )
        instrucciones.setAlignment(Qt.AlignCenter)
        instrucciones.setWordWrap(True)
        layout.addWidget(instrucciones)
        
        layout.addWidget(QLabel("Código de identificación:"))
        self.label_id = QLabel(self.id_instalacion)
        self.label_id.setStyleSheet("""
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px;
            font-family: monospace;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.label_id.setAlignment(Qt.AlignCenter)
        self.label_id.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.label_id)
        
        btn_copiar = QPushButton("📋 Copiar código")
        btn_copiar.clicked.connect(self.copiar_id)
        btn_copiar.setStyleSheet("padding: 5px;")
        layout.addWidget(btn_copiar)
        
        layout.addWidget(QLabel(""))
        
        layout.addWidget(QLabel("Ingrese la clave de activación proporcionada:"))
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Ingrese los 4 caracteres de activación")
        self.input_clave.setMaxLength(4)
        self.input_clave.setAlignment(Qt.AlignCenter)
        self.input_clave.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.input_clave)
        
        btn_activar = QPushButton("✅ Activar Licencia")
        btn_activar.clicked.connect(self.activar_licencia)
        btn_activar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        btn_salir = QPushButton("🚪 Salir")
        btn_salir.clicked.connect(self.reject)
        btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_activar)
        btn_layout.addWidget(btn_salir)
        
        layout.addLayout(btn_layout)
        
        contacto = QLabel(
            "📧 Contacto: davillar.dv.321@gmail.com\n"
            "📞 Teléfono: 0975-539-793"
        )
        contacto.setAlignment(Qt.AlignCenter)
        contacto.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        layout.addWidget(contacto)
        
        self.setLayout(layout)
        
    def copiar_id(self):
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.id_instalacion)
        QMessageBox.information(self, "Copiado", "Código copiado al portapapeles")
        
    def activar_licencia(self):
        clave = self.input_clave.text().strip()
        if len(clave) != 4:
            QMessageBox.warning(self, "Error", "La clave debe tener exactamente 4 caracteres")
            return
            
        resultado, mensaje = activar_licencia(clave)
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", mensaje)