from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QCheckBox, QGridLayout, QScrollArea, 
                             QMessageBox, QListWidget, QListWidgetItem, QGroupBox, 
                             QSizePolicy, QFormLayout, QComboBox, QTabWidget,QWidget)
from PyQt5.QtCore import Qt
from views.base_window import BaseWindow
from views.consulta_window import VentanaHistorialConsultas

class VentanaCargarPaciente(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        
        layout = QVBoxLayout(content)
        self.setup_form_fields(layout)
        
        # Botones DENTRO del scroll
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("💾 Guardar Paciente")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_guardar.clicked.connect(self.guardar)

        btn_volver = QPushButton("⬅️ Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; 
                color: white; 
                padding: 12px; 
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)

        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_volver)
        layout.addLayout(btn_layout)
        layout.addStretch()

        # Solo el scroll va al layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def setup_form_fields(self, layout):
        # (Este método se mantiene IGUAL al que ya tenías)
        titulo = QLabel("➕ Cargar Nuevo Paciente")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #27ae60;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Campos básicos del paciente
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        
        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Apellido")
        
        self.input_cedula = QLineEdit()
        self.input_cedula.setPlaceholderText("Número de cédula")
        
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Número de teléfono")
        
        self.input_edad = QLineEdit()
        self.input_edad.setPlaceholderText("Edad")

        campos_basicos = [
            ("Nombre", self.input_nombre),
            ("Apellido", self.input_apellido),
            ("Cédula", self.input_cedula),
            ("Teléfono", self.input_telefono),
            ("Edad", self.input_edad)
        ]

        for texto, widget in campos_basicos:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout.addWidget(lbl)
            widget.setMinimumHeight(30)
            layout.addWidget(widget)

        # Historial médico
        lbl_historial = QLabel("📋 HISTORIAL MÉDICO")
        lbl_historial.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout.addWidget(lbl_historial)

        self.input_medicamento_actual = QLineEdit()
        self.input_medicamento_actual.setPlaceholderText("Medicamento actual")
        layout.addWidget(QLabel("Medicamento actual:"))
        layout.addWidget(self.input_medicamento_actual)

        self.input_alergias = QLineEdit()
        self.input_alergias.setPlaceholderText("Alergias")
        layout.addWidget(QLabel("Alergias:"))
        layout.addWidget(self.input_alergias)

        # Checkboxes para condiciones médicas
        self.check_embarazada = QCheckBox("¿Está embarazada?")
        self.check_hemorragias = QCheckBox("¿Tuvo hemorragias anormales?")
        self.check_problemas_tratamiento = QCheckBox("¿Presentó algún problema serio asociado con el tratamiento?")
        self.check_enfermedad_cardiovascular = QCheckBox("¿Sufre de alguna enfermedad cardiovascular?")

        for checkbox in [
            self.check_embarazada, self.check_hemorragias,
            self.check_problemas_tratamiento, self.check_enfermedad_cardiovascular
        ]:
            layout.addWidget(checkbox)

        # Enfermedades
        lbl_enfermedades = QLabel("Enfermedades:")
        lbl_enfermedades.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(lbl_enfermedades)

        self.check_diabetes = QCheckBox("Diabetes")
        self.check_hepatitis = QCheckBox("Hepatitis")
        self.check_artritis = QCheckBox("Artritis")
        self.check_tuberculosis = QCheckBox("Tuberculosis")
        self.check_enfermedades_venereas = QCheckBox("Enfermedades venéreas")
        self.check_hipertension = QCheckBox("Hipertensión")
        self.check_enfermedades_sanguineas = QCheckBox("Enfermedades sanguíneas")
        self.check_otras_enfermedades = QCheckBox("Otras enfermedades")
        
        self.input_especificar_otras = QLineEdit()
        self.input_especificar_otras.setPlaceholderText("Especifique otras enfermedades")

        enfermedades_grid = QGridLayout()
        enfermedades = [
            (self.check_diabetes, 0, 0),
            (self.check_hepatitis, 0, 1),
            (self.check_artritis, 0, 2),
            (self.check_tuberculosis, 1, 0),
            (self.check_enfermedades_venereas, 1, 1),
            (self.check_hipertension, 1, 2),
            (self.check_enfermedades_sanguineas, 2, 0),
            (self.check_otras_enfermedades, 2, 1)
        ]
        
        for checkbox, row, col in enfermedades:
            enfermedades_grid.addWidget(checkbox, row, col)
        
        layout.addLayout(enfermedades_grid)
        layout.addWidget(self.input_especificar_otras)

        # Examen clínico
        lbl_examen = QLabel("🔍 EXAMEN CLÍNICO")
        lbl_examen.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout.addWidget(lbl_examen)

        self.input_tejidos_intraorales = QTextEdit()
        self.input_tejidos_intraorales.setPlaceholderText("Describa el estado de los tejidos blandos intraorales")
        
        self.input_tejidos_extraorales = QTextEdit()
        self.input_tejidos_extraorales.setPlaceholderText("Describa el estado de los tejidos blandos extraorales")
        
        self.input_ganglios = QTextEdit()
        self.input_ganglios.setPlaceholderText("Describa el estado de los ganglios")
        
        self.input_aspecto_clinico = QTextEdit()
        self.input_aspecto_clinico.setPlaceholderText("Describa el aspecto clínico general")

        examenes = [
            ("Tejidos blandos intraorales", self.input_tejidos_intraorales),
            ("Tejidos blandos extraorales", self.input_tejidos_extraorales),
            ("Ganglios", self.input_ganglios),
            ("Aspecto clínico general", self.input_aspecto_clinico)
        ]
        
        for texto, widget in examenes:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout.addWidget(lbl)
            widget.setMinimumHeight(80)
            layout.addWidget(widget)

    def limpiar_campos(self):
        # (Método igual al que ya tenías)
        campos = [
            self.input_nombre, self.input_apellido, self.input_cedula,
            self.input_telefono, self.input_edad, self.input_medicamento_actual,
            self.input_alergias, self.input_especificar_otras
        ]
        
        for campo in campos:
            campo.clear()
        
        self.input_tejidos_intraorales.clear()
        self.input_tejidos_extraorales.clear()
        self.input_ganglios.clear()
        self.input_aspecto_clinico.clear()

        for checkbox in [
            self.check_embarazada, self.check_hemorragias,
            self.check_problemas_tratamiento, self.check_enfermedad_cardiovascular,
            self.check_diabetes, self.check_hepatitis, self.check_artritis,
            self.check_tuberculosis, self.check_enfermedades_venereas,
            self.check_hipertension, self.check_enfermedades_sanguineas,
            self.check_otras_enfermedades
        ]:
            checkbox.setChecked(False)

    def guardar(self):
        # (Método igual al que ya tenías)
        try:
            if not self.input_nombre.text() or not self.input_apellido.text():
                QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
                return
            
            cedula = self.input_cedula.text().strip()
            if cedula and self.db.existe_paciente_cedula(cedula):
                QMessageBox.warning(self, "Error", "Ya existe un paciente con esta cédula")
                return
            
            if self.input_edad.text() and not self.input_edad.text().isdigit():
                QMessageBox.warning(self, "Error", "La edad debe ser un número válido")
                return
            
            paciente_id = self.db.agregar_paciente(
                nombre=self.input_nombre.text(),
                apellido=self.input_apellido.text(),
                cedula=cedula,
                telefono=self.input_telefono.text(),
                edad=int(self.input_edad.text()) if self.input_edad.text() else 0,
                medicamento_actual=self.input_medicamento_actual.text(),
                alergias=self.input_alergias.text(),
                embarazada=1 if self.check_embarazada.isChecked() else 0,
                hemorragias=1 if self.check_hemorragias.isChecked() else 0,
                problemas_tratamiento=1 if self.check_problemas_tratamiento.isChecked() else 0,
                enfermedad_cardiovascular=1 if self.check_enfermedad_cardiovascular.isChecked() else 0,
                diabetes=1 if self.check_diabetes.isChecked() else 0,
                hepatitis=1 if self.check_hepatitis.isChecked() else 0,
                artritis=1 if self.check_artritis.isChecked() else 0,
                tuberculosis=1 if self.check_tuberculosis.isChecked() else 0,
                enfermedades_venereas=1 if self.check_enfermedades_venereas.isChecked() else 0,
                hipertension=1 if self.check_hipertension.isChecked() else 0,
                enfermedades_sanguineas=1 if self.check_enfermedades_sanguineas.isChecked() else 0,
                otras_enfermedades=1 if self.check_otras_enfermedades.isChecked() else 0,
                especificar_otras=self.input_especificar_otras.text(),
                tejidos_blandos_intraorales=self.input_tejidos_intraorales.toPlainText(),
                tejidos_blandos_extraorales=self.input_tejidos_extraorales.toPlainText(),
                ganglios=self.input_ganglios.toPlainText(),
                aspecto_clinico_general=self.input_aspecto_clinico.toPlainText()
            )
            
            QMessageBox.information(self, "Éxito", "Paciente guardado correctamente")
            self.limpiar_campos()
            
            # Preguntar si desea agregar una consulta inmediatamente
            respuesta = QMessageBox.question(
                self, "Nueva Consulta",
                "¿Desea agregar una consulta para este paciente ahora?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                from views.consulta_window import VentanaCargarConsulta
                ventana_consulta = VentanaCargarConsulta(self.parent, self.db, paciente_id)
                ventana_consulta.exec_()
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar: {str(e)}")

class VentanaDetallePaciente(QDialog):  # CAMBIADO a QDialog
    def __init__(self, paciente, db, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # Ventana independiente
        self.paciente = paciente  # Diccionario
        self.db = db
        self.setWindowTitle("Detalle del Paciente")
        self.resize(900, 800)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Pestañas
        tab_info = QWidget()
        self.setup_info_tab(tab_info)

        tab_odonto = QWidget()
        self.setup_odontograma_tab(tab_odonto)

        self.tab_widget.addTab(tab_info, "📋 Información del Paciente")
        self.tab_widget.addTab(tab_odonto, "🦷 Odontograma")

        layout.addWidget(self.tab_widget)

        # Botón cerrar DENTRO del layout principal
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("padding: 10px; font-size: 14px; margin-top: 10px;")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)

    def setup_info_tab(self, tab):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignTop)

        # Título
        nombre = self.paciente.get('nombre', '')
        apellido = self.paciente.get('apellido', '')
        titulo = QLabel(f"🩺 {nombre} {apellido}")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #e67e22;")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(titulo)

        # Datos básicos
        edad = self.paciente.get('edad')
        edad_str = str(edad) if edad not in (None, '') else "No especificada"
        telefono = self.paciente.get('telefono', '') or "No especificado"
        cedula = self.paciente.get('cedula', '') or "No especificada"

        # Crear grid para datos básicos
        grid_datos = QGridLayout()
        grid_datos.setSpacing(10)
        
        datos_basicos = [
            ("Cédula", cedula),
            ("Edad", edad_str),
            ("Teléfono", telefono),
        ]
        
        for i, (campo, valor) in enumerate(datos_basicos):
            lbl_campo = QLabel(f"<b>{campo}:</b>")
            lbl_campo.setStyleSheet("font-size: 14px;")
            lbl_valor = QLabel(valor)
            lbl_valor.setStyleSheet("font-size: 14px; padding-left: 10px;")
            
            grid_datos.addWidget(lbl_campo, i, 0)
            grid_datos.addWidget(lbl_valor, i, 1)
        
        layout.addLayout(grid_datos)
        layout.addSpacing(20)

        # Historial médico
        lbl_historial = QLabel("📋 HISTORIAL MÉDICO")
        lbl_historial.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2980b9; 
            margin-top: 15px;
            padding: 5px;
            background-color: #ecf0f1;
            border-radius: 5px;
        """)
        lbl_historial.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_historial)

        # Medicamento actual
        medicamento = self.paciente.get('medicamento_actual', '')
        if medicamento:
            lbl_med = QLabel(f"<b>Medicamento actual:</b> {medicamento}")
            lbl_med.setStyleSheet("font-size: 14px; padding: 5px;")
            lbl_med.setWordWrap(True)
            layout.addWidget(lbl_med)

        # Alergias
        alergias = self.paciente.get('alergias', '')
        if alergias:
            lbl_alergias = QLabel(f"<b>Alergias:</b> {alergias}")
            lbl_alergias.setStyleSheet("font-size: 14px; padding: 5px;")
            lbl_alergias.setWordWrap(True)
            layout.addWidget(lbl_alergias)

        # Condiciones (checkboxes convertidos a texto)
        condiciones_grid = QGridLayout()
        condiciones_grid.setSpacing(5)
        
        condiciones = [
            ("embarazada", "¿Está embarazada?", 0),
            ("hemorragias", "¿Tuvo hemorragias anormales?", 1),
            ("problemas_tratamiento", "¿Problemas con tratamientos?", 2),
            ("enfermedad_cardiovascular", "¿Enfermedad cardiovascular?", 3),
        ]
        
        row = 0
        col = 0
        for campo, texto, _ in condiciones:
            if self.paciente.get(campo):
                lbl = QLabel(f"✓ {texto}")
                lbl.setStyleSheet("font-size: 13px; color: #27ae60; padding: 3px;")
                condiciones_grid.addWidget(lbl, row, col)
                col += 1
                if col > 1:
                    col = 0
                    row += 1
        
        if row > 0 or col > 0:
            layout.addLayout(condiciones_grid)
            layout.addSpacing(10)

        # Enfermedades
        lbl_enfermedades = QLabel("Enfermedades:")
        lbl_enfermedades.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(lbl_enfermedades)

        enfermedades = [
            ('Diabetes', 'diabetes'),
            ('Hepatitis', 'hepatitis'),
            ('Artritis', 'artritis'),
            ('Tuberculosis', 'tuberculosis'),
            ('Enfermedades venéreas', 'enfermedades_venereas'),
            ('Hipertensión', 'hipertension'),
            ('Enfermedades sanguíneas', 'enfermedades_sanguineas'),
            ('Otras enfermedades', 'otras_enfermedades')
        ]
        
        enfermedades_grid = QGridLayout()
        enfermedades_grid.setSpacing(8)
        
        enfermedades_presentes = []
        for i, (nombre, campo) in enumerate(enfermedades):
            if self.paciente.get(campo):
                lbl = QLabel(f"• {nombre}")
                lbl.setStyleSheet("font-size: 14px; padding: 2px;")
                enfermedades_grid.addWidget(lbl, i // 2, i % 2)
                enfermedades_presentes.append(nombre)
        
        if enfermedades_presentes:
            layout.addLayout(enfermedades_grid)
            
            # Especificar otras
            especificar = self.paciente.get('especificar_otras', '')
            if especificar:
                lbl_otras = QLabel(f"<b>Especificar otras:</b> {especificar}")
                lbl_otras.setStyleSheet("font-size: 14px; padding: 5px; background-color: #f8f9fa; border-radius: 5px;")
                lbl_otras.setWordWrap(True)
                layout.addWidget(lbl_otras)
        
        # Examen clínico
        lbl_examen = QLabel("🔍 EXAMEN CLÍNICO")
        lbl_examen.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2980b9; 
            margin-top: 20px;
            padding: 5px;
            background-color: #ecf0f1;
            border-radius: 5px;
        """)
        lbl_examen.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_examen)

        examenes = [
            ('tejidos_blandos_intraorales', 'Tejidos blandos intraorales'),
            ('tejidos_blandos_extraorales', 'Tejidos blandos extraorales'),
            ('ganglios', 'Ganglios'),
            ('aspecto_clinico_general', 'Aspecto clínico general')
        ]
        
        for campo, texto in examenes:
            valor = self.paciente.get(campo, '')
            if valor:
                lbl_titulo = QLabel(f"<b>{texto}:</b>")
                lbl_titulo.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
                layout.addWidget(lbl_titulo)
                
                lbl_valor = QLabel(valor)
                lbl_valor.setStyleSheet("""
                    font-size: 13px; 
                    padding: 8px; 
                    background-color: #f8f9fa; 
                    border-radius: 5px;
                    border: 1px solid #dee2e6;
                """)
                lbl_valor.setWordWrap(True)
                layout.addWidget(lbl_valor)

        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll)

    def setup_odontograma_tab(self, tab):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignTop)

        nombre = self.paciente.get('nombre', '')
        apellido = self.paciente.get('apellido', '')
        titulo = QLabel(f"🦷 Odontograma - {nombre} {apellido}")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Obtener la última consulta del paciente para mostrar su odontograma
        try:
            consultas = self.db.obtener_consultas_paciente(self.paciente['id'])
            if consultas:
                ultima_consulta = consultas[0]  # La más reciente
                from views.odontograma_view_widget import OdontogramaViewWidget
                odontograma_view = OdontogramaViewWidget(ultima_consulta[0], self.db)
                odontograma_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout.addWidget(odontograma_view)
            else:
                error_label = QLabel("⚠️ Este paciente no tiene consultas registradas")
                error_label.setStyleSheet("color: #e74c3c; padding: 20px; font-size: 14px;")
                error_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(error_label)
        except Exception as e:
            print(f"Error mostrando odontograma: {e}")
            error_label = QLabel("⚠️ No se pudo cargar el odontograma")
            error_label.setStyleSheet("color: #e74c3c; padding: 20px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll)

class VentanaBuscar(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        titulo = QLabel("🔍 Buscar Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Buscar por nombre, apellido, cédula o teléfono...")
        self.input_buscar.textChanged.connect(self.buscar)
        self.input_buscar.setMinimumHeight(30)
        layout.addWidget(self.input_buscar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Apellido", "Cédula", "Teléfono", "Edad"
        ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.cellDoubleClicked.connect(self.mostrar_detalle)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)

        btn_volver = QPushButton("⬅️ Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; 
                color: white; 
                padding: 8px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)
        layout.addWidget(btn_volver)
        
        self.buscar()

    def buscar(self):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        self.tabla.setRowCount(len(resultados))
        
        for i, paciente in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(paciente.get('nombre', '')))
            self.tabla.setItem(i, 1, QTableWidgetItem(paciente.get('apellido', '')))
            self.tabla.setItem(i, 2, QTableWidgetItem(paciente.get('cedula', '')))
            self.tabla.setItem(i, 3, QTableWidgetItem(paciente.get('telefono', '')))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(paciente.get('edad', ''))))

    def mostrar_detalle(self, row, col):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        
        if row < len(resultados):
            paciente = resultados[row]
            detalle = VentanaDetallePaciente(paciente, self.db, self)
            detalle.exec_()  # Modal

