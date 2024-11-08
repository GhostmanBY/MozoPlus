# Definición de constantes de color
# Colores base
# Definición de constantes de color
# Colores base - Tonos cálidos y elegantes
COLOR_PRIMARIO = "#8B4513"  # Marrón elegante
COLOR_SECUNDARIO = "#CD853F"  # Marrón claro
COLOR_TERCERO = "#DEB887"  # Beige oscuro
COLOR_ERROR = "#8B0000"  # Rojo oscuro elegante

# Colores de fondo
COLOR_FONDO = "#FDF5E6"  # Blanco hueso
COLOR_FONDO_CLARO = "#FEFCF8"  # Blanco cálido
COLOR_FONDO_DARK = "#F5DEB3"  # Beige
COLOR_FONDO_VENTANA = "#FFF8DC"  # Blanco maíz
COLOR_FONDO_FECHA = "#FAEBD7"  # Blanco antiguo

# Colores de texto
COLOR_TEXTO = "#2F1810"  # Marrón muy oscuro
COLOR_TEXTO_CLARO = "#FFF8DC"  # Blanco maíz
COLOR_TEXTO_DARK = "#4A2511"  # Marrón oscuro
COLOR_TEXTO_SECUNDARIO = "#6B4423"  # Marrón medio

# Colores hover
COLOR_TEXTO_HOVER = "#A0522D"  # Siena
COLOR_TEXTO_HOVER_SECUNDARIO = "#8B4513"  # Marrón silla
COLOR_TEXTO_HOVER_ERROR = "#800000"  # Granate

# Colores de bordes
COLOR_BORDES = "#DEB887"  # Beige oscuro
COLOR_BORDE_TABLA = "#8B4513"  # Marrón silla

# Colores de tabla
COLOR_FONDO_TABLA = "#FFF8DC"  # Blanco maíz
COLOR_HEADER_TABLA = "#8B4513"  # Marrón silla
COLOR_ITEM_SELECCIONADO = "#FFE4C4"  # Bisque
COLOR_HEADER_HISTORIAL = "#654321"  # Marrón oscuro

# Colores de scroll
COLOR_SCROLL_AREA = "#DEB887"  # Beige oscuro
COLOR_SCROLL_HANDLE = "#8B4513"  # Marrón silla

# Colores de botones
## Botón cargar
COLOR_BOTON_CARGAR = "#8B4513"  # Marrón silla
COLOR_BOTON_CARGAR_HOVER = "#A0522D"  # Siena
COLOR_BOTON_CARGAR_PRESSED = "#6B4423"  # Marrón medio

## Botón agregar
COLOR_BOTON_AGREGAR = "#85AC41"  # Verde oliva oscuro
COLOR_BOTON_EDITAR_HOVER = "#6B8E23"  # Verde oliva
COLOR_DISPO_F = "#C62828"

## Botón exportar
COLOR_BOTON_EXPORTAR = "#8B4513"  # Marrón silla
COLOR_BOTON_EXPORTAR_HOVER = "#A0522D"  # Siena
COLOR_BOTON_EXPORTAR_PRESSED = "#6B4423"  # Marrón medio

## Botones de configuración
COLOR_BOTON_CONFIG_MENU = "#556B2F"  # Verde oliva oscuro
COLOR_BOTON_GUARDAR = "#2E8B57"  # Verde mar oscuro
COLOR_BOTON_GUARDAR_PRESSED = "#2F4F4F"  # Verde gris oscuro


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
# Variable: header_frame
resumen_estilo_scroll = f"""
            QScrollArea {{
                border: 2px solid #DEB887;
                border-radius: 10px;
                background-color: #FEFCF8;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #FDF5E6;
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #8B4513;
                min-height: 30px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

Header_Frame_Style = """
    QFrame {
        background-color: #FFF8DC;
        border-radius: 10px;
        padding: 5px;
    }
"""

# Variable: title_label
Title_Label_Style = """
    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #8B4513;
        padding: 5px;
        border-bottom: 2px solid #DEB887;
    }
