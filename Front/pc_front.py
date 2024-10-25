import sys
import json
import os
import re
import socket
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QTabWidget,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QScrollArea,
    QDesktopWidget,
    QLineEdit,
    QHeaderView,
    QMessageBox,
    QDialog,  # Asegúrate de que QTabBar esté importado
    QSizePolicy,  # Asegúrate de que QSizePolicy esté importado
    QFrame,
    QComboBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from Back.Panel_Admin_Back import (
    Eliminar_empleados,
    Mostrar_Mozos,
    Alta_Mozo,
    Editar_Mozo,
    Mostrar_Menu,
    Modificar_Menu,
    Cargar_Producto,
    Eliminar_Producto,
    Recargar_menu,
)

base_dir = os.path.dirname(os.path.abspath(__file__))

class RestaurantInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pagina_mozos = 0
        self.pagina_menu = 0
        self.setWindowTitle("Interfaz de Restaurante")
        self.ajustar_tamano_pantalla()
        self.set_style()

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.mozos_table = None
        self.load_cubiertos_price()
        self.load_mesas_count()

        # Inicializar los atributos de entrada
        self.cubiertos_input = QLineEdit()
        self.cubiertos_input.setPlaceholderText(f"{self.load_cubiertos_price()}")
        self.mesas_input = QLineEdit()
        self.mesas_input.setPlaceholderText(f"{self.load_mesas_count()}")
        self.idioma_input = QComboBox()


        # Configurar la interfaz principal
        self.setup_main_tab()
        self.setup_mozos_tab()
        self.setup_menu_tab()
        self.setup_info_tab()

        # Añadir una pestaña de configuración
        self.setup_config_tab()

        # Configurar el temporizador para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cargar_mesas)
        self.timer.start(5000)  # Actualizar cada 5 segundos (5000 ms)


    def setup_info_tab(self):
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)

        # Estilo para el widget de desplazamiento
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        """
        )
        info_layout.addWidget(self.scroll_area)

        # Mejora del botón "Cargar resumen de registros"
        load_button = QPushButton("Cargar resumen de registros")
        load_button.clicked.connect(self.load_summary)
        load_button.setStyleSheet(
            """
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
        )
        info_layout.addWidget(load_button)

        self.central_widget.addTab(info_widget, "Resumen")

    def load_summary(self):
        with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        registros = self.get_summary_records()

        for fecha, data in registros.items():
            fecha_frame = QFrame()
            fecha_frame.setStyleSheet(
                """
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 10px;
                    margin: 10px;
                    padding: 10px;
                }
            """
            )
            fecha_layout = QVBoxLayout(fecha_frame)

            fecha_label = QLabel(f"Fecha: {fecha}")
            fecha_label.setStyleSheet(
                """
                font-weight: bold;
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 10px;
            """
            )
            fecha_layout.addWidget(fecha_label)

            for entry in data:
                entry_frame = QFrame()
                entry_frame.setStyleSheet(
                    """
                    QFrame {
                        background-color: white;
                        border: 1px solid #bdc3c7;
                        border-radius: 5px;
                        margin: 5px;
                        padding: 10px;
                    }
                """
                )
                entry_layout = QVBoxLayout(entry_frame)

                mozo_label = QLabel(f"Mozo: {entry['mozo']}")
                mozo_label.setStyleSheet("font-weight: bold; color: #2980b9;")
                entry_layout.addWidget(mozo_label)

                mesa_label = QLabel(f"Mesa: {entry['mesa']}")
                entry_layout.addWidget(mesa_label)

                hora_label = QLabel(f"Hora Apertura: {entry['hora']}")
                entry_layout.addWidget(hora_label)

                hora_cierre_label = QLabel(f"Hora Cierre: {entry['hora_cierre']}")
                entry_layout.addWidget(hora_cierre_label)

                productos_label = QLabel(f"Productos: {', '.join(entry['productos'])}")
                productos_label.setWordWrap(True)
                productos_label.setStyleSheet("color: #27ae60;")
                entry_layout.addWidget(productos_label)

                total_general = 0
                for producto in entry['productos']:
                    for categoria in menu["menu"]:
                        for pedido in menu["menu"][categoria]:
                            if producto == pedido["name"]:
                                precio = pedido["price"]
                                total = precio
                                total_general += total
                               
                with open(os.path.join(base_dir, "../Docs/config.json"), "r", encoding="utf-8") as f:
                    config = json.load(f)
                    precio_cubiertos = config[0].get("precio_cubiertos", 0)
                total_general += int(precio_cubiertos)
                
                Precio_total_label = QLabel(f"Total: ${total_general}")
                entry_layout.addWidget(Precio_total_label)

                fecha_layout.addWidget(entry_frame)

            self.scroll_layout.addWidget(fecha_frame)

    def get_summary_records(self):
        fecha_hoy = datetime.now().date()
        fecha_txt = datetime.now()
        fecha = fecha_txt.strftime("%H:%M")

        resumen = {}
        docs_dir = os.path.join(base_dir, "../Docs/Registro")
        data = Mostrar_Mozos(self.pagina_mozos)

        for filename in os.listdir(docs_dir):
            for mozo in enumerate(data):
                if filename == f"{fecha_hoy}_{mozo[1][1]}.json":
                    if filename.endswith(".json"):
                        mozo_name = filename.replace(f"{fecha_hoy}_", "").replace(".json", "")
                        date_str = filename.replace(f"_{mozo_name}", "").replace(".json", "")
                        
                        with open(os.path.join(docs_dir, filename), "r", encoding="utf-8") as file:
                            entries = json.load(file)

                        if date_str not in resumen:
                            resumen[date_str] = []
                        for entry in entries:
                            resumen[date_str].append(
                                {
                                    "mozo": mozo_name,
                                    "mesa": entry["Mesa"],
                                    "hora": entry["Hora"],
                                    "hora_cierre": entry["Hora_cierre"],
                                    "productos": entry["productos"],
                                }
                            )
        return resumen

    def setup_menu_tab(self):

        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)

        # Add Product section
        add_product_layout = QGridLayout()
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Categoría")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del Producto")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Precio")
        add_product_button = QPushButton("Agregar Producto")
        add_product_button.clicked.connect(self.add_product)
        add_product_button.setStyleSheet(
            """
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
        )

        add_product_layout.addWidget(QLabel("Categoría:"), 0, 0)
        add_product_layout.addWidget(self.category_input, 0, 1)
        add_product_layout.addWidget(QLabel("Nombre:"), 1, 0)
        add_product_layout.addWidget(self.name_input, 1, 1)
        add_product_layout.addWidget(QLabel("Precio:"), 2, 0)
        add_product_layout.addWidget(self.price_input, 2, 1)
        add_product_layout.addWidget(add_product_button, 3, 0, 1, 2)

        menu_layout.addLayout(add_product_layout)

        # Menu Table
        self.menu_table = QTableWidget(0, 4)
        self.menu_table.setHorizontalHeaderLabels(
            ["Nombre", "Categoría", "Precio", "Acciones"]
        )
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        menu_layout.addWidget(self.menu_table)

        menu_pagination_layout = QHBoxLayout()
        
        self.btn_anterior_menu = QPushButton("Página Anterior", self)
        self.btn_anterior_menu.setStyleSheet(
            """
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
        )
        self.btn_anterior_menu.clicked.connect(self.cargar_anterior_menu)
        
        self.btn_siguiente_menu = QPushButton("Siguiente Página", self)
        self.btn_siguiente_menu.setStyleSheet(
            """
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
        )
        self.btn_siguiente_menu.clicked.connect(self.cargar_siguiente_menu)
        
        menu_pagination_layout.addWidget(self.btn_anterior_menu)
        menu_pagination_layout.addWidget(self.btn_siguiente_menu)
        menu_pagination_layout.addStretch()  # Esto empujará los botones hacia la izquierda
        
        menu_layout.addLayout(menu_pagination_layout)

        # Refresh button
        refresh_button = QPushButton("Actualizar Menu")
        refresh_button.clicked.connect(self.load_menu)
        refresh_button.setStyleSheet(
            """
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
        )
        menu_layout.addWidget(refresh_button)

        bottom_layout = QHBoxLayout()
    
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.btn_anterior_menu)
        pagination_layout.addWidget(self.btn_siguiente_menu)
        pagination_layout.addStretch()
        
        bottom_layout.addLayout(pagination_layout)
        bottom_layout.addStretch()
        bottom_layout.addWidget(refresh_button)
        
        menu_layout.addLayout(bottom_layout)

        self.central_widget.addTab(menu_widget, "Gestión de Menú")

        # Load initial menu data
        self.load_menu()

    def add_product(self):
        category = self.category_input.text()
        name = self.name_input.text()
        price = self.price_input.text()

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", category):
            QMessageBox.warning(
                self, "Error", "Porfavor, no ingrese caracteres invalido."
            )
            return
        elif not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", name):
            QMessageBox.warning(
                self, "Error", "Porfavor, no ingrese caracteres invalido."
            )
            return
        if category and name and price:
            try:
                price = float(price)
                Cargar_Producto(category, name, price)
                self.category_input.clear()
                self.name_input.clear()
                self.price_input.clear()
                self.load_menu()
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "El precio debe ser un número válido."
                )
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

    def cargar_siguiente_menu(self):
        self.pagina_menu += 1
        self.load_menu()

    def cargar_anterior_menu(self):
        if self.pagina_menu > 0:
            self.pagina_menu -= 1
            self.load_menu()

    def load_menu(self):
        menu_items = Mostrar_Menu(self.pagina_menu)
        if menu_items != []:
            self.menu_table.setRowCount(0)
            self.menu_table.setEditTriggers(QTableWidget.NoEditTriggers)
            for row, item in enumerate(menu_items):
                self.menu_table.insertRow(row)
                self.menu_table.setItem(row, 0, QTableWidgetItem(item[1]))  # Categoría
                self.menu_table.setItem(row, 1, QTableWidgetItem(item[0]))  # Nombre
                self.menu_table.setItem(row, 2, QTableWidgetItem(str(item[2])))  # Precio

                # Edit and Delete buttons
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.setContentsMargins(0, 0, 0, 0)

                edit_button = QPushButton("Editar")
                edit_button.clicked.connect(lambda _, r=row: self.edit_product(r))
                edit_button.setStyleSheet(
                    """
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
                )
                delete_button = QPushButton("Eliminar")
                delete_button.clicked.connect(lambda _, n=item[1]: self.delete_product(n))
                delete_button.setStyleSheet(
                    """
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
                )

                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)

                self.menu_table.setCellWidget(row, 3, button_widget)

            Recargar_menu()  # Update the JSON file
        else:
            self.pagina_menu -= 1

    def edit_product(self, row):
        name = self.menu_table.item(row, 0).text()
        category = self.menu_table.item(row, 1).text()
        price = self.menu_table.item(row, 2).text()

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar Producto: {name}")
        dialog_layout = QVBoxLayout(dialog)

        category_input = QLineEdit(category)
        name_input = QLineEdit(name)
        price_input = QLineEdit(price)

        dialog_layout.addWidget(QLabel("Categoría:"))
        dialog_layout.addWidget(category_input)
        dialog_layout.addWidget(QLabel("Nombre:"))
        dialog_layout.addWidget(name_input)
        dialog_layout.addWidget(QLabel("Precio:"))
        dialog_layout.addWidget(price_input)

        save_button = QPushButton("Guardar")
        save_button.setStyleSheet(
            """
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
        )
        save_button.clicked.connect(
            lambda: self.save_product_edit(
                name,
                category_input.text(),
                name_input.text(),
                price_input.text(),
                dialog,
            )
        )
        dialog_layout.addWidget(save_button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def save_product_edit(self, old_name, new_category, new_name, new_price, dialog):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", new_category):
            QMessageBox.warning(
                self, "Error", "Porfavor, no ingrese caracteres invalido."
            )
            return
        elif not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", new_name):
            QMessageBox.warning(
                self, "Error", "Porfavor, no ingrese caracteres invalido."
            )
            return
        try:
            new_price = float(new_price)
            Modificar_Menu(old_name, "Categoria", f"'{new_category}'")
            Modificar_Menu(old_name, "Nombre", f"'{new_name}'")
            Modificar_Menu(old_name, "Precio", new_price)
            self.load_menu()
            dialog.close()
        except ValueError:
            QMessageBox.warning(dialog, "Error", "El precio debe ser un número válido.")

    def delete_product(self, name):
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el producto {name}?",

            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            #print(name)
            Eliminar_Producto(name)
            self.load_menu()

    def setup_mozos_tab(self):
        mozos_widget = QWidget()
        mozos_layout = QVBoxLayout(mozos_widget)
        mozos_layout.setContentsMargins(10, 10, 10, 10)

        # Sección para agregar mozo
        add_mozo_layout = QHBoxLayout()
        self.mozo_name_input = QLineEdit()
        self.mozo_name_input.setPlaceholderText("Nombre del Mozo")
        self.mozo_name_input.setStyleSheet(
            """
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 14px;
            }
        """
        )
        add_mozo_button = QPushButton("Agregar Mozo")
        add_mozo_button.setStyleSheet(
            """
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
        )
        add_mozo_button.clicked.connect(self.add_mozo)
        add_mozo_layout.addWidget(self.mozo_name_input, 3)
        add_mozo_layout.addWidget(add_mozo_button, 1)
        mozos_layout.addLayout(add_mozo_layout)

        # Tabla de Mozos
        self.mozos_table = QTableWidget(0, 7)
        self.mozos_table.setHorizontalHeaderLabels(["Nombre", "Código", "Hora de entrada", "Hora de salida", "Fecha", "Mesas Totales", "Acciones",])

        self.mozos_table.setStyleSheet(
            """
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
        )
        self.mozos_table.horizontalHeader().setStretchLastSection(True)
        self.mozos_table.verticalHeader().setDefaultSectionSize(40)
        self.mozos_table.setMinimumHeight(300)  # Establecer una altura mínima
        mozos_layout.addWidget(self.mozos_table)

        pagination_layout = QHBoxLayout()
    
        self.btn_anterior_mozos = QPushButton("Página Anterior", self)
        self.btn_anterior_mozos.setStyleSheet(
            """
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
        )
        self.btn_anterior_mozos.clicked.connect(self.cargar_anterior_mozos)
        
        self.btn_siguiente_mozos = QPushButton("Siguiente Página", self)
        self.btn_siguiente_mozos.setStyleSheet(
            """
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
        )
        self.btn_siguiente_mozos.clicked.connect(self.cargar_siguiente_mozos)
        
        pagination_layout.addWidget(self.btn_anterior_mozos)
        pagination_layout.addWidget(self.btn_siguiente_mozos)
        pagination_layout.addStretch()  # Esto empujará los botones hacia la izquierda
        
        mozos_layout.addLayout(pagination_layout)

        # Modificar el botón de actualizar
        self.refresh_button = QPushButton("Actualizar Lista")
        self.refresh_button.setStyleSheet(
            """
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
        )
        self.refresh_button.clicked.connect(self.update_current_view)
        mozos_layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

        bottom_layout = QHBoxLayout()
    
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.btn_anterior_mozos)
        pagination_layout.addWidget(self.btn_siguiente_mozos)
        pagination_layout.addStretch()
        
        bottom_layout.addLayout(pagination_layout)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.refresh_button)
        
        mozos_layout.addLayout(bottom_layout)

        self.central_widget.addTab(mozos_widget, "Gestión de Mozos")

        # Cargar datos iniciales
        self.load_mozos()

    def update_current_view(self):
        self.load_mozos()
        
        # Asegurar que la tabla ocupe todo el espacio disponible
        self.mozos_table.horizontalHeader().setStretchLastSection(True)

    def add_mozo(self):
        name = self.mozo_name_input.text()
        if re.search(r'[^a-zA-Z ]', name):
            QMessageBox.warning(
                self, "Error", "Por favor, no Ingrese caracteres especiales."
            )

        if name:
            response =Alta_Mozo(name)
            if response:
                QMessageBox.warning(
                    self, "Mozo no agregado", "Nombre de Mozo duplicado, por favor intente otro nombre"
                )
            self.mozo_name_input.clear()
            self.load_mozos()
        else:
            QMessageBox.warning(
                self, "Error", "Por favor, ingrese un nombre para el mozo."
            )

    def cargar_siguiente_mozos(self):
        self.pagina_mozos += 1
        self.load_mozos()

    def cargar_anterior_mozos(self):
        if self.pagina_mozos > 0:
            self.pagina_mozos -= 1
            self.load_mozos()

    def load_mozos(self):   
        fecha_hoy = datetime.now().date()
        fecha_txt = datetime.now()
        fecha = fecha_txt.strftime("%H:%M")

        mozos = Mostrar_Mozos(self.pagina_mozos)
        if mozos != []:
            self.mozos_table.setRowCount(0)
            self.mozos_table.setEditTriggers(QTableWidget.NoEditTriggers)
            registry_file = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")
            
            # Preparar datos del registro una sola vez
            registry_file = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")
            try:
                with open(registry_file, "r", encoding="utf-8") as file:
                    datos_registro = json.load(file)
            except FileNotFoundError:
                datos_registro = []
                with open(registry_file, 'w') as file:
                    json.dump(datos_registro, file)
            
            # Crear un diccionario para búsqueda rápida
            registro_dict = {list(reg.keys())[0]: list(reg.values())[0] for reg in datos_registro}
            
            # Preparar todos los datos antes de actualizar la tabla
            table_data = []
            for Mozo in mozos:
                row_data = []
                # Datos básicos del mozo
                nombre_mozo = Mozo[1]
                row_data.extend([nombre_mozo, Mozo[2]])
                
                # Obtener datos del registro si existen
                if nombre_mozo in registro_dict:
                    detalles = registro_dict[nombre_mozo]
                    row_data.extend([
                        detalles.get("Horario_entrada", ""),
                        detalles.get("Horario_salida", ""),
                        detalles.get("Fecha", ""),
                        str(detalles.get("Mesas totales", ""))
                    ])
                else:
                    row_data.extend(["", "", "", ""])
                
                table_data.append(row_data)
            
            # Actualizar la tabla de una sola vez
            self.mozos_table.setRowCount(len(table_data))
            
            # Crear los estilos de los botones una sola vez
            edit_button_style = """
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
            
            delete_button_style = """
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
            
            # Actualizar la tabla
            for row, row_data in enumerate(table_data):
                # Insertar datos en las columnas
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(data)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.mozos_table.setItem(row, col, item)
                
                # Crear widget de botones
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.setContentsMargins(5, 2, 5, 2)
                button_layout.setSpacing(10)
                
                edit_button = QPushButton("Editar")
                edit_button.setStyleSheet(edit_button_style)
                edit_button.clicked.connect(lambda _, r=row: self.edit_mozo(r))
                
                delete_button = QPushButton("Eliminar")
                delete_button.setStyleSheet(delete_button_style)
                delete_button.clicked.connect(lambda _, n=row_data[0]: self.delete_mozo(n))
                
                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)
                button_layout.addStretch()
                
                self.mozos_table.setCellWidget(row, 6, button_widget)
            
            # Ajustar tamaños de columnas una sola vez al final
            self.mozos_table.resizeColumnsToContents()
            self.mozos_table.setColumnWidth(0, 150)
            self.mozos_table.setColumnWidth(3, 125)
        else:
            self.pagina_mozos -= 1

    def edit_mozo(self, row):
        name = self.mozos_table.item(row, 0).text()
        code = self.mozos_table.item(row, 1).text()

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", name) :
            QMessageBox.warning(
                self, "Error", "Por favor, no Ingrese caracteres especiales."
            )
        else:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Editar Mozo: {name}")
            dialog.setFixedSize(400, 250)
            dialog.setStyleSheet(
                """
                QDialog {
                    background-color: #f5f5f5;
                    border-radius: 10px;
                }
                QLabel {
                    font-size: 14px;
                    color: #333;
                    min-width: 60px;
                }
                QLineEdit {
                    padding: 10px;
                    font-size: 14px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: white;
                }
                QLineEdit:disabled {
                    background-color: #e0e0e0;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """
            )

            layout = QVBoxLayout(dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            code_layout = QHBoxLayout()
            code_label = QLabel("Código:")
            code_input = QLineEdit(code)
            code_input.setDisabled(True)
            code_layout.addWidget(code_label)
            code_layout.addWidget(code_input)
            layout.addLayout(code_layout)

            name_layout = QHBoxLayout()
            name_label = QLabel("Nombre:")
            name_input = QLineEdit(name)
            name_input.setPlaceholderText("Ingresa el nombre del mozo")
            name_layout.addWidget(name_label)
            name_layout.addWidget(name_input)
            layout.addLayout(name_layout)

            save_button = QPushButton("Guardar")
            save_button.clicked.connect(
                lambda: self.save_mozo_edit(name, name_input.text(), dialog)
            )
            layout.addWidget(save_button, alignment=Qt.AlignCenter)

            dialog.setLayout(layout)
            dialog.exec_()

    def save_mozo_edit(self, old_name, new_name, dialog):
        if old_name != new_name:
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", new_name):
                QMessageBox.warning(
                    self, "Error", "Por favor, no Ingrese caracteres especiales."
                )
            else:
                Editar_Mozo(old_name, "Nombre", new_name)
                self.load_mozos()
                dialog.close()

    def delete_mozo(self, name):
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al mozo {name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            Eliminar_empleados(name)
            self.load_mozos()

    def set_style(self):
        # Paleta de colores mejorada
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#F0F0F0"))
        palette.setColor(QPalette.WindowText, QColor("#333333"))
        palette.setColor(QPalette.Button, QColor("#4CAF50"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, QColor("#009688"))
        self.setPalette(palette)

        # Estilo general
        self.setStyleSheet(
            """
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
        )

    def ajustar_tamano_pantalla(self):
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.showMaximized()

    def setup_main_tab(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sección izquierda para mesas
        mesas_scroll = QScrollArea()
        mesas_scroll.setWidgetResizable(True)
        mesas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mesas_widget = QWidget()
        self.mesas_layout = QGridLayout(mesas_widget)
        self.mesas_layout.setSpacing(20)

        mesas_scroll.setWidget(mesas_widget)

        # Estilo para el QScrollArea (mesas_scroll)
        mesas_scroll.setStyleSheet(
            """
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
        )

        # Sección derecha para pedidos y registro
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Estilo para el widget derecho
        right_widget.setStyleSheet(
            """
            QWidget {
                background-color: #FAFAFA;
                border-radius: 10px;
            }
        """
        )

        # Área de pedidos
        pedidos_widget = QWidget()
        pedidos_layout = QVBoxLayout(pedidos_widget)
        pedidos_label = QLabel("Datos del pedido:")
        pedidos_layout.addWidget(pedidos_label)

        # Estilo para las etiquetas
        pedidos_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            }
        """
        )

        self.json_input = QTextEdit()
        self.json_input.setFont(QFont("Courier New", 12))
        self.json_input.setPlaceholderText("Datos del pedido se mostrarán aquí")
        self.json_input.setStyleSheet(
            """
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
        )
        self.json_input.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )

        self.json_input.setReadOnly(True)
        pedidos_layout.addWidget(self.json_input)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(pedidos_widget)
        right_layout.addWidget(splitter)

        # Estilo para el QSplitter
        splitter.setStyleSheet(
            """
            QSplitter::handle {
                background-color: #E0E0E0;
            }
        """
        )

        main_layout.addWidget(mesas_scroll, 6)
        main_layout.addWidget(right_widget, 4)

        self.central_widget.addTab(main_widget, "Restaurante")

        self.cargar_mesas()

    def cargar_mesas(self):
        # Limpiar el layout de mesas existente
        for i in reversed(range(self.mesas_layout.count())): 
            self.mesas_layout.itemAt(i).widget().setParent(None)
        
        directorio_json = os.path.join(base_dir, "../tmp")
        archivos_json = [f for f in os.listdir(directorio_json) if f.endswith(".json")]
        archivos_json_Final = sorted(
            archivos_json,
            key=lambda archivo: int(archivo.replace("Mesa ", "").replace(".json", "")),
            reverse=False,
        )

        for archivo in archivos_json_Final:
            nombre_mesa = archivo.replace("Mesa ", "").replace(".json", "")

            try:
                mesa_num = int(nombre_mesa)
                mesa_button = QPushButton(f"Mesa {mesa_num}")
                mesa_button.setFont(QFont("Arial", 14, QFont.Bold))
                mesa_button.setMinimumSize(200, 150)
                mesa_button.clicked.connect(
                    lambda _, num=mesa_num: self.mesa_clicked(num)
                )

                with open(
                    os.path.join(directorio_json, archivo), "r", encoding="utf-8"
                ) as file:
                    mesa_data = json.load(file)

                if mesa_data.get("Disponible", True):
                    mesa_button.setStyleSheet(
                        """
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
                    )
                else:
                    mesa_button.setStyleSheet(
                        """
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
                    )

                self.mesas_layout.addWidget(
                    mesa_button, (mesa_num - 1) // 3, (mesa_num - 1) % 3
                )

            except ValueError:
                print(f"Error: El nombre del archivo '{archivo}' no es válido")

    def mesa_clicked(self, mesa_num):
        print(f"Clic en mesa {mesa_num}")
        self.cargar_json(mesa_num)

    def cargar_json(self, mesa_num):
        print(f"Cargando JSON para mesa {mesa_num}")
        ruta_archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa_num}.json")
        print(f"Ruta del archivo: {ruta_archivo}")
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                pedido_json = json.load(f)
                self.procesar_pedido_con_json(pedido_json)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al cargar JSON para Mesa {mesa_num}: {e}")

    def procesar_pedido_con_json(self, pedido_json):
        with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)

        mesa = pedido_json.get("Mesa", "")
        fecha = pedido_json.get("Fecha", "")
        hora = pedido_json.get("Hora", "")
        mozo = pedido_json.get("Mozo", "")
        productos = pedido_json.get("productos", [])
        cantidad_comensales = pedido_json.get("cantidad_comensales", 0)
        comensales_infantiles = pedido_json.get("comensales_infantiles", 0)
        aclaraciones = pedido_json.get("Extra", "")

        estado = "Disponible" if pedido_json.get("Disponible", True) else "Ocupada"

        if productos or cantidad_comensales > 0 or comensales_infantiles > 0:
            fecha_formateada = self.formatear_fecha(fecha)
            comanda_texto = f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .comanda {{
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
            </style>
            <div class="comanda">
                <h2>COMANDA MESA: {mesa}</h2>
                <div class="info">
                    <p><strong>Fecha:</strong> {fecha}</p>
                    <p><strong>Hora:</strong> {hora}</p>
                    <p><strong>Mozo:</strong> {mozo}</p>
                    <p><strong>Comensales:</strong> {cantidad_comensales} (Infantiles: {comensales_infantiles})</p>
                </div>
                <div class="aclaraciones">
                    <p><strong>Aclaraciones:</strong> {aclaraciones if aclaraciones else "No hay aclaraciones sobre el pedido"}</p>
                </div>

                <table>
                    <tr>
                        <th>Item</th>
                        <th>Cant.</th>
                        <th>Precio</th>
                        <th>Total</th>
                    </tr>
            """

            total_general = 0
            for producto in productos:
                for categoria in menu["menu"]:
                    for pedido in menu["menu"][categoria]:
                        if producto == pedido["name"]:
                            precio = pedido["price"]
                            total = precio
                            total_general += total
                            comanda_texto += f"""
                            <tr>
                                <td>{producto}</td>
                                <td>1</td>
                                <td>${precio:.2f}</td>
                                <td>${total:.2f}</td>
                            </tr>
                            """

            comanda_texto += f"""
                <tr class="total">
                    <td colspan="3">Total General:</td>
                    <td>${total_general:.2f}</td>
                </tr>
            </table>
            </div>
            """
        else:
            comanda_texto = f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .comanda-vacia {{
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
                    color: {('#4CAF50' if estado == 'Disponible' else '#F44336')};
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
            </style>
            <div class="comanda-vacia">
                <h2>MESA {mesa}</h2>
                <div class="icon">📋</div>
                <p>No hay pedidos registrados para esta mesa.</p>
                <p>Esta mesa está actualmente:</p>
                <p class="estado">{estado.upper()}</p>
                <div class="aclaraciones">
                    <p><strong>Aclaraciones:</strong> {aclaraciones if aclaraciones else "No hay aclaraciones sobre el pedido"}</p>
                </div>
            </div>
            """

        self.json_input.setHtml(comanda_texto)

    def formatear_fecha(self, fecha_str):
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
            return fecha_obj.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return fecha_str

    def formatear_fecha(self, fecha_str):
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
            return fecha_obj.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return fecha_str

    def setup_config_tab(self):
        """Configura la pestaña de configuración con opciones."""
        config_widget = QWidget()
        config_layout = QGridLayout(config_widget)  # Usar QGridLayout para disposición en cuadrícula

        # Crear cartas dinámicamente
        self.create_config_card(
            config_layout,
            "💰",
            "Precio de cubiertos",
            self.cubiertos_input,
            None,
            self.save_config,
            0, 0  # Posición en la cuadrícula
        )

        self.create_config_card(
            config_layout,
            "🍽️",
            "Cantidad de mesas",
            self.mesas_input,
            None,
            self.save_config,
            0, 1  # Posición en la cuadrícula
        )
        self.central_widget.addTab(config_widget, "Configuración")

    def create_config_card(self, layout, emoji, label_text, input_ref, lista_items, save_callback, row, col):
        """Crea una carta de configuración."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                min-height: 150px;
            }
            """
        )
        card_layout = QVBoxLayout(card)

        emoji_label = QLabel(emoji)
        emoji_label.setAlignment(Qt.AlignCenter)
        emoji_label.setStyleSheet("font-size: 64px;")
        card_layout.addWidget(emoji_label)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        card_layout.addWidget(label)

        if isinstance(input_ref, QComboBox):
            input_ref.addItems(lista_items)  # Ejemplo de opciones
            input_ref.setStyleSheet(
                """
                QComboBox {
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    padding: 12px;
                    font-size: 18px;
                    background-color: #FFFFFF;
                }
                QComboBox:hover {
                    background-color: #4CAF50;
                }
                QComboBox::drop-down {
                    border: none;
                    background-color: #4CAF50;
                    width: 25px;
                }
                QComboBox QAbstractItemView {
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #4CAF50;
                    color: #000000;
                    selection-background-color: #4CAF50;
                    selection-color: #45a049;
                    border-radius: 10px;
                    border: 1px solid #4CAF50;
                }
                """
            )
        else:
            input_ref.setStyleSheet(
                """
                QLineEdit {
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    padding: 12px;
                    font-size: 18px;
                }
                """
            )
        card_layout.addWidget(input_ref)

        save_button = QPushButton("Guardar cambios")
        save_button.clicked.connect(lambda: save_callback(label_text))
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        card_layout.addWidget(save_button)

        layout.addWidget(card, row, col)  # Añadir la carta a la posición especificada en la cuadrícula

    def save_config(self, text_input):
        """Guarda las configuraciones ingresadas por el usuario."""
        try:
            precio_cubiertos = self.cubiertos_input.text()
            cantidad_mesas = self.mesas_input.text()
            if os.path.exists(os.path.join(base_dir, "../Docs/Config.json")):
                with open(os.path.join(base_dir, "../Docs/Config.json"), "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                config = [
                    {"precio_cubiertos": 0},
                    {"cantidad_mesas": 0},
                ]
            print(text_input)   

            if text_input == "Precio de cubiertos":
                config[0]["precio_cubiertos"] = str(precio_cubiertos)
            elif text_input == "Cantidad de mesas":
                config[1]["cantidad_mesas"] = int(cantidad_mesas)

                self.update_mesas_count(int(cantidad_mesas))

            with open(os.path.join(base_dir, "../Docs/Config.json"), "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            QMessageBox.information(self, "Configuración Guardada", "Las configuraciones han sido guardadas exitosamente.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores válidos para las configuraciones.")
    
    def update_mesas_count(self, new_count):
        # Actualizar la cantidad de mesas en el sistema
        from Back.Menu_de_mesas_Back import creas_mesas, crea_mesas_tmp
        creas_mesas(new_count)  # Asegúrate de que esta función esté correctamente implementada en la API
        crea_mesas_tmp()  # Asegúrate de que esta función también esté correctamente implementada
        self.cargar_mesas()  # Recargar las mesas en la interfaz

    def load_cubiertos_price(self):
        try:
            with open(os.path.join(base_dir, "../Docs/config.json"), "r") as f:
                config = json.load(f)
                return config[0].get("precio_cubiertos", 0)
        except FileNotFoundError:
            return 0
    def load_mesas_count(self):
        try:
            with open(os.path.join(base_dir, "../Docs/config.json"), "r") as f:
                config = json.load(f)
                return config[1].get("cantidad_mesas", 1)
        except FileNotFoundError:
            return 1

if __name__ == "__main__":
    def exception_hook(exctype, value, traceback):
        print(f"Excepción no manejada: {exctype}, {value}")
        print("Traceback:")
        print("".join(traceback.format_tb(traceback)))
        sys.__excepthook__(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(
        """
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
    )

    ventana = RestaurantInterface()
    ventana.showMaximized()
    sys.exit(app.exec_())