class VentanaModificar(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.selected_id = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        titulo = QLabel("🛠️ Modificar / Eliminar Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Buscar paciente por nombre, apellido, cédula o teléfono...")
        self.input_buscar.textChanged.connect(self.buscar)
        self.input_buscar.setMinimumHeight(30)
        layout.addWidget(self.input_buscar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Apellido", "Cédula", "Teléfono", "Edad", "Acciones"
        ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.cellClicked.connect(self.seleccionar_paciente)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tabla)

        btn_editar = QPushButton("✏️ Editar Paciente")
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 8px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_editar.clicked.connect(self.editar)
        
        btn_eliminar = QPushButton("🗑️ Eliminar Paciente")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 8px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar)
        
        btn_consultas = QPushButton("📋 Ver Consultas")
        btn_consultas.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; 
                color: white; 
                padding: 8px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_consultas.clicked.connect(self.ver_consultas)
        
        btn_volver = QPushButton("⬅️ Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; 
                color: white; 
                padding: 8px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_eliminar)
        btn_layout.addWidget(btn_consultas)
        btn_layout.addWidget(btn_volver)
        
        layout.addLayout(btn_layout)
        self.buscar()

    def buscar(self):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        self.tabla.setRowCount(len(resultados))
        
        for i, paciente in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(paciente.get('nombre', '')))
            self.tabla.setItem(i, 1, QTableWidgetItem(paciente.get('apellido', '')))
            self.tabla.setItem(i, 2, QTableWidgetItem(paciente.get('cedula', '')))
            self.tabla.setItem(i, 3, QTableWidgetItem(paciente.get('telefono', '')))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(paciente.get('edad', ''))))
            
            # Botón ver detalle rápido
            btn_ver = QPushButton("👁️ Ver")
            btn_ver.setStyleSheet("padding: 5px;")
            btn_ver.clicked.connect(lambda checked, pid=paciente['id']: self.ver_detalle_rapido(pid))
            self.tabla.setCellWidget(i, 5, btn_ver)
            
        self.selected_id = None

    def seleccionar_paciente(self, row, col):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        if row < len(resultados):
            self.selected_id = resultados[row].get('id')
    
    def ver_detalle_rapido(self, paciente_id):
        paciente = self.db.obtener_paciente_por_id(paciente_id)
        if paciente:
            ventana_detalle = VentanaDetallePaciente(paciente, self.db, self)
            ventana_detalle.exec_()
    
    def editar(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un paciente")
            return
        ventana_editar = VentanaEditar(self, self.db, self.selected_id)
        ventana_editar.exec_()  # Modal
    
    def eliminar(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un paciente")
            return
        
        # Verificar si tiene consultas
        consultas = self.db.obtener_consultas_paciente(self.selected_id)
        if consultas:
            respuesta = QMessageBox.warning(
                self, "Confirmar Eliminación",
                f"Este paciente tiene {len(consultas)} consultas registradas.\n\n"
                "¿Está seguro de eliminar al paciente?\n"
                "TODAS las consultas asociadas también se eliminarán.",
                QMessageBox.Yes | QMessageBox.No
            )
        else:
            respuesta = QMessageBox.question(
                self, "Confirmar", 
                "¿Desea eliminar este paciente?",
                QMessageBox.Yes | QMessageBox.No
            )
        
        if respuesta == QMessageBox.Yes:
            if self.db.eliminar_paciente(self.selected_id):
                QMessageBox.information(self, "Éxito", "Paciente eliminado correctamente")
                self.buscar()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el paciente")
    
    def ver_consultas(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un paciente")
            return
        
        paciente = self.db.obtener_paciente_por_id(self.selected_id)
        if paciente:
            ventana_consultas = VentanaHistorialConsultas(self, self.db, self.selected_id)
            ventana_consultas.exec_()  # Modal

class VentanaEditar(QDialog):  # CAMBIADO a QDialog
    def __init__(self, parent, db, paciente_id):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)  # Ventana independiente
        self.parent = parent
        self.db = db
        self.paciente_id = paciente_id
        self.paciente = self.db.obtener_paciente_por_id(paciente_id)

        if not self.paciente:
            QMessageBox.warning(self, "Error", "Paciente no encontrado")
            self.close()
            return

        self.setWindowTitle("✏️ Editar Paciente")
        self.resize(1000, 700)
        self.setup_ui()
        self.cargar_datos()
    
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Scroll area que contiene TODO
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        
        content_layout = QVBoxLayout(content)
        
        # Título
        titulo = QLabel("✏️ Editar Información del Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #e67e22; padding: 10px;")
        titulo.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(titulo)
        
        # Campos de edición
        self.setup_campos_edicion(content_layout)
        
        # Botones DENTRO del contenido scrollable
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("💾 Guardar Cambios")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_guardar.clicked.connect(self.guardar)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                margin-top: 20px;
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
        content_layout.addStretch()  # Espacio flexible al final
        
        # Solo el scroll va al layout principal
        main_layout.addWidget(scroll)
    
    def setup_campos_edicion(self, layout):
        # Título
        titulo = QLabel("✏️ Editar Información del Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #e67e22;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Campos básicos del paciente
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")
        
        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Apellido")
        
        self.input_cedula = QLineEdit()
        self.input_cedula.setPlaceholderText("Número de cédula")
        
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Número de teléfono")
        
        self.input_edad = QLineEdit()
        self.input_edad.setPlaceholderText("Edad")
        
        campos_basicos = [
            ("Nombre", self.input_nombre),
            ("Apellido", self.input_apellido),
            ("Cédula", self.input_cedula),
            ("Teléfono", self.input_telefono),
            ("Edad", self.input_edad)
        ]
        
        for texto, widget in campos_basicos:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout.addWidget(lbl)
            widget.setMinimumHeight(30)
            layout.addWidget(widget)
        
        # Historial médico
        lbl_historial = QLabel("📋 HISTORIAL MÉDICO")
        lbl_historial.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout.addWidget(lbl_historial)
        
        self.input_medicamento_actual = QLineEdit()
        self.input_medicamento_actual.setPlaceholderText("Medicamento actual")
        layout.addWidget(QLabel("Medicamento actual:"))
        layout.addWidget(self.input_medicamento_actual)
        
        self.input_alergias = QLineEdit()
        self.input_alergias.setPlaceholderText("Alergias")
        layout.addWidget(QLabel("Alergias:"))
        layout.addWidget(self.input_alergias)
        
        # Checkboxes para condiciones médicas
        self.check_embarazada = QCheckBox("¿Está embarazada?")
        self.check_hemorragias = QCheckBox("¿Tuvo hemorragias anormales?")
        self.check_problemas_tratamiento = QCheckBox("¿Presentó algún problema serio asociado con el tratamiento?")
        self.check_enfermedad_cardiovascular = QCheckBox("¿Sufre de alguna enfermedad cardiovascular?")
        
        for checkbox in [
            self.check_embarazada, self.check_hemorragias,
            self.check_problemas_tratamiento, self.check_enfermedad_cardiovascular
        ]:
            layout.addWidget(checkbox)
        
        # Enfermedades
        lbl_enfermedades = QLabel("Enfermedades:")
        lbl_enfermedades.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(lbl_enfermedades)
        
        self.check_diabetes = QCheckBox("Diabetes")
        self.check_hepatitis = QCheckBox("Hepatitis")
        self.check_artritis = QCheckBox("Artritis")
        self.check_tuberculosis = QCheckBox("Tuberculosis")
        self.check_enfermedades_venereas = QCheckBox("Enfermedades venéreas")
        self.check_hipertension = QCheckBox("Hipertensión")
        self.check_enfermedades_sanguineas = QCheckBox("Enfermedades sanguíneas")
        self.check_otras_enfermedades = QCheckBox("Otras enfermedades")
        
        self.input_especificar_otras = QLineEdit()
        self.input_especificar_otras.setPlaceholderText("Especifique otras enfermedades")
        
        enfermedades_grid = QGridLayout()
        enfermedades = [
            (self.check_diabetes, 0, 0),
            (self.check_hepatitis, 0, 1),
            (self.check_artritis, 0, 2),
            (self.check_tuberculosis, 1, 0),
            (self.check_enfermedades_venereas, 1, 1),
            (self.check_hipertension, 1, 2),
            (self.check_enfermedades_sanguineas, 2, 0),
            (self.check_otras_enfermedades, 2, 1)
        ]
        
        for checkbox, row, col in enfermedades:
            enfermedades_grid.addWidget(checkbox, row, col)
        
        layout.addLayout(enfermedades_grid)
        layout.addWidget(self.input_especificar_otras)
        
        # Examen clínico
        lbl_examen = QLabel("🔍 EXAMEN CLÍNICO")
        lbl_examen.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout.addWidget(lbl_examen)
        
        self.input_tejidos_intraorales = QTextEdit()
        self.input_tejidos_intraorales.setPlaceholderText("Describa el estado de los tejidos blandos intraorales")
        
        self.input_tejidos_extraorales = QTextEdit()
        self.input_tejidos_extraorales.setPlaceholderText("Describa el estado de los tejidos blandos extraorales")
        
        self.input_ganglios = QTextEdit()
        self.input_ganglios.setPlaceholderText("Describa el estado de los ganglios")
        
        self.input_aspecto_clinico = QTextEdit()
        self.input_aspecto_clinico.setPlaceholderText("Describa el aspecto clínico general")
        
        examenes = [
            ("Tejidos blandos intraorales", self.input_tejidos_intraorales),
            ("Tejidos blandos extraorales", self.input_tejidos_extraorales),
            ("Ganglios", self.input_ganglios),
            ("Aspecto clínico general", self.input_aspecto_clinico)
        ]
        
        for texto, widget in examenes:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout.addWidget(lbl)
            widget.setMinimumHeight(80)
            layout.addWidget(widget)

    def cargar_datos(self):
        if not self.paciente:
            return
            
        self.input_nombre.setText(self.paciente.get('nombre', '') or "")
        self.input_apellido.setText(self.paciente.get('apellido', '') or "")
        self.input_cedula.setText(self.paciente.get('cedula', '') or "")
        self.input_telefono.setText(self.paciente.get('telefono', '') or "")
        self.input_edad.setText(str(self.paciente.get('edad', '')) if self.paciente.get('edad') else "")
        
        self.input_medicamento_actual.setText(self.paciente.get('medicamento_actual', '') or "")
        self.input_alergias.setText(self.paciente.get('alergias', '') or "")
        self.check_embarazada.setChecked(bool(self.paciente.get('embarazada', 0)))
        self.check_hemorragias.setChecked(bool(self.paciente.get('hemorragias', 0)))
        self.check_problemas_tratamiento.setChecked(bool(self.paciente.get('problemas_tratamiento', 0)))
        self.check_enfermedad_cardiovascular.setChecked(bool(self.paciente.get('enfermedad_cardiovascular', 0)))
        
        self.check_diabetes.setChecked(bool(self.paciente.get('diabetes', 0)))
        self.check_hepatitis.setChecked(bool(self.paciente.get('hepatitis', 0)))
        self.check_artritis.setChecked(bool(self.paciente.get('artritis', 0)))
        self.check_tuberculosis.setChecked(bool(self.paciente.get('tuberculosis', 0)))
        self.check_enfermedades_venereas.setChecked(bool(self.paciente.get('enfermedades_venereas', 0)))
        self.check_hipertension.setChecked(bool(self.paciente.get('hipertension', 0)))
        self.check_enfermedades_sanguineas.setChecked(bool(self.paciente.get('enfermedades_sanguineas', 0)))
        self.check_otras_enfermedades.setChecked(bool(self.paciente.get('otras_enfermedades', 0)))
        self.input_especificar_otras.setText(self.paciente.get('especificar_otras', '') or "")
        
        self.input_tejidos_intraorales.setPlainText(self.paciente.get('tejidos_blandos_intraorales', '') or "")
        self.input_tejidos_extraorales.setPlainText(self.paciente.get('tejidos_blandos_extraorales', '') or "")
        self.input_ganglios.setPlainText(self.paciente.get('ganglios', '') or "")
        self.input_aspecto_clinico.setPlainText(self.paciente.get('aspecto_clinico_general', '') or "")

    def guardar(self):
        try:
            if not self.input_nombre.text() or not self.input_apellido.text():
                QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
                return
            
            cedula = self.input_cedula.text().strip()
            if cedula and self.db.existe_paciente_cedula(cedula, self.paciente_id):
                QMessageBox.warning(self, "Error", "Ya existe otro paciente con esta cédula")
                return
            
            if self.input_edad.text() and not self.input_edad.text().isdigit():
                QMessageBox.warning(self, "Error", "La edad debe ser un número válido")
                return
            
            success = self.db.modificar_paciente(
                self.paciente_id,
                nombre=self.input_nombre.text(),
                apellido=self.input_apellido.text(),
                cedula=cedula,
                telefono=self.input_telefono.text(),
                edad=int(self.input_edad.text()) if self.input_edad.text() else 0,
                medicamento_actual=self.input_medicamento_actual.text(),
                alergias=self.input_alergias.text(),
                embarazada=1 if self.check_embarazada.isChecked() else 0,
                hemorragias=1 if self.check_hemorragias.isChecked() else 0,
                problemas_tratamiento=1 if self.check_problemas_tratamiento.isChecked() else 0,
                enfermedad_cardiovascular=1 if self.check_enfermedad_cardiovascular.isChecked() else 0,
                diabetes=1 if self.check_diabetes.isChecked() else 0,
                hepatitis=1 if self.check_hepatitis.isChecked() else 0,
                artritis=1 if self.check_artritis.isChecked() else 0,
                tuberculosis=1 if self.check_tuberculosis.isChecked() else 0,
                enfermedades_venereas=1 if self.check_enfermedades_venereas.isChecked() else 0,
                hipertension=1 if self.check_hipertension.isChecked() else 0,
                enfermedades_sanguineas=1 if self.check_enfermedades_sanguineas.isChecked() else 0,
                otras_enfermedades=1 if self.check_otras_enfermedades.isChecked() else 0,
                especificar_otras=self.input_especificar_otras.text(),
                tejidos_blandos_intraorales=self.input_tejidos_intraorales.toPlainText(),
                tejidos_blandos_extraorales=self.input_tejidos_extraorales.toPlainText(),
                ganglios=self.input_ganglios.toPlainText(),
                aspecto_clinico_general=self.input_aspecto_clinico.toPlainText()
            )

            if success:
                QMessageBox.information(self, "Éxito", "Paciente modificado correctamente")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No se pudo modificar el paciente")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al modificar: {str(e)}")