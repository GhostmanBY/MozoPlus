###########################################
# PALETA DE COLORES BASE
###########################################

# Marrones - Colores principales
COLOR_MARRON_OSCURO = "#8B4513"    # Marrón silla
COLOR_MARRON_MEDIO = "#CD853F"      # Marrón claro
COLOR_MARRON_CLARO = "#DEB887"      # Beige oscuro
COLOR_MARRON_MUY_OSCURO = "#2F1810" # Marrón muy oscuro
COLOR_MARRON_MEDIO_OSCURO = "#6B4423" # Marrón medio
COLOR_MARRON_SIENA = "#A0522D"      # Siena

# Blancos y Beiges - Colores de fondo
COLOR_BLANCO_HUESO = "#FDF5E6"     # Blanco hueso
COLOR_BLANCO_CALIDO = "#FEFCF8"    # Blanco cálido
COLOR_BEIGE = "#F5DEB3"            # Beige
COLOR_BLANCO_MAIZ = "#FFF8DC"      # Blanco maíz
COLOR_BLANCO_ANTIGUO = "#FAEBD7"   # Blanco antiguo
COLOR_BISQUE = "#FFE4C4"           # Bisque

# Verdes - Acciones positivas
COLOR_VERDE_OLIVA = "#85AC41"      # Verde oliva
COLOR_VERDE_OLIVA_OSCURO = "#556B2F" # Verde oliva oscuro
COLOR_VERDE_MAR = "#2E8B57"        # Verde mar
COLOR_VERDE_GRIS = "#2F4F4F"       # Verde gris

# Rojos - Alertas y errores
COLOR_ROJO_OSCURO = "#8B0000"      # Rojo oscuro
COLOR_ROJO_GRANATE = "#800000"     # Granate

###########################################
# ESTILOS GENERALES
###########################################

# Estilo General de la Aplicación
Estilo_General = f"""
    QWidget {{
        font-family: 'Playfair Display', serif;
    }}
    QLabel {{
        font-size: 15px;
        font-weight: bold;
        color: {COLOR_MARRON_MUY_OSCURO};
        margin-bottom: 8px;
    }}
    QPushButton {{
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        font-weight: bold;
        font-family: 'Playfair Display', serif;
    }}
    QTabWidget::pane {{
        border: 2px solid {COLOR_MARRON_CLARO};
        border-radius: 8px;
    }}
    QTabBar::tab {{
        background-color: {COLOR_BEIGE};
        color: {COLOR_MARRON_MUY_OSCURO};
        padding: 10px 20px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-family: 'Playfair Display', serif;
    }}
    QTabBar::tab:selected {{
        background-color: {COLOR_MARRON_OSCURO};
        color: {COLOR_BLANCO_MAIZ};
    }}
"""

###########################################
# ESTILOS DE COMPONENTES
###########################################

# Estilos de Tablas
Estilo_Tabla_Base = f"""
    QTableWidget {{
        background-color: {COLOR_BLANCO_MAIZ}; 
        border: 2px solid {COLOR_MARRON_CLARO};
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        gridline-color: {COLOR_MARRON_CLARO};
    }}
    QHeaderView::section {{
        background-color: {COLOR_MARRON_OSCURO}; 
        color: {COLOR_BLANCO_MAIZ};
        padding: 12px;
        border: none;
        font-weight: bold;
        font-size: 14px;
    }}
    QTableWidget::item:selected {{
        background-color: {COLOR_BISQUE};
        color: {COLOR_MARRON_MUY_OSCURO};
    }}
"""

Tabla_Menu = f"""
    {Estilo_Tabla_Base}
    QHeaderView::section {{
        padding: 8px;
        text-align: center;
        font-size: 11px;
    }}
"""

# Estilos de Botones
Boton_Primario = f"""
    QPushButton {{
        background-color: {COLOR_MARRON_OSCURO};
        color: {COLOR_BLANCO_MAIZ};
        padding: 8px 20px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        min-width: 120px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_MARRON_SIENA};
    }}
"""

