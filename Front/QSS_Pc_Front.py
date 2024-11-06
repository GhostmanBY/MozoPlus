# Definición de constantes de color
# Colores base
COLOR_PRIMARIO = "#DA1F3D"    # Rojo Chichilo
COLOR_SECUNDARIO = "#1B3159"  # Azul Marino
COLOR_TERCERO = "#F5F7FA"     # Gris Claro
COLOR_ERROR = "#DA1F3D"       # Rojo Chichilo

# Colores de fondo
COLOR_FONDO = "#F5F7FA"       # Gris Claro
COLOR_FONDO_CLARO = "#FFFFFF" # Blanco Base
COLOR_FONDO_DARK = "#F5F7FA"  # Gris Claro
COLOR_FONDO_VENTANA = "#FFFFFF" # Blanco Base
COLOR_FONDO_FECHA = "#F5F7FA"   # Gris Claro

# Colores de texto
COLOR_TEXTO = "#4A5568"       # Gris Texto
COLOR_TEXTO_CLARO = "#FFFFFF" # Blanco Base
COLOR_TEXTO_DARK = "#1B3159"  # Azul Marino
COLOR_TEXTO_SECUNDARIO = "#2B4F8C" # Azul Acento

# Colores hover
COLOR_TEXTO_HOVER = "#FF4D6A"     # Rojo Claro
COLOR_TEXTO_HOVER_SECUNDARIO = "#FF4D6A" # Rojo Claro
COLOR_TEXTO_HOVER_ERROR = "#DA1F3D"      # Rojo Chichilo

# Colores de bordes
COLOR_BORDES = "#1B3159"      # Azul Marino
COLOR_BORDE_TABLA = "#2B4F8C" # Azul Acento

# Colores de tabla
COLOR_FONDO_TABLA = "#FFFFFF"   # Blanco Base
COLOR_HEADER_TABLA = "#1B3159"  # Azul Marino
COLOR_ITEM_SELECCIONADO = "#F5F7FA" # Gris Claro
COLOR_HEADER_HISTORIAL = "#4A5568"   # Gris Texto

# Colores de scroll
COLOR_SCROLL_AREA = "#1B3159"   # Azul Marino
COLOR_SCROLL_HANDLE = "#2B4F8C" # Azul Acento

# Colores de botones
## Botón cargar
COLOR_BOTON_CARGAR = "#DA1F3D"        # Rojo Chichilo
COLOR_BOTON_CARGAR_HOVER = "#FF4D6A"  # Rojo Claro
COLOR_BOTON_CARGAR_PRESSED = "#4A5568" # Gris Texto

## Botón agregar
COLOR_BOTON_AGREGAR = "#10B981"       # Verde Estado
COLOR_BOTON_EDITAR_HOVER = "#10B981"  # Verde Estado

## Botón exportar
COLOR_BOTON_EXPORTAR = "#DA1F3D"       # Rojo Chichilo
COLOR_BOTON_EXPORTAR_HOVER = "#FF4D6A" # Rojo Claro
COLOR_BOTON_EXPORTAR_PRESSED = "#4A5568" # Gris Texto

## Botones de configuración
COLOR_BOTON_CONFIG_MENU = "#1B3159"    # Azul Marino
COLOR_BOTON_GUARDAR = "#10B981"        # Verde Estado
COLOR_BOTON_GUARDAR_PRESSED = "#4A5568" # Gris Texto


