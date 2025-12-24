from PyQt5.QtWidgets import QMainWindow, QMessageBox
from config.license_manager import verificar_licencia
from database.database import Database
from views.login_window import VentanaLogin
from views.inicio_window import VentanaInicio
from utilidades.helpers import hay_internet
from config.config_manager import obtener_ruta_onedrive
import os, sys
import shutil
from datetime import datetime

class SistemaPacientes(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.licencia_valida, self.mensaje_licencia = verificar_licencia()
        if not self.licencia_valida:
            QMessageBox.critical(self, "Error de Licencia", 
                                f"Error en la licencia: {self.mensaje_licencia}")
            sys.exit(1)
            
        self.db = Database()
        self.setWindowTitle("Sistema de Odontología")
        self.resize(800, 600)
        self.mostrar_login()

    def mostrar_login(self):
        self.ventana_login = VentanaLogin(self, self.db)
        self.ventana_login.show()

    def mostrar_inicio(self):
        self.verificar_configuracion_onedrive()
        self.ventana_inicio = VentanaInicio(self)
        self.setCentralWidget(self.ventana_inicio)

    def verificar_configuracion_onedrive(self):
        ruta_onedrive = obtener_ruta_onedrive()
        if not ruta_onedrive or not os.path.exists(ruta_onedrive):
            respuesta = QMessageBox.question(
                self, 
                "📁 Configuración de OneDrive",
                "No se ha configurado la ruta de OneDrive para las copias de seguridad.\n\n"
                "¿Desea configurarla ahora?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                from views.config_window import VentanaConfiguracion
                ventana_config = VentanaConfiguracion(self)
                ventana_config.exec_()

    def closeEvent(self, event):
        try:
            ruta_onedrive = obtener_ruta_onedrive()
            
            if hay_internet() and ruta_onedrive and os.path.exists(ruta_onedrive):
                try:
                    excel_filename = f"consultas_exportadas.xlsx"
                    db_filename = f"odontologia_backup.db"
                    
                    excel_ruta = os.path.join(ruta_onedrive, excel_filename)
                    db_ruta = os.path.join(ruta_onedrive, db_filename)
                    
                    self.db.exportar_consultas_a_excel(excel_ruta)
                    print(f"✅ Copia de seguridad de consultas exportada a: {excel_ruta}")
                    
                    db_path = self.db.obtener_ruta_db()
                    shutil.copy2(db_path, db_ruta)
                    print(f"✅ Copia de seguridad de base de datos exportada a: {db_ruta}")
                    
                except Exception as e:
                    print(f"⚠️ Error al exportar copia de seguridad a OneDrive: {e}")
                    
            try:
                if hasattr(self, 'db') and self.db.conn:
                    self.db.conn.close()
                    print("✅ Conexión a base de datos local cerrada correctamente")
            except Exception as e:
                print(f"ℹ️ Error al cerrar conexión: {e}")
                
        except Exception as e:
            print(f"⚠️ Error en el proceso de cierre: {e}")
        
        event.accept()

    def mostrar_buscar(self):
        from views.patient_window import VentanaBuscar
        self.ventana_buscar = VentanaBuscar(self, self.db)
        self.setCentralWidget(self.ventana_buscar)

    def mostrar_modificar(self):
        from views.patient_window import VentanaModificar
        self.ventana_modificar = VentanaModificar(self, self.db)
        self.setCentralWidget(self.ventana_modificar)

    def mostrar_cargar(self):
        from views.patient_window import VentanaCargarPaciente
        self.ventana_cargar = VentanaCargarPaciente(self, self.db)
        self.setCentralWidget(self.ventana_cargar)
        
    def mostrar_calendario(self):
        from views.calendar_window import VentanaCalendario
        self.ventana_calendario = VentanaCalendario(self, self.db)
        self.setCentralWidget(self.ventana_calendario)
        
    def mostrar_estadisticas(self):
        from views.stats_window import VentanaEstadisticas
        self.ventana_estadisticas = VentanaEstadisticas(self, self.db)
        self.setCentralWidget(self.ventana_estadisticas)