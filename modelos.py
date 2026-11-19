from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, ServicioNoDisponibleError, ReservaError
from logger import RegistroEventos

# 1. Clase abstracta general del sistema
class EntidadSistema(ABC):
    def __init__(self, id_entidad: str):
        if not id_entidad or not id_entidad.strip():
            raise DatoInvalidoError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass


# 2. Clase Cliente con encapsulación y validaciones estrictas
class Cliente(EntidadSistema):
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise DatoInvalidoError(f"Teléfono inválido (solo dígitos, mín. 7): '{valor}'.")
        self._telefono = valor

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


# 3. Clase abstracta Servicio y 3 servicios especializados
class Servicio(EntidadSistema, ABC):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @abstractmethod
    def validar_parametros(self, duracion_horas: int):
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: int) -> float:
        pass

    # Método sobrecargado mediante parámetros opcionales (impuestos, descuentos, recargo)
    def calcular_costo_total(self, duracion_horas: int, descuento_pct: float = 0.0, incluir_iva: bool = True) -> float:
        if descuento_pct < 0 or descuento_pct > 50:
            raise DatoInvalidoError("El porcentaje de descuento debe estar entre 0% y 50%.")
        subtotal = self.calcular_costo_base(duracion_horas)
        monto_descuento = subtotal * (descuento_pct / 100.0)
        subtotal_desc = subtotal - monto_descuento
        iva = subtotal_desc * 0.19 if incluir_iva else 0.0
        return round(subtotal_desc + iva, 2)

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.describir_servicio()} ({estado}) - Base: ${self.tarifa_base:,.2f}/h"


class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion_horas: int):
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatoInvalidoError("Las salas se reservan entre 1 y 12 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros(duracion_horas)
        return self.tarifa_base * duracion_horas

    def describir_servicio(self) -> str:
        return f"Sala '{self.nombre}' [Capacidad: {self.capacidad} personas]"


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, categoria: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not categoria or not categoria.strip():
            raise DatoInvalidoError("La categoría del equipo es obligatoria.")
        self.categoria = categoria.strip()

    def validar_parametros(self, duracion_horas: int):
        if duracion_horas < 2:
            raise DatoInvalidoError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros(duracion_horas)
        seguro_equipo = 15000.0
        return (self.tarifa_base * duracion_horas) + seguro_equipo

    def describir_servicio(self) -> str:
        return f"Equipo '{self.nombre}' [Categoría: {self.categoria}]"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not especialidad.strip():
            raise DatoInvalidoError("La especialidad de la asesoría es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int):
        if duracion_horas < 1 or duracion_horas > 8:
            raise DatoInvalidoError("Las asesorías duran entre 1 y 8 horas.")

    def calcular_costo_base(self, duracion_horas: int) -> float:
        self.validar_parametros(duracion_horas)
        return self.tarifa_base * duracion_horas

    def describir_servicio(self) -> str:
        return f"Asesoría '{self.nombre}' [Área: {self.especialidad}]"


# 4. Clase Reserva que integra Cliente, Servicio, duración y estado
class Reserva(EntidadSistema):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int, descuento_pct: float = 0.0, incluir_iva: bool = True):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ReservaError("Se requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Se requiere un objeto Servicio válido.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.descuento_pct = descuento_pct
        self.incluir_iva = incluir_iva
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_y_confirmar(self):
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible actualmente.")
            self.costo_total = self.servicio.calcular_costo_total(
                self.duracion_horas, self.descuento_pct, self.incluir_iva
            )
        except Exception as err:
            self.estado = "RECHAZADA"
            # Encadenamiento de excepciones (raise ... from err)
            raise ReservaError(f"No se pudo procesar la reserva {self.id}.") from err
        else:
            self.estado = "CONFIRMADA"
            RegistroEventos.registrar("INFO", f"Reserva {self.id} confirmada para {self.cliente.nombre} - Total: ${self.costo_total:,.2f}")
        finally:
            RegistroEventos.registrar("AUDIT", f"Intento de procesamiento finalizado para reserva {self.id} (Estado: {self.estado})")

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise ReservaError(f"La reserva {self.id} ya se encuentra cancelada.")
        if self.estado == "RECHAZADA":
            raise ReservaError(f"No se puede cancelar una reserva rechazada ({self.id}).")
        self.estado = "CANCELADA"
        RegistroEventos.registrar("INFO", f"Reserva {self.id} cancelada por solicitud del cliente {self.cliente.nombre}.")

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self.id}] | Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} ({self.duracion_horas}h) | Total: ${self.costo_total:,.2f}")
