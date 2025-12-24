import sqlite3
import os
import sys
import shutil
from datetime import datetime
import glob

def encontrar_base_datos():
    """Busca la base de datos pacientes.db en diferentes ubicaciones"""
    
    posibles_rutas = [
        # 1. En la carpeta actual
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.db"),
        
        # 2. En la carpeta donde está el ejecutable (si está compilado)
        os.path.join(os.path.dirname(sys.executable), "pacientes.db") if getattr(sys, 'frozen', False) else "",
        
        # 3. En el directorio padre
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pacientes.db"),
        
        # 4. Buscar en toda la carpeta del proyecto
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.db"),
        
        # 5. Buscar en el directorio del usuario
        os.path.join(os.path.expanduser("~"), "pacientes.db"),
    ]
    
    # Filtrar rutas vacías
    posibles_rutas = [r for r in posibles_rutas if r]
    
    print("🔍 Buscando base de datos pacientes.db...")
    
    for ruta in posibles_rutas:
        # Si es un patrón con wildcard
        if '*' in ruta:
            archivos = glob.glob(ruta)
            for archivo in archivos:
                if 'pacientes' in os.path.basename(archivo).lower():
                    print(f"✅ Encontrado: {archivo}")
                    return archivo
        # Si es una ruta específica
        elif os.path.exists(ruta):
            print(f"✅ Encontrado: {ruta}")
            return ruta
    
    # Si no se encontró, listar archivos .db en la carpeta actual
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    archivos_db = glob.glob(os.path.join(carpeta_actual, "*.db"))
    
    if archivos_db:
        print("\n📁 Archivos .db encontrados en la carpeta actual:")
        for archivo in archivos_db:
            print(f"  - {os.path.basename(archivo)}")
        
        # Preguntar cuál usar
        print("\n⚠️  No se encontró 'pacientes.db' exactamente.")
        respuesta = input("¿Desea usar uno de los archivos anteriores? (s/n): ").strip().lower()
        
        if respuesta == 's':
            if len(archivos_db) == 1:
                return archivos_db[0]
            else:
                print("\nSeleccione un archivo:")
                for i, archivo in enumerate(archivos_db, 1):
                    print(f"{i}. {os.path.basename(archivo)}")
                
                try:
                    seleccion = int(input("\nNúmero: ").strip())
                    if 1 <= seleccion <= len(archivos_db):
                        return archivos_db[seleccion - 1]
                except ValueError:
                    pass
    
    return None