Boton_Accion = f"""
    QPushButton {{
        background-color: {COLOR_VERDE_OLIVA};
        color: white;
        padding: 5px 15px;
        border: none;
        border-radius: 3px;
        font-size: 14px;
        min-width: 100px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_VERDE_OLIVA_OSCURO};
    }}
"""

Boton_Eliminar = f"""
    QPushButton {{
        background-color: {COLOR_ROJO_OSCURO};
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_ROJO_GRANATE};
    }}
"""

###########################################
# ESTILOS DE VENTANAS Y DIÁLOGOS
###########################################

Ventana_Config = f"""
    QDialog {{
        background-color: {COLOR_BLANCO_MAIZ};
        border-radius: 18px;
        border: 1px solid {COLOR_MARRON_CLARO};
    }}
    QLabel {{
        font-size: 18px;
        font-weight: bold;
        color: {COLOR_MARRON_MUY_OSCURO};
        margin-bottom: 12px;
    }}
    QLineEdit {{
        font-size: 16px;
        padding: 12px;
        border: 2px solid {COLOR_VERDE_OLIVA_OSCURO};
        border-radius: 10px;
        background-color: {COLOR_MARRON_CLARO};
        color: {COLOR_BLANCO_MAIZ};
    }}
    QPushButton {{
        font-size: 16px;
        font-weight: bold;
        padding: 12px 24px;
        background-color: {COLOR_VERDE_MAR};
        color: white;
        border: none;
        border-radius: 10px;
        margin-top: 20px;
    }}
    QPushButton:hover {{
        background-color: {COLOR_VERDE_OLIVA};
    }}
"""

Ventana_Historial = f"""
    QDialog {{
        background-color: {COLOR_BLANCO_MAIZ};
        border-radius: 10px;
    }}
    QLabel {{
        font-size: 18px;
        font-weight: bold;
        color: {COLOR_MARRON_MUY_OSCURO};
        padding: 10px;
    }}
    QTableWidget {{
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: white;
    }}
    QTableWidget::item {{
        padding: 12px;
        border-bottom: 1px solid #eee;
    }}
    QHeaderView::section {{
        background-color: {COLOR_MARRON_MUY_OSCURO};
        color: white;
        padding: 15px;
    }}
"""

###########################################
# ESTILOS DE ELEMENTOS ESPECÍFICOS
###########################################

# Estilos de Scroll
Estilo_Scroll = f"""
    QScrollArea {{
        border: 1px solid {COLOR_MARRON_CLARO};
        border-radius: 5px;
        background-color: {COLOR_BLANCO_CALIDO};
    }}
    QScrollBar:vertical {{
        border: none;
        background: {COLOR_BEIGE};
        width: 10px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_MARRON_OSCURO};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

# Estilos de Frames
Estilo_Frame = f"""
    QFrame {{
        background-color: white;
        border: 1px solid {COLOR_MARRON_CLARO};
        border-radius: 5px;
        margin: 5px;
        padding: 10px;
    }}
"""

# Estilos de Inputs
Estilo_Input = """
    QLineEdit {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
        font-size: 14px;
    }
"""

###########################################
# ESTILOS HTML PARA COMANDAS
###########################################

Estilo_Comanda = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: {COLOR_BLANCO_CALIDO};
    }}
    .comanda {{
        background-color: white;
        border-radius: 12px;
        padding: 30px;
        width: 100%;
        box-sizing: border-box;
    }}
    h2 {{
        color: {COLOR_VERDE_MAR};
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
    }}
    th {{
        background-color: {COLOR_VERDE_MAR};
        color: white;
        padding: 15px;
    }}
    .total {{
        font-weight: bold;
        background-color: {COLOR_BLANCO_CALIDO};
    }}
"""

Estilo_Comanda_Vacia = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: {COLOR_BLANCO_CALIDO};
    }}
    .comanda-vacia {{
        background-color: white;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
    }}
    h2 {{
        color: {COLOR_VERDE_MAR};
        font-size: 24px;
    }}
    .estado {{
        font-size: 18px;
        font-weight: bold;
        color: {COLOR_VERDE_OLIVA};
        margin-top: 20px;
    }}
"""