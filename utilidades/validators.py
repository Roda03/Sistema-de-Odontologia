from datetime import datetime

def validar_fecha(fecha_str):
    """Valida el formato DD/MM/AAAA"""
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_hora(hora_str):
    """Valida el formato HH:MM"""
    try:
        if not hora_str:
            return True
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False