"""

# Variable: fecha_label y mozo_label
Icon_Label_Style = "font-size: 16px;"

# Variable: fecha_input y mozo_input
Search_Input_Style = """
    QLineEdit {
        padding: 8px;
        border: 2px solid #DEB887;
        border-radius: 5px;
        background: white;
        font-size: 14px;
        min-width: 200px;
    }
    QLineEdit:focus {
        border-color: #8B4513;
    }
"""

# Variable: search_button
Search_Button_Style = """
    QPushButton {
        background-color: #8B4513;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        min-width: 100px;
    }
    QPushButton:hover {
        background-color: #A0522D;
    }
    QPushButton:pressed {
        background-color: #6B4423;
    }
"""

# Variable: load_button
Load_Button_Style = """
    QPushButton {
        background-color: #CD853F;
        color: white;
        padding: 8px 15px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        min-width: 100px;
    }
    QPushButton:hover {
        background-color: #8B4513;
    }
    QPushButton:pressed {
        background-color: #6B4423;
    }
"""

# Variable: scroll_area
Info_Scroll_Area_Style = """
    QScrollArea {
        border: 2px solid #DEB887;
        border-radius: 10px;
        background-color: #FEFCF8;
        min-height: 850px;
    }
    QScrollBar:vertical {
        border: none;
        background: #FDF5E6;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #8B4513;
        min-height: 30px;
        border-radius: 6px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

# MARK: load_summary
# Variable: fecha_frame
Summary_Fecha_Frame_Style = """
    QFrame {
        background-color: #FFF8DC;
        border-radius: 15px;
        margin: 10px;
        padding: 15px;
    }
"""

# Variable: fecha_label
Summary_Fecha_Label_Style = """
    QLabel {
        font-size: 18px;
        font-weight: bold;
        color: #8B4513;
        padding: 5px;
        border-bottom: 2px solid #DEB887;
    }
"""

# Variable: entry_frame
Summary_Entry_Frame_Style = """
    QFrame {
        background-color: white;
        border: 1px solid #DEB887;
        border-radius: 10px;
        margin: 5px;
        padding: 15px;
    }
    QFrame:hover {
        border: 1px solid #8B4513;
        background-color: #FEFCF8;
    }
"""

# Variable: info_label
Summary_Info_Label_Style = """
    QLabel {
        font-size: 14px;
        color: #6B4423;
        margin: 3px 0;
    }
"""

# Variable: productos_detalle
Summary_Productos_Detalle_Style = """
    QLabel {
        color: #6B4423;
        margin-left: 15px;
        font-size: 13px;
    }
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

# MARK: load_menu
#Variable: edit_button
boton_editar_Plato = f"""
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
                background-color: {COLOR_SECUNDARIO};
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
                background-color: {COLOR_PRIMARIO};
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
# MARK: load_mozos
#Varaible: edit_button_style
Boton_Editar_mozo = f"""
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

# MARK: show_detailed_info
# Variable: dialog
Detail_Dialog_Style = """
    QDialog {
        background-color: #FFF8DC;
        border-radius: 15px;
    }
    QLabel {
        color: #6B4423;
        font-size: 14px;
        margin: 5px 0;
    }
    QFrame {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
    }
"""

# Variable: scroll
Detail_Scroll_Style = """
    QScrollArea {
        border: none;
        background-color: #FFF8DC;
    }
    QScrollBar:vertical {
        border: none;
        background: #FDF5E6;
        width: 12px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #8B4513;
        min-height: 30px;
        border-radius: 6px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

# Variable: title
Detail_Title_Style = """
    font-size: 24px;
    font-weight: bold;
    color: #8B4513;
    padding-bottom: 10px;
    border-bottom: 2px solid #DEB887;
"""

# Variable: producto_label
Detail_Product_Style = "margin-left: 20px;"

# Variable: total_label
Detail_Total_Style = """
    font-size: 18px;
    font-weight: bold;
    color: #2E7D32;
    margin-top: 10px;
    padding: 10px;
    background-color: #E8F5E9;
    border: 2px solid #1A561D;
    border-radius: 5px;
"""

# Variable: close_button
Detail_Close_Button_Style = """
    QPushButton {
        background-color: #8B4513;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #A0522D;
    }
"""
