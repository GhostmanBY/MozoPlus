COLOR_TEXTO_SECUNDARIO = "#6B4423"  # Marrón medio
COLOR_TEXTO_HOVER = "#A0522D"  # Siena
COLOR_FONDO_VENTANA = "#FFF8DC"  # Blanco maíz
COLOR_TEXTO_DARK = "#4A2511"  # Marrón oscuro
COLOR_TEXTO_CLARO = "#FFF8DC"  # Blanco maíz
COLOR_TERCERO = "#DEB887"  # Beige oscuro
COLOR_BOTON_CONFIG_MENU = "#556B2F"  # Verde oliva oscuro
COLOR_BOTON_AGREGAR = "#85AC41"  # Verde oliva oscuro
COLOR_BOTON_GUARDAR = "#2E8B57"  # Verde mar oscuro
COLOR_BOTON_GUARDAR_PRESSED = "#2F4F4F"  # Verde gris oscuro
COLOR_BORDES = "#DEB887"  # Beige oscuro

# MARK: setup_config_menu
#Variable: config_button
Config_Style_boton = f"""
            QToolButton {{
                color: {COLOR_TEXTO_SECUNDARIO};
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
            background-color: white;
            border: 1px solid {COLOR_BOTON_CONFIG_MENU};
            padding: 8px;
            border-radius: 12px;
            font-size: 14px;
        }}
        QMenu::item {{
            padding: 10px 20px;
            border-radius: 8px;
            background-color: {COLOR_BOTON_AGREGAR};
            margin-bottom: 5px;
            color: white
        }}
        QMenu::item:selected {{
            background-color: {COLOR_TEXTO_HOVER};
        }}
        QMenu::icon {{
            padding-right: 12px;
        }}
        """
# MARK: show_config_dialog
Ventanta_de_configuracion = f"""
            QDialog {{
                background-color: {COLOR_FONDO_VENTANA};
                border-radius: 18px;
                border: 1px solid COLOR_BORDES;
            }}
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {COLOR_TEXTO_DARK};
                margin-bottom: 12px;
            }}
            QLineEdit {{
                font-size: 16px;
                padding: 12px;
                border: 2px solid {COLOR_BOTON_CONFIG_MENU};
                border-radius: 10px;
                background-color: {COLOR_TERCERO};
                color: {COLOR_TEXTO_CLARO};
            }}
            QLineEdit:focus {{
                border-color: {COLOR_BOTON_CONFIG_MENU};
            }}
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                background-color: {COLOR_BOTON_GUARDAR};
                color: white;
                border: none;
                border-radius: 10px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_BOTON_GUARDAR_PRESSED};
            }}
        """