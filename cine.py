import time
from datetime import datetime


class Funcion:
    def __init__(self, codigo: str, pelicula: str, hora: str, precio: float):
        self.codigo = codigo
        self.pelicula = pelicula
        self.hora = hora
        self.precio = float(precio)


def cargar_funciones():
    """Inicializa el almacén en memoria de funciones (sin persistencia en archivos)."""
    return {}


def registrar_funcion(funciones):
    print("\nRegistrar nueva función")
    codigo = input("Código (único): ").strip()
    if not codigo:
        print("Código inválido.")
        return
    if codigo in funciones:
        print("Ya existe una función con ese código.")
        return
    pelicula = input("Película: ").strip()
    hora = input("Hora (ej. 18:30): ").strip()
    precio_s = input("Precio por entrada: ").strip()
    try:
        precio = float(precio_s)
        if precio < 0:
            raise ValueError()
    except ValueError:
        print("Precio inválido.")
        return
    func = Funcion(codigo, pelicula, hora, precio)
    funciones[codigo] = func
    print("Función registrada con éxito (memoria).")


def listar_funciones(funciones):
    start = time.time()
    print("\nFunciones disponibles:")
    if not funciones:
        print("(No hay funciones registradas)")
    else:
        print("{:8} | {:30} | {:6} | {}".format("Código", "Película", "Hora", "Precio"))
        print("-" * 68)
        for codigo, fobj in sorted(funciones.items()):
            pelicula = (fobj.pelicula[:27] + '...') if len(fobj.pelicula) > 30 else fobj.pelicula
            print(f"{codigo:8} | {pelicula:30} | {fobj.hora:6} | ${fobj.precio:.2f}")
    elapsed = time.time() - start
    if elapsed >= 2.0:
        print(f"Aviso: Listado tardó {elapsed:.2f}s (supera 2s)")


def vender_boletos(funciones, ventas):
    """Vende boletos usando estructuras en memoria. Registra la venta en la lista `ventas`."""
    print("\nVender boletos")
    codigo = input("Código de la función: ").strip()
    if codigo not in funciones:
        print("Error: función inexistente.")
        return
    cantidad_s = input("Cantidad de boletos: ").strip()
    try:
        cantidad = int(cantidad_s)
        if cantidad <= 0:
            raise ValueError()
    except ValueError:
        print("Error: cantidad inválida.")
        return
    precio_unit = funciones[codigo].precio
    total = precio_unit * cantidad
    print(f"Total a pagar: ${total:.2f}")
    confirmar = input("Confirmar venta? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Venta cancelada.")
        return
    ventas.append({
        'timestamp': datetime.now().isoformat(),
        'codigo': codigo,
        'cantidad': cantidad,
        'total': total,
    })
    print("Venta registrada (memoria).")


def resumen_ventas(ventas):
    total_boletos = 0
    total_dinero = 0.0
    if not ventas:
        print("\nNo hay ventas registradas hoy.")
        return
    for sale in ventas:
        try:
            cantidad = int(sale.get('cantidad', 0))
            total = float(sale.get('total', 0.0))
        except (ValueError, TypeError):
            continue
        total_boletos += cantidad
        total_dinero += total
    print("\nResumen de ventas del día:")
    print(f"Boletos vendidos: {total_boletos}")
    print(f"Dinero recaudado: ${total_dinero:.2f}")


def cargar_menu():
    funciones = cargar_funciones()
    ventas = []
    return funciones, ventas


def main():
    funciones, ventas = cargar_menu()
    while True:
        print("\n--- Menú principal ---")
        print("1. Registrar función")
        print("2. Listar funciones")
        print("3. Vender boletos")
        print("4. Resumen de ventas del día")
        print("5. Salir")
        opcion = input("Seleccione una opción (1-5): ").strip()
        if opcion == '1':
            registrar_funcion(funciones)
        elif opcion == '2':
            listar_funciones(funciones)
        elif opcion == '3':
            vender_boletos(funciones, ventas)
        elif opcion == '4':
            resumen_ventas(ventas)
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == '__main__':
    main()