# Colores comunes
COLOR_PRIMARIO = "#8B4513"
COLOR_SECUNDARIO = "#CD853F"
COLOR_ERROR = "#8B0000"
COLOR_FONDO = "#FDF5E6"
COLOR_FONDO_VENTANA = "#FFF8DC"
COLOR_TEXTO = "#2F1810"
COLOR_TEXTO_CLARO = "#FFF8DC"
COLOR_TEXTO_HOVER = "#A0522D"
COLOR_TEXTO_HOVER_SECUNDARIO = "#8B4513"
COLOR_TEXTO_HOVER_ERROR = "#800000"
COLOR_BORDES = "#DEB887"
COLOR_FONDO_TABLA = "#FFF8DC"
COLOR_HEADER_TABLA = "#8B4513"
COLOR_ITEM_SELECCIONADO = "#FFE4C4"
COLOR_BOTON_CARGAR = "#8B4513"
COLOR_BOTON_AGREGAR = "#85AC41"
COLOR_BOTON_EXPORTAR = "#8B4513"
COLOR_BOTON_GUARDAR = "#2E8B57"

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
        background-color: {COLOR_SECUNDARIO};
        color: white;
        padding: 5px 15px;
        border: none;
        border-radius: 3px;
        font-size: 14px;
        min-width: 100px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_PRIMARIO};
    }}
"""

Estilo_Tabla = f"""
    QTableWidget {{
        background-color: {COLOR_FONDO_TABLA}; 
        border: 2px solid {COLOR_BORDES};
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        gridline-color: {COLOR_BORDES};
    }}
    QHeaderView::section {{
        background-color: {COLOR_HEADER_TABLA}; 
        color: {COLOR_TEXTO_CLARO};
        padding: 12px;
        border: none;
        font-weight: bold;
        font-size: 14px;
    }}
    QTableWidget QTableCornerButton::section {{
        background-color: {COLOR_HEADER_TABLA};
        border: none;
    }}
    QTableWidget::item:selected {{
        background-color: {COLOR_ITEM_SELECCIONADO};
        color: {COLOR_TEXTO};
    }}
"""

Botones_Navegacion = f"""
    QPushButton {{
        background-color: {COLOR_BOTON_CARGAR};
        color: {COLOR_TEXTO_CLARO};
        padding: 8px 20px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        min-width: 120px;
        font-family: 'Playfair Display', serif;
    }}
    QPushButton:hover {{
        background-color: {COLOR_TEXTO_HOVER_SECUNDARIO};
    }}
"""

# MARK: load_items
Boton_Editar = f"""
    QPushButton {{
        background-color: {COLOR_SECUNDARIO};
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_PRIMARIO};
    }}
"""

Boton_Eliminar = f"""
    QPushButton {{
        background-color: {COLOR_ERROR};
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_TEXTO_HOVER_ERROR};
    }}
"""

# MARK: edit_item
Ventana_Editar = f"""
    QDialog {{
        background-color: {COLOR_FONDO_VENTANA};
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
        border: 2px solid {COLOR_BOTON_AGREGAR};
        border-radius: 8px;
        background-color: white;
        color: #333;
    }}
    QLineEdit:focus {{
        border-color: {COLOR_TEXTO_HOVER};
    }}
    QPushButton {{
        font-size: 16px;
        font-weight: bold;
        padding: 12px 24px;
        background-color: {COLOR_BOTON_AGREGAR};
        color: white;
        border: none;
        border-radius: 8px;
        margin-top: 20px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_TEXTO_HOVER};
    }}
    QPushButton:pressed {{
        background-color: #3d8b40;
    }}
"""