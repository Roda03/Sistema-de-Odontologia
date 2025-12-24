from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QFrame, QCalendarWidget,QDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from views.base_window import BaseWindow
from views.consulta_window import VentanaCargarConsulta


class VentanaCalendario(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setWindowTitle("📅 Calendario de Consultas")
        self.resize(1000, 700)
        self.consultas_por_fecha = {}
        self.setup_ui()
        self.cargar_consultas()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        header = QHBoxLayout()
        header.setSpacing(8)

        titulo = QLabel("📅 Calendario de Consultas")
        titulo.setStyleSheet("""
            QLabel { font-size: 22px; font-weight: 800; color: #2c3e50; }
        """)
        header.addWidget(titulo)
        header.addStretch(1)

        btn_hoy = QPushButton("Hoy")
        btn_hoy.clicked.connect(self.ir_a_hoy)
        btn_hoy.setCursor(Qt.PointingHandCursor)
        btn_hoy.setStyleSheet(self._pill_button("#2ecc71", "#27ae60", bold=True))

        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.clicked.connect(self.cargar_consultas)
        btn_actualizar.setCursor(Qt.PointingHandCursor)
        btn_actualizar.setStyleSheet(self._pill_button("#3498db", "#2980b9", bold=True))

        header.addWidget(btn_hoy)
        header.addWidget(btn_actualizar)
        root.addLayout(header)

        main = QHBoxLayout()
        main.setSpacing(12)

        left = QVBoxLayout()
        left.setSpacing(8)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 12px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #eaf2fb;
                border-bottom: 1px solid #d6e4f5;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                padding: 6px;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                background: #3498db; color: white; border: none; border-radius: 6px;
                padding: 6px 10px; font-weight: 700;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background: #2980b9;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton,
            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                background: transparent; color: #1f2d3d; font-weight: 700; padding: 4px 6px; border: none;
            }
            QCalendarWidget QTableView {
                selection-background-color: #3498db; selection-color: #ffffff;
                outline: none; alternate-background-color: #f7f9fb;
            }
            QCalendarWidget QTableView::item { padding: 6px; }
        """)
        self.calendar.clicked.connect(self.mostrar_consultas_dia)
        left.addWidget(self.calendar)

        chips = QHBoxLayout()
        chips.setSpacing(8)

        chip_total = QFrame()
        chip_total.setStyleSheet(self._chip_style("#e74c3c"))
        self.lbl_total_consultas = QLabel("Total consultas: 0")
        self.lbl_total_consultas.setStyleSheet("color: white; font-weight: 800;")
        lyt_chip_total = QHBoxLayout(chip_total)
        lyt_chip_total.setContentsMargins(10, 6, 10, 6)
        lyt_chip_total.addWidget(self.lbl_total_consultas)

        chip_mes = QFrame()
        chip_mes.setStyleSheet(self._chip_style("#27ae60"))
        self.lbl_consultas_mes = QLabel("Consultas este mes: 0")
        self.lbl_consultas_mes.setStyleSheet("color: white; font-weight: 800;")
        lyt_chip_mes = QHBoxLayout(chip_mes)
        lyt_chip_mes.setContentsMargins(10, 6, 10, 6)
        lyt_chip_mes.addWidget(self.lbl_consultas_mes)

        chips.addWidget(chip_total)
        chips.addWidget(chip_mes)
        chips.addStretch(1)
        left.addLayout(chips)

        right = QVBoxLayout()
        right.setSpacing(10)

        lbl_consultas = QLabel("📋 Consultas del día seleccionado")
        lbl_consultas.setStyleSheet("font-size: 16px; font-weight: 800; color: #2c3e50;")
        right.addWidget(lbl_consultas)

        self.lista_consultas = QListWidget()
        self.lista_consultas.setStyleSheet("""
            QListWidget {
                background: #ffffff; border: 2px solid #bdc3c7; border-radius: 12px; padding: 6px;
            }
            QListWidget::item {
                margin: 4px; padding: 10px 12px; border: 1px solid #dcdde1; border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: rgba(41, 128, 185, 150); color: white;
            }
            QListWidget::item:selected {
                background-color: rgba(41, 128, 185, 200); color: white; border: 1px solid #21618c;
            }
        """)
        self.lista_consultas.itemDoubleClicked.connect(self.mostrar_detalle_consulta)
        right.addWidget(self.lista_consultas, 1)

        lbl_next = QLabel("⏭️ Próximas 5 consultas")
        lbl_next.setStyleSheet("font-size: 15px; font-weight: 800; color: #2c3e50; margin-top: 6px;")
        right.addWidget(lbl_next)

        self.lista_proximas = QListWidget()
        self.lista_proximas.setSelectionMode(QListWidget.NoSelection)
        self.lista_proximas.setFocusPolicy(Qt.NoFocus)
        self.lista_proximas.setStyleSheet("""
            QListWidget {
                background: #ffffff; border: 2px solid #bdc3c7; border-radius: 12px; padding: 6px;
            }
            QListWidget::item {
                margin: 4px; padding: 8px 10px; border: 1px dashed #dcdde1; border-radius: 8px; color: #2c3e50;
            }
            QListWidget::item:hover {
                background-color: rgba(41, 128, 185, 90); color: white;
            }
        """)
        self.lista_proximas.itemDoubleClicked.connect(self.mostrar_detalle_consulta)
        right.addWidget(self.lista_proximas)

        main.addLayout(left, 1)
        main.addLayout(right, 1)
        root.addLayout(main)

        btn_volver = QPushButton("⬅️ Volver al Inicio")
        btn_volver.clicked.connect(self.parent.mostrar_inicio)
        btn_volver.setCursor(Qt.PointingHandCursor)
        btn_volver.setStyleSheet(self._pill_button("#95a5a6", "#7f8c8d", bold=True))
        root.addWidget(btn_volver, alignment=Qt.AlignRight)

        self.setLayout(root)

    def _pill_button(self, color, hover, bold=False):
        fw = "700" if bold else "600"
        return f"""
            QPushButton {{
                background: {color}; color: white; border: none;
                border-radius: 20px; padding: 8px 16px; font-weight: {fw};
            }}
            QPushButton:hover {{ background: {hover}; }}
            QPushButton:pressed {{ background: #2c3e50; }}
        """

    def _chip_style(self, color):
        return f"""QFrame {{ background: {color}; border-radius: 14px; }}"""

    def cargar_consultas(self):
        try:
            self.consultas_por_fecha = {}
            consultas = self.db.obtener_todas_consultas()

            total_consultas = 0
            consultas_este_mes = 0
            mes_actual = QDate.currentDate().month()
            año_actual = QDate.currentDate().year()

            for consulta in consultas:
                fecha_str = consulta[2]  # fecha en formato YYYY-MM-DD
                try:
                    año, mes, dia = map(int, fecha_str.split('-'))
                    fecha_qdate = QDate(año, mes, dia)

                    if fecha_qdate.isValid():
                        hora_str = consulta[3] or ""
                        paciente_nombre = f"{consulta[8]} {consulta[9]}"  # nombre y apellido del paciente
                        precio = consulta[4]
                        
                        info_consulta = f"{hora_str} - {paciente_nombre}"
                        info_consulta += f"  ·  💰 Gs {precio:,.0f}"
                        
                        if fecha_str not in self.consultas_por_fecha:
                            self.consultas_por_fecha[fecha_str] = []

                        self.consultas_por_fecha[fecha_str].append({
                            'id': consulta[0],
                            'texto': info_consulta,
                            'fecha_qdate': fecha_qdate,
                            'hora': hora_str,
                            'paciente_nombre': paciente_nombre,
                            'precio': precio,
                            'motivo': consulta[5] or "",
                            'observaciones': consulta[6] or ""
                        })

                        total_consultas += 1
                        if mes == mes_actual and año == año_actual:
                            consultas_este_mes += 1
                except (ValueError, IndexError) as e:
                    print(f"Error procesando fecha {consulta[2]}: {e}")
                    continue

            self.lbl_total_consultas.setText(f"Total consultas: {total_consultas}")
            self.lbl_consultas_mes.setText(f"Consultas este mes: {consultas_este_mes}")

            self.resaltar_fechas_con_consultas()
            self.ir_a_hoy()
            self._refrescar_proximas_consultas()

        except Exception as e:
            print(f"Error cargando consultas: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar las consultas: {str(e)}")

    def _refrescar_proximas_consultas(self):
        self.lista_proximas.clear()

        hoy = QDate.currentDate()
        futuras = []

        for _, consultas in self.consultas_por_fecha.items():
            for c in consultas:
                qd = c['fecha_qdate']
                if not qd.isValid() or qd < hoy:
                    continue
                
                h_key = (99, 99)
                if c['hora']:
                    try:
                        hh, mm = map(int, c['hora'].split(':')[:2])
                        h_key = (hh, mm)
                    except Exception:
                        pass
                futuras.append((qd, h_key, c))

        futuras.sort(key=lambda x: (x[0].toJulianDay(), x[1]))

        for qd, _, c in futuras[:5]:
            fecha_s = qd.toString("dd/MM/yyyy")
            hora_s = c['hora'] if c['hora'] else "Sin hora"
            nombre = c['paciente_nombre']
            precio = c['precio']
            txt = f"{fecha_s} {hora_s} — {nombre} · 💰 Gs {precio:,.0f}"
            item = QListWidgetItem(txt)
            item.setData(Qt.UserRole, c['id'])
            
            tip = f"Fecha: {fecha_s}\nHora: {hora_s}\nPaciente: {nombre}"
            tip += f"\nPrecio: Gs {precio:,.0f}"
            if c['motivo']:
                tip += f"\nMotivo: {c['motivo'][:100]}..."
            item.setToolTip(tip)
            self.lista_proximas.addItem(item)

        if self.lista_proximas.count() == 0:
            self.lista_proximas.addItem(QListWidgetItem("✅ No hay próximas consultas"))

    def resaltar_fechas_con_consultas(self):
        try:
            self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

            today = QDate.currentDate()
            fmt_hoy = QTextCharFormat()
            fmt_hoy.setBackground(QColor("#27ae60"))
            fmt_hoy.setForeground(Qt.white)
            fmt_hoy.setFontWeight(QFont.Bold)
            self.calendar.setDateTextFormat(today, fmt_hoy)

            for fecha_str, consultas in self.consultas_por_fecha.items():
                try:
                    a, m, d = map(int, fecha_str.split('-'))
                    qd = QDate(a, m, d)
                    if qd.isValid():
                        fmt = QTextCharFormat()
                        fmt.setBackground(QColor("#e67e22"))
                        fmt.setForeground(Qt.white)
                        fmt.setFontWeight(QFont.Bold)
                        self.calendar.setDateTextFormat(qd, fmt)
                except Exception:
                    continue
        except Exception as e:
            print(f"Error resaltando fechas: {e}")

    def mostrar_consultas_dia(self, fecha):
        self.lista_consultas.clear()
        fecha_str = fecha.toString("yyyy-MM-dd")

        if fecha_str in self.consultas_por_fecha:
            consultas = self.consultas_por_fecha[fecha_str]
            for consulta in consultas:
                item = QListWidgetItem(consulta['texto'])
                item.setData(Qt.UserRole, consulta['id'])
                self.lista_consultas.addItem(item)
            self.lista_consultas.setToolTip(f"{len(consultas)} consulta(s) para {fecha.toString('dd/MM/yyyy')}")
        else:
            item = QListWidgetItem("📭 No hay consultas programadas para este día")
            item.setFlags(Qt.NoItemFlags)
            self.lista_consultas.addItem(item)

    def mostrar_detalle_consulta(self, item):
        consulta_id = item.data(Qt.UserRole)
        if consulta_id:
            consulta = self.db.obtener_consulta_por_id(consulta_id)
            if consulta:
                # Crear ventana de diálogo
                detalle = QDialog(self)
                detalle.setWindowTitle("📋 Detalle de Consulta")
                detalle.resize(500, 400)
                
                layout = QVBoxLayout(detalle)
                layout.setContentsMargins(15, 15, 15, 15)
                layout.setSpacing(8)
                
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
                    fila_layout.setContentsMargins(8, 4, 8, 4)
                    fila_layout.setSpacing(10)
                    
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
                    contenido_layout.setSpacing(2)
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
                info_layout.setSpacing(4)
                info_layout.setContentsMargins(0, 0, 0, 0)
                
                # Agregar filas de información
                info_layout.addWidget(crear_fila("👤", "PACIENTE", nombre_paciente, "#e74c3c"))
                
                # Línea separadora sutil
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
                
                # Motivo
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
                btn_layout.setSpacing(10)
                
                # Botón para nueva consulta
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
                btn_nueva.clicked.connect(lambda: self.abrir_nueva_consulta_desde_detalle(paciente, consulta, detalle))
                
                # Botón ver odontograma
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
                btn_odonto.clicked.connect(lambda: self.ver_odontograma_desde_calendario(consulta_id, paciente, detalle))
                
                # Botón cerrar
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
                
                # Si no hay paciente, deshabilitar algunos botones
                if not paciente:
                    btn_nueva.setEnabled(False)
                    btn_nueva.setToolTip("No se puede crear consulta sin paciente")
                    btn_odonto.setEnabled(False)
                    btn_odonto.setToolTip("No hay información del paciente")
                
                btn_layout.addWidget(btn_nueva)
                btn_layout.addWidget(btn_odonto)
                btn_layout.addWidget(btn_cerrar)
                
                layout.addLayout(btn_layout)
                
                # Mostrar diálogo
                detalle.exec_()

    def abrir_nueva_consulta_desde_detalle(self, paciente, consulta, parent_dialog):
        """Abrir nueva consulta desde el detalle del calendario"""
        if paciente:
            parent_dialog.close()
            from views.consulta_window import VentanaCargarConsulta
            ventana_consulta = VentanaCargarConsulta(self.parent, self.db, paciente['id'])
            ventana_consulta.exec_()
            # Recargar consultas en el calendario
            self.cargar_consultas()

    def ver_odontograma_desde_calendario(self, consulta_id, paciente, parent_dialog):
        """Ver odontograma desde el calendario"""
        parent_dialog.close()
        
        # Obtener información de la consulta
        consulta = self.db.obtener_consulta_por_id(consulta_id)
        if not consulta:
            QMessageBox.warning(self, "Error", "No se encontró la consulta")
            return
        
        from views.odontograma_view_widget import OdontogramaViewWidget
        
        odontograma_window = QDialog(self)
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

    def ir_a_hoy(self):
        hoy = QDate.currentDate()
        self.calendar.setSelectedDate(hoy)
        self.mostrar_consultas_dia(hoy)