# Nuevos nombres para las constantes de color
AZUL_FONDO_SCROLL = "#EDF2F7"
BLANCO_FONDO_CLARO = "#F7FAFC"
AZUL_PASTEL_FONDO = "#CBD5E0"
AZUL_ACERO_SCROLL = "#4A5568"
AZUL_TEXTO_OSCURO = "#2D3748"
BLANCO_PURO = "#FFFFFF"
AZUL_BOTON_MEDIO = "#4299E1"
AZUL_PRINCIPAL = "#3182CE"
AZUL_HOVER = "#2B6CB0"
AZUL_MESA_OCUPADA = "#E53E3E"
AZUL_ERROR = "#C53030"
AZUL_SECUNDARIO = "#2C5282"
AZUL_BORDE_TABLA = "#63B3ED"

AZUL_FONDO_COMANDA = "#F7FAFC"
AZUL_TEXTO_ENCABEZADO = "#2D3748"
AZUL_FONDO_ACLARACIONES = "#EBF8FF"
AZUL_BORDE_ACLARACIONES = "#63B3ED"
AZUL_BORDE_TABLA = "#2C7BB6"
AZUL_TABLA_HEADER = "#3182CE"
BLANCO_TABLA = "#FFFFFF"

# MARK: setup_main_tab
#Variable: mesas_scroll
Frame_Scroll_mesas = f"""
    QScrollArea {{
        border: 2px solid {AZUL_FONDO_SCROLL};
        border-radius: 10px;
        background-color: {BLANCO_FONDO_CLARO};
    }}
    
    QScrollBar:vertical {{
        border: none;
        background: {AZUL_PASTEL_FONDO};
        width: 12px;
        margin: 0px 0px 0px 0px;
        border-radius: 6px;
    }}
    QScrollBar::handle:vertical {{
        background: {AZUL_ACERO_SCROLL};
        min-height: 25px;
        border-radius: 6px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

#Variable: right_widget
right_widget_style = f"""
    QWidget {{
        background-color: {BLANCO_FONDO_CLARO};
        border-radius: 15px;
        border: 2px solid {AZUL_FONDO_SCROLL};
    }}
"""

#Variable: pedidos_label
pedidos_label_Style = f"""
    QLabel {{
        font-size: 18px;
        font-weight: bold;
        color: {AZUL_TEXTO_OSCURO};
        margin-bottom: 10px;
        border: none;
        padding: 5px;
        background-color: {AZUL_FONDO_SCROLL};
        border-radius: 8px;
    }}
"""

#Variable: json_input
Placeholder_text_pedido = f"""
    QTextEdit {{
        border: 2px solid {AZUL_BOTON_MEDIO};
        border-radius: 12px;
        padding: 15px;
        background-color: {BLANCO_PURO};
        selection-background-color: {AZUL_BOTON_MEDIO};
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: {AZUL_TEXTO_OSCURO};
    }}
"""

#Variable: splitter
splitter_style = f"""
    QSplitter::handle {{
        background-color: {AZUL_PASTEL_FONDO};
        height: 10px;
        border-radius: 5px;
    }}
"""

# MARK: cargar_mesas
#Variable: mesa_button
Mesas_True = f"""
    QPushButton {{
        background-color: {AZUL_PRINCIPAL};
        color: white;
        border-radius: 20px;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: {AZUL_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {AZUL_HOVER};
    }}
"""

#Variable: mesa_button
Mesas_False = f"""
    QPushButton {{
        background-color: {AZUL_MESA_OCUPADA};
        color: white;
        border-radius: 20px;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: {AZUL_ERROR};
    }}
    QPushButton:pressed {{
        background-color: {AZUL_MESA_OCUPADA};
    }}
"""

#MARK: CSS Comandas
Comanda_Style = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: {AZUL_FONDO_COMANDA};
    }}
    .comanda {{
        background-color: {BLANCO_TABLA};
        border-radius: 15px;
        padding: 30px;
        width: 100%;
        box-sizing: border-box;
    }}
    h2 {{
        color: {AZUL_TEXTO_ENCABEZADO};
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
        border-bottom: 2px solid {AZUL_TEXTO_ENCABEZADO};
        padding-bottom: 10px;
    }}
    .info {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 20px;
        background-color: {AZUL_FONDO_ACLARACIONES};
        padding: 15px;
        border-radius: 10px;
    }}
    .info p {{
        margin: 5px 0;
        flex: 1 1 40%;
        font-size: 20px;
        font-family: 'Arial', sans-serif;
        color: {AZUL_TEXTO_ENCABEZADO};
    }}
    .aclaraciones {{
        background-color: {AZUL_FONDO_ACLARACIONES};
        border-left: 5px solid {AZUL_BORDE_ACLARACIONES};
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
    }}
    .aclaraciones p {{
        font-size: 20px;
        font-family: 'Arial', sans-serif;
        color: {AZUL_TEXTO_ENCABEZADO};
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
        font-size: 14px;
    }}
    th, td {{
        border: 1px solid {AZUL_BORDE_TABLA};
        padding: 10px;
        text-align: left;
        white-space: nowrap;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight: bold;
    }}
    th {{
        background-color: {AZUL_TABLA_HEADER};
        color: white;
    }}
    tr:nth-child(even) {{
        background-color: #F0F8FF;
    }}
    .total {{
        font-weight: bold;
        background-color: #E6F2FF;
        color: {AZUL_TEXTO_ENCABEZADO};
    }}
"""

# Estilos para la comanda vacía
Comanda_Vacia_Style = f"""
    body {{
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        background-color: {AZUL_FONDO_COMANDA};
    }}
    .comanda-vacia {{
        background-color: {BLANCO_TABLA};
        border-radius: 15px;
        padding: 30px;
        width: 100%;
        box-sizing: border-box;
        text-align: center;
    }}
    h2 {{
        color: {AZUL_TEXTO_ENCABEZADO};
        font-size: 24px;
        margin-bottom: 20px;
        border-bottom: 2px solid {AZUL_TEXTO_ENCABEZADO};
        padding-bottom: 10px;
    }}
    .icon {{
        font-size: 48px;
        color: #4682B4;
        margin-bottom: 20px;
    }}
    p {{
        font-size: 16px;
        color: {AZUL_TEXTO_ENCABEZADO};
        margin: 10px 0;
        line-height: 1.5;
    }}
    .estado {{
        font-size: 18px;
        font-weight: bold;
        color: {AZUL_TEXTO_ENCABEZADO};
        margin-top: 20px;
        background-color: {AZUL_FONDO_ACLARACIONES};
        padding: 10px;
        border-radius: 10px;
    }}
    .aclaraciones {{
        background-color: {AZUL_FONDO_ACLARACIONES};
        border-left: 5px solid {AZUL_BORDE_ACLARACIONES};
        padding: 10px;
        margin-top: 20px;
        border-radius: 5px;
        text-align: left;
        font-style: italic;
    }}
"""