from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QFrame, QCalendarWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from views.base_window import BaseWindow


class VentanaCalendario(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setWindowTitle("📅 Calendario de Citas")
        self.resize(1000, 700)
        self.citas_por_fecha = {}
        self.setup_ui()
        self.cargar_citas()

    # -------------------- Eventos globales --------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    # -------------------- UI --------------------
    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # Header con acciones
        header = QHBoxLayout()
        header.setSpacing(8)

        titulo = QLabel("📅 Calendario de Citas")
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
        btn_actualizar.clicked.connect(self.cargar_citas)
        btn_actualizar.setCursor(Qt.PointingHandCursor)
        btn_actualizar.setStyleSheet(self._pill_button("#3498db", "#2980b9", bold=True))

        header.addWidget(btn_hoy)
        header.addWidget(btn_actualizar)
        root.addLayout(header)

        # Contenido principal (izq: calendario / der: listas)
        main = QHBoxLayout()
        main.setSpacing(12)

        # ------------ Panel izquierdo: Calendario ------------
        left = QVBoxLayout(); left.setSpacing(8)

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
        self.calendar.clicked.connect(self.mostrar_citas_dia)
        left.addWidget(self.calendar)

        # Chips de estado
        chips = QHBoxLayout(); chips.setSpacing(8)

        chip_total = QFrame(); chip_total.setStyleSheet(self._chip_style("#e74c3c"))
        self.lbl_total_citas = QLabel("Total citas: 0"); self.lbl_total_citas.setStyleSheet("color: white; font-weight: 800;")
        lyt_chip_total = QHBoxLayout(chip_total); lyt_chip_total.setContentsMargins(10,6,10,6)
        lyt_chip_total.addWidget(self.lbl_total_citas)

        chip_mes = QFrame(); chip_mes.setStyleSheet(self._chip_style("#27ae60"))
        self.lbl_citas_mes = QLabel("Citas este mes: 0"); self.lbl_citas_mes.setStyleSheet("color: white; font-weight: 800;")
        lyt_chip_mes = QHBoxLayout(chip_mes); lyt_chip_mes.setContentsMargins(10,6,10,6)
        lyt_chip_mes.addWidget(self.lbl_citas_mes)

        chips.addWidget(chip_total); chips.addWidget(chip_mes); chips.addStretch(1)
        left.addLayout(chips)

        # ------------ Panel derecho: Listas ------------
        right = QVBoxLayout(); right.setSpacing(10)

        lbl_citas = QLabel("📋 Citas del día seleccionado")
        lbl_citas.setStyleSheet("font-size: 16px; font-weight: 800; color: #2c3e50;")
        right.addWidget(lbl_citas)

        self.lista_citas = QListWidget()
        self.lista_citas.setStyleSheet("""
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
        self.lista_citas.itemDoubleClicked.connect(self.mostrar_detalle_cita)
        right.addWidget(self.lista_citas, 1)

        # ---- Preview Próximas 3 citas ----
        lbl_next = QLabel("⏭️ Próximas 3 citas")
        lbl_next.setStyleSheet("font-size: 15px; font-weight: 800; color: #2c3e50; margin-top: 6px;")
        right.addWidget(lbl_next)

        self.lista_proximas = QListWidget()
        self.lista_proximas.setSelectionMode(QListWidget.NoSelection)  # no resalto, pero igual abre con doble clic
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
        # -> ahora también abre el detalle al doble clic
        self.lista_proximas.itemDoubleClicked.connect(self.mostrar_detalle_cita)
        right.addWidget(self.lista_proximas)

        # Armar columnas
        main.addLayout(left, 1); main.addLayout(right, 1)
        root.addLayout(main)

        # Footer
        btn_volver = QPushButton("⬅️ Volver al Inicio")
        btn_volver.clicked.connect(self.parent.mostrar_inicio)
        btn_volver.setCursor(Qt.PointingHandCursor)
        btn_volver.setStyleSheet(self._pill_button("#95a5a6", "#7f8c8d", bold=True))
        root.addWidget(btn_volver, alignment=Qt.AlignRight)

        self.setLayout(root)

    # -------------------- Estilos helpers --------------------
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

    # -------------------- Datos --------------------
    def cargar_citas(self):
        try:
            self.citas_por_fecha = {}
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT id, nombre, apellido, fecha_cita, hora_cita, telefono
                FROM pacientes 
                WHERE fecha_cita IS NOT NULL AND fecha_cita != ''
                ORDER BY fecha_cita, hora_cita
            """)
            citas = cursor.fetchall()

            total_citas = 0
            citas_este_mes = 0
            mes_actual = QDate.currentDate().month()
            año_actual = QDate.currentDate().year()

            for cita in citas:
                if cita[3]:
                    try:
                        fecha_str = cita[3]  # "dd/MM/yyyy"
                        dia, mes, año = map(int, fecha_str.split('/'))
                        fecha_qdate = QDate(año, mes, dia)

                        if fecha_qdate.isValid():
                            hora_str = cita[4] or ""
                            info_cita = f"{hora_str or 'Sin hora'} - {cita[1]} {cita[2]}"
                            if cita[5]:
                                info_cita += f"  ·  📞 {cita[5]}"

                            if fecha_str not in self.citas_por_fecha:
                                self.citas_por_fecha[fecha_str] = []

                            # Guardamos info completa para detalle/preview
                            self.citas_por_fecha[fecha_str].append({
                                'id': cita[0],
                                'texto': info_cita,
                                'fecha_qdate': fecha_qdate,
                                'hora': hora_str,
                                'nombre': cita[1],
                                'apellido': cita[2],
                                'telefono': cita[5] or ""
                            })

                            total_citas += 1
                            if mes == mes_actual and año == año_actual:
                                citas_este_mes += 1
                    except (ValueError, IndexError) as e:
                        print(f"Error procesando fecha {cita[3]}: {e}")
                        continue

            self.lbl_total_citas.setText(f"Total citas: {total_citas}")
            self.lbl_citas_mes.setText(f"Citas este mes: {citas_este_mes}")

            self.resaltar_fechas_con_citas()
            self.ir_a_hoy()
            self._refrescar_proximas_citas()

            QMessageBox.information(self, "Citas Cargadas",
                                    f"Se cargaron {total_citas} citas correctamente")

        except Exception as e:
            print(f"Error cargando citas: {e}")
            QMessageBox.warning(self, "Error", f"No se pudieron cargar las citas: {str(e)}")

    def _refrescar_proximas_citas(self):
        """Calcula y muestra las próximas 3 citas (>= hoy) y habilita doble clic a detalle."""
        self.lista_proximas.clear()

        hoy = QDate.currentDate()
        futuras = []

        for _, citas in self.citas_por_fecha.items():
            for c in citas:
                qd = c['fecha_qdate']
                if not qd.isValid() or qd < hoy:
                    continue
                # parse hora HH:MM si existe
                h_key = (99, 99)
                if c['hora']:
                    try:
                        hh, mm = map(int, c['hora'].split(':')[:2])
                        h_key = (hh, mm)
                    except Exception:
                        pass
                futuras.append((qd, h_key, c))

        # Orden por fecha y hora
        futuras.sort(key=lambda x: (x[0].toJulianDay(), x[1]))

        # Top 3
        for qd, _, c in futuras[:3]:
            fecha_s = qd.toString("dd/MM/yyyy")
            hora_s = c['hora'] if c['hora'] else "Sin hora"
            nombre = f"{c['nombre']} {c['apellido']}".strip()
            tel = c['telefono']
            txt = f"{fecha_s} {hora_s} — {nombre}" + (f" · 📞 {tel}" if tel else "")
            item = QListWidgetItem(txt)
            # -> guardo el id para abrir detalle al doble clic
            item.setData(Qt.UserRole, c['id'])
            # tooltip con info
            tip = f"Fecha: {fecha_s}\nHora: {hora_s}\nPaciente: {nombre}"
            if tel:
                tip += f"\nTeléfono: {tel}"
            item.setToolTip(tip)
            self.lista_proximas.addItem(item)

        if self.lista_proximas.count() == 0:
            self.lista_proximas.addItem(QListWidgetItem("✅ No hay próximas citas"))

    def resaltar_fechas_con_citas(self):
        try:
            # Limpiar todos los formatos previos
            self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

            # HOY (verde intenso)
            today = QDate.currentDate()
            fmt_hoy = QTextCharFormat()
            fmt_hoy.setBackground(QColor("#27ae60"))
            fmt_hoy.setForeground(Qt.white)
            fmt_hoy.setFontWeight(QFont.Bold)
            self.calendar.setDateTextFormat(today, fmt_hoy)

            # DÍAS CON CITAS (naranja fuerte)
            for fecha_str, citas in self.citas_por_fecha.items():
                try:
                    d, m, a = map(int, fecha_str.split('/'))
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

    # -------------------- Interacciones --------------------
    def mostrar_citas_dia(self, fecha):
        self.lista_citas.clear()
        fecha_str = fecha.toString("dd/MM/yyyy")

        if fecha_str in self.citas_por_fecha:
            citas = self.citas_por_fecha[fecha_str]
            for cita in citas:
                item = QListWidgetItem(cita['texto'])
                item.setData(Qt.UserRole, cita['id'])  # <-- ya tenías esto bien
                self.lista_citas.addItem(item)
            self.lista_citas.setToolTip(f"{len(citas)} cita(s) para {fecha_str}")
        else:
            item = QListWidgetItem("📭 No hay citas programadas para este día")
            item.setFlags(Qt.NoItemFlags)
            self.lista_citas.addItem(item)

    def mostrar_detalle_cita(self, item):
        paciente_id = item.data(Qt.UserRole)
        if paciente_id:
            paciente_dict = self.db.obtener_paciente_por_id(paciente_id)
            if paciente_dict:
                from views.patient_window import VentanaDetallePaciente
                self.detalle = VentanaDetallePaciente(paciente_dict, self.db)
                self.detalle.show()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar la información del paciente")

    def ir_a_hoy(self):
        hoy = QDate.currentDate()
        self.calendar.setSelectedDate(hoy)
        self.mostrar_citas_dia(hoy)
