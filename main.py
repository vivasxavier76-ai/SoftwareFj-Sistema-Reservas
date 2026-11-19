from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada, Reserva
from excepciones import ErrorSistemaFJ
from logger import RegistroEventos

class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, id_c, nombre, correo, telefono):
        try:
            cliente = Cliente(id_c, nombre, correo, telefono)
        except ErrorSistemaFJ as e:
            print(f"[ERROR CLIENTE] {e}")
            RegistroEventos.registrar("ERROR", f"Fallo al registrar cliente '{nombre}'", str(e))
        else:
            self.clientes.append(cliente)
            print(f"[OK] {cliente.obtener_resumen()}")
            RegistroEventos.registrar("INFO", f"Cliente registrado: {cliente.id}")
            return cliente
        finally:
            pass

    def registrar_servicio(self, servicio_obj):
        self.servicios.append(servicio_obj)
        print(f"[OK] Servicio agregado -> {servicio_obj.obtener_resumen()}")
        RegistroEventos.registrar("INFO", f"Servicio registrado: {servicio_obj.id}")

    def crear_reserva(self, id_r, cliente, servicio, horas, descuento=0.0, iva=True):
        try:
            reserva = Reserva(id_r, cliente, servicio, horas, descuento, iva)
            reserva.procesar_y_confirmar()
        except ErrorSistemaFJ as e:
            causa = e.__cause__ if e.__cause__ else e
            print(f"[ERROR RESERVA] {e} -> Causa: {causa}")
            RegistroEventos.registrar("ERROR", f"Fallo en reserva {id_r}", f"{e} | Causa: {causa}")
        else:
            self.reservas.append(reserva)
            print(f"[OK] {reserva.obtener_resumen()}")
            return reserva


def ejecutar_simulacion():
    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    sistema = SistemaSoftwareFJ()

    # Operación 1: Registro válido de cliente 1
    c1 = sistema.registrar_cliente("C01", "Laura Gómez", "laura.gomez@correo.com", "3104567890")

    # Operación 2: Registro válido de cliente 2
    c2 = sistema.registrar_cliente("C02", "Carlos Pérez", "carlos.perez@empresa.co", "3209876543")

    # Operación 3: Registro inválido de cliente (correo sin @ y teléfono corto)
    sistema.registrar_cliente("C03", "Ana", "correo_invalido", "123")

    # Operación 4: Registro inválido de cliente (nombre muy corto)
    sistema.registrar_cliente("C04", "Jo", "jo@correo.com", "3001112233")

    # Operación 5: Creación válida de 3 tipos de servicios
    s1 = ReservaSala("S01", "Sala Ejecutiva Norte", 80000, capacidad=12, disponible=True)
    s2 = AlquilerEquipo("S02", "Servidor Portátil Xeon", 45000, categoria="Cómputo", disponible=True)
    s3 = AsesoriaEspecializada("S03", "Arquitectura Cloud", 120000, especialidad="Nube y DevOps", disponible=False)
    sistema.registrar_servicio(s1)
    sistema.registrar_servicio(s2)
    sistema.registrar_servicio(s3)

    # Operación 6: Creación incorrecta de servicio (tarifa negativa)
    try:
        ServicioInvalido = ReservaSala("S04", "Sala Sur", -50000, capacidad=5)
    except ErrorSistemaFJ as e:
        print(f"[ERROR SERVICIO] {e}")
        RegistroEventos.registrar("ERROR", "Intento de crear servicio con tarifa negativa", str(e))

    # Operación 7: Reserva exitosa de Sala (con IVA estándar)
    r1 = sistema.crear_reserva("R01", c1, s1, horas=4)

    # Operación 8: Reserva exitosa de Equipo (sobrecarga con 10% descuento y sin IVA)
    r2 = sistema.crear_reserva("R02", c2, s2, horas=5, descuento=10.0, iva=False)

    # Operación 9: Reserva fallida por servicio no disponible (encadenamiento de excepciones)
    sistema.crear_reserva("R03", c1, s3, horas=2)

    # Operación 10: Reserva fallida por duración inválida (alquiler de equipo menor a 2 horas)
    sistema.crear_reserva("R04", c2, s2, horas=1)

    # Operación 11: Cancelación exitosa de reserva confirmada
    if r1:
        try:
            r1.cancelar()
            print(f"[OK] {r1.obtener_resumen()}")
        except ErrorSistemaFJ as e:
            print(f"[ERROR CANCELACIÓN] {e}")

    # Operación 12: Intento fallido de volver a cancelar una reserva ya cancelada
    if r1:
        try:
            r1.cancelar()
        except ErrorSistemaFJ as e:
            print(f"[ERROR CANCELACIÓN] {e}")
            RegistroEventos.registrar("ERROR", "Doble cancelación bloqueada", str(e))

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revisa el archivo 'sistema_eventos.log' para ver la auditoría completa.")

if __name__ == "__main__":
    ejecutar_simulacion()
