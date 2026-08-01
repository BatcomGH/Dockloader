from pathlib import Path
import os

rutaActual = Path(__file__).resolve()
rutaCookies = rutaActual.parent.parent.parent / "cookies.txt"

def isCookiesEmpty():
    if not os.path.exists(rutaCookies):
        with open(rutaCookies, 'w') as f:
            f.write('')
        print("Archivo cookies.txt creado. Sin cookies. Añadir cookies para una mayor compatibilidad con descargas de videos privados o restringidos.")
        return True
    
    if os.path.exists(rutaCookies):
        if os.path.getsize(rutaCookies) == 0:
            print("Archivo cookies.txt vacío. Añadir cookies para una mayor compatibilidad con descargas de videos privados o restringidos.")
            return True
        
    return False