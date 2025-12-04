import requests

def hay_internet():
    """Verifica si hay conexión a Internet"""
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False