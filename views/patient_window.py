from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QCheckBox, QGridLayout, QScrollArea, 
                             QMessageBox, QListWidget, QListWidgetItem,QGroupBox,QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from views.base_window import BaseWindow
from utilidades.validators import validar_fecha, validar_hora
from views.odontograma_widget import OdontogramaWidget
from PyQt5.QtWidgets import QTabWidget
from views.odontograma_view_widget import OdontogramaViewWidget

class VentanaCargar(BaseWindow):  # ✅ Ya hereda de BaseWindow
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        # Scroll para todos los campos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        
        layout = QVBoxLayout(content)
        self.setup_form_fields(layout, include_buttons=False)  # Los botones no van en el scroll

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

        # --- Botones fuera del scroll ---
        btn_guardar = QPushButton("💾 Guardar")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
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
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_inicio)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_volver)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def setup_form_fields(self, layout, include_buttons=True):
        # Título
        titulo = QLabel("➕ Cargar Nuevo Paciente")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #27ae60;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Campos básicos
        self.input_nombre = QLineEdit()
        self.input_apellido = QLineEdit()
        self.input_cedula = QLineEdit()
        self.input_cedula.setPlaceholderText("Número de cédula")
        self.input_edad = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_fecha_cita = QLineEdit()
        self.input_fecha_cita.setPlaceholderText("DD/MM/AAAA")
        self.input_hora_cita = QLineEdit()
        self.input_hora_cita.setPlaceholderText("HH:MM")
        self.input_precio_consulta = QLineEdit()
        self.input_precio_consulta.setPlaceholderText("Precio de la consulta")
        self.input_obs = QTextEdit()
        self.input_obs.setMinimumHeight(100)

        self.input_medicamento_actual = QLineEdit()
        self.input_alergias = QLineEdit()

        self.check_embarazada = QCheckBox("¿Está embarazada?")
        self.check_hemorragias = QCheckBox("¿Tuvo hemorragias anormales?")
        self.check_problemas_tratamiento = QCheckBox("¿Presentó algún problema serio asociado con el tratamiento?")
        self.check_enfermedad_cardiovascular = QCheckBox("¿Sufre de alguna enfermedad cardiovascular?")

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

        self.input_tejidos_intraorales = QTextEdit()
        self.input_tejidos_intraorales.setPlaceholderText("Describa el estado de los tejidos blandos intraorales")
        self.input_tejidos_extraorales = QTextEdit()
        self.input_tejidos_extraorales.setPlaceholderText("Describa el estado de los tejidos blandos extraorales")
        self.input_ganglios = QTextEdit()
        self.input_ganglios.setPlaceholderText("Describa el estado de los ganglios")
        self.input_aspecto_clinico = QTextEdit()
        self.input_aspecto_clinico.setPlaceholderText("Describa el aspecto clínico general")

        # Agregar campos al layout
        campos_basicos = [
            ("Nombre", self.input_nombre),
            ("Apellido", self.input_apellido),
            ("Cédula", self.input_cedula),
            ("Edad", self.input_edad),
            ("Teléfono", self.input_telefono),
            ("Fecha de Cita (DD/MM/AAAA)", self.input_fecha_cita),
            ("Hora de Cita (HH:MM)", self.input_hora_cita),
            ("Precio Consulta", self.input_precio_consulta),
            ("Observaciones", self.input_obs)
        ]

        for texto, widget in campos_basicos:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout.addWidget(lbl)
            if isinstance(widget, QLineEdit):
                widget.setMinimumHeight(30)
            layout.addWidget(widget)

        # Historial médico
        lbl_historial = QLabel("📋 HISTORIAL MÉDICO")
        lbl_historial.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout.addWidget(lbl_historial)
        layout.addWidget(QLabel("Medicamento actual:"))
        layout.addWidget(self.input_medicamento_actual)
        layout.addWidget(QLabel("Alergias y a qué:"))
        layout.addWidget(self.input_alergias)

        for checkbox in [
            self.check_embarazada, self.check_hemorragias,
            self.check_problemas_tratamiento, self.check_enfermedad_cardiovascular
        ]:
            layout.addWidget(checkbox)

        lbl_enfermedades = QLabel("Enfermedades:")
        lbl_enfermedades.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(lbl_enfermedades)

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

    # --- Limpiar campos ---
    def limpiar_campos(self):
        campos = [
            self.input_nombre, self.input_apellido, self.input_cedula,
            self.input_edad, self.input_telefono, self.input_fecha_cita,
            self.input_hora_cita, self.input_precio_consulta,
            self.input_medicamento_actual, self.input_alergias,
            self.input_especificar_otras
        ]
        for campo in campos:
            campo.clear()
        self.input_obs.clear()
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
            checkbox.setChecked(False)

    def guardar(self):
        try:
            if not self.input_nombre.text() or not self.input_apellido.text():
                QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
                return
            
            if self.input_edad.text() and not self.input_edad.text().isdigit():
                QMessageBox.warning(self, "Error", "La edad debe ser un número válido")
                return
                
            if self.input_fecha_cita.text() and not validar_fecha(self.input_fecha_cita.text()):
                QMessageBox.warning(self, "Error", "Formato de fecha inválido. Use DD/MM/AAAA")
                return
                
            # Validar que el precio sea numérico si se ingresa
            if self.input_precio_consulta.text() and not self.input_precio_consulta.text().replace('.', '').isdigit():
                QMessageBox.warning(self, "Error", "El precio debe ser un número válido")
                return
                
            self.db.agregar_paciente(
                nombre=self.input_nombre.text(),
                apellido=self.input_apellido.text(),
                cedula=self.input_cedula.text(),  # NUEVO
                edad=int(self.input_edad.text()) if self.input_edad.text() else 0,
                telefono=self.input_telefono.text(),
                obs=self.input_obs.toPlainText(),
                fecha_cita=self.input_fecha_cita.text(),
                hora_cita=self.input_hora_cita.text(),
                precio_consulta=float(self.input_precio_consulta.text()) if self.input_precio_consulta.text() else 0.0,  # NUEVO
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
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar: {str(e)}")

class VentanaDetallePaciente(QWidget):
    def __init__(self, paciente, db):
        super().__init__()
        self.paciente = paciente  # Diccionario
        self.db = db
        self.setWindowTitle("Detalle del Paciente")
        self.resize(900, 800)
        self.setup_ui()
        
    def setup_ui(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Pestañas
        tab_info = QWidget()
        self.setup_info_tab(tab_info)

        tab_odonto = QWidget()
        self.setup_odontograma_tab(tab_odonto)

        self.tab_widget.addTab(tab_info, "📋 Información del Paciente")
        self.tab_widget.addTab(tab_odonto, "🦷 Odontograma")

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("padding: 10px; font-size: 14px; margin-top: 20px;")
        btn_cerrar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_cerrar.clicked.connect(self.close)
        main_layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.show()

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

        fecha_cita = self.paciente.get('fecha_cita', '') or "No especificada"
        hora_cita = self.paciente.get('hora_cita', '') or "No especificada"

        precio = self.paciente.get('precio_consulta', 0)
        try:
            precio_formateado = f"${float(precio):.2f}"
        except (ValueError, TypeError):
            precio_formateado = str(precio) if precio else "No especificado"

        cedula = self.paciente.get('cedula', '') or "No especificada"

        datos_basicos = [
            ("Cédula", cedula),
            ("Edad", edad_str),
            ("Teléfono", telefono),
            ("Fecha de Cita", fecha_cita),
            ("Hora de Cita", hora_cita),
            ("Precio Consulta", precio_formateado)
        ]

        for campo, valor in datos_basicos:
            lbl = QLabel(f"{campo}: {valor}")
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; padding: 3px;")
            layout.addWidget(lbl)

        # Historial médico
        self.agregar_seccion(layout, "📋 HISTORIAL MÉDICO", [
            ("Medicamento actual", 'medicamento_actual'),
            ("Alergias", 'alergias'),
            ("¿Está embarazada?", 'embarazada', lambda x: "Sí" if x in (1, True) else "No"),
            ("¿Tuvo hemorragias anormales?", 'hemorragias', lambda x: "Sí" if x in (1, True) else "No"),
            ("¿Problemas con tratamientos?", 'problemas_tratamiento', lambda x: "Sí" if x in (1, True) else "No"),
            ("¿Enfermedad cardiovascular?", 'enfermedad_cardiovascular', lambda x: "Sí" if x in (1, True) else "No")
        ])

        # Enfermedades
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
        enfermedades_presentes = [enfermedad for enfermedad, campo in enfermedades
                                 if self.paciente.get(campo) in (1, True) or bool(self.paciente.get(campo))]
        if enfermedades_presentes:
            lbl_enfermedades = QLabel("Enfermedades: " + ", ".join(enfermedades_presentes))
            lbl_enfermedades.setStyleSheet("font-size: 16px; font-weight: bold; padding: 3px;")
            layout.addWidget(lbl_enfermedades)
            if self.paciente.get('especificar_otras'):
                lbl_otras = QLabel(f"Especificar otras: {self.paciente['especificar_otras']}")
                lbl_otras.setStyleSheet("font-size: 14px; padding: 3px;")
                layout.addWidget(lbl_otras)

        # Examen clínico
        self.agregar_seccion(layout, "🔍 EXAMEN CLÍNICO", [
            ("Tejidos blandos intraorales", 'tejidos_blandos_intraorales'),
            ("Tejidos blandos extraorales", 'tejidos_blandos_extraorales'),
            ("Ganglios", 'ganglios'),
            ("Aspecto clínico general", 'aspecto_clinico_general')
        ])

        # Observaciones
        obs = self.paciente.get('obs')
        if obs:
            lbl_obs_titulo = QLabel("Observación:")
            lbl_obs_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 15px;")
            lbl_obs_titulo.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl_obs_titulo)

            lbl_obs_texto = QLabel(str(obs))
            lbl_obs_texto.setWordWrap(True)
            lbl_obs_texto.setStyleSheet("font-size: 14px; padding: 5px;")
            layout.addWidget(lbl_obs_texto)

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

        # Widget odontograma
        try:
            from views.odontograma_view_widget import OdontogramaViewWidget
            odontograma_view = OdontogramaViewWidget(self.paciente['id'], self.db)
            odontograma_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(odontograma_view)
        except Exception as e:
            print(f"Error mostrando odontograma: {e}")
            error_label = QLabel("⚠️ No se pudo cargar el odontograma")
            error_label.setStyleSheet("color: #e74c3c; padding: 10px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll)

    def agregar_seccion(self, layout, titulo, campos):
        campos_con_valor = []
        for nombre, clave, *func in campos:
            valor = self.paciente.get(clave)
            if valor not in (None, ''):
                if func:
                    valor = func[0](valor)
                campos_con_valor.append((nombre, valor))

        if not campos_con_valor:
            return

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 15px; color: #2980b9;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        for nombre, valor in campos_con_valor:
            lbl = QLabel(f"{nombre}: {valor}")
            lbl.setStyleSheet("font-size: 14px; padding: 3px;")
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

class VentanaBuscar(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("🔍 Buscar Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese nombre o apellido...")
        self.input_buscar.textChanged.connect(self.buscar)
        self.input_buscar.setMinimumHeight(30)
        layout.addWidget(self.input_buscar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)  # CAMBIADO de 9 a 11
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Apellido", "Cédula", "Edad", "Teléfono", 
            "Fecha Cita", "Hora Cita", "Precio", "Alergias", "Medicamento", "Obs."
        ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.cellClicked.connect(self.mostrar_detalle)
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
        
        self.setLayout(layout)
        self.buscar()

    def buscar(self):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        self.tabla.setRowCount(len(resultados))
        
        for i, paciente in enumerate(resultados):
            # ORDEN CORRECTO según los headers:
            self.tabla.setItem(i, 0, QTableWidgetItem(paciente.get('nombre', '')))        # Columna 0: Nombre
            self.tabla.setItem(i, 1, QTableWidgetItem(paciente.get('apellido', '')))      # Columna 1: Apellido
            self.tabla.setItem(i, 2, QTableWidgetItem(paciente.get('cedula', '')))        # Columna 2: Cédula
            self.tabla.setItem(i, 3, QTableWidgetItem(str(paciente.get('edad', ''))))     # Columna 3: Edad
            self.tabla.setItem(i, 4, QTableWidgetItem(paciente.get('telefono', '')))      # Columna 4: Teléfono
            self.tabla.setItem(i, 5, QTableWidgetItem(paciente.get('fecha_cita', '')))    # Columna 5: Fecha Cita
            self.tabla.setItem(i, 6, QTableWidgetItem(paciente.get('hora_cita', '')))     # Columna 6: Hora Cita
            self.tabla.setItem(i, 7, QTableWidgetItem(str(paciente.get('precio_consulta', ''))))  # Columna 7: Precio
            self.tabla.setItem(i, 8, QTableWidgetItem(paciente.get('alergias', '')))      # Columna 8: Alergias
            self.tabla.setItem(i, 9, QTableWidgetItem(paciente.get('medicamento_actual', '')))    # Columna 9: Medicamento
            
            obs = paciente.get('obs', '')
            obs_preview = obs[:30] + "..." if obs and len(obs) > 30 else obs
            self.tabla.setItem(i, 10, QTableWidgetItem(obs_preview))  # Columna 10: Obs

    def mostrar_detalle(self, row, col):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        
        if row < len(resultados):
            paciente = resultados[row]  # Ya es un diccionario
            self.detalle = VentanaDetallePaciente(paciente, self.db)

class VentanaModificar(BaseWindow):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.selected_id = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        titulo = QLabel("🛠️ Modificar / Eliminar Paciente")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Buscar paciente por nombre o apellido...")
        self.input_buscar.textChanged.connect(self.buscar)
        self.input_buscar.setMinimumHeight(30)
        layout.addWidget(self.input_buscar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)  # CAMBIADO de 9 a 11
        self.tabla.setHorizontalHeaderLabels([
            "Nombre", "Apellido", "Cédula", "Edad", "Teléfono", 
            "Fecha Cita", "Hora Cita", "Precio", "Alergias", "Medicamento", "Obs."
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
        btn_layout.addWidget(btn_volver)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.buscar()

    def buscar(self):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        self.tabla.setRowCount(len(resultados))
        
        for i, paciente in enumerate(resultados):
            # ORDEN CORRECTO según los headers:
            self.tabla.setItem(i, 0, QTableWidgetItem(paciente.get('nombre', '')))        # Columna 0: Nombre
            self.tabla.setItem(i, 1, QTableWidgetItem(paciente.get('apellido', '')))      # Columna 1: Apellido
            self.tabla.setItem(i, 2, QTableWidgetItem(paciente.get('cedula', '')))        # Columna 2: Cédula
            self.tabla.setItem(i, 3, QTableWidgetItem(str(paciente.get('edad', ''))))     # Columna 3: Edad
            self.tabla.setItem(i, 4, QTableWidgetItem(paciente.get('telefono', '')))      # Columna 4: Teléfono
            self.tabla.setItem(i, 5, QTableWidgetItem(paciente.get('fecha_cita', '')))    # Columna 5: Fecha Cita
            self.tabla.setItem(i, 6, QTableWidgetItem(paciente.get('hora_cita', '')))     # Columna 6: Hora Cita
            self.tabla.setItem(i, 7, QTableWidgetItem(str(paciente.get('precio_consulta', ''))))  # Columna 7: Precio
            self.tabla.setItem(i, 8, QTableWidgetItem(paciente.get('alergias', '')))      # Columna 8: Alergias
            self.tabla.setItem(i, 9, QTableWidgetItem(paciente.get('medicamento_actual', '')))    # Columna 9: Medicamento
            
            obs = paciente.get('obs', '')
            obs_preview = obs[:30] + "..." if obs and len(obs) > 30 else obs
            self.tabla.setItem(i, 10, QTableWidgetItem(obs_preview))  # Columna 10: Obs
            
        self.selected_id = None

    def seleccionar_paciente(self, row, col):
        texto = self.input_buscar.text()
        resultados = self.db.buscar_paciente(texto)
        if row < len(resultados):
            self.selected_id = resultados[row].get('id')
            
    def editar(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un paciente")
            return
        self.parent.mostrar_editar(self.selected_id)

    def eliminar(self):
        if self.selected_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un paciente")
            return
        confirm = QMessageBox.question(self, "Confirmar", "¿Desea eliminar este paciente?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.eliminar_paciente(self.selected_id)
            self.buscar()
            QMessageBox.information(self, "Éxito", "Paciente eliminado")

class VentanaEditar(QWidget):
    def __init__(self, parent, db, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.paciente_id = paciente_id
        self.paciente = self.db.obtener_paciente_por_id(paciente_id)

        if not self.paciente:
            QMessageBox.warning(self, "Error", "Paciente no encontrado")
            self.parent.mostrar_modificar()
            return

        self.setWindowTitle("✏️ Editar Paciente")
        self.resize(1000, 700)
        self.setup_ui_con_pestanas()
        self.cargar_datos()
        

    def setup_ui_con_pestanas(self):
        """Setup con pestañas para información y odontograma"""
        from PyQt5.QtWidgets import QTabWidget
        
        # Crear widget de pestañas
        self.tab_widget = QTabWidget()
        
        # Pestaña 1: Información del paciente
        tab_info = QWidget()
        layout_info = QVBoxLayout(tab_info)
        
        # Scroll area para información
        scroll_info = QScrollArea()
        scroll_info.setWidgetResizable(True)
        content_info = QWidget()
        scroll_info.setWidget(content_info)
        layout_content = QVBoxLayout(content_info)
        
        # Título
        titulo = QLabel("✏️ Editar Información del Paciente")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #e67e22;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_content.addWidget(titulo)
        
        # Campos básicos del paciente (AGREGAR NUEVOS CAMPOS)
        self.input_nombre = QLineEdit()
        self.input_apellido = QLineEdit()
        self.input_cedula = QLineEdit()  # NUEVO CAMPO
        self.input_cedula.setPlaceholderText("Número de cédula")
        self.input_edad = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_fecha_cita = QLineEdit()
        self.input_fecha_cita.setPlaceholderText("DD/MM/AAAA")
        self.input_hora_cita = QLineEdit()
        self.input_hora_cita.setPlaceholderText("HH:MM")
        self.input_precio_consulta = QLineEdit()  # NUEVO CAMPO
        self.input_precio_consulta.setPlaceholderText("Precio de la consulta")
        self.input_obs = QTextEdit()
        self.input_obs.setMinimumHeight(100)

        # Campos del historial médico
        self.input_medicamento_actual = QLineEdit()
        self.input_alergias = QLineEdit()
        
        # Checkboxes para condiciones médicas
        self.check_embarazada = QCheckBox("¿Está embarazada?")
        self.check_hemorragias = QCheckBox("¿Tuvo hemorragias anormales?")
        self.check_problemas_tratamiento = QCheckBox("¿Presentó algún problema serio asociado con el tratamiento?")
        self.check_enfermedad_cardiovascular = QCheckBox("¿Sufre de alguna enfermedad cardiovascular?")
        
        # Checkboxes para enfermedades específicas
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
        
        # Examen clínico
        self.input_tejidos_intraorales = QTextEdit()
        self.input_tejidos_intraorales.setPlaceholderText("Describa el estado de los tejidos blandos intraorales")
        self.input_tejidos_extraorales = QTextEdit()
        self.input_tejidos_extraorales.setPlaceholderText("Describa el estado de los tejidos blandos extraorales")
        self.input_ganglios = QTextEdit()
        self.input_ganglios.setPlaceholderText("Describa el estado de los ganglios")
        self.input_aspecto_clinico = QTextEdit()
        self.input_aspecto_clinico.setPlaceholderText("Describa el aspecto clínico general")

        # Agregar campos básicos al layout
        campos_basicos = [
            ("Nombre", self.input_nombre),
            ("Apellido", self.input_apellido),
            ("Cédula", self.input_cedula),  # NUEVO
            ("Edad", self.input_edad),
            ("Teléfono", self.input_telefono),
            ("Fecha de Cita (DD/MM/AAAA)", self.input_fecha_cita),
            ("Hora de Cita (HH:MM)", self.input_hora_cita),
            ("Precio Consulta", self.input_precio_consulta),  # NUEVO
            ("Observaciones", self.input_obs)
        ]

        for texto, widget in campos_basicos:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout_content.addWidget(lbl)
            if isinstance(widget, QLineEdit):
                widget.setMinimumHeight(30)
            layout_content.addWidget(widget)

        # Sección de Historial Médico
        lbl_historial = QLabel("📋 HISTORIAL MÉDICO")
        lbl_historial.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout_content.addWidget(lbl_historial)

        layout_content.addWidget(QLabel("Medicamento actual:"))
        layout_content.addWidget(self.input_medicamento_actual)
        layout_content.addWidget(QLabel("Alergias y a qué:"))
        layout_content.addWidget(self.input_alergias)

        # Checkboxes de condiciones
        condiciones = [
            self.check_embarazada,
            self.check_hemorragias,
            self.check_problemas_tratamiento,
            self.check_enfermedad_cardiovascular
        ]
        
        for checkbox in condiciones:
            layout_content.addWidget(checkbox)

        # Enfermedades específicas
        lbl_enfermedades = QLabel("Enfermedades:")
        lbl_enfermedades.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout_content.addWidget(lbl_enfermedades)
        
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
        
        layout_content.addLayout(enfermedades_grid)
        layout_content.addWidget(self.input_especificar_otras)

        # Examen clínico
        lbl_examen = QLabel("🔍 EXAMEN CLÍNICO")
        lbl_examen.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin-top: 20px;")
        layout_content.addWidget(lbl_examen)

        examenes = [
            ("Tejidos blandos intraorales", self.input_tejidos_intraorales),
            ("Tejidos blandos extraorales", self.input_tejidos_extraorales),
            ("Ganglios", self.input_ganglios),
            ("Aspecto clínico general", self.input_aspecto_clinico)
        ]
        
        for texto, widget in examenes:
            lbl = QLabel(texto)
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            layout_content.addWidget(lbl)
            widget.setMinimumHeight(80)
            layout_content.addWidget(widget)

        layout_info.addWidget(scroll_info)
        
        # Pestaña 2: Odontograma editable
        tab_odonto = QWidget()
        layout_odonto = QVBoxLayout(tab_odonto)
        
        # Crear widget de odontograma editable
        from views.odontograma_widget import OdontogramaWidget
        self.odontograma = OdontogramaWidget(self.paciente_id, self.db)
        layout_odonto.addWidget(self.odontograma)
        
        # Agregar pestañas
        self.tab_widget.addTab(tab_info, "📋 Información General")
        self.tab_widget.addTab(tab_odonto, "🦷 Odontograma Dental")
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        
        # Botones en la parte inferior
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
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_guardar.clicked.connect(self.guardar)
        
        btn_volver = QPushButton("⬅️ Volver a Modificar")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_volver.clicked.connect(self.parent.mostrar_modificar)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_volver)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def cargar_datos(self):
        """Carga los datos del paciente en los campos del formulario"""
        if not self.paciente:
            return
            
        self.input_nombre.setText(self.paciente.get('nombre', '') or "")
        self.input_apellido.setText(self.paciente.get('apellido', '') or "")
        self.input_cedula.setText(self.paciente.get('cedula', '') or "")  # NUEVO
        self.input_edad.setText(str(self.paciente.get('edad', '')) if self.paciente.get('edad') else "")
        self.input_telefono.setText(self.paciente.get('telefono', '') or "")
        
        # NUEVO - Precio de consulta
        precio = self.paciente.get('precio_consulta', 0.0)
        self.input_precio_consulta.setText(str(precio) if precio and precio != 0.0 else "")
        
        self.input_obs.setPlainText(self.paciente.get('obs', '') or "")
        self.input_fecha_cita.setText(self.paciente.get('fecha_cita', '') or "")
        self.input_hora_cita.setText(self.paciente.get('hora_cita', '') or "")
        
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
            # Validar campos básicos
            if not self.input_nombre.text() or not self.input_apellido.text():
                QMessageBox.warning(self, "Error", "Nombre y apellido son obligatorios")
                return
            
            # Validar fecha
            if self.input_fecha_cita.text() and not validar_fecha(self.input_fecha_cita.text()):
                QMessageBox.warning(self, "Error", "Formato de fecha inválido. Use DD/MM/AAAA")
                return
            
            # Validar hora
            if self.input_hora_cita.text() and not validar_hora(self.input_hora_cita.text()):
                QMessageBox.warning(self, "Error", "Formato de hora inválido. Use HH:MM")
                return
            
            # Validar que el precio sea numérico si se ingresa
            if self.input_precio_consulta.text() and not self.input_precio_consulta.text().replace('.', '').isdigit():
                QMessageBox.warning(self, "Error", "El precio debe ser un número válido")
                return
            
            # Actualizar paciente
            self.db.modificar_paciente(
                self.paciente_id,
                nombre=self.input_nombre.text(),
                apellido=self.input_apellido.text(),
                cedula=self.input_cedula.text(),  # NUEVO
                edad=int(self.input_edad.text()) if self.input_edad.text() else 0,
                telefono=self.input_telefono.text(),
                obs=self.input_obs.toPlainText(),
                fecha_cita=self.input_fecha_cita.text(),
                hora_cita=self.input_hora_cita.text(),
                precio_consulta=float(self.input_precio_consulta.text()) if self.input_precio_consulta.text() else 0.0,  # NUEVO
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

            QMessageBox.information(self, "Éxito", "Paciente modificado correctamente")
            self.parent.mostrar_modificar()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al modificar: {str(e)}")
            import traceback
            print(traceback.format_exc())