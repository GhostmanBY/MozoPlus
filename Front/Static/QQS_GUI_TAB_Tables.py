# Colores comunes
AZUL_PRIMARIO = "#3182CE"          # Azul principal
AZUL_SECUNDARIO = "#4299E1"        # Azul más claro
ROJO_ERROR = "#E53E3E"             # Rojo para errores
BLANCO_FONDO = "#F7FAFC"           # Fondo principal
BLANCO_FONDO_ALT = "#EDF2F7"       # Fondo alternativo
GRIS_TEXTO = "#2D3748"             # Texto principal
BLANCO_TEXTO = "#FFFFFF"           # Texto claro
AZUL_HOVER = "#2B6CB0"             # Azul hover
AZUL_HOVER_SECUNDARIO = "#2C5282"  # Azul hover secundario
ROJO_HOVER = "#C53030"             # Rojo hover
GRIS_BORDES = "#CBD5E0"            # Bordes
BLANCO_TABLA = "#FFFFFF"           # Fondo tabla
AZUL_HEADER = "#3182CE"            # Header tabla
AZUL_SELECCION = "#BEE3F8"         # Item seleccionado
VERDE_BOTON = "#38A169"            # Botón verde
VERDE_HOVER = "#2F855A"            # Verde hover
VERDE_PRESSED = "#276749"          # Verde muy oscuro

# MARK: setup_tab
Entry_input = """
    QLineEdit {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
        font-size: 14px;
    }
"""

Boton_Agregar = f"""
    QPushButton {{
        background-color: {AZUL_SECUNDARIO};
        color: white;
        padding: 5px 15px;
        border: none;
        border-radius: 3px;
        font-size: 14px;
        min-width: 100px;
    }}
    QPushButton:hover {{
        background-color: {AZUL_PRIMARIO};
    }}
"""

Estilo_Tabla = f"""
    QTableWidget {{
        background-color: {BLANCO_TABLA}; 
        border: 2px solid {GRIS_BORDES};
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        gridline-color: {GRIS_BORDES};
    }}
    QHeaderView::section {{
        background-color: {AZUL_HEADER}; 
        color: {BLANCO_TEXTO};
        padding: 12px;
        border: none;
        font-weight: bold;
        font-size: 14px;
    }}
    QTableWidget QTableCornerButton::section {{
        background-color: {AZUL_HEADER};
        border: none;
    }}
    QTableWidget::item:selected {{
        background-color: {AZUL_SELECCION};
        color: {GRIS_TEXTO};
    }}
"""

Botones_Navegacion = f"""
    QPushButton {{
        background-color: {VERDE_BOTON};
        color: {BLANCO_TEXTO};
        padding: 8px 20px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        min-width: 120px;
        font-family: 'Playfair Display', serif;
    }}
    QPushButton:hover {{
        background-color: {AZUL_HOVER_SECUNDARIO};
    }}
"""

# MARK: load_items
Boton_Editar = f"""
    QPushButton {{
        background-color: {AZUL_SECUNDARIO};
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {AZUL_PRIMARIO};
    }}
"""

Boton_Eliminar = f"""
    QPushButton {{
        background-color: {ROJO_ERROR};
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {ROJO_HOVER};
    }}
"""

# MARK: edit_item
Ventana_Editar = f"""
    QDialog {{
        background-color: {BLANCO_FONDO_ALT};
        border-radius: 15px;
        border: 1px solid #dcdcdc;
    }}
    QLabel {{
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }}
    QLineEdit {{
        font-size: 16px;
        padding: 12px;
        border: 2px solid {VERDE_BOTON};
        border-radius: 8px;
        background-color: white;
        color: #333;
    }}
    QLineEdit:focus {{
        border-color: {AZUL_HOVER};
    }}
    QPushButton {{
        font-size: 16px;
        font-weight: bold;
        padding: 12px 24px;
        background-color: {VERDE_BOTON};
        color: white;
        border: none;
        border-radius: 8px;
        margin-top: 20px;
    }}
    QPushButton:hover {{
        background-color: {AZUL_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {VERDE_PRESSED};
    }}
"""