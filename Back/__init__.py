from .Panel_Admin_Back import *
from .Menu_de_mesas_Back import *

# Funciones relacionadas con resúmenes y reportes
__all_reportes__ = [
    "obtener_resumen_por_fecha",    # Busca archivos JSON de registro por fecha/mozo
]

# Funciones relacionadas con la base de datos
__all_db__ = [
    "crear_tablas",                 # Crea las tablas necesarias en la DB
]

# Funciones relacionadas con empleados/mozos
__all_empleados__ = [
    "Generar_Codigo",              # Genera código de identificación para mozos
    "Alta_Mozo",                   # Registra un nuevo mozo
    "Mostrar_Mozos",              # Muestra lista de mozos (con paginación opcional)
    "Editar_Mozo",                # Edita información de un mozo
    "Eliminar_empleados",         # Elimina un mozo del sistema
]

# Funciones relacionadas con el menú
__all_menu__ = [
    "Cargar_Producto",            # Añade nuevo producto al menú
    "Modificar_Menu",             # Modifica un producto existente
    "Mostrar_Menu",               # Muestra productos del menú (con paginación)
    "Mostrar_menu_json",          # Muestra el menú en formato JSON
    "Eliminar_Producto",          # Elimina un producto del menú
    "Recargar_menu",              # Actualiza el archivo JSON del menú
    "obtener_menu_en_json",       # Obtiene el contenido del menú en JSON
    "obtener_cubiertos_json",     # Obtiene el precio de los cubiertos
]

# Funciones relacionadas con mesas
__all_mesas__ = [
    "ver_mesas",                # Devuelve lista de mesas y sus valores
    "crea_mesas_tmp",          # Crea mesas temporales
    "creas_mesas",             # Crea mesas con valores por defecto
    "guardar_mesa",            # Edita una mesa específica
    "editar_mesa",             # Obtiene datos de una mesa específica
    "abrir_mesa",              # Abre una mesa y la marca como no disponible
    "cerrar_mesa",             # Cierra una mesa y la marca como disponible
    "comanda_preview",         # Genera vista previa de comanda
    "imprir",                  # Imprime comanda
    "cantidad_de_mesas",       # Cuenta total de mesas
    "crear_comanda",           # Crea una comanda con formato específico
    "verifica_directorio",     # Verifica si existe un directorio
    "dividir_cuenta",          # Divide la cuenta entre cantidad especificada
]

# Funciones relacionadas con sub-mesas
__all_submesas__ = [
    "crear_sub_mesa",          # Crea una nueva sub-mesa
    "editar_sub_mesa",         # Edita una sub-mesa existente
    "cerrar_sub_mesa",         # Cierra una sub-mesa
    "crear_comanda_sub_mesa",  # Crea comanda para sub-mesa
]

__all__ = __all_empleados__ + __all_menu__ + __all_mesas__ + __all_submesas__ + __all_reportes__ + __all_db__
