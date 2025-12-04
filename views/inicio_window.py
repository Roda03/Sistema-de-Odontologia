from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QLabel,
    QGridLayout
)
from PyQt5.QtCore import Qt
from views.base_window import BaseWindow


class VentanaInicio(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(30)

        # --- Título principal
        titulo = QLabel("🏥 Sistema de Pacientes - Odontología")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        """)
        root.addWidget(titulo)

        subtitulo = QLabel("Seleccioná una acción para comenzar")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color:#7f8c8d; font-size:15px; margin-bottom:20px;")
        root.addWidget(subtitulo)

        # --- Grilla de botones
        grid = QGridLayout()
        grid.setSpacing(20)
        root.addLayout(grid)

        def mk_btn(texto, slot, kind="primary"):
            btn = QPushButton(texto)
            btn.clicked.connect(slot)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(60)
            btn.setStyleSheet(self._button_style(kind))
            return btn

        btn_estadisticas = mk_btn("💰 Estadísticas de Ingresos", self.parent.mostrar_estadisticas, "accent")
        btn_buscar       = mk_btn("🔍 Buscar Paciente",        self.parent.mostrar_buscar, "primary")
        btn_modificar    = mk_btn("🛠️ Modificar / Eliminar",   self.parent.mostrar_modificar, "primary")
        btn_cargar       = mk_btn("➕ Cargar Paciente",         self.parent.mostrar_cargar, "primary")
        btn_calendario   = mk_btn("📅 Calendario de Citas",     self.parent.mostrar_calendario, "purple")
        btn_config       = mk_btn("⚙️ Configurar OneDrive",     self.mostrar_configuracion, "primary")

        # 2 columnas x 3 filas
        grid.addWidget(btn_buscar,     0, 0)
        grid.addWidget(btn_cargar,     0, 1)
        grid.addWidget(btn_modificar,  1, 0)
        grid.addWidget(btn_calendario, 1, 1)
        grid.addWidget(btn_estadisticas, 2, 0)
        grid.addWidget(btn_config,      2, 1)

        # --- Pie
        pie = QLabel("• v1.0.0")
        pie.setAlignment(Qt.AlignCenter)
        pie.setStyleSheet("color:#95a5a6; font-size:12px; margin-top:20px;")
        root.addWidget(pie)

    def _button_style(self, kind):
        colors = {
            "primary": ("#3498db", "#2980b9", "#21618c"),
            "accent":  ("#f39c12", "#e67e22", "#d35400"),
            "purple":  ("#9b59b6", "#8e44ad", "#7d3c98"),
        }
        normal, hover, pressed = colors.get(kind, colors["primary"])
        return f"""
            QPushButton {{
                background-color: {normal};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 12px 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """

    def mostrar_configuracion(self):
        from views.config_window import VentanaConfiguracion
        ventana_config = VentanaConfiguracion(self.parent)
        ventana_config.exec_()