def crear_base_nueva_desde_cero():
    """Crea una base de datos nueva desde cero"""
    
    carpeta = os.path.dirname(os.path.abspath(__file__))
    db_nueva = os.path.join(carpeta, "odontologia.db")
    
    print(f"\n🔨 Creando nueva base de datos desde cero...")
    print(f"📁 Ruta: {db_nueva}")
    
    # Eliminar si existe
    if os.path.exists(db_nueva):
        os.remove(db_nueva)
        print("🗑️  Base de datos anterior eliminada")
    
    try:
        conn = sqlite3.connect(db_nueva)
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.execute("""
        CREATE TABLE pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cedula TEXT UNIQUE,
            telefono TEXT,
            edad INTEGER,
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
            aspecto_clinico_general TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE consultas (
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
        
        cursor.execute("""
        CREATE TABLE odontograma (
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
        
        cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
        """)
        
        # Crear usuario admin
        import hashlib
        clave_hash = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", clave_hash))
        
        conn.commit()
        conn.close()
        
        print("\n✅ Base de datos creada exitosamente")
        print("👤 Usuario: admin")
        print("🔑 Contraseña: 1234")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def migrar_base_datos_completa(db_vieja_path):
    """Migra desde una base de datos específica"""
    
    carpeta = os.path.dirname(os.path.abspath(__file__))
    db_nueva = os.path.join(carpeta, "odontologia.db")
    
    print(f"\n🔧 Migrando desde: {db_vieja_path}")
    print(f"📁 Hacia: {db_nueva}")
    
    # Verificar que exista la base vieja
    if not os.path.exists(db_vieja_path):
        print(f"❌ No existe: {db_vieja_path}")
        return False
    
    try:
        # 1. Hacer backup
        backup_name = f"backup_{os.path.basename(db_vieja_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = os.path.join(carpeta, backup_name)
        shutil.copy2(db_vieja_path, backup_path)
        print(f"💾 Backup creado: {backup_path}")
        
        # 2. Conectar a bases
        conn_vieja = sqlite3.connect(db_vieja_path)
        conn_vieja.row_factory = sqlite3.Row
        
        # 3. Crear base nueva (borrar si existe)
        if os.path.exists(db_nueva):
            os.remove(db_nueva)
        
        conn_nueva = sqlite3.connect(db_nueva)
        cursor_nueva = conn_nueva.cursor()
        
        # 4. Crear tablas (igual que la función anterior)
        cursor_nueva.execute("""
        CREATE TABLE pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cedula TEXT UNIQUE,
            telefono TEXT,
            edad INTEGER,
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
            aspecto_clinico_general TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor_nueva.execute("""
        CREATE TABLE consultas (
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
        
        cursor_nueva.execute("""
        CREATE TABLE odontograma (
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
        
        cursor_nueva.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
        """)
        
        # 5. Migrar usuarios
        try:
            cursor_vieja = conn_vieja.cursor()
            cursor_vieja.execute("SELECT * FROM usuarios")
            usuarios = cursor_vieja.fetchall()
            
            if usuarios:
                for usuario in usuarios:
                    try:
                        cursor_nueva.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", 
                                          (usuario[1], usuario[2]))
                    except:
                        continue
                print(f"✅ {len(usuarios)} usuarios migrados")
            else:
                # Crear usuario por defecto
                import hashlib
                clave_hash = hashlib.sha256("1234".encode()).hexdigest()
                cursor_nueva.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", clave_hash))
                print("✅ Usuario admin creado (1234)")
        except:
            # Crear usuario por defecto si hay error
            import hashlib
            clave_hash = hashlib.sha256("1234".encode()).hexdigest()
            cursor_nueva.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", clave_hash))
            print("✅ Usuario admin creado (1234)")
        
        # 6. Migrar pacientes
        print("\n👤 Migrando pacientes...")
        
        # Obtener estructura de la tabla vieja
        cursor_vieja.execute("PRAGMA table_info(pacientes)")
        columnas_info = cursor_vieja.fetchall()
        nombres_columnas = [col[1] for col in columnas_info]
        
        # Obtener datos
        cursor_vieja.execute("SELECT * FROM pacientes")
        pacientes = cursor_vieja.fetchall()
        
        pacientes_migrados = 0
        
        for paciente in pacientes:
            try:
                # Convertir a diccionario para acceso por nombre
                paciente_dict = {}
                for i, col_name in enumerate(nombres_columnas):
                    if i < len(paciente):
                        paciente_dict[col_name] = paciente[i]
                
                # Extraer datos
                nombre = paciente_dict.get('nombre', '')
                apellido = paciente_dict.get('apellido', '')
                
                if not nombre or not apellido:
                    continue
                
                # Insertar en nueva tabla
                cursor_nueva.execute("""
                INSERT INTO pacientes (
                    nombre, apellido, cedula, telefono, edad,
                    medicamento_actual, alergias, embarazada, hemorragias,
                    problemas_tratamiento, enfermedad_cardiovascular, diabetes,
                    hepatitis, artritis, tuberculosis, enfermedades_venereas,
                    hipertension, enfermedades_sanguineas, otras_enfermedades,
                    especificar_otras, tejidos_blandos_intraorales,
                    tejidos_blandos_extraorales, ganglios, aspecto_clinico_general
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nombre, apellido,
                    paciente_dict.get('cedula', ''),
                    paciente_dict.get('telefono', ''),
                    paciente_dict.get('edad', 0),
                    paciente_dict.get('medicamento_actual', ''),
                    paciente_dict.get('alergias', ''),
                    paciente_dict.get('embarazada', 0),
                    paciente_dict.get('hemorragias', 0),
                    paciente_dict.get('problemas_tratamiento', 0),
                    paciente_dict.get('enfermedad_cardiovascular', 0),
                    paciente_dict.get('diabetes', 0),
                    paciente_dict.get('hepatitis', 0),
                    paciente_dict.get('artritis', 0),
                    paciente_dict.get('tuberculosis', 0),
                    paciente_dict.get('enfermedades_venereas', 0),
                    paciente_dict.get('hipertension', 0),
                    paciente_dict.get('enfermedades_sanguineas', 0),
                    paciente_dict.get('otras_enfermedades', 0),
                    paciente_dict.get('especificar_otras', ''),
                    paciente_dict.get('tejidos_blandos_intraorales', ''),
                    paciente_dict.get('tejidos_blandos_extraorales', ''),
                    paciente_dict.get('ganglios', ''),
                    paciente_dict.get('aspecto_clinico_general', '')
                ))
                
                paciente_id_nuevo = cursor_nueva.lastrowid
                pacientes_migrados += 1
                
                # 7. Crear consulta para este paciente
                fecha_cita = paciente_dict.get('fecha_cita', '')
                hora_cita = paciente_dict.get('hora_cita', '09:00')
                precio = paciente_dict.get('precio_consulta', 0.0)
                observaciones = paciente_dict.get('obs', '')
                
                # Procesar fecha
                fecha_nueva = ''
                if fecha_cita:
                    try:
                        if '/' in fecha_cita:
                            partes = fecha_cita.split('/')
                            if len(partes) == 3:
                                dia, mes, año = partes
                                if len(año) == 2:
                                    año = '20' + año if int(año) < 50 else '19' + año
                                fecha_nueva = f"{año}-{mes.zfill(2)}-{dia.zfill(2)}"
                        else:
                            fecha_nueva = fecha_cita
                    except:
                        fecha_nueva = datetime.now().strftime('%Y-%m-%d')
                else:
                    fecha_nueva = datetime.now().strftime('%Y-%m-%d')
                
                # Insertar consulta
                cursor_nueva.execute("""
                INSERT INTO consultas (paciente_id, fecha, hora, precio, motivo, observaciones)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    paciente_id_nuevo, 
                    fecha_nueva, 
                    hora_cita if hora_cita else '09:00',
                    float(precio) if precio else 0.0,
                    "Consulta inicial migrada",
                    observaciones
                ))
                
                consulta_id = cursor_nueva.lastrowid
                
                # 8. Migrar odontograma si existe
                try:
                    # Obtener ID viejo del paciente
                    id_viejo = paciente_dict.get('id', paciente[0] if paciente else 0)
                    
                    cursor_vieja.execute("SELECT * FROM odontograma WHERE paciente_id = ?", (id_viejo,))
                    odontogramas = cursor_vieja.fetchall()
                    
                    for odonto in odontogramas:
                        try:
                            cursor_nueva.execute("""
                            INSERT INTO odontograma (consulta_id, diente_numero, cara, estado, procedimiento, observaciones)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                consulta_id,
                                odonto[2] if len(odonto) > 2 else 0,  # diente_numero
                                odonto[3] if len(odonto) > 3 else '',  # cara
                                odonto[4] if len(odonto) > 4 else 'sano',  # estado
                                odonto[5] if len(odonto) > 5 else '',  # procedimiento
                                odonto[6] if len(odonto) > 6 else ''   # observaciones
                            ))
                        except:
                            continue
                except:
                    pass  # No hay odontograma o error
                
            except Exception as e:
                print(f"⚠️ Error en paciente {nombre if 'nombre' in locals() else 'desconocido'}: {e}")
                continue
        
        conn_nueva.commit()
        
        # 9. Resumen
        print(f"\n📊 RESULTADO DE MIGRACIÓN:")
        print(f"👤 Pacientes migrados: {pacientes_migrados}")
        
        cursor_nueva.execute("SELECT COUNT(*) FROM consultas")
        consultas = cursor_nueva.fetchone()[0]
        print(f"📅 Consultas creadas: {consultas}")
        
        cursor_nueva.execute("SELECT COUNT(*) FROM odontograma")
        odontos = cursor_nueva.fetchone()[0]
        print(f"🦷 Registros de odontograma: {odontos}")
        
        # 10. Cerrar conexiones
        conn_vieja.close()
        conn_nueva.close()
        
        print(f"\n🎉 ¡Migración completada!")
        print(f"📁 Nueva base de datos: {db_nueva}")
        print(f"💾 Backup original: {backup_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR en migración: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    
    print("="*60)
    print("🚀 MIGRADOR DE BASE DE DATOS - SISTEMA ODONTOLÓGICO")
    print("="*60)
    print("\nEste script realizará:")
    print("1. Buscará tu base de datos actual")
    print("2. Creará una nueva base de datos 'odontologia.db'")
    print("3. Migrará todos los datos a la nueva estructura")
    print("4. Hará un backup automático")
    print("="*60)
    
    # Opciones
    print("\n¿Qué deseas hacer?")
    print("1. Buscar y migrar desde base de datos existente")
    print("2. Crear nueva base de datos vacía (sin migrar)")
    print("3. Cancelar")
    
    opcion = input("\nSeleccione opción (1-3): ").strip()
    
    if opcion == '1':
        # Buscar base de datos
        db_vieja = encontrar_base_datos()
        
        if not db_vieja:
            print("\n❌ No se encontró ninguna base de datos para migrar.")
            respuesta = input("¿Desea crear una nueva base de datos vacía? (s/n): ").strip().lower()
            
            if respuesta == 's':
                crear_base_nueva_desde_cero()
            else:
                print("❌ Operación cancelada")
            return
        
        print(f"\n✅ Base de datos encontrada: {db_vieja}")
        
        # Confirmar migración
        confirmar = input("\n¿Continuar con la migración? (s/n): ").strip().lower()
        
        if confirmar == 's':
            migrar_base_datos_completa(db_vieja)
        else:
            print("❌ Migración cancelada")
    
    elif opcion == '2':
        crear_base_nueva_desde_cero()
    
    elif opcion == '3':
        print("❌ Operación cancelada")
    
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()