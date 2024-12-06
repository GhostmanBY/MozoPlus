GRIS_TEXTO = "#2D3748"
BLANCO_FONDO = "#F7FAFC"
GRIS_BORDES = "#CBD5E0"
AZUL_PRIMARIO = "#3182CE"
BLANCO_TEXTO = "#FFFFFF"
AZUL_BORDE = "#4299E1"
GRIS_FONDO_ALT = "#EDF2F7"
BLANCO_FONDO_BASE = "#FFFFFF"
AZUL_SCROLL = "#4A5568"

# Estilo General
# Funcion: set_style
Estilo_General = f"""
        QWidget {{
            font-family: 'Inter', sans-serif;
        }}
        QLabel {{
            font-size: 15px;
            font-weight: 600;
            color: {GRIS_TEXTO};
            margin-bottom: 8px;
        }}
        QPushButton {{
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
        }}
        QTableWidget {{
            alternate-background-color: {BLANCO_FONDO};
            gridline-color: {GRIS_BORDES};
        }}
        QHeaderView::section {{
            background-color: {AZUL_PRIMARIO};
            color: {BLANCO_TEXTO};
            padding: 10px;
            border: 1px solid {AZUL_BORDE};
            font-weight: 600;
        }}
        QTabWidget::pane {{
            border: 2px solid {GRIS_BORDES};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background-color: {GRIS_FONDO_ALT};
            color: {GRIS_TEXTO};
            padding: 10px 20px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-family: 'Inter', sans-serif;
        }}
        QTabBar::tab:selected {{
            background-color: {AZUL_PRIMARIO};
            color: {BLANCO_TEXTO};
        }}
    """

#MARK:APP
#Variable: app
Estilo_app = f"""
        QMainWindow {{
            background-color: {BLANCO_FONDO_BASE};
        }}
        QScrollBar:vertical {{
            border: none;
            background: {GRIS_FONDO_ALT};
            width: 10px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {AZUL_SCROLL};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
    """