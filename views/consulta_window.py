from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QScrollArea, QDateEdit,
                             QTimeEdit, QDoubleSpinBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont
from views.base_window import BaseWindow
from views.odontograma_widget import OdontogramaWidget

class VentanaCargarConsulta(QDialog):  # CAMBIADO a QDialog
    def __init__(self, parent, db, paciente_id):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # Ventana independiente
        self.parent = parent
        self.db = db
        self.paciente_id = paciente_id
        self.paciente = self.db.obtener_paciente_por_id(paciente_id)
        self.setWindowTitle("➕ Nueva Consulta")
        self.resize(1000, 700)
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Scroll area que contiene TODO
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Título con nombre del paciente
        nombre_completo = f"{self.paciente.get('nombre', '')} {self.paciente.get('apellido', '')}"
        titulo = QLabel(f"➕ Nueva Consulta - {nombre_completo}")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
        titulo.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(titulo)
        
        # Tabs para organizar
        self.tab_widget = QTabWidget()
        
        # Tab 1: Información básica de la consulta
        tab_consulta = QWidget()
        layout_consulta = QVBoxLayout(tab_consulta)
        layout_consulta.setContentsMargins(10, 10, 10, 10)
        
        # Campos de fecha y hora
        fecha_hora_layout = QHBoxLayout()
        
        fecha_label = QLabel("📅 Fecha:")
        fecha_label.setStyleSheet("font-weight: bold;")
        self.date_fecha = QDateEdit()
        self.date_fecha.setDate(QDate.currentDate())
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setDisplayFormat("dd/MM/yyyy")
        
        hora_label = QLabel("🕐 Hora:")
        hora_label.setStyleSheet("font-weight: bold;")
        self.time_hora = QTimeEdit()
        self.time_hora.setTime(QTime.currentTime())
        self.time_hora.setDisplayFormat("HH:mm")
        
        fecha_hora_layout.addWidget(fecha_label)
        fecha_hora_layout.addWidget(self.date_fecha)
        fecha_hora_layout.addWidget(hora_label)
        fecha_hora_layout.addWidget(self.time_hora)
        fecha_hora_layout.addStretch()
        
        layout_consulta.addLayout(fecha_hora_layout)
        
        # Precio
        precio_layout = QHBoxLayout()
        precio_label = QLabel("💰 Precio (Gs):")
        precio_label.setStyleSheet("font-weight: bold;")
        self.spin_precio = QDoubleSpinBox()
        self.spin_precio.setRange(0, 10000000)
        self.spin_precio.setValue(0)
        self.spin_precio.setDecimals(0)
        self.spin_precio.setSingleStep(10000)
        self.spin_precio.setPrefix("Gs ")
        
        precio_layout.addWidget(precio_label)
        precio_layout.addWidget(self.spin_precio)
        precio_layout.addStretch()
        layout_consulta.addLayout(precio_layout)
        
        # Motivo de la consulta
        motivo_label = QLabel("📝 Motivo / Procedimiento:")
        motivo_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout_consulta.addWidget(motivo_label)
        
        self.input_motivo = QTextEdit()
        self.input_motivo.setPlaceholderText("Describa el motivo de la consulta o procedimiento a realizar...")
        self.input_motivo.setMinimumHeight(80)
        layout_consulta.addWidget(self.input_motivo)
        
        # Observaciones
        obs_label = QLabel("📋 Observaciones:")
        obs_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout_consulta.addWidget(obs_label)
        
        self.input_observaciones = QTextEdit()
        self.input_observaciones.setPlaceholderText("Observaciones adicionales de la consulta...")
        self.input_observaciones.setMinimumHeight(100)
        layout_consulta.addWidget(self.input_observaciones)
        
        # Tab 2: Odontograma
        tab_odonto = QWidget()
        layout_odonto = QVBoxLayout(tab_odonto)
        layout_odonto.setContentsMargins(10, 10, 10, 10)
        
        # El odontograma se creará después de guardar la consulta
        self.odontograma_label = QLabel("🦷 Complete primero los datos de la consulta para habilitar el odontograma")
        self.odontograma_label.setStyleSheet("font-size: 14px; color: #7f8c8d; padding: 20px;")
        self.odontograma_label.setAlignment(Qt.AlignCenter)
        layout_odonto.addWidget(self.odontograma_label)
        
        self.odontograma_widget = None
        
        # Agregar tabs
        self.tab_widget.addTab(tab_consulta, "📋 Consulta")
        self.tab_widget.addTab(tab_odonto, "🦷 Odontograma")
        content_layout.addWidget(self.tab_widget)
        
        # Botones DENTRO del contenido scrollable
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("💾 Guardar Consulta")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_consulta)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cancelar.clicked.connect(self.close)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancelar)
        
        content_layout.addLayout(btn_layout)
        content_layout.addStretch()
        
        # Solo el scroll va al layout principal
        layout.addWidget(scroll)
    
    def guardar_consulta(self):
        try:
            fecha = self.date_fecha.date().toString("yyyy-MM-dd")
            hora = self.time_hora.time().toString("HH:mm")
            precio = self.spin_precio.value()
            motivo = self.input_motivo.toPlainText().strip()
            observaciones = self.input_observaciones.toPlainText().strip()
            
            if precio <= 0:
                QMessageBox.warning(self, "Error", "Ingrese un precio válido para la consulta")
                return
            
            # Guardar consulta
            consulta_id = self.db.agregar_consulta(
                self.paciente_id, fecha, hora, precio, motivo, observaciones
            )
            
            # Habilitar odontograma
            self.consulta_id = consulta_id
            self.habilitar_odontograma()
            
            QMessageBox.information(self, "Éxito", "Consulta guardada correctamente")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar consulta: {str(e)}")
    
    def habilitar_odontograma(self):
        # Remover label y crear widget de odontograma
        layout = self.tab_widget.widget(1).layout()
        layout.removeWidget(self.odontograma_label)
        self.odontograma_label.deleteLater()
        
        self.odontograma_widget = OdontogramaWidget(self.consulta_id, self.db)
        layout.addWidget(self.odontograma_widget)
        
        # Cambiar al tab de odontograma
        self.tab_widget.setCurrentIndex(1)

