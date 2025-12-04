import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog
from config.license_manager import verificar_licencia, es_primera_ejecucion, iniciar_licencia_prueba
from views.activation_window import VentanaActivacion
from views.main_window import SistemaPacientes

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Primera ejecución → crear licencia trial
    if es_primera_ejecucion():
        ok, msg = iniciar_licencia_prueba()
        if not ok:
            QMessageBox.critical(None, "Error", msg)
            sys.exit(0)

    # 2. Verificar licencia
    licencia_valida, mensaje = verificar_licencia()

    if not licencia_valida:
        # Licencia expirada o inválida → pedir activación
        QMessageBox.warning(None, "Licencia", mensaje)
        ventana_activacion = VentanaActivacion()
        resultado = ventana_activacion.exec_()

        if resultado != QDialog.Accepted:
            QMessageBox.critical(None, "Activación Requerida",
                                "El sistema no puede iniciar sin licencia válida.")
            sys.exit(0)

        licencia_valida, mensaje = verificar_licencia()
        if not licencia_valida:
            QMessageBox.critical(None, "Error", "No se pudo activar la licencia.")
            sys.exit(0)

    # 3. Abrir sistema
    if "Licencia activa" not in mensaje:
        QMessageBox.information(None, "Licencia", mensaje)
    ventana = SistemaPacientes()
    ventana.showMaximized()
    sys.exit(app.exec_())