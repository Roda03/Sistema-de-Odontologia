from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from config.config_manager import obtener_ruta_onedrive, guardar_configuracion
import os

class VentanaConfiguracion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración - Ruta de OneDrive")
        self.resize(500, 250)
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        titulo = QLabel("📁 Configurar Ruta de OneDrive")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        instrucciones = QLabel(
            "Seleccione la carpeta de OneDrive donde se guardarán las copias de seguridad:"
        )
        instrucciones.setWordWrap(True)
        layout.addWidget(instrucciones)
        
        ruta_layout = QHBoxLayout()
        self.input_ruta = QLineEdit()
        self.input_ruta.setPlaceholderText("Clic en 'Examinar' para seleccionar carpeta...")
        self.input_ruta.setText(obtener_ruta_onedrive())
        
        btn_examinar = QPushButton("Examinar...")
        btn_examinar.clicked.connect(self.seleccionar_carpeta)
        
        ruta_layout.addWidget(self.input_ruta)
        ruta_layout.addWidget(btn_examinar)
        layout.addLayout(ruta_layout)
        
        btn_guardar = QPushButton("💾 Guardar Configuración")
        btn_guardar.clicked.connect(self.guardar_configuracion)
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                padding: 10px;
                font-weight: bold;
            }
        """)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet("padding: 10px;")
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def seleccionar_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(
            self, 
            "Seleccionar carpeta de OneDrive",
            os.path.expanduser("~")
        )
        if carpeta:
            self.input_ruta.setText(carpeta)
            
    def guardar_configuracion(self):
        ruta = self.input_ruta.text().strip()
        if not ruta:
            QMessageBox.warning(self, "Error", "Por favor, seleccione una carpeta válida")
            return
            
        if not os.path.exists(ruta):
            respuesta = QMessageBox.question(
                self, 
                "Carpeta no existe", 
                f"La carpeta '{ruta}' no existe.\n\n¿Desea crearla?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                try:
                    os.makedirs(ruta)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo crear la carpeta: {str(e)}")
                    return
            else:
                return
        
        try:
            test_file = os.path.join(ruta, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                            f"No tiene permisos de escritura en esta carpeta:\n{str(e)}")
            return
        
        config = {"ruta_onedrive": ruta}
        if guardar_configuracion(config):
            QMessageBox.information(self, "✅ Configuración Guardada", 
                                f"La ruta de OneDrive se ha configurado correctamente:\n\n{ruta}")
            self.accept()
        else:
            QMessageBox.critical(self, "❌ Error", "No se pudo guardar la configuración")