class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ."""
    pass

class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro o dato personal no cumple la validación."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio está inactivo o sin cupo."""
    pass

class ReservaError(ErrorSistemaFJ):
    """Se lanza ante errores en el procesamiento, confirmación o cancelación de reservas."""
    pass
