COLOR_TEXTO = "#2F1810"
COLOR_FONDO_VENTANA = "#FFF8DC"
COLOR_BORDES = "#DEB887"
COLOR_PRIMARIO = "#8B4513"
COLOR_TEXTO_CLARO = "#FFF8DC"
COLOR_BORDE_TABLA = "#8B4513"
COLOR_FONDO_DARK = "#F5DEB3"
COLOR_FONDO = "#FDF5E6"
COLOR_SCROLL_HANDLE = "#8B4513"

# Estilo General
# Funcion: set_style
Estilo_General = f"""
        QWidget {{
            font-family: 'Playfair Display', serif;
        }}
        QLabel {{
            font-size: 15px;
            font-weight: bold;
            color: {COLOR_TEXTO};
            margin-bottom: 8px;
        }}
        QPushButton {{
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            font-family: 'Playfair Display', serif;
        }}
        QTableWidget {{
            alternate-background-color: {COLOR_FONDO_VENTANA};
            gridline-color: {COLOR_BORDES};
        }}
        QHeaderView::section {{
            background-color: {COLOR_PRIMARIO};
            color: {COLOR_TEXTO_CLARO};
            padding: 10px;
            border: 1px solid {COLOR_BORDE_TABLA};
            font-weight: bold;
        }}
        QTabWidget::pane {{
            border: 2px solid {COLOR_BORDES};
            border-radius: 8px;
        }}
        QTabBar::tab {{
            background-color: {COLOR_FONDO_DARK};
            color: {COLOR_TEXTO};
            padding: 10px 20px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-family: 'Playfair Display', serif;
        }}
        QTabBar::tab:selected {{
            background-color: {COLOR_PRIMARIO};
            color: {COLOR_TEXTO_CLARO};
        }}
    """
#MARK:APP
#Variable: app
Estilo_app = f"""
        QMainWindow {{
            background-color: {COLOR_FONDO};
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