# MARK: Estilos generales
# Paginacion
# Variable: btn_anterior_menu y btn_anterior_mozos, btn_siguiente_menu y btn_siguiente_mozos, refresh_button(Menu) y refresh_button(mozo)
Paginas_atras_adelante_reset = f"""
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
#Variable: mozos_table y munu_table
Tablas_Mozo = f"""
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
Tablas_Menu = f"""
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
                padding: 8px;
                text-align: center;
                border: none;
                font-weight: bold;
                font-size: 11px;
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

# MARK: setup_info_tab
# Variable: scroll_area
Style_Scroll_Area = f"""
                QScrollArea {{
                    border: 1px solid {COLOR_SCROLL_AREA};
                    border-radius: 5px;
                    background-color: {COLOR_FONDO_CLARO};
                }}
            """
# Variable: load_button
Cargar_Resumen_boton = f"""
                QPushButton {{
                    background-color: {COLOR_BOTON_CARGAR};
                    color: {COLOR_TEXTO_CLARO};
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {COLOR_BOTON_CARGAR_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {COLOR_BOTON_CARGAR_PRESSED};
                }}
            """

# MARK: mostrar_resumen Y load_summary
#Variable: fecha_frame
Estilo_Fecha =f"""
                QFrame {{
                    background-color: {COLOR_FONDO_FECHA};
                    border-radius: 10px;
                    margin: 10px;
                    padding: 10px;
                }}
            """
#Variable: fecha_label
Estilo_fecha_label =f"""
                font-weight: bold;
                font-size: 18px;
                color: {COLOR_TEXTO_DARK};
                margin-bottom: 10px;
            """
#Variable: entry_frame
Estilo_Frame = f"""
                QFrame {{
                    background-color: white;
                    border: 1px solid {COLOR_SCROLL_AREA};
                    border-radius: 5px;
                    margin: 5px;
                    padding: 10px;
                }}
            """

# MARK: setup_menu_tab
#Variable: add_product_button
Agregar_Plato_boton = f"""
            QPushButton {{
                background-color: {COLOR_BOTON_AGREGAR};
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
        """

# MARK: load_menu
#Variable: edit_button
boton_editar_Plato = f"""
                    QPushButton {{
                        background-color: {COLOR_TERCERO};
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                        min-width: 80px;
                        max-width: 80px;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {COLOR_BOTON_EDITAR_HOVER};
                    }}
                """
#Variable: delete_button
boton_eliminar_PLato = f"""
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
# MARK: edit_product
#Variable: save_button
Guardar_cambios_Plato = f"""
            QPushButton {{
                background-color: {COLOR_BOTON_AGREGAR};
                color: white;
                padding: 10px 20px;
                margin: 25px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                min-width: 80px;
                max-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
            """
# MARK: setup_mozos_tab
#Variable: mozo_name_input
Entry_name_mozo = """
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 14px;
            }
        """
#Variable: add_mozo_button
Agregar_Mozo = f"""
            QPushButton {{
                background-color: {COLOR_BOTON_AGREGAR};
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
        """
# MARK: load_mozos
#Varaible: edit_button_style
Boton_Editar_mozo = f"""
                QPushButton {{
                    background-color: {COLOR_TERCERO};
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 80px;
                    max-width: 80px;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {COLOR_BOTON_EDITAR_HOVER};
                }}
            """
#Variable: delete_button_style
Boton_eliminar_Mozo = f"""
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

# MARK: edit_mozo
#Variable: dialog
Ventanta_de_editar_Mozo = f"""
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
                border: 2px solid {COLOR_BOTON_AGREGAR};
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
                background-color: {COLOR_BOTON_AGREGAR};
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLOR_TEXTO_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #3D8B40;
            }}
            """
#Variable: mesa_button
Mesas_False = f"""
        QPushButton {{
            background-color: {COLOR_ERROR};
            color: white;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_TEXTO_HOVER_ERROR};
        }}
        QPushButton:pressed {{
            background-color: #C62828;
        }}
        """
# MARK: mostrar_historial_mesa
#Variable: dialog
Ventana_de_historial_mesa = f"""
            QDialog {{
                background-color: {COLOR_FONDO_VENTANA};
                border-radius: 10px;
            }}
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {COLOR_HEADER_HISTORIAL};
                padding: 10px;
            }}
            QTableWidget {{
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                gridline-color: #ddd;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #eee;
            }}
            QHeaderView::section {{
                background-color: {COLOR_HEADER_HISTORIAL};
                color: white;
                padding: 15px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {COLOR_FONDO};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLOR_HEADER_HISTORIAL};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
#Variable: export_button
Boton_Exportar_comadna = f"""
                QPushButton {{
                    background-color: {COLOR_BOTON_EXPORTAR};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {COLOR_BOTON_EXPORTAR_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {COLOR_BOTON_EXPORTAR_PRESSED};
                }}
            """
#Variable: export_menu
Exportar_menu = f"""
                QMenu {{
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 5px;
                }}
                QMenu::item {{
                    padding: 8px 20px;
                    font-size: 13px;
                }}
                QMenu::item:selected {{
                    background-color: {COLOR_BOTON_EXPORTAR};
                    color: white;
                }}
            """
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

# MARK: Style HTML
# Estilos para la comanda
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
        color: #2E7D32;
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
    }}
    .aclaraciones {{
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        font-style: italic;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
        font-size: 14px;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
        white-space: nowrap;
    }}
    th {{
        background-color: #2E7D32;
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
        color: #2E7D32;
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
        color: #4CAF50;
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

# MARK: if __name__ == "__main__"
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
