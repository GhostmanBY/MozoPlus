GRIS_TEXTO = "#2D3748"             # Gris oscuro principal
GRIS_TEXTO_HOVER = "#4A5568"       # Gris oscuro para hover
BLANCO_FONDO = "#F7FAFC"           # Blanco con toque gris
GRIS_TEXTO_OSCURO = "#1A202C"      # Gris muy oscuro
BLANCO_TEXTO = "#FFFFFF"           # Blanco puro
GRIS_BORDES = "#CBD5E0"            # Gris medio
VERDE_PRIMARIO = "#38A169"         # Verde para acciones principales
VERDE_SECUNDARIO = "#48BB78"       # Verde más claro
VERDE_EXITO = "#2F855A"            # Verde oscuro
VERDE_PRESSED = "#276749"          # Verde muy oscuro
GRIS_BORDES_SUAVE = "#E2E8F0"      # Gris claro para bordes

# MARK: setup_config_menu
#Variable: config_button
Config_Style_boton = f"""
            QToolButton {{
                color: {GRIS_TEXTO};
                background-color: transparent;
                border: none;
                padding: 15px;  
                margin: 30px;
                margin-right: 0px;  
            }}
            QToolButton:hover {{
                background-color: rgba(224, 224, 224, 0.5);
                border-radius: 5px;
            }}
            QToolButton:pressed {{
                background-color: rgba(200, 200, 200, 0.7);
            }}
            QToolButton::menu-indicator {{
                image: none;
            }}
            """
#Variable: config_menu
Config_Desplegable_Menu = f"""
        QMenu {{
            background-color: {BLANCO_FONDO};
            border: 1px solid {VERDE_PRIMARIO};
            padding: 8px;
            border-radius: 12px;
            font-size: 14px;
        }}
        QMenu::item {{
            padding: 10px 20px;
            border-radius: 8px;
            background-color: {VERDE_SECUNDARIO};
            margin-bottom: 5px;
            color: white
        }}
        QMenu::item:selected {{
            background-color: {GRIS_TEXTO_HOVER};
        }}
        QMenu::icon {{
            padding-right: 12px;
        }}
        """
# MARK: show_config_dialog
Ventanta_de_configuracion = f"""
            QDialog {{
                background-color: {BLANCO_FONDO};
                border-radius: 18px;
                border: 1px solid {GRIS_BORDES};
            }}
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {GRIS_TEXTO_OSCURO};
                margin-bottom: 12px;
            }}
            QLineEdit {{
                font-size: 16px;
                padding: 12px;
                border: 2px solid {VERDE_PRIMARIO};
                border-radius: 10px;
                background-color: {VERDE_EXITO};
                color: {BLANCO_TEXTO};
            }}
            QLineEdit:focus {{
                border-color: {VERDE_PRIMARIO};
            }}
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                background-color: {VERDE_PRESSED};
                color: white;
                border: none;
                border-radius: 10px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {GRIS_TEXTO_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {VERDE_PRESSED};
            }}
        """

Ventana_Agregar_Plato = f"""
    QDialog {{
        background-color: {BLANCO_FONDO};
        border: 2px solid {GRIS_BORDES};
        padding: 20px;
    }}
    QLabel {{
        font-size: 18px;
        font-weight: bold;
        background-color: transparent;
        color: {GRIS_TEXTO_OSCURO};
        margin-bottom: 12px;
    }}
    QLineEdit {{
        font-size: 16px;
        padding: 5px;
        border: 2px solid {VERDE_PRIMARIO};
        border-radius: 10px;
        background-color: {VERDE_EXITO};
        color: {BLANCO_TEXTO};
    }}
    QLineEdit:focus {{
        border-color: {VERDE_PRIMARIO};
    }}
    QPushButton {{
        font-size: 16px;
        font-weight: bold;
        padding: 12px 24px;
        background-color: {VERDE_SECUNDARIO};
        color: white;
        border: none;
        border-radius: 10px;
        margin-top: 20px;
    }}
    QPushButton:hover {{
        background-color: {VERDE_PRIMARIO};
    }}
    QPushButton:pressed {{
        background-color: {VERDE_PRESSED};
    }}
"""