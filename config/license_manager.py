import os
import hashlib
import json
import platform
import uuid
from datetime import datetime, timedelta
import ctypes

APP_NAME = "Cache"
LICENSE_FILE = "Cache.lic"

# Carpeta oculta para guardar first_run
if platform.system() == "Windows":
    PROGRAMDATA = os.getenv('PROGRAMDATA')
    HIDDEN_DIR = os.path.join(PROGRAMDATA, f".{APP_NAME}")
else:
    HIDDEN_DIR = os.path.join(os.path.expanduser("~"), f".{APP_NAME}")

FIRST_RUN_FILE = os.path.join(HIDDEN_DIR, ".first_run.dat")
LICENSE_PATH = os.path.join(HIDDEN_DIR, LICENSE_FILE)

def generar_id_instalacion():
    """Genera un ID único de instalación"""
    try:
        sistema_info = {
            "sistema": platform.system(),
            "maquina": platform.machine(),
            "usuario": os.getlogin()
        }
        info_str = json.dumps(sistema_info, sort_keys=True)
        return hashlib.sha256(info_str.encode()).hexdigest()[:20].upper()
    except:
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:20].upper()

def es_primera_ejecucion():
    """Determina si es la primera ejecución del programa"""
    return not os.path.exists(FIRST_RUN_FILE)

def registrar_primera_ejecucion(fecha):
    """Guarda la fecha de la primera ejecución en un archivo oculto"""
    os.makedirs(HIDDEN_DIR, exist_ok=True)
    data = {"first_run": fecha.isoformat()}
    with open(FIRST_RUN_FILE, "w") as f:
        json.dump(data, f)
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetFileAttributesW(FIRST_RUN_FILE, 2)  # oculto

def leer_primera_ejecucion():
    """Retorna la fecha de primera ejecución si existe"""
    if os.path.exists(FIRST_RUN_FILE):
        with open(FIRST_RUN_FILE, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["first_run"])
    return None

def iniciar_licencia_prueba():
    """Crea una licencia de prueba de 30 días"""
    try:
        id_instalacion = generar_id_instalacion()
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(days=30)
        licencia_data = {
            "tipo": "trial",
            "id_instalacion": id_instalacion,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "producto": "Sistema Odontológico",
            "version": "1.0"
        }
        os.makedirs(HIDDEN_DIR, exist_ok=True)
        with open(LICENSE_PATH, 'w') as f:
            json.dump(licencia_data, f, indent=2)
        registrar_primera_ejecucion(fecha_inicio)
        return True, "Licencia de prueba iniciada"
    except Exception as e:
        return False, f"Error iniciando licencia de prueba: {str(e)}"

def verificar_licencia():
    """Verifica si existe una licencia válida"""
    try:
        if os.path.exists(LICENSE_PATH):
            with open(LICENSE_PATH, 'r') as f:
                licencia_data = json.load(f)

            # Verificación básica
            if not all(key in licencia_data for key in ['tipo', 'id_instalacion']):
                return False, "Formato de licencia inválido"

            # Licencia completa
            if licencia_data['tipo'] == 'completa':
                if validar_clave_licencia(licencia_data['id_instalacion'], licencia_data['clave_activacion']):
                    return True, "Licencia activa"
                return False, "Clave de licencia inválida"

            # Licencia trial
            if licencia_data['tipo'] == 'trial':
                fecha_inicio = datetime.fromisoformat(licencia_data['fecha_inicio'])
                fecha_fin = datetime.fromisoformat(licencia_data['fecha_fin'])
                # Evitar manipulación: usar first_run si existe
                first_run = leer_primera_ejecucion()
                if first_run:
                    fecha_fin = first_run + timedelta(days=30)
                if datetime.now() <= fecha_fin:
                    dias_restantes = (fecha_fin - datetime.now()).days
                    return True, f"Licencia de prueba activa. Días restantes: {dias_restantes}"
                else:
                    return False, "Licencia de prueba expirada"

        else:
            # Si borraron el license, usar first_run si existe
            first_run = leer_primera_ejecucion()
            if first_run:
                # Crear licencia vencida automáticamente
                fecha_fin = first_run + timedelta(days=30)
                id_instalacion = generar_id_instalacion()
                licencia_data = {
                    "tipo": "trial",
                    "id_instalacion": id_instalacion,
                    "fecha_inicio": first_run.isoformat(),
                    "fecha_fin": fecha_fin.isoformat(),
                    "producto": "Sistema Odontológico",
                    "version": "1.0"
                }
                with open(LICENSE_PATH, 'w') as f:
                    json.dump(licencia_data, f)
                return False, "Licencia vencida"

            # Primera ejecución
            return iniciar_licencia_prueba()

    except Exception as e:
        return False, f"Error en la licencia: {e}"

    return False, "Licencia inválida"

def validar_clave_licencia(id_instalacion, clave_ingresada):
    """Valida la clave de licencia"""
    if len(id_instalacion) >= 12 and len(clave_ingresada) == 4:
        clave_correcta = f"{id_instalacion[2]}{id_instalacion[5]}{id_instalacion[8]}{id_instalacion[11]}"
        return clave_ingresada.upper() == clave_correcta.upper()
    return False

def activar_licencia(clave_ingresada):
    """Activa la licencia con la clave proporcionada"""
    try:
        id_instalacion = generar_id_instalacion()
        if validar_clave_licencia(id_instalacion, clave_ingresada):
            licencia_data = {
                "tipo": "completa",
                "id_instalacion": id_instalacion,
                "clave_activacion": clave_ingresada.upper(),
                "fecha_activacion": datetime.now().isoformat(),
                "producto": "Sistema Odontológico",
                "version": "1.0"
            }
            os.makedirs(HIDDEN_DIR, exist_ok=True)
            with open(LICENSE_PATH, 'w') as f:
                json.dump(licencia_data, f, indent=2)
            return True, "Licencia activada correctamente"
        else:
            return False, "Clave de activación incorrecta"
    except Exception as e:
        return False, f"Error activando licencia: {str(e)}"