class VentanaHistorialConsultas(QDialog):  # CAMBIADO a QDialog
    def __init__(self, parent, db, paciente_id):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # Ventana independiente
        self.parent = parent
        self.db = db
        self.paciente_id = paciente_id
        self.paciente = self.db.obtener_paciente_por_id(paciente_id)
        self.setWindowTitle("📋 Historial de Consultas")
        self.resize(900, 600)
        self.setup_ui()
        self.cargar_consultas()
        
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título con nombre del paciente
        nombre_completo = f"{self.paciente.get('nombre', '')} {self.paciente.get('apellido', '')}"
        titulo = QLabel(f"📋 Historial de Consultas - {nombre_completo}")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Tabla de consultas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Fecha", "Hora", "Precio (Gs)", "Motivo", "Observaciones", "Acciones", "Odontograma"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_nueva = QPushButton("➕ Nueva Consulta")
        btn_nueva.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_nueva.clicked.connect(self.nueva_consulta)
        
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        
        btn_layout.addWidget(btn_nueva)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
    
    def cargar_consultas(self):
        consultas = self.db.obtener_consultas_paciente(self.paciente_id)
        self.tabla.setRowCount(len(consultas))
        
        for i, consulta in enumerate(consultas):
            # Fecha
            fecha_item = QTableWidgetItem(consulta[2])  # fecha
            self.tabla.setItem(i, 0, fecha_item)
            
            # Hora
            hora_item = QTableWidgetItem(consulta[3])  # hora
            self.tabla.setItem(i, 1, hora_item)
            
            # Precio
            precio = consulta[4]  # precio
            precio_item = QTableWidgetItem(f"Gs {precio:,.0f}")
            precio_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla.setItem(i, 2, precio_item)
            
            # Motivo
            motivo = consulta[5] or ""  # motivo
            motivo_item = QTableWidgetItem(motivo[:50] + "..." if len(motivo) > 50 else motivo)
            self.tabla.setItem(i, 3, motivo_item)
            
            # Observaciones
            obs = consulta[6] or ""  # observaciones
            obs_item = QTableWidgetItem(obs[:50] + "..." if len(obs) > 50 else obs)
            self.tabla.setItem(i, 4, obs_item)
            
            # Botón ver detalle
            btn_ver = QPushButton("👁️ Ver")
            btn_ver.setStyleSheet("padding: 5px;")
            btn_ver.clicked.connect(lambda checked, cid=consulta[0]: self.ver_detalle_consulta(cid))
            
            # Botón eliminar
            btn_eliminar = QPushButton("🗑️ Eliminar")
            btn_eliminar.setStyleSheet("padding: 5px; background-color: #e74c3c; color: white;")
            btn_eliminar.clicked.connect(lambda checked, cid=consulta[0]: self.eliminar_consulta(cid))
            
            # Layout para botones
            widget_botones = QWidget()
            layout_botones = QHBoxLayout(widget_botones)
            layout_botones.addWidget(btn_ver)
            layout_botones.addWidget(btn_eliminar)
            layout_botones.setContentsMargins(0, 0, 0, 0)
            
            self.tabla.setCellWidget(i, 5, widget_botones)
            
            # Botón ver odontograma
            btn_odonto = QPushButton("🦷 Ver")
            btn_odonto.setStyleSheet("padding: 5px; background-color: #9b59b6; color: white;")
            btn_odonto.clicked.connect(lambda checked, cid=consulta[0]: self.ver_odontograma(cid))
            self.tabla.setCellWidget(i, 6, btn_odonto)
    
    def ver_detalle_consulta(self, consulta_id):
        consulta = self.db.obtener_consulta_por_id(consulta_id)
        if not consulta:
            return
        
        # Crear ventana de diálogo
        detalle = QDialog(self)
        detalle.setWindowTitle("📋 Detalle de Consulta")
        detalle.resize(500, 400)  # Más compacto
        
        layout = QVBoxLayout(detalle)
        layout.setContentsMargins(15, 15, 15, 15)  # Menos márgenes
        layout.setSpacing(8)  # Menor espaciado
        
        # Título
        titulo = QLabel("📋 Detalle de Consulta")
        titulo.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding-bottom: 8px;
            border-bottom: 1px solid #3498db;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Información del paciente
        paciente = self.db.obtener_paciente_por_id(consulta[1])
        nombre_paciente = f"{paciente.get('nombre', '')} {paciente.get('apellido', '')}" if paciente else "Desconocido"
        
        # Función para crear fila compacta
        def crear_fila(icono, titulo_texto, contenido, color="#3498db"):
            fila = QWidget()
            fila_layout = QHBoxLayout(fila)
            fila_layout.setContentsMargins(8, 4, 8, 4)  # Márgenes internos reducidos
            fila_layout.setSpacing(10)  # Menos espacio entre icono y texto
            
            # Icono
            icon_label = QLabel(icono)
            icon_label.setStyleSheet(f"""
                font-size: 16px;
                color: {color};
                min-width: 25px;
            """)
            
            # Contenido
            contenido_widget = QWidget()
            contenido_layout = QVBoxLayout(contenido_widget)
            contenido_layout.setSpacing(2)  # Muy poco espacio entre título y contenido
            contenido_layout.setContentsMargins(0, 0, 0, 0)
            
            titulo_label = QLabel(titulo_texto)
            titulo_label.setStyleSheet("""
                font-weight: bold;
                font-size: 11px;
                color: #7f8c8d;
            """)
            
            contenido_label = QLabel(contenido)
            contenido_label.setStyleSheet("""
                font-size: 13px;
                color: #2c3e50;
            """)
            contenido_label.setWordWrap(True)
            
            contenido_layout.addWidget(titulo_label)
            contenido_layout.addWidget(contenido_label)
            
            fila_layout.addWidget(icon_label)
            fila_layout.addWidget(contenido_widget, 1)
            
            return fila
        
        # Contenedor para la información
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(4)  # Espaciado muy pequeño entre filas
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Agregar filas de información
        info_layout.addWidget(crear_fila("👤", "PACIENTE", nombre_paciente, "#e74c3c"))
        
        # Agregar línea separadora sutil
        linea1 = QWidget()
        linea1.setFixedHeight(1)
        linea1.setStyleSheet("background-color: #f1f2f6;")
        info_layout.addWidget(linea1)
        
        info_layout.addWidget(crear_fila("📅", "FECHA", consulta[2], "#3498db"))
        info_layout.addWidget(crear_fila("🕐", "HORA", consulta[3], "#9b59b6"))
        info_layout.addWidget(crear_fila("💰", "PRECIO", f"Gs {consulta[4]:,.0f}", "#27ae60"))
        
        linea2 = QWidget()
        linea2.setFixedHeight(1)
        linea2.setStyleSheet("background-color: #f1f2f6;")
        info_layout.addWidget(linea2)
        
        # Motivo (puede ser largo)
        motivo_texto = consulta[5] or "No especificado"
        fila_motivo = crear_fila("📝", "MOTIVO / PROCEDIMIENTO", motivo_texto, "#f39c12")
        info_layout.addWidget(fila_motivo)
        
        # Observaciones (si existen)
        observaciones_texto = consulta[6] or "No especificado"
        if observaciones_texto != "No especificado":
            linea3 = QWidget()
            linea3.setFixedHeight(1)
            linea3.setStyleSheet("background-color: #f1f2f6;")
            info_layout.addWidget(linea3)
            
            fila_obs = crear_fila("📋", "OBSERVACIONES", observaciones_texto, "#1abc9c")
            info_layout.addWidget(fila_obs)
        
        # Agregar contenedor de información al layout principal
        layout.addWidget(info_container)
        
        # Espaciador mínimo
        layout.addSpacing(10)
        
        # Botones compactos
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)  # Espacio entre botones
        
        btn_odonto = QPushButton("🦷 Ver Odontograma")
        btn_odonto.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_odonto.clicked.connect(lambda: self.ver_odontograma_desde_detalle(consulta_id, detalle))
        
        btn_nueva = QPushButton("➕ Nueva Consulta")
        btn_nueva.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        if paciente:
            btn_nueva.clicked.connect(lambda: self.nueva_consulta_desde_detalle(paciente['id'], detalle))
        else:
            btn_nueva.setEnabled(False)
            btn_nueva.setToolTip("No se puede crear consulta sin paciente")
        
        btn_cerrar = QPushButton("✖️ Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cerrar.clicked.connect(detalle.close)
        
        btn_layout.addWidget(btn_odonto)
        btn_layout.addWidget(btn_nueva)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        
        # Mostrar diálogo
        detalle.exec_()

    def ver_odontograma_desde_detalle(self, consulta_id, parent_dialog):
        """Método para ver odontograma desde el detalle"""
        parent_dialog.close()  # Cerrar ventana de detalle primero
        self.ver_odontograma(consulta_id)

    def nueva_consulta_desde_detalle(self, paciente_id, parent_dialog):
        """Método para nueva consulta desde el detalle"""
        if paciente_id:
            parent_dialog.close()  # Cerrar ventana de detalle
            ventana_consulta = VentanaCargarConsulta(self.parent, self.db, paciente_id)
            ventana_consulta.exec_()
            self.cargar_consultas()  # Recargar lista de consultas
    
    def eliminar_consulta(self, consulta_id):
        confirm = QMessageBox.question(
            self, "Confirmar", 
            "¿Está seguro de eliminar esta consulta?\n\nNota: También se eliminará el odontograma asociado.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            if self.db.eliminar_consulta(consulta_id):
                QMessageBox.information(self, "Éxito", "Consulta eliminada correctamente")
                self.cargar_consultas()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar la consulta")
    
    def ver_odontograma(self, consulta_id):
        from views.odontograma_view_widget import OdontogramaViewWidget
        
        # Obtener información de la consulta
        consulta = self.db.obtener_consulta_por_id(consulta_id)
        if not consulta:
            QMessageBox.warning(self, "Error", "No se encontró la consulta")
            return
        
        paciente = self.db.obtener_paciente_por_id(consulta[1])
        
        odontograma_window = QDialog(self)  # QDialog en lugar de QWidget
        odontograma_window.setWindowFlags(Qt.Window)
        if paciente:
            nombre_completo = f"{paciente.get('nombre', '')} {paciente.get('apellido', '')}"
            odontograma_window.setWindowTitle(f"🦷 Odontograma - {nombre_completo}")
        else:
            odontograma_window.setWindowTitle(f"🦷 Odontograma - Consulta {consulta_id}")
        
        odontograma_window.resize(800, 600)
        
        layout = QVBoxLayout(odontograma_window)
        
        # Título con información
        if paciente:
            titulo = QLabel(f"🦷 Odontograma - {nombre_completo}")
            subtitulo = QLabel(f"Consulta del {consulta[2]} {consulta[3]}")
        else:
            titulo = QLabel(f"🦷 Odontograma - Consulta {consulta_id}")
            subtitulo = QLabel(f"Fecha: {consulta[2]} - Hora: {consulta[3]}")
        
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; padding: 10px;")
        titulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 14px; color: #7f8c8d; padding: 5px;")
        subtitulo.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        
        # Widget de odontograma
        odontograma_widget = OdontogramaViewWidget(consulta_id, self.db)
        layout.addWidget(odontograma_widget)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(odontograma_window.close)
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)
        
        odontograma_window.exec_()
    
    def nueva_consulta(self):
        ventana_consulta = VentanaCargarConsulta(self.parent, self.db, self.paciente_id)
        ventana_consulta.exec_()
        self.cargar_consultas()  # Recargar después de crear nueva consulta