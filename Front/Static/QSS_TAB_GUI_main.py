COLOR_SCROLL_AREA = "#DEB887"
COLOR_FONDO_CLARO = "#FEFCF8"
COLOR_FONDO_DARK = "#F5DEB3"
COLOR_SCROLL_HANDLE = "#8B4513"
COLOR_TEXTO = "#2F1810"
COLOR_TEXTO_CLARO = "#FFF8DC"
COLOR_BOTON_AGREGAR = "#85AC41"
COLOR_PRIMARIO = "#8B4513"
COLOR_TEXTO_HOVER = "#A0522D"
COLOR_DISPO_F = "#C62828"
COLOR_ERROR = "#8B0000"
COLOR_TEXTO_SECUNDARIO = "#6B4423"
COLOR_BORDE_TABLA = "#8B4513"

# MARK: setup_main_tab
#Variable: mesas_scroll
Frame_Scroll_mesas = f"""
            QScrollArea {{
                border: 1px solid {COLOR_SCROLL_AREA};
                border-radius: 5px;
                background-color: {COLOR_FONDO_CLARO};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background: {COLOR_FONDO_DARK};
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLOR_SCROLL_HANDLE};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
#Variable: right_widget
right_widget_style = f"""
            QWidget {{
                background-color: #FAFAFA;
                border-radius: 10px;
                border: 1px solid {COLOR_SCROLL_AREA};
            }}
            
        """
#Variable: pedidos_label
pedidos_label_Style = f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {COLOR_TEXTO};
                margin-bottom: 5px;
                border: none;
            }}
        """
#Variable: json_input
Placeholder_text_pedido = f"""
            QTextEdit {{
                border: 2px solid {COLOR_SCROLL_AREA};
                border-radius: 10px;
                padding: 10px;
                background-color: {COLOR_TEXTO_CLARO};
                selection-background-color: {COLOR_BOTON_AGREGAR};
                font-family: 'Playfair Display', serif;
                font-size: 12px;
            }}
        """
#Variable: splitter
splitter_style = """
            QSplitter::handle {
                background-color: {COLOR_FONDO_DARK};
            }
        """

# MARK: cargar_mesas
#Varaible: mesa_button
Mesas_True = f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
            """
#Variable: mesa_button
Mesas_False = f"""
        QPushButton {{
            background-color: {COLOR_DISPO_F};
            color: white;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_ERROR};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_DISPO_F};
        }}
        """

#MARK: CSS Comandas
Comanda_Style = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f9f9f9;
    }}
    .comanda {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 30px;
        width: 100%;
        box-sizing: border-box;
    }}
    h2 {{
        color: {COLOR_TEXTO_SECUNDARIO};
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }}
    .info {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 20px;
    }}
    .info p {{
        margin: 5px 0;
        flex: 1 1 40%;
        font-size: 20px;
        font-family: 'Playfair Display', serif;
    }}
    .aclaraciones {{
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
    }}
    .aclaraciones p {{
        font-size: 20px;
        font-family: 'Playfair Display', serif;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
        font-size: 14px;
    }}
    th, td {{
        border: 1px solid {COLOR_BORDE_TABLA};
        padding: 10px;
        text-align: left;
        white-space: nowrap;
        font-family: 'Playfair Display', serif;
        font-size: 14px;
        font-weight: bold;
    }}
    th {{
        background-color: {COLOR_BORDE_TABLA};
        color: white;
    }}
    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
    .total {{
        font-weight: bold;
        background-color: #E8F5E9;
    }}
"""

# Estilos para la comanda vacía
Comanda_Vacia_Style = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f9f9f9;
    }}
    .comanda-vacia {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 30px;
        width: 100%;
        box-sizing: border-box;
        text-align: center;
    }}
    h2 {{
        color: {COLOR_TEXTO_SECUNDARIO};
        font-size: 24px;
        margin-bottom: 20px;
    }}
    .icon {{
        font-size: 48px;
        color: #9E9E9E;
        margin-bottom: 20px;
    }}
    p {{
        font-size: 16px;
        color: #616161;
        margin: 10px 0;
        line-height: 1.5;
    }}
    .estado {{
        font-size: 18px;
        font-weight: bold;
        color: {COLOR_TEXTO_SECUNDARIO};
        margin-top: 20px;
    }}
    .aclaraciones {{
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 10px;
        margin-top: 20px;
        border-radius: 5px;
        text-align: left;
        font-style: italic;
    }}
"""