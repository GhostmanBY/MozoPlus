# MARK: Estilos generales
#Paginacion
#Variable: btn_anterior_menu y btn_anterior_mozos
Paginas_atras = """
                QPushButton {
                    background-color: #008CBA;
                    color: white;
                    padding: 5px 15px;
                    border: none;
                    border-radius: 3px;
                    font-size: 14px;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #007B9A;
                }
            """
#Variable: btn_siguiente_menu y btn_siguiente_mozos
Paginas_Adelante = """
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
            """
#Variable: refresh_button(Menu) y refresh_button(mozo)
Recargar_Tablas = """
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
        """
#Estilo General
#Funcion: set_style
Estilo_General = """
        QWidget {
            font-family: Arial, sans-serif;
        }
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 5px;
        }
        QPushButton {
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        QTableWidget {
            alternate-background-color: #F5F5F5;
            gridline-color: #D0D0D0;
        }
        QHeaderView::section {
            background-color: #009688;
            color: white;
            padding: 8px;
            border: 1px solid #00796B;
            font-weight: bold;
        }
        QTabWidget::pane {
            border: 1px solid #D0D0D0;
            border-radius: 5px;
        }
        QTabBar::tab {
            background-color: #E0E0E0;
            color: #333333;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
        }
    """

# MARK: setup_info_tab
#Variable: scroll_area
Style_Scroll_Area ="""
                QScrollArea {
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
            """
#Variable: load_button
Cargar_Resumen_boton ="""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #2573a7;
                }
            """

# MARK: mostrar_resumen Y load_summary
#Variable: fecha_frame
Estilo_Fecha ="""
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 10px;
                    margin: 10px;
                    padding: 10px;
                }
            """
#Variable: fecha_label
Estilo_fecha_label ="""
                font-weight: bold;
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 10px;
            """
#Variable: entry_frame
Estilo_Frame = """
                QFrame {
                    background-color: white;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    margin: 5px;
                    padding: 10px;
                }
            """

# MARK: setup_menu_tab
#Variable: add_product_button
Agregar_Plato_boton = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

# MARK: load_menu
#Variable: edit_button
boton_editar_Plato = """
                    QPushButton {
                        background-color: #FFA500;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                        min-width: 80px;
                        max-width: 80px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #FF8C00;
                    }
                """
#Variable: delete_button
boton_eliminar_PLato = """
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 3px;
                        min-width: 80px;
                        max-width: 80px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                """
# MARK: edit_product
#Variable: save_button
Guardar_cambios_Plato = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin: 25px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                min-width: 80px;
                max-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
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
Agregar_Mozo = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
#Variable: mozos_table
Tabla_Mozo = """
            QTableWidget {
                background-color: white; 
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #009688; 
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #333333;
            }
        """
# MARK: load_mozos
#Varaible: edit_button_style
Boton_Editar_mozo = """
                QPushButton {
                    background-color: #FFA500;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 80px;
                    max-width: 80px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
            """
#Variable: delete_button_style
Boton_eliminar_Mozo = """
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 80px;
                    max-width: 80px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """

# MARK: edit_mozo
#Variable: dialog
Ventanta_de_editar_Mozo = """
                QDialog {
                    background-color: #f5f5f5;
                    border-radius: 15px;
                    border: 1px solid #dcdcdc;
                }
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                QLineEdit {
                    font-size: 16px;
                    padding: 12px;
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    background-color: white;
                    color: #333;
                }
                QLineEdit:focus {
                    border-color: #45a049;
                }
                QPushButton {
                    font-size: 16px;
                    font-weight: bold;
                    padding: 12px 24px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    margin-top: 20px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """

# MARK: setup_main_tab
#Variable: mesas_scroll
Frame_Scroll_mesas = """
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
            QScrollBar:vertical {
                border: none;
                background: #E0E0E0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
#Variable: right_widget
right_widget_style = """
            QWidget {
                background-color: #FAFAFA;
                border-radius: 10px;
            }
        """
#Variable: pedidos_label
pedidos_label_Style = """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            }
        """
#Variable: json_input
Placeholder_text_pedido = """
            QTextEdit {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
                background-color: #FFFFFF;
                selection-background-color: #81C784;
                font-family: 'Courier New';
                font-size: 12px;
            }
        """
#Variable: splitter
splitter_style = """
            QSplitter::handle {
                background-color: #E0E0E0;
            }
        """

# MARK: cargar_mesas
#Varaible: mesa_button
Mesas_True = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #3D8B40;
            }
            """
#Variable: mesa_button
Mesas_False = """
        QPushButton {
            background-color: #F44336;
            color: white;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #D32F2F;
        }
        QPushButton:pressed {
            background-color: #C62828;
        }
        """
# MARK: mostrar_historial_mesa
#Variable: dialog
Ventana_de_historial_mesa = """
            QDialog {
                background-color: #f5f5f5;
                border-radius: 10px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2E7D32;
                padding: 10px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #2E7D32;
                color: white;
                padding: 15px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2E7D32;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
#Variable: export_button
Boton_Exportar_comadna = """
                QPushButton {
                    background-color: #FF5722;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #F4511E;
                }
                QPushButton:pressed {
                    background-color: #E64A19;
                }
            """
#Variable: export_menu
Exportar_menu = """
                QMenu {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 5px;
                }
                QMenu::item {
                    padding: 8px 20px;
                    font-size: 13px;
                }
                QMenu::item:selected {
                    background-color: #FF5722;
                    color: white;
                }
            """
# MARK: setup_config_menu
#Variable: config_button
Config_Style_boton = """
            QToolButton {
                color: #555555;
                background-color: transparent;
                border: none;
                padding: 15px;  
                margin: 30px;
                margin-right: 0px;  
            }
            QToolButton:hover {
                background-color: rgba(224, 224, 224, 0.5);
                border-radius: 5px;
            }
            QToolButton:pressed {
                background-color: rgba(200, 200, 200, 0.7);
            }
            QToolButton::menu-indicator {
                image: none;
            }
            """
#Variable: config_menu
Config_Desplegable_Menu = """
        QMenu {
            background-color: white;
            border: 1px solid #44dc4a;
            padding: 8px;
            border-radius: 12px;
            font-size: 14px;
        }
        QMenu::item {
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #4caf50;
            margin-bottom: 5px;
            color: white
        }
        QMenu::item:selected {
            background-color: #45A049;
        }
        QMenu::icon {
            padding-right: 12px;
        }
        """
# MARK: show_config_dialog
Ventanta_de_configuracion = """
            QDialog {
                background-color: #f5f5f5;
                border-radius: 18px;
                border: 1px solid #d0d0d0;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 12px;
            }
            QLineEdit {
                font-size: 16px;
                padding: 12px;
                border: 2px solid #44dc4a;
                border-radius: 10px;
                background-color: white;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #44dc4a;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
                background-color: #31b736;
                color: white;
                border: none;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """

# MARK: if __name__ == "__main__"
#Variable: app
Estilo_app = """
        QMainWindow {
            background-color: #F0F0F0;
        }
        QScrollBar:vertical {
            border: none;
            background: #E0E0E0;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #BDBDBD;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """



                