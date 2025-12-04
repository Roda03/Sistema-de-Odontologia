import os
import json

CONFIG_FILE = "config.json"

def cargar_configuracion():
    """Carga la configuración desde el archivo JSON"""
    configuracion = {"ruta_onedrive": ""}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                configuracion = json.load(f)
        except:
            pass
    return configuracion

def guardar_configuracion(configuracion):
    """Guarda la configuración en el archivo JSON"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(configuracion, f, indent=4)
        return True
    except:
        return False

def obtener_ruta_onedrive():
    """Obtiene la ruta de OneDrive desde la configuración"""
    config = cargar_configuracion()
    return config.get("ruta_onedrive", "")