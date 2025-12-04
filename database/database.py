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

        self.db_path = os.path.join(carpeta, "pacientes.db")
        print(f"📁 Usando base de datos local: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path)

        self.crear_tabla_usuarios()
        self.crear_tabla_pacientes()
        self.crear_tabla_odontograma() 

        if not self.validar_usuario("admin", "1234"):
            self.agregar_usuario("admin", "1234")
    
    def obtener_ruta_db(self):
        return self.db_path

    def crear_tabla_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            clave TEXT
        )
        """)
        self.conn.commit()

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

    def crear_tabla_pacientes(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            cedula TEXT,  -- NUEVO CAMPO
            edad INTEGER,
            telefono TEXT,
            obs TEXT,
            fecha_cita TEXT,
            hora_cita TEXT,
            precio_consulta REAL,  -- NUEVO CAMPO (REAL para decimales)
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
            tejidos_blandos_intraorales TEXT,
            tejidos_blandos_extraorales TEXT,
            ganglios TEXT,
            aspecto_clinico_general TEXT
        )
        """)
        
        # Agregar las nuevas columnas si no existen (para BD existentes)
        try:
            cursor.execute("ALTER TABLE pacientes ADD COLUMN cedula TEXT")
        except:
            pass  # La columna ya existe
            
        try:
            cursor.execute("ALTER TABLE pacientes ADD COLUMN precio_consulta REAL")
        except:
            pass  # La columna ya existe
            
        self.conn.commit()

    def agregar_paciente(self, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO pacientes 
        (nombre, apellido, edad, telefono, obs, fecha_cita, hora_cita, 
        medicamento_actual, alergias, embarazada, hemorragias, 
        problemas_tratamiento, enfermedad_cardiovascular, diabetes, hepatitis, 
        artritis, tuberculosis, enfermedades_venereas, hipertension, 
        enfermedades_sanguineas, otras_enfermedades, especificar_otras, 
        tejidos_blandos_intraorales, tejidos_blandos_extraorales, ganglios, 
        aspecto_clinico_general, cedula, precio_consulta)  -- ⬅️ NUEVOS CAMPOS AL FINAL
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kwargs.get('nombre'), kwargs.get('apellido'), 
            kwargs.get('edad'), kwargs.get('telefono'), kwargs.get('obs'), 
            kwargs.get('fecha_cita'), kwargs.get('hora_cita'), 
            kwargs.get('medicamento_actual'), kwargs.get('alergias'),
            kwargs.get('embarazada', 0), kwargs.get('hemorragias', 0), 
            kwargs.get('problemas_tratamiento', 0), kwargs.get('enfermedad_cardiovascular', 0),
            kwargs.get('diabetes', 0), kwargs.get('hepatitis', 0), kwargs.get('artritis', 0),
            kwargs.get('tuberculosis', 0), kwargs.get('enfermedades_venereas', 0),
            kwargs.get('hipertension', 0), kwargs.get('enfermedades_sanguineas', 0),
            kwargs.get('otras_enfermedades', 0), kwargs.get('especificar_otras', ''),
            kwargs.get('tejidos_blandos_intraorales', ''), kwargs.get('tejidos_blandos_extraorales', ''),
            kwargs.get('ganglios', ''), kwargs.get('aspecto_clinico_general', ''),
            kwargs.get('cedula', ''),  # ⬅️ NUEVO CAMPO AL FINAL
            kwargs.get('precio_consulta', 0.0)  # ⬅️ NUEVO CAMPO AL FINAL
        ))
        self.conn.commit()

    def buscar_paciente(self, texto):
        """Busca pacientes por nombre, apellido, nombre completo O cédula"""
        cursor = self.conn.cursor()
        texto = f"%{texto}%"
        cursor.execute("""
            SELECT * FROM pacientes 
            WHERE nombre LIKE ? 
            OR apellido LIKE ? 
            OR (nombre || ' ' || apellido) LIKE ?
            OR cedula LIKE ?  -- ⬅️ NUEVA BÚSQUEDA POR CÉDULA
        """, (texto, texto, texto, texto))
        
        resultados = cursor.fetchall()
        return [self.fila_a_diccionario(fila) for fila in resultados]

    def modificar_paciente(self, paciente_id, **kwargs):
        """CORREGIDO: Ahora hace UPDATE correctamente en lugar de INSERT"""
        cursor = self.conn.cursor()
        
        # Construir la consulta UPDATE dinámicamente
        campos = []
        valores = []
        
        # Mapear los nombres de campos con los valores
        mapeo_campos = {
            'nombre': kwargs.get('nombre'),
            'apellido': kwargs.get('apellido'),
            'cedula': kwargs.get('cedula', ''),
            'edad': kwargs.get('edad'),
            'telefono': kwargs.get('telefono', ''),
            'obs': kwargs.get('obs', ''),
            'fecha_cita': kwargs.get('fecha_cita', ''),
            'hora_cita': kwargs.get('hora_cita', ''),
            'precio_consulta': kwargs.get('precio_consulta', 0.0),
            'medicamento_actual': kwargs.get('medicamento_actual', ''),
            'alergias': kwargs.get('alergias', ''),
            'embarazada': kwargs.get('embarazada', 0),
            'hemorragias': kwargs.get('hemorragias', 0),
            'problemas_tratamiento': kwargs.get('problemas_tratamiento', 0),
            'enfermedad_cardiovascular': kwargs.get('enfermedad_cardiovascular', 0),
            'diabetes': kwargs.get('diabetes', 0),
            'hepatitis': kwargs.get('hepatitis', 0),
            'artritis': kwargs.get('artritis', 0),
            'tuberculosis': kwargs.get('tuberculosis', 0),
            'enfermedades_venereas': kwargs.get('enfermedades_venereas', 0),
            'hipertension': kwargs.get('hipertension', 0),
            'enfermedades_sanguineas': kwargs.get('enfermedades_sanguineas', 0),
            'otras_enfermedades': kwargs.get('otras_enfermedades', 0),
            'especificar_otras': kwargs.get('especificar_otras', ''),
            'tejidos_blandos_intraorales': kwargs.get('tejidos_blandos_intraorales', ''),
            'tejidos_blandos_extraorales': kwargs.get('tejidos_blandos_extraorales', ''),
            'ganglios': kwargs.get('ganglios', ''),
            'aspecto_clinico_general': kwargs.get('aspecto_clinico_general', '')
        }
        
        # Preparar campos y valores para el UPDATE
        for campo, valor in mapeo_campos.items():
            if valor is not None:  # Solo actualizar campos con valores
                campos.append(f"{campo} = ?")
                valores.append(valor)
        
        # Agregar el ID al final de los valores
        valores.append(paciente_id)
        
        # Construir la consulta SQL
        sql = f"UPDATE pacientes SET {', '.join(campos)} WHERE id = ?"
        
        try:
            cursor.execute(sql, valores)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error modificando paciente: {e}")
            self.conn.rollback()
            return False

    def eliminar_paciente(self, paciente_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id=?", (paciente_id,))
        self.conn.commit()
    
    def crear_tabla_odontograma(self):
        """Crea la tabla para almacenar odontogramas"""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS odontograma (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            diente_numero INTEGER,
            cara TEXT,
            estado TEXT DEFAULT 'sano',
            procedimiento TEXT,
            observaciones TEXT,
            fecha TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
            UNIQUE(paciente_id, diente_numero, cara)
        )
        """)
        self.conn.commit()

    def guardar_odontograma(self, paciente_id, diente_numero, cara, estado, procedimiento, observaciones):
        """Guarda o actualiza un registro de odontograma - CORREGIDO"""
        try:
            cursor = self.conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # ✅ PRIMERO verificar si ya existe el registro
            cursor.execute("""
                SELECT id FROM odontograma 
                WHERE paciente_id = ? AND diente_numero = ? AND cara = ?
            """, (paciente_id, diente_numero, cara))
            
            existe = cursor.fetchone()
            
            if existe:
                # ✅ ACTUALIZAR registro existente
                cursor.execute("""
                    UPDATE odontograma 
                    SET estado = ?, procedimiento = ?, observaciones = ?, fecha = ?
                    WHERE paciente_id = ? AND diente_numero = ? AND cara = ?
                """, (estado, procedimiento, observaciones, fecha_actual, 
                    paciente_id, diente_numero, cara))
            else:
                # ✅ INSERTAR nuevo registro
                cursor.execute("""
                    INSERT INTO odontograma 
                    (paciente_id, diente_numero, cara, estado, procedimiento, observaciones, fecha)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (paciente_id, diente_numero, cara, estado, procedimiento, observaciones, fecha_actual))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error guardando odontograma: {e}")
            self.conn.rollback()
            return False

    def obtener_odontograma_paciente(self, paciente_id):
        """Obtiene todo el odontograma de un paciente"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT diente_numero, cara, estado, procedimiento, observaciones, fecha
            FROM odontograma WHERE paciente_id = ? ORDER BY diente_numero, cara
            """, (paciente_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo odontograma: {e}")
            return []

    def eliminar_registro_odontograma(self, paciente_id, diente_numero, cara):
        """Elimina un registro específico del odontograma"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            DELETE FROM odontograma 
            WHERE paciente_id = ? AND diente_numero = ? AND cara = ?
            """, (paciente_id, diente_numero, cara))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error eliminando registro odontograma: {e}")
            return False

    def limpiar_odontograma_paciente(self, paciente_id):
        """Limpia todo el odontograma de un paciente"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM odontograma WHERE paciente_id = ?", (paciente_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error limpiando odontograma: {e}")
            return False
      
    def fila_a_diccionario(self, fila):
        """Convierte una fila de la base de datos a diccionario - COMPATIBLE con cualquier estructura"""
        if not fila:
            return None
        
        # ✅ Obtener los nombres de las columnas REALES de la base de datos
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(pacientes)")
        columnas_info = cursor.fetchall()
        nombres_columnas = [col[1] for col in columnas_info]  # Nombres reales de columnas
        
        # Crear mapeo de índice de columna a nombre
        mapeo_columnas = {}
        for i, nombre_columna in enumerate(nombres_columnas):
            mapeo_columnas[nombre_columna] = i
        
        # ✅ Crear diccionario basado en los nombres reales de columnas
        paciente_dict = {
            'id': fila[0],
            'nombre': str(fila[1]) if fila[1] is not None else '',
            'apellido': str(fila[2]) if fila[2] is not None else '',
            'edad': fila[mapeo_columnas.get('edad', 3)] if mapeo_columnas.get('edad', 3) < len(fila) else 0,
            'telefono': str(fila[mapeo_columnas.get('telefono', 4)]) if mapeo_columnas.get('telefono', 4) < len(fila) and fila[mapeo_columnas.get('telefono', 4)] is not None else '',
            'obs': str(fila[mapeo_columnas.get('obs', 5)]) if mapeo_columnas.get('obs', 5) < len(fila) and fila[mapeo_columnas.get('obs', 5)] is not None else '',
            'fecha_cita': str(fila[mapeo_columnas.get('fecha_cita', 6)]) if mapeo_columnas.get('fecha_cita', 6) < len(fila) and fila[mapeo_columnas.get('fecha_cita', 6)] is not None else '',
            'hora_cita': str(fila[mapeo_columnas.get('hora_cita', 7)]) if mapeo_columnas.get('hora_cita', 7) < len(fila) and fila[mapeo_columnas.get('hora_cita', 7)] is not None else '',
            'medicamento_actual': str(fila[mapeo_columnas.get('medicamento_actual', 8)]) if mapeo_columnas.get('medicamento_actual', 8) < len(fila) and fila[mapeo_columnas.get('medicamento_actual', 8)] is not None else '',
            'alergias': str(fila[mapeo_columnas.get('alergias', 9)]) if mapeo_columnas.get('alergias', 9) < len(fila) and fila[mapeo_columnas.get('alergias', 9)] is not None else '',
            'embarazada': fila[mapeo_columnas.get('embarazada', 10)] if mapeo_columnas.get('embarazada', 10) < len(fila) else 0,
            'hemorragias': fila[mapeo_columnas.get('hemorragias', 11)] if mapeo_columnas.get('hemorragias', 11) < len(fila) else 0,
            'problemas_tratamiento': fila[mapeo_columnas.get('problemas_tratamiento', 12)] if mapeo_columnas.get('problemas_tratamiento', 12) < len(fila) else 0,
            'enfermedad_cardiovascular': fila[mapeo_columnas.get('enfermedad_cardiovascular', 13)] if mapeo_columnas.get('enfermedad_cardiovascular', 13) < len(fila) else 0,
            'diabetes': fila[mapeo_columnas.get('diabetes', 14)] if mapeo_columnas.get('diabetes', 14) < len(fila) else 0,
            'hepatitis': fila[mapeo_columnas.get('hepatitis', 15)] if mapeo_columnas.get('hepatitis', 15) < len(fila) else 0,
            'artritis': fila[mapeo_columnas.get('artritis', 16)] if mapeo_columnas.get('artritis', 16) < len(fila) else 0,
            'tuberculosis': fila[mapeo_columnas.get('tuberculosis', 17)] if mapeo_columnas.get('tuberculosis', 17) < len(fila) else 0,
            'enfermedades_venereas': fila[mapeo_columnas.get('enfermedades_venereas', 18)] if mapeo_columnas.get('enfermedades_venereas', 18) < len(fila) else 0,
            'hipertension': fila[mapeo_columnas.get('hipertension', 19)] if mapeo_columnas.get('hipertension', 19) < len(fila) else 0,
            'enfermedades_sanguineas': fila[mapeo_columnas.get('enfermedades_sanguineas', 20)] if mapeo_columnas.get('enfermedades_sanguineas', 20) < len(fila) else 0,
            'otras_enfermedades': fila[mapeo_columnas.get('otras_enfermedades', 21)] if mapeo_columnas.get('otras_enfermedades', 21) < len(fila) else 0,
            'especificar_otras': str(fila[mapeo_columnas.get('especificar_otras', 22)]) if mapeo_columnas.get('especificar_otras', 22) < len(fila) and fila[mapeo_columnas.get('especificar_otras', 22)] is not None else '',
            'tejidos_blandos_intraorales': str(fila[mapeo_columnas.get('tejidos_blandos_intraorales', 23)]) if mapeo_columnas.get('tejidos_blandos_intraorales', 23) < len(fila) and fila[mapeo_columnas.get('tejidos_blandos_intraorales', 23)] is not None else '',
            'tejidos_blandos_extraorales': str(fila[mapeo_columnas.get('tejidos_blandos_extraorales', 24)]) if mapeo_columnas.get('tejidos_blandos_extraorales', 24) < len(fila) and fila[mapeo_columnas.get('tejidos_blandos_extraorales', 24)] is not None else '',
            'ganglios': str(fila[mapeo_columnas.get('ganglios', 25)]) if mapeo_columnas.get('ganglios', 25) < len(fila) and fila[mapeo_columnas.get('ganglios', 25)] is not None else '',
            'aspecto_clinico_general': str(fila[mapeo_columnas.get('aspecto_clinico_general', 26)]) if mapeo_columnas.get('aspecto_clinico_general', 26) < len(fila) and fila[mapeo_columnas.get('aspecto_clinico_general', 26)] is not None else '',
            'cedula': str(fila[mapeo_columnas.get('cedula', 27)]) if mapeo_columnas.get('cedula', 27) < len(fila) and fila[mapeo_columnas.get('cedula', 27)] is not None else '',
            'precio_consulta': fila[mapeo_columnas.get('precio_consulta', 28)] if mapeo_columnas.get('precio_consulta', 28) < len(fila) else 0.0
        }
        
        return paciente_dict
    
    def obtener_paciente_por_id(self, paciente_id):
        """Obtiene un paciente por ID como diccionario"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,))
        fila = cursor.fetchone()
        return self.fila_a_diccionario(fila)
    
    def exportar_pacientes_a_excel(self, ruta):
        try:
            print(f"🔍 Intentando exportar a: {ruta}")
            
            # Verificar si la ruta es válida
            if not ruta or not isinstance(ruta, str):
                print("❌ Ruta de exportación inválida")
                return False
                
            # Leer todos los pacientes
            df = pd.read_sql_query("SELECT * FROM pacientes", self.conn)
            
            if df.empty:
                print("⚠️ No hay pacientes para exportar")
                # Crear archivo vacío para mantener consistencia de backups
                try:
                    df_empty = pd.DataFrame(columns=['nombre', 'apellido', 'cedula', 'telefono'])
                    df_empty.to_excel(ruta, index=False)
                    print("✅ Archivo Excel vacío creado")
                    return True
                except:
                    return False
                    
            print(f"📊 Encontrados {len(df)} pacientes")

            # Eliminar la columna 'id' si existe
            if 'id' in df.columns:
                df = df.drop(columns=['id'])
                print("✅ Columna 'id' eliminada")

            # Convertir campos booleanos a Sí/No
            campos_booleanos = [
                'embarazada', 'hemorragias', 'problemas_tratamiento', 
                'enfermedad_cardiovascular', 'diabetes', 'hepatitis', 
                'artritis', 'tuberculosis', 'enfermedades_venereas', 
                'hipertension', 'enfermedades_sanguineas', 'otras_enfermedades'
            ]
            
            for campo in campos_booleanos:
                if campo in df.columns:
                    df[campo] = df[campo].apply(lambda x: 'Sí' if x else 'No')
                    print(f"✅ Campo {campo} convertido")

            # Verificar permisos de escritura
            try:
                # Crear directorio si no existe
                directorio = os.path.dirname(ruta)
                if directorio and not os.path.exists(directorio):
                    os.makedirs(directorio, exist_ok=True)
                    print(f"✅ Directorio creado: {directorio}")
                
                # Guardar en Excel
                df.to_excel(ruta, index=False, engine='openpyxl')
                print(f"✅ Excel creado exitosamente en: {ruta}")
                
                # Verificar que el archivo se creó correctamente
                if os.path.exists(ruta) and os.path.getsize(ruta) > 1024:  # Más de 1KB
                    print("✅ Archivo verificado: existe y tiene contenido")
                    return True
                else:
                    print("❌ Archivo no se creó correctamente (tamaño insuficiente)")
                    return False
                    
            except PermissionError:
                print("❌ Error de permisos al escribir el archivo")
                return False
            except Exception as e:
                print(f"❌ Error al guardar Excel: {e}")
                # Intentar con engine alternativo
                try:
                    df.to_excel(ruta, index=False, engine='xlsxwriter')
                    print("✅ Excel creado con engine alternativo")
                    return True
                except Exception as e2:
                    print(f"❌ Error con todos los engines: {e2}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error general en exportar_pacientes_a_excel: {e}")
            import traceback
            traceback.print_exc()
            return False