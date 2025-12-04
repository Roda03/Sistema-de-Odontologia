from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from views.base_window import BaseWindow
import sqlite3

class VentanaEstadisticas(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setWindowTitle("💰 Estadísticas de Ingresos")
        self.resize(900, 600)
        self.setup_ui()
        self.cargar_estadisticas()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
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

        # Botones de período
        btn_layout = QHBoxLayout()
        
        btn_semanal = QPushButton("📅 Fechas")
        btn_semanal.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_semanal.clicked.connect(self.mostrar_semanal)
        
        btn_mensual = QPushButton("📊 Mensual")
        btn_mensual.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; 
                color: white; 
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_mensual.clicked.connect(self.mostrar_mensual)
        
        btn_layout.addWidget(btn_semanal)
        btn_layout.addWidget(btn_mensual)
        layout.addLayout(btn_layout)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Período", "Cantidad de Citas", "Ingresos Total"])
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
        layout.addWidget(self.tabla)

        # Totales
        total_layout = QHBoxLayout()
        
        self.lbl_total_citas = QLabel("Total Citas: 0")
        self.lbl_total_citas.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
        
        self.lbl_total_ingresos = QLabel("Total Ingresos: $0.00")
        self.lbl_total_ingresos.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
        
        total_layout.addWidget(self.lbl_total_citas)
        total_layout.addWidget(self.lbl_total_ingresos)
        layout.addLayout(total_layout)

        # Botón volver
        btn_volver = QPushButton("⬅️ Volver al Inicio")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; 
                color: white; 
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)
        layout.addWidget(btn_volver)

        self.setLayout(layout)

    def cargar_estadisticas(self):
        self.mostrar_semanal()  # Mostrar semanal por defecto

    def mostrar_semanal(self):
        try:
            # Obtener lunes de esta semana
            hoy = QDate.currentDate()
            lunes = hoy.addDays(-(hoy.dayOfWeek() - 1))
            
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT fecha_cita, COUNT(*) as citas, SUM(precio_consulta) as ingresos
                FROM pacientes 
                WHERE fecha_cita IS NOT NULL 
                AND fecha_cita != ''
                AND precio_consulta > 0
                GROUP BY fecha_cita
                ORDER BY fecha_cita
            """)
            
            resultados = cursor.fetchall()
            self.mostrar_resultados(resultados, "semanal")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def mostrar_mensual(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT 
                    SUBSTR(fecha_cita, 4, 7) as mes_anio,  -- Extraer MM/AAAA
                    COUNT(*) as citas, 
                    SUM(precio_consulta) as ingresos
                FROM pacientes 
                WHERE fecha_cita IS NOT NULL 
                AND fecha_cita != ''
                AND precio_consulta > 0
                GROUP BY mes_anio
                ORDER BY mes_anio
            """)
            
            resultados = cursor.fetchall()
            self.mostrar_resultados(resultados, "mensual")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar estadísticas: {str(e)}")

    def mostrar_resultados(self, resultados, tipo):
        self.tabla.setRowCount(len(resultados))
        
        total_citas = 0
        total_ingresos = 0.0
        
        for i, (periodo, citas, ingresos) in enumerate(resultados):
            if ingresos is None:
                ingresos = 0.0
                
            total_citas += citas
            total_ingresos += ingresos
            
            # Formatear período
            if tipo == "semanal":
                periodo_str = periodo  # Ya viene como DD/MM/AAAA
            else:
                # Convertir "MM/AAAA" a "Mes AAAA"
                mes, anio = periodo.split('/')
                meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                periodo_str = f"{meses[int(mes)-1]} {anio}"
            
            self.tabla.setItem(i, 0, QTableWidgetItem(periodo_str))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(citas)))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"{ingresos:,.0f} Gs"))
            
            # Colorear filas pares
            if i % 2 == 0:
                for j in range(3):
                    self.tabla.item(i, j).setBackground(QColor(245, 245, 245))
        
        # Actualizar totales
        self.lbl_total_citas.setText(f"Total Citas: {total_citas}")
        self.lbl_total_ingresos.setText(f"Total Ingresos: {total_ingresos:,.0f} Gs")