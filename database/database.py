import sqlite3
import os
import sys
import hashlib
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            carpeta = os.path.dirname(sys.executable)
        else:
            carpeta = os.path.dirname(os.path.abspath(__file__))

        self.db_path = os.path.join(carpeta, "odontologia.db")
        print(f"📁 Usando base de datos: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        
        self.crear_tablas()
        
        if not self.validar_usuario("admin", "1234"):
            self.agregar_usuario("admin", "1234")
    
    def obtener_ruta_db(self):
        return self.db_path
    
    def crear_tablas(self):
        cursor = self.conn.cursor()
        
        # Tabla usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
        """)
        
        # Tabla pacientes (datos permanentes)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cedula TEXT UNIQUE,
            telefono TEXT,
            edad INTEGER,
            -- Historial médico (texto completo)
            medicamento_actual TEXT,
            alergias TEXT,
            embarazada INTEGER DEFAULT 0,
            hemorragias INTEGER DEFAULT 0,
            problemas_tratamiento INTEGER DEFAULT 0,
            enfermedad_cardiovascular INTEGER DEFAULT 0,
            diabetes INTEGER DEFAULT 0,
            hepatitis INTEGER DEFAULT 0,
            artritis INTEGER DEFAULT 0,
            tuberculosis INTEGER DEFAULT 0,
            enfermedades_venereas INTEGER DEFAULT 0,
            hipertension INTEGER DEFAULT 0,
            enfermedades_sanguineas INTEGER DEFAULT 0,
            otras_enfermedades INTEGER DEFAULT 0,
            especificar_otras TEXT,
            -- Examen clínico (texto completo)
            tejidos_blandos_intraorales TEXT,
            tejidos_blandos_extraorales TEXT,
            ganglios TEXT,
            aspecto_clinico_general TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabla consultas (eventos independientes)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            precio REAL NOT NULL DEFAULT 0.0,
            motivo TEXT,
            observaciones TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
        )
        """)
        
        # Tabla odontograma (relacionado con consulta)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS odontograma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consulta_id INTEGER NOT NULL,
            diente_numero INTEGER NOT NULL,
            cara TEXT NOT NULL,
            estado TEXT DEFAULT 'sano',
            procedimiento TEXT,
            observaciones TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consulta_id) REFERENCES consultas (id) ON DELETE CASCADE,
            UNIQUE(consulta_id, diente_numero, cara)
        )
        """)
        
        self.conn.commit()
    
    # ========== MÉTODOS USUARIOS ==========
    def agregar_usuario(self, usuario, clave):
        cursor = self.conn.cursor()
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario, clave_hash))
        self.conn.commit()
    
    def validar_usuario(self, usuario, clave):
        cursor = self.conn.cursor()
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND clave=?", (usuario, clave_hash))
        return cursor.fetchone() is not None
    
    # ========== MÉTODOS PACIENTES ==========
    def agregar_paciente(self, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO pacientes 
        (nombre, apellido, cedula, telefono, edad,
         medicamento_actual, alergias, embarazada, hemorragias,
         problemas_tratamiento, enfermedad_cardiovascular, diabetes,
         hepatitis, artritis, tuberculosis, enfermedades_venereas,
         hipertension, enfermedades_sanguineas, otras_enfermedades,
         especificar_otras, tejidos_blandos_intraorales,
         tejidos_blandos_extraorales, ganglios, aspecto_clinico_general)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kwargs.get('nombre', ''),
            kwargs.get('apellido', ''),
            kwargs.get('cedula', ''),
            kwargs.get('telefono', ''),
            kwargs.get('edad', 0),
            kwargs.get('medicamento_actual', ''),
            kwargs.get('alergias', ''),
            kwargs.get('embarazada', 0),
            kwargs.get('hemorragias', 0),
            kwargs.get('problemas_tratamiento', 0),
            kwargs.get('enfermedad_cardiovascular', 0),
            kwargs.get('diabetes', 0),
            kwargs.get('hepatitis', 0),
            kwargs.get('artritis', 0),
            kwargs.get('tuberculosis', 0),
            kwargs.get('enfermedades_venereas', 0),
            kwargs.get('hipertension', 0),
            kwargs.get('enfermedades_sanguineas', 0),
            kwargs.get('otras_enfermedades', 0),
            kwargs.get('especificar_otras', ''),
            kwargs.get('tejidos_blandos_intraorales', ''),
            kwargs.get('tejidos_blandos_extraorales', ''),
            kwargs.get('ganglios', ''),
            kwargs.get('aspecto_clinico_general', '')
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def buscar_paciente(self, texto):
        cursor = self.conn.cursor()
        texto = f"%{texto}%"
        cursor.execute("""
            SELECT * FROM pacientes 
            WHERE nombre LIKE ? 
            OR apellido LIKE ? 
            OR (nombre || ' ' || apellido) LIKE ?
            OR cedula LIKE ?
            OR telefono LIKE ?
        """, (texto, texto, texto, texto, texto))
        
        resultados = cursor.fetchall()
        return [self.fila_a_diccionario(fila) for fila in resultados]
    
    def obtener_paciente_por_id(self, paciente_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,))
        fila = cursor.fetchone()
        return self.fila_a_diccionario(fila)
    
    def modificar_paciente(self, paciente_id, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE pacientes SET
            nombre = ?,
            apellido = ?,
            cedula = ?,
            telefono = ?,
            edad = ?,
            medicamento_actual = ?,
            alergias = ?,
            embarazada = ?,
            hemorragias = ?,
            problemas_tratamiento = ?,
            enfermedad_cardiovascular = ?,
            diabetes = ?,
            hepatitis = ?,
            artritis = ?,
            tuberculosis = ?,
            enfermedades_venereas = ?,
            hipertension = ?,
            enfermedades_sanguineas = ?,
            otras_enfermedades = ?,
            especificar_otras = ?,
            tejidos_blandos_intraorales = ?,
            tejidos_blandos_extraorales = ?,
            ganglios = ?,
            aspecto_clinico_general = ?
        WHERE id = ?
        """, (
            kwargs.get('nombre', ''),
            kwargs.get('apellido', ''),
            kwargs.get('cedula', ''),
            kwargs.get('telefono', ''),
            kwargs.get('edad', 0),
            kwargs.get('medicamento_actual', ''),
            kwargs.get('alergias', ''),
            kwargs.get('embarazada', 0),
            kwargs.get('hemorragias', 0),
            kwargs.get('problemas_tratamiento', 0),
            kwargs.get('enfermedad_cardiovascular', 0),
            kwargs.get('diabetes', 0),
            kwargs.get('hepatitis', 0),
            kwargs.get('artritis', 0),
            kwargs.get('tuberculosis', 0),
            kwargs.get('enfermedades_venereas', 0),
            kwargs.get('hipertension', 0),
            kwargs.get('enfermedades_sanguineas', 0),
            kwargs.get('otras_enfermedades', 0),
            kwargs.get('especificar_otras', ''),
            kwargs.get('tejidos_blandos_intraorales', ''),
            kwargs.get('tejidos_blandos_extraorales', ''),
            kwargs.get('ganglios', ''),
            kwargs.get('aspecto_clinico_general', ''),
            paciente_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def eliminar_paciente(self, paciente_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id=?", (paciente_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def existe_paciente_cedula(self, cedula, excluir_id=None):
        cursor = self.conn.cursor()
        if excluir_id:
            cursor.execute("SELECT id FROM pacientes WHERE cedula=? AND id!=?", (cedula, excluir_id))
        else:
            cursor.execute("SELECT id FROM pacientes WHERE cedula=?", (cedula,))
        return cursor.fetchone() is not None
    
    # ========== MÉTODOS CONSULTAS ==========
    def agregar_consulta(self, paciente_id, fecha, hora, precio, motivo="", observaciones=""):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO consultas (paciente_id, fecha, hora, precio, motivo, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (paciente_id, fecha, hora, precio, motivo, observaciones))
        self.conn.commit()
        return cursor.lastrowid
    
    def obtener_consultas_paciente(self, paciente_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM consultas 
        WHERE paciente_id = ? 
        ORDER BY fecha DESC, hora DESC
        """, (paciente_id,))
        return cursor.fetchall()
    
    def obtener_consulta_por_id(self, consulta_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM consultas WHERE id=?", (consulta_id,))
        return cursor.fetchone()
    
    def modificar_consulta(self, consulta_id, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE consultas SET
            fecha = ?,
            hora = ?,
            precio = ?,
            motivo = ?,
            observaciones = ?
        WHERE id = ?
        """, (
            kwargs.get('fecha', ''),
            kwargs.get('hora', ''),
            kwargs.get('precio', 0.0),
            kwargs.get('motivo', ''),
            kwargs.get('observaciones', ''),
            consulta_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def eliminar_consulta(self, consulta_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM consultas WHERE id=?", (consulta_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def obtener_consultas_entre_fechas(self, fecha_inicio, fecha_fin):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.*, p.nombre, p.apellido 
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.fecha BETWEEN ? AND ?
        ORDER BY c.fecha, c.hora
        """, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
    
    def obtener_todas_consultas(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.*, p.nombre, p.apellido 
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        ORDER BY c.fecha DESC, c.hora DESC
        """)
        return cursor.fetchall()
    
        # ========== MÉTODOS ODONTOGRAMA ==========
    def guardar_odontograma(self, consulta_id, diente_numero, cara, estado, procedimiento="", observaciones=""):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO odontograma 
            (consulta_id, diente_numero, cara, estado, procedimiento, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (consulta_id, diente_numero, cara, estado, procedimiento, observaciones))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error guardando odontograma: {e}")
            return False
    
    def obtener_odontograma_consulta(self, consulta_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT diente_numero, cara, estado, procedimiento, observaciones, created_at
        FROM odontograma WHERE consulta_id = ? ORDER BY diente_numero, cara
        """, (consulta_id,))
        return cursor.fetchall()
    
    def obtener_ultimo_odontograma_paciente(self, paciente_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT o.* FROM odontograma o
        JOIN consultas c ON o.consulta_id = c.id
        WHERE c.paciente_id = ?
        ORDER BY c.fecha DESC, c.hora DESC
        LIMIT 1
        """, (paciente_id,))
        return cursor.fetchone()
    
    def limpiar_odontograma_consulta(self, consulta_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM odontograma WHERE consulta_id = ?", (consulta_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # AGREGAR ESTE MÉTODO FALTANTE
    def eliminar_registro_odontograma(self, consulta_id, diente_numero, cara):
        """Elimina un registro específico del odontograma"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            DELETE FROM odontograma 
            WHERE consulta_id = ? AND diente_numero = ? AND cara = ?
            """, (consulta_id, diente_numero, cara))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando registro odontograma: {e}")
            return False
    
    # ========== MÉTODOS ESTADÍSTICAS ==========
    def obtener_ingresos_por_mes(self, año=None):
        cursor = self.conn.cursor()
        if año:
            cursor.execute("""
            SELECT 
                strftime('%m', fecha) as mes,
                COUNT(*) as total_consultas,
                SUM(precio) as total_ingresos
            FROM consultas
            WHERE strftime('%Y', fecha) = ?
            GROUP BY mes
            ORDER BY mes
            """, (str(año),))
        else:
            cursor.execute("""
            SELECT 
                strftime('%m/%Y', fecha) as mes_anio,
                COUNT(*) as total_consultas,
                SUM(precio) as total_ingresos
            FROM consultas
            GROUP BY mes_anio
            ORDER BY fecha DESC
            """)
        return cursor.fetchall()
    
    def obtener_ingresos_por_dia(self, fecha):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT 
            COUNT(*) as total_consultas,
            SUM(precio) as total_ingresos
        FROM consultas
        WHERE fecha = ?
        """, (fecha,))
        return cursor.fetchone()
    
    def obtener_ingresos_totales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(precio) as total_ingresos FROM consultas WHERE precio > 0")
        resultado = cursor.fetchone()
        return resultado[0] if resultado and resultado[0] else 0.0
    
    def obtener_consultas_hoy(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.*, p.nombre, p.apellido 
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.fecha = ?
        ORDER BY c.hora
        """, (hoy,))
        return cursor.fetchall()
    
    def obtener_consultas_fecha(self, fecha):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.*, p.nombre, p.apellido 
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.fecha = ?
        ORDER BY c.hora
        """, (fecha,))
        return cursor.fetchall()
    
    def obtener_proximas_consultas(self, limite=10):
        hoy = datetime.now().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.*, p.nombre, p.apellido 
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.fecha >= ?
        ORDER BY c.fecha, c.hora
        LIMIT ?
        """, (hoy, limite))
        return cursor.fetchall()
    
    # ========== MÉTODOS UTILITARIOS ==========
    def fila_a_diccionario(self, fila):
        if not fila:
            return None
        
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(pacientes)")
        columnas_info = cursor.fetchall()
        nombres_columnas = [col[1] for col in columnas_info]
        
        mapeo_columnas = {}
        for i, nombre_columna in enumerate(nombres_columnas):
            mapeo_columnas[nombre_columna] = i
        
        paciente_dict = {
            'id': fila[0],
            'nombre': str(fila[1]) if fila[1] is not None else '',
            'apellido': str(fila[2]) if fila[2] is not None else '',
            'cedula': str(fila[mapeo_columnas.get('cedula', 3)]) if mapeo_columnas.get('cedula', 3) < len(fila) and fila[mapeo_columnas.get('cedula', 3)] is not None else '',
            'telefono': str(fila[mapeo_columnas.get('telefono', 4)]) if mapeo_columnas.get('telefono', 4) < len(fila) and fila[mapeo_columnas.get('telefono', 4)] is not None else '',
            'edad': fila[mapeo_columnas.get('edad', 5)] if mapeo_columnas.get('edad', 5) < len(fila) else 0,
            'medicamento_actual': str(fila[mapeo_columnas.get('medicamento_actual', 6)]) if mapeo_columnas.get('medicamento_actual', 6) < len(fila) and fila[mapeo_columnas.get('medicamento_actual', 6)] is not None else '',
            'alergias': str(fila[mapeo_columnas.get('alergias', 7)]) if mapeo_columnas.get('alergias', 7) < len(fila) and fila[mapeo_columnas.get('alergias', 7)] is not None else '',
            'embarazada': fila[mapeo_columnas.get('embarazada', 8)] if mapeo_columnas.get('embarazada', 8) < len(fila) else 0,
            'hemorragias': fila[mapeo_columnas.get('hemorragias', 9)] if mapeo_columnas.get('hemorragias', 9) < len(fila) else 0,
            'problemas_tratamiento': fila[mapeo_columnas.get('problemas_tratamiento', 10)] if mapeo_columnas.get('problemas_tratamiento', 10) < len(fila) else 0,
            'enfermedad_cardiovascular': fila[mapeo_columnas.get('enfermedad_cardiovascular', 11)] if mapeo_columnas.get('enfermedad_cardiovascular', 11) < len(fila) else 0,
            'diabetes': fila[mapeo_columnas.get('diabetes', 12)] if mapeo_columnas.get('diabetes', 12) < len(fila) else 0,
            'hepatitis': fila[mapeo_columnas.get('hepatitis', 13)] if mapeo_columnas.get('hepatitis', 13) < len(fila) else 0,
            'artritis': fila[mapeo_columnas.get('artritis', 14)] if mapeo_columnas.get('artritis', 14) < len(fila) else 0,
            'tuberculosis': fila[mapeo_columnas.get('tuberculosis', 15)] if mapeo_columnas.get('tuberculosis', 15) < len(fila) else 0,
            'enfermedades_venereas': fila[mapeo_columnas.get('enfermedades_venereas', 16)] if mapeo_columnas.get('enfermedades_venereas', 16) < len(fila) else 0,
            'hipertension': fila[mapeo_columnas.get('hipertension', 17)] if mapeo_columnas.get('hipertension', 17) < len(fila) else 0,
            'enfermedades_sanguineas': fila[mapeo_columnas.get('enfermedades_sanguineas', 18)] if mapeo_columnas.get('enfermedades_sanguineas', 18) < len(fila) else 0,
            'otras_enfermedades': fila[mapeo_columnas.get('otras_enfermedades', 19)] if mapeo_columnas.get('otras_enfermedades', 19) < len(fila) else 0,
            'especificar_otras': str(fila[mapeo_columnas.get('especificar_otras', 20)]) if mapeo_columnas.get('especificar_otras', 20) < len(fila) and fila[mapeo_columnas.get('especificar_otras', 20)] is not None else '',
            'tejidos_blandos_intraorales': str(fila[mapeo_columnas.get('tejidos_blandos_intraorales', 21)]) if mapeo_columnas.get('tejidos_blandos_intraorales', 21) < len(fila) and fila[mapeo_columnas.get('tejidos_blandos_intraorales', 21)] is not None else '',
            'tejidos_blandos_extraorales': str(fila[mapeo_columnas.get('tejidos_blandos_extraorales', 22)]) if mapeo_columnas.get('tejidos_blandos_extraorales', 22) < len(fila) and fila[mapeo_columnas.get('tejidos_blandos_extraorales', 22)] is not None else '',
            'ganglios': str(fila[mapeo_columnas.get('ganglios', 23)]) if mapeo_columnas.get('ganglios', 23) < len(fila) and fila[mapeo_columnas.get('ganglios', 23)] is not None else '',
            'aspecto_clinico_general': str(fila[mapeo_columnas.get('aspecto_clinico_general', 24)]) if mapeo_columnas.get('aspecto_clinico_general', 24) < len(fila) and fila[mapeo_columnas.get('aspecto_clinico_general', 24)] is not None else ''
        }
        
        return paciente_dict
    
    def exportar_consultas_a_excel(self, ruta):
        try:
            df = pd.read_sql_query("""
            SELECT 
                p.nombre,
                p.apellido,
                p.cedula,
                c.fecha,
                c.hora,
                c.precio,
                c.motivo,
                c.observaciones
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            ORDER BY c.fecha DESC, c.hora DESC
            """, self.conn)
            
            if df.empty:
                df = pd.DataFrame(columns=['nombre', 'apellido', 'cedula', 'fecha', 'hora', 'precio', 'motivo', 'observaciones'])
            
            df.to_excel(ruta, index=False, engine='openpyxl')
            return True
        except Exception as e:
            print(f"Error exportando consultas: {e}")
            return False