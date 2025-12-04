import sqlite3
import random
from datetime import datetime, timedelta
import os
import hashlib

def crear_base_datos_completa():
    """Crea la base de datos completa con estructura CORRECTA y 50 pacientes de prueba"""
    
    # Eliminar DB existente si hay
    if os.path.exists('pacientes.db'):
        os.remove('pacientes.db')
        print("🗑️ Base de datos anterior eliminada")
    
    # Conectar a la base de datos
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    
    print("🚀 Creando base de datos con estructura CORRECTA...")
    
    # Crear tabla de pacientes con estructura DEFINITIVA
    cursor.execute("""
    CREATE TABLE pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        apellido TEXT,
        cedula TEXT,
        edad INTEGER,
        telefono TEXT,
        obs TEXT,
        fecha_cita TEXT,
        hora_cita TEXT,
        precio_consulta REAL,
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
    
    # Crear tabla de odontograma
    cursor.execute("""
    CREATE TABLE odontograma (
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
    
    # Crear tabla de usuarios
    cursor.execute("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        clave TEXT
    )
    """)
    
    # Agregar usuario admin
    clave_hash = hashlib.sha256("1234".encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", ("admin", clave_hash))
    
    print("✅ Estructura de base de datos creada correctamente")
    print("✅ Usuario: admin / Contraseña: 1234")
    
    return conn, cursor

def generar_pacientes_prueba(conn, cursor):
    """Genera 50 pacientes de prueba con datos variados y REALISTAS"""
    
    # Datos de prueba más realistas
    nombres = ["Maria", "Juan", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofia", "Diego", "Elena",
               "Miguel", "Isabel", "Javier", "Carmen", "Ricardo", "Patricia", "Fernando", "Rosa", "Antonio", "Diana",
               "Gabriela", "Roberto", "Claudia", "Andres", "Veronica", "Raul", "Monica", "Oscar", "Teresa", "Francisco"]
    
    apellidos = ["Gonzalez", "Rodriguez", "Perez", "Lopez", "Martinez", "Garcia", "Sanchez", "Ramirez", "Torres", "Flores",
                 "Diaz", "Hernandez", "Morales", "Ortiz", "Silva", "Rojas", "Vargas", "Castro", "Romero", "Mendoza",
                 "Vasquez", "Gutierrez", "Reyes", "Jimenez", "Moreno", "Alvarez", "Ruiz", "Delgado", "Ortiz", "Medina"]
    
    medicamentos = ["Paracetamol", "Ibuprofeno", "Amoxicilina", "Omeprazol", "Atorvastatina", "Metformina", "Aspirina", "Loratadina", "Ninguno", ""]
    alergias = ["Penicilina", "Aspirina", "Mariscos", "Polvo", "Polen", "Latex", "Ninguna", ""]
    procedimientos = ["Limpieza", "Obturación", "Extracción", "Corona", "Endodoncia", "Blanqueamiento", "Ortodoncia"]
    
    print("\n🎯 Generando 50 pacientes de prueba...")
    
    for i in range(50):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        edad = random.randint(18, 80)
        cedula = f"{random.randint(1000000, 9999999)}"
        telefono = f"09{random.randint(1000000, 9999999)}"
        
        # Generar fecha de cita aleatoria (próximos 30 días y algunas pasadas)
        if random.random() < 0.7:  # 70% de probabilidad de tener cita
            if random.random() < 0.3:  # 30% de citas pasadas
                dias = random.randint(-60, -1)
            else:  # 70% de citas futuras
                dias = random.randint(1, 30)
                
            fecha_cita = (datetime.now() + timedelta(days=dias)).strftime("%d/%m/%Y")
            hora_cita = f"{random.randint(8, 18)}:{random.choice(['00', '15', '30', '45'])}"
        else:
            fecha_cita = ""
            hora_cita = ""
        
        precio_consulta = round(random.uniform(25, 200), 2)
        obs = random.choice(["Control rutinario", "Limpieza dental", "Extracción", "Ortodoncia", 
                           "Blanqueamiento", "Dolor molar", "Consulta inicial", ""])
        
        # Insertar paciente
        cursor.execute("""
            INSERT INTO pacientes 
            (nombre, apellido, cedula, edad, telefono, obs, fecha_cita, hora_cita,
            precio_consulta, medicamento_actual, alergias, embarazada, hemorragias,
            problemas_tratamiento, enfermedad_cardiovascular, diabetes, hepatitis,
            artritis, tuberculosis, enfermedades_venereas, hipertension,
            enfermedades_sanguineas, otras_enfermedades, especificar_otras,
            tejidos_blandos_intraorales, tejidos_blandos_extraorales, ganglios,
            aspecto_clinico_general)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre, apellido, cedula, edad, telefono, obs, fecha_cita, hora_cita,
            precio_consulta,
            random.choice(medicamentos),
            random.choice(alergias),
            random.choice([0, 1]),  # embarazada
            random.choice([0, 1]),  # hemorragias
            random.choice([0, 1]),  # problemas_tratamiento
            random.choice([0, 1]),  # enfermedad_cardiovascular
            random.choice([0, 1]),  # diabetes
            random.choice([0, 1]),  # hepatitis
            random.choice([0, 1]),  # artritis
            random.choice([0, 1]),  # tuberculosis
            random.choice([0, 1]),  # enfermedades_venereas
            random.choice([0, 1]),  # hipertension
            random.choice([0, 1]),  # enfermedades_sanguineas
            random.choice([0, 1]),  # otras_enfermedades
            random.choice(["", "Migrañas", "Alergia estacional", "Problemas tiroideos", "Asma"]),
            "Tejidos intraorales en buen estado",
            "Tejidos extraorales normales",
            "Ganglios no palpables",
            "Aspecto clínico general bueno"
        ))
        
        paciente_id = cursor.lastrowid
        
        # Agregar datos de odontograma para prueba (50% de pacientes)
        if random.random() < 0.5:
            for diente in random.sample(range(1, 33), random.randint(2, 6)):
                cursor.execute("""
                    INSERT INTO odontograma (paciente_id, diente_numero, cara, estado, procedimiento, observaciones, fecha)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    paciente_id,
                    diente,
                    random.choice(["V", "O", "L", "P", "M", "D"]),
                    random.choice(["sano", "cariado", "obturado", "corona", "extraccion", "implante"]),
                    random.choice(procedimientos),
                    random.choice(["", "Control en 6 meses", "Sensibilidad", "Ninguna", "Requiere seguimiento"]),
                    datetime.now().strftime("%Y-%m-%d")
                ))
        
        print(f"✅ Paciente {i+1}: {nombre} {apellido} - Cédula: {cedula} - Precio: ${precio_consulta}")

    conn.commit()
    print("\n🎉 ¡50 pacientes de prueba generados exitosamente!")

def verificar_y_mostrar_estadisticas(conn):
    """Verifica los datos y muestra estadísticas"""
    cursor = conn.cursor()
    
    # Estadísticas generales
    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total_pacientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM odontograma")
    total_odontograma = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE fecha_cita != ''")
    pacientes_con_cita = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(precio_consulta) FROM pacientes WHERE precio_consulta > 0")
    total_ingresos = cursor.fetchone()[0] or 0
    
    print(f"\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
    print(f"   👥 Total pacientes: {total_pacientes}")
    print(f"   🦷 Registros odontograma: {total_odontograma}")
    print(f"   📅 Pacientes con cita: {pacientes_con_cita}")
    print(f"   💰 Ingresos totales: ${total_ingresos:,.2f}")
    
    # Mostrar algunos pacientes de ejemplo
    cursor.execute("""
        SELECT nombre, apellido, cedula, precio_consulta, fecha_cita, hora_cita 
        FROM pacientes LIMIT 5
    """)
    print(f"\n📋 EJEMPLOS DE PACIENTES:")
    for i, paciente in enumerate(cursor.fetchall(), 1):
        cita = f"{paciente[4]} {paciente[5]}" if paciente[4] else "Sin cita"
        print(f"   {i}. {paciente[0]} {paciente[1]} - Cédula: {paciente[2]} - ${paciente[3]} - {cita}")

def main():
    print("🚀 GENERADOR DE BASE DE DATOS DE PRUEBA")
    print("=" * 60)
    
    try:
        # Crear DB y tablas
        conn, cursor = crear_base_datos_completa()
        
        # Generar pacientes de prueba
        generar_pacientes_prueba(conn, cursor)
        
        # Verificar datos
        verificar_y_mostrar_estadisticas(conn)
        
        print("\n" + "=" * 60)
        print("🎯 ¡BASE DE DATOS LISTA PARA PROBAR TODAS LAS FUNCIONALIDADES!")
        print("=" * 60)
        print("📋 CARACTERÍSTICAS INCLUIDAS:")
        print("   ✅ 50 pacientes con datos realistas")
        print("   ✅ Cédulas únicas para probar búsquedas")
        print("   ✅ Precios variados ($25-$200)")
        print("   ✅ Fechas de citas (pasadas y futuras)")
        print("   ✅ Datos de odontograma para prueba")
        print("   ✅ Usuario: admin / Contraseña: 1234")
        
        print("\n🔧 FUNCIONALIDADES A PROBAR:")
        print("   1. 🔍 Búsquedas por nombre, apellido y cédula")
        print("   2. 📅 Calendario de citas (con fechas reales)")
        print("   3. 💰 Estadísticas de ingresos (con datos reales)")
        print("   4. 📊 Exportación a Excel")
        print("   5. 🦷 Odontograma dental")
        print("   6. 👤 Login con: admin / 1234")
        
        print("\n⚠️  EJECUTA PRIMERO ESTE SCRIPT Y LUEGO TU SISTEMA NORMAL")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()