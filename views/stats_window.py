from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                             QComboBox, QDateEdit, QFormLayout, QGroupBox, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFont
from views.base_window import BaseWindow
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class SimpleBarChart(QWidget):
    """Widget para mostrar gráfico de barras simple"""
    def __init__(self, data, labels, title="", max_value=None):
        super().__init__()
        self.data = data or [0]
        self.labels = labels or [""]
        self.title = title
        self.max_value = max_value if max_value else max(self.data) if self.data else 1
        self.setMinimumHeight(150)
        self.setMinimumWidth(300)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Margenes
        margin_left = 40
        margin_right = 20
        margin_top = 30
        margin_bottom = 40
        
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        
        if chart_width <= 0 or chart_height <= 0 or not self.data:
            return
        
        # Título
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(int(width // 2 - len(self.title) * 3), 20, self.title)
        
        # Eje Y
        painter.drawLine(margin_left, margin_top, margin_left, margin_top + chart_height)
        
        # Eje X
        painter.drawLine(margin_left, margin_top + chart_height, 
                        margin_left + chart_width, margin_top + chart_height)
        
        # Barras
        bar_width = max(10, int(chart_width / len(self.data) * 0.7))
        spacing = int(chart_width / len(self.data) * 0.3)
        
        bar_colors = [QColor(52, 152, 219), QColor(46, 204, 113), QColor(155, 89, 182), 
                     QColor(241, 196, 15), QColor(231, 76, 60), QColor(52, 73, 94)]
        
        for i, (value, label) in enumerate(zip(self.data, self.labels)):
            x = margin_left + i * (bar_width + spacing)
            bar_height = int((value / self.max_value) * chart_height) if self.max_value > 0 else 0
            
            # Dibujar barra
            painter.setBrush(QBrush(bar_colors[i % len(bar_colors)]))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawRect(int(x), int(margin_top + chart_height - bar_height), 
                           bar_width, bar_height)
            
            # Valor encima de la barra (solo si hay espacio)
            if bar_height > 15:
                painter.setPen(QPen(Qt.black))
                painter.setFont(QFont("Arial", 8, QFont.Bold))
                value_text = f"{value:,.0f}"
                text_width = len(value_text) * 5
                painter.drawText(int(x + bar_width/2 - text_width/2), 
                               int(margin_top + chart_height - bar_height - 5), 
                               value_text)
            
            # Etiqueta
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("Arial", 8))
            # Limitar longitud de etiqueta
            short_label = label[:8] + "..." if len(label) > 8 else label
            text_width = len(short_label) * 6
            painter.drawText(int(x + bar_width/2 - text_width/2), 
                           int(margin_top + chart_height + 20), 
                           short_label)

class VentanaEstadisticas(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setWindowTitle("💰 Estadísticas de Ingresos")
        self.resize(1100, 750)
        self.setup_ui()
        self.cargar_estadisticas_mes_actual()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("💰 ESTADÍSTICAS DE INGRESOS")
        titulo.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 10px;
        """)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Contenedor de filtros
        filtros_container = QWidget()
        filtros_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        filtros_layout = QHBoxLayout(filtros_container)
        filtros_layout.setSpacing(15)
        
        # Filtro por período
        periodos = ["Hoy", "Esta semana", "Este mes", "Este año", "Personalizado"]
        self.combo_periodo = QComboBox()
        self.combo_periodo.addItems(periodos)
        self.combo_periodo.setCurrentText("Este mes")
        self.combo_periodo.currentTextChanged.connect(self.cambiar_periodo)
        
        # Filtro por año
        self.combo_anio = QComboBox()
        anios = [str(year) for year in range(2020, 2031)]
        self.combo_anio.addItems(anios)
        self.combo_anio.setCurrentText(str(QDate.currentDate().year()))
        self.combo_anio.currentTextChanged.connect(self.cargar_estadisticas_por_anio)
        
        # Fechas personalizadas
        self.date_inicio = QDateEdit()
        self.date_inicio.setDate(QDate.currentDate().addDays(-30))
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDisplayFormat("dd/MM/yyyy")
        self.date_inicio.setMaximumWidth(120)
        
        self.date_fin = QDateEdit()
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDisplayFormat("dd/MM/yyyy")
        self.date_fin.setMaximumWidth(120)
        
        btn_aplicar_fecha = QPushButton("Aplicar")
        btn_aplicar_fecha.setStyleSheet("""
            QPushButton {
                background-color: #6c757d; 
                color: white; 
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        btn_aplicar_fecha.clicked.connect(self.cargar_estadisticas_personalizado)
        
        filtros_layout.addWidget(QLabel("Período:"))
        filtros_layout.addWidget(self.combo_periodo)
        filtros_layout.addWidget(QLabel("Año:"))
        filtros_layout.addWidget(self.combo_anio)
        filtros_layout.addWidget(QLabel("Desde:"))
        filtros_layout.addWidget(self.date_inicio)
        filtros_layout.addWidget(QLabel("Hasta:"))
        filtros_layout.addWidget(self.date_fin)
        filtros_layout.addWidget(btn_aplicar_fecha)
        filtros_layout.addStretch()
        
        layout.addWidget(filtros_container)

        # Contenedor principal (tabla + gráficos)
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setSpacing(15)
        
        # Columna izquierda (tabla y resumen)
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        
        # Resumen general
        resumen_group = QGroupBox("📊 Resumen General")
        resumen_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        resumen_layout = QHBoxLayout()
        
        # Tarjetas de resumen
        def crear_tarjeta_resumen(titulo, valor, color, icono):
            tarjeta = QFrame()
            tarjeta.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 10px;
                    padding: 15px;
                    min-width: 180px;
                }}
            """)
            
            tarjeta_layout = QVBoxLayout(tarjeta)
            tarjeta_layout.setSpacing(8)
            
            titulo_label = QLabel(f"{icono} {titulo}")
            titulo_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            
            valor_label = QLabel(valor)
            valor_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 22px;
                    font-weight: bold;
                }
            """)
            
            tarjeta_layout.addWidget(titulo_label)
            tarjeta_layout.addWidget(valor_label)
            
            return tarjeta
        
        self.tarjeta_consultas = crear_tarjeta_resumen("Consultas", "0", "#e74c3c", "📋")
        self.tarjeta_ingresos = crear_tarjeta_resumen("Ingresos", "Gs 0", "#27ae60", "💰")
        self.tarjeta_promedio = crear_tarjeta_resumen("Promedio", "Gs 0", "#f39c12", "📈")
        
        resumen_layout.addWidget(self.tarjeta_consultas)
        resumen_layout.addWidget(self.tarjeta_ingresos)
        resumen_layout.addWidget(self.tarjeta_promedio)
        
        resumen_group.setLayout(resumen_layout)
        left_column.addWidget(resumen_group)
        
        # Tabla de estadísticas
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Período", "Consultas", "Ingresos Total", "Promedio"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        left_column.addWidget(self.tabla, 1)
        
        # Columna derecha (solo gráfico)
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        
        # Gráfico de ingresos por mes
        self.grafico_container = QGroupBox("📈 Gráfico de Ingresos")
        self.grafico_container.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        self.grafico_layout = QVBoxLayout(self.grafico_container)
        self.chart_widget = None
        self.grafico_layout.addWidget(QLabel("Seleccione un período para ver el gráfico"))
        
        right_column.addWidget(self.grafico_container, 1)
        
        # Agregar columnas al layout principal
        main_layout.addLayout(left_column, 2)
        main_layout.addLayout(right_column, 1)
        
        layout.addWidget(main_container, 1)

        # Botones de acción
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setSpacing(10)
        
        btn_exportar_pdf = QPushButton("📄 Exportar a PDF")
        btn_exportar_pdf.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_exportar_pdf.clicked.connect(self.exportar_a_pdf)
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_actualizar.clicked.connect(self.cargar_estadisticas_mes_actual)
        
        btn_volver = QPushButton("⬅️ Volver al Inicio")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; 
                color: white; 
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)
        
        btn_layout.addWidget(btn_exportar_pdf)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_volver)
        
        layout.addWidget(btn_container)

        self.setLayout(layout)

    def cambiar_periodo(self, periodo):
        if periodo == "Hoy":
            self.cargar_estadisticas_hoy()
        elif periodo == "Esta semana":
            self.cargar_estadisticas_semana_actual()
        elif periodo == "Este mes":
            self.cargar_estadisticas_mes_actual()
        elif periodo == "Este año":
            self.cargar_estadisticas_anio_actual()
        elif periodo == "Personalizado":
            self.date_inicio.setEnabled(True)
            self.date_fin.setEnabled(True)

    def cargar_estadisticas_por_anio(self, anio=None):
        try:
            if not anio:
                anio = self.combo_anio.currentText()
            
            datos = self.db.obtener_ingresos_por_mes(anio)
            
            total_consultas = 0
            total_ingresos = 0.0
            
            meses = [
                "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
            ]
            
            ingresos_mensuales = [0.0] * 12
            consultas_mensuales = [0] * 12
            
            self.tabla.setRowCount(len(datos))
            
            for i, (mes_num, consultas, ingresos) in enumerate(datos):
                if ingresos is None:
                    ingresos = 0.0
                
                total_consultas += consultas
                total_ingresos += ingresos
                
                mes_index = int(mes_num) - 1
                if 0 <= mes_index < 12:
                    ingresos_mensuales[mes_index] = ingresos
                    consultas_mensuales[mes_index] = consultas
                
                mes_nombre = meses[mes_index] if mes_index < len(meses) else mes_num
                periodo_str = f"{mes_nombre} {anio}"
                promedio = ingresos / consultas if consultas > 0 else 0
                
                self.tabla.setItem(i, 0, QTableWidgetItem(periodo_str))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(consultas)))
                self.tabla.setItem(i, 2, QTableWidgetItem(f"Gs {ingresos:,.0f}"))
                self.tabla.setItem(i, 3, QTableWidgetItem(f"Gs {promedio:,.0f}"))
                
                if i % 2 == 0:
                    for j in range(4):
                        self.tabla.item(i, j).setBackground(QColor(245, 245, 245))
            
            self.actualizar_resumen(total_consultas, total_ingresos)
            
            # Actualizar gráfico
            self.actualizar_grafico_mensual(meses, ingresos_mensuales, f"Ingresos {anio}")
            
        except Exception as e:
            print(f"Error cargando estadísticas por año: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def cargar_estadisticas_mes_actual(self):
        try:
            hoy = QDate.currentDate()
            anio = hoy.year()
            mes = hoy.month()
            
            fecha_inicio = QDate(anio, mes, 1)
            fecha_fin = fecha_inicio.addMonths(1).addDays(-1)
            
            consultas = self.db.obtener_consultas_entre_fechas(
                fecha_inicio.toString("yyyy-MM-dd"),
                fecha_fin.toString("yyyy-MM-dd")
            )
            
            total_consultas = len(consultas)
            total_ingresos = sum(c[4] for c in consultas if c[4] is not None)
            
            meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            
            self.tabla.setRowCount(1)
            mes_nombre = meses[mes-1]
            
            self.tabla.setItem(0, 0, QTableWidgetItem(f"{mes_nombre} {anio}"))
            self.tabla.setItem(0, 1, QTableWidgetItem(str(total_consultas)))
            self.tabla.setItem(0, 2, QTableWidgetItem(f"Gs {total_ingresos:,.0f}"))
            
            promedio = total_ingresos / total_consultas if total_consultas > 0 else 0
            self.tabla.setItem(0, 3, QTableWidgetItem(f"Gs {promedio:,.0f}"))
            
            self.actualizar_resumen(total_consultas, total_ingresos)
            
            # Gráfico para el mes actual
            self.actualizar_grafico_mensual([mes_nombre], [total_ingresos], f"Ingresos {mes_nombre} {anio}")
            
        except Exception as e:
            print(f"Error cargando estadísticas del mes actual: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def cargar_estadisticas_semana_actual(self):
        try:
            hoy = QDate.currentDate()
            inicio_semana = hoy.addDays(-hoy.dayOfWeek() + 1)
            
            consultas = self.db.obtener_consultas_entre_fechas(
                inicio_semana.toString("yyyy-MM-dd"),
                hoy.toString("yyyy-MM-dd")
            )
            
            total_consultas = len(consultas)
            total_ingresos = sum(c[4] for c in consultas if c[4] is not None)
            
            dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
            ingresos_diarios = [0.0] * 7
            
            for consulta in consultas:
                fecha_str = consulta[2]
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                dia_semana = fecha.dayOfWeek() - 1
                if 0 <= dia_semana < 7:
                    ingresos_diarios[dia_semana] += consulta[4] or 0.0
            
            self.tabla.setRowCount(7)
            for i in range(7):
                fecha_dia = inicio_semana.addDays(i)
                self.tabla.setItem(i, 0, QTableWidgetItem(fecha_dia.toString("dd/MM")))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(ingresos_diarios[i])))
                self.tabla.setItem(i, 2, QTableWidgetItem(f"Gs {ingresos_diarios[i]:,.0f}"))
                self.tabla.setItem(i, 3, QTableWidgetItem(""))
                
                if i % 2 == 0:
                    for j in range(4):
                        if self.tabla.item(i, j):
                            self.tabla.item(i, j).setBackground(QColor(245, 245, 245))
            
            self.actualizar_resumen(total_consultas, total_ingresos)
            
            # Gráfico para la semana
            self.actualizar_grafico_mensual(dias_semana, ingresos_diarios, "Ingresos por día (esta semana)")
            
        except Exception as e:
            print(f"Error cargando estadísticas de la semana: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def cargar_estadisticas_anio_actual(self):
        try:
            anio = QDate.currentDate().year()
            self.combo_anio.setCurrentText(str(anio))
            self.cargar_estadisticas_por_anio(str(anio))
        except Exception as e:
            print(f"Error cargando estadísticas del año actual: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def cargar_estadisticas_hoy(self):
        try:
            hoy = QDate.currentDate().toString("yyyy-MM-dd")
            datos = self.db.obtener_ingresos_por_dia(hoy)
            
            if datos and datos[0] is not None:
                total_consultas, total_ingresos = datos
                total_ingresos = total_ingresos or 0.0
            else:
                total_consultas = 0
                total_ingresos = 0.0
            
            self.tabla.setRowCount(1)
            fecha_formateada = QDate.currentDate().toString("dd/MM/yyyy")
            
            self.tabla.setItem(0, 0, QTableWidgetItem(f"Hoy ({fecha_formateada})"))
            self.tabla.setItem(0, 1, QTableWidgetItem(str(total_consultas)))
            self.tabla.setItem(0, 2, QTableWidgetItem(f"Gs {total_ingresos:,.0f}"))
            
            promedio = total_ingresos / total_consultas if total_consultas > 0 else 0
            self.tabla.setItem(0, 3, QTableWidgetItem(f"Gs {promedio:,.0f}"))
            
            self.actualizar_resumen(total_consultas, total_ingresos)
            
            # Gráfico simple para hoy
            self.actualizar_grafico_mensual(["Hoy"], [total_ingresos], "Ingresos de hoy")
            
        except Exception as e:
            print(f"Error cargando estadísticas de hoy: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def cargar_estadisticas_personalizado(self):
        try:
            fecha_inicio = self.date_inicio.date().toString("yyyy-MM-dd")
            fecha_fin = self.date_fin.date().toString("yyyy-MM-dd")
            
            consultas = self.db.obtener_consultas_entre_fechas(fecha_inicio, fecha_fin)
            
            total_consultas = len(consultas)
            total_ingresos = sum(c[4] for c in consultas if c[4] is not None)
            
            # Agrupar por día
            ingresos_por_dia = {}
            for consulta in consultas:
                fecha = consulta[2]
                precio = consulta[4] or 0.0
                if fecha in ingresos_por_dia:
                    ingresos_por_dia[fecha] += precio
                else:
                    ingresos_por_dia[fecha] = precio
            
            self.tabla.setRowCount(len(ingresos_por_dia))
            for i, (fecha, ingresos) in enumerate(sorted(ingresos_por_dia.items())):
                fecha_qdate = QDate.fromString(fecha, "yyyy-MM-dd")
                fecha_formateada = fecha_qdate.toString("dd/MM/yyyy")
                
                self.tabla.setItem(i, 0, QTableWidgetItem(fecha_formateada))
                self.tabla.setItem(i, 1, QTableWidgetItem("1"))  # 1 consulta por fila
                self.tabla.setItem(i, 2, QTableWidgetItem(f"Gs {ingresos:,.0f}"))
                self.tabla.setItem(i, 3, QTableWidgetItem(f"Gs {ingresos:,.0f}"))
                
                if i % 2 == 0:
                    for j in range(4):
                        self.tabla.item(i, j).setBackground(QColor(245, 245, 245))
            
            self.actualizar_resumen(total_consultas, total_ingresos)
            
            # Gráfico para período personalizado
            fechas = sorted(ingresos_por_dia.keys())
            labels = [QDate.fromString(f, "yyyy-MM-dd").toString("dd/MM") for f in fechas]
            valores = [ingresos_por_dia[f] for f in fechas]
            
            self.actualizar_grafico_mensual(labels, valores, f"Ingresos {fecha_inicio} a {fecha_fin}")
            
        except Exception as e:
            print(f"Error cargando estadísticas personalizadas: {e}")
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def actualizar_resumen(self, total_consultas, total_ingresos):
        # Actualizar tarjetas
        tarjeta_consultas = self.tarjeta_consultas.layout().itemAt(1).widget()
        tarjeta_consultas.setText(str(total_consultas))
        
        tarjeta_ingresos = self.tarjeta_ingresos.layout().itemAt(1).widget()
        tarjeta_ingresos.setText(f"Gs {total_ingresos:,.0f}")
        
        promedio = total_ingresos / total_consultas if total_consultas > 0 else 0
        tarjeta_promedio = self.tarjeta_promedio.layout().itemAt(1).widget()
        tarjeta_promedio.setText(f"Gs {promedio:,.0f}")

    def actualizar_grafico_mensual(self, labels, valores, titulo):
        # Limpiar gráfico anterior
        if self.chart_widget:
            self.grafico_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        
        # Crear nuevo gráfico
        max_valor = max(valores) if valores else 1
        self.chart_widget = SimpleBarChart(valores, labels, titulo, max_valor)
        self.grafico_layout.addWidget(self.chart_widget)

    def exportar_a_pdf(self):
        from config.config_manager import obtener_ruta_onedrive
        import os
        
        ruta_onedrive = obtener_ruta_onedrive()
        if not ruta_onedrive or not os.path.exists(ruta_onedrive):
            QMessageBox.warning(self, "Error", 
                              "Configure primero la ruta de OneDrive en Configuración")
            return
        
        fecha_actual = QDate.currentDate().toString("yyyyMMdd_HHmm")
        ruta_pdf = os.path.join(ruta_onedrive, f"estadisticas_{fecha_actual}.pdf")
        
        try:
            # Crear documento PDF
            doc = SimpleDocTemplate(ruta_pdf, pagesize=A4)
            story = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=18,
                spaceAfter=30,
                textColor=colors.HexColor('#2c3e50')
            )
            
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=10,
                textColor=colors.HexColor('#3498db')
            )
            
            # Título
            story.append(Paragraph("Reporte de Estadísticas de Ingresos", title_style))
            story.append(Paragraph(f"Fecha: {QDate.currentDate().toString('dd/MM/yyyy')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Resumen
            story.append(Paragraph("Resumen General", header_style))
            
            # Obtener datos del resumen
            consultas = self.tarjeta_consultas.layout().itemAt(1).widget().text()
            ingresos = self.tarjeta_ingresos.layout().itemAt(1).widget().text()
            promedio = self.tarjeta_promedio.layout().itemAt(1).widget().text()
            
            resumen_data = [
                ['Métrica', 'Valor'],
                ['Total Consultas', consultas],
                ['Total Ingresos', ingresos],
                ['Promedio por Consulta', promedio]
            ]
            
            resumen_table = Table(resumen_data, colWidths=[200, 200])
            resumen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            
            story.append(resumen_table)
            story.append(Spacer(1, 30))
            
            # Detalle de estadísticas
            story.append(Paragraph("Detalle de Estadísticas", header_style))
            
            # Obtener datos de la tabla
            table_data = [['Período', 'Consultas', 'Ingresos Total', 'Promedio']]
            
            for row in range(self.tabla.rowCount()):
                row_data = []
                for col in range(self.tabla.columnCount()):
                    item = self.tabla.item(row, col)
                    row_data.append(item.text() if item else "")
                table_data.append(row_data)
            
            if len(table_data) > 1:
                detail_table = Table(table_data, colWidths=[120, 80, 120, 120])
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                
                story.append(detail_table)
            else:
                story.append(Paragraph("No hay datos para mostrar.", styles['Normal']))
            
            # Pie de página
            story.append(Spacer(1, 50))
            story.append(Paragraph("Sistema de Odontología - Reporte generado automáticamente", 
                                  ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                               textColor=colors.grey)))
            
            # Generar PDF
            doc.build(story)
            
            QMessageBox.information(self, "Éxito", 
                                  f"Reporte PDF exportado correctamente a:\n{ruta_pdf}")
            
        except Exception as e:
            print(f"Error generando PDF: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF: {str(e)}")