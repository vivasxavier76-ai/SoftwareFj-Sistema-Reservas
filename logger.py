from datetime import datetime

class RegistroEventos:
    ARCHIVO_LOG = "sistema_eventos.log"

    @classmethod
    def registrar(cls, nivel: str, mensaje: str, detalle_error: str = ""):
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}"
        if detalle_error:
            linea += f" | Detalle: {detalle_error}"
        with open(cls.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
