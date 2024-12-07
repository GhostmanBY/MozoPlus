import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QHeaderView,
    QMessageBox,
    QDialog,
)

from Back.Panel_Admin_Back import (
    Mostrar_Menu,
    Modificar_Menu,
    Cargar_Producto,
    Eliminar_Producto,
    Recargar_menu,
)

from Front.Static.QQS_GUI_TAB_Tables import (
    Boton_Agregar,
    Estilo_Tabla,
    Botones_Navegacion,
    Boton_Editar,
    Boton_Eliminar,
    Ventana_Editar
)
from Front.Static.Utils import Utils

base_dir = os.path.dirname(os.path.abspath(__file__))

class Menu_Tab(QWidget, Utils):
    """
    Pestaña para gestionar el menú del restaurante
    """
    def __init__(self):
        super().__init__()
        self.pagina_menu = 0
        
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)

        self.add_product_layout = QGridLayout()
        self.category_input = QLineEdit()

        self.name_input = QLineEdit()
    
        self.price_input = QLineEdit()
    
        self.add_product_button = QPushButton("Agregar Producto")
    
        self.menu_table = QTableWidget(0, 4)

        self.menu_pagination_layout = QHBoxLayout()
        
        self.btn_anterior_menu = QPushButton("Página Anterior")
        
        self.btn_siguiente_menu = QPushButton("Siguiente Página")
        
        self.refresh_button = QPushButton("Actualizar Menu")
    
        self.bottom_layout = QHBoxLayout()
    
        self.pagination_layout = QHBoxLayout()

        #llamar funcion
        self.setup_menu_tab()

    def setup_menu_tab(self):
        # Add Product section
        self.category_input.setPlaceholderText("Categoría")
        
        self.name_input.setPlaceholderText("Nombre del Producto")
        
        self.price_input.setPlaceholderText("Precio")
        
        self.add_product_button.clicked.connect(self.add_product)
        self.add_product_button.setStyleSheet(Boton_Agregar)

        self.add_product_layout.addWidget(QLabel("Categoría:"), 0, 0)
        self.add_product_layout.addWidget(self.category_input, 0, 1)
        self.add_product_layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.add_product_layout.addWidget(self.name_input, 1, 1)
        self.add_product_layout.addWidget(QLabel("Precio:"), 2, 0)
        self.add_product_layout.addWidget(self.price_input, 2, 1)
        self.add_product_layout.addWidget(self.add_product_button, 3, 0, 1, 2)

        self.menu_layout.addLayout(self.add_product_layout)

        # Menu Table
        self.menu_table.setHorizontalHeaderLabels(
            ["Nombre", "Categoría", "Precio", "Acciones"]
        )
        self.menu_table.setStyleSheet(Estilo_Tabla)
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.menu_layout.addWidget(self.menu_table)

        self.btn_anterior_menu.setStyleSheet(Botones_Navegacion)
        self.btn_anterior_menu.clicked.connect(self.cargar_anterior_menu)
        
        self.btn_siguiente_menu.setStyleSheet(Botones_Navegacion)
        self.btn_siguiente_menu.clicked.connect(self.cargar_siguiente_menu)
        
        self.menu_pagination_layout.addWidget(self.btn_anterior_menu)
        self.menu_pagination_layout.addWidget(self.btn_siguiente_menu)
        self.menu_pagination_layout.addStretch()  # Esto empujará los botones hacia la izquierda
        
        self.menu_layout.addLayout(self.menu_pagination_layout)

        # Refresh button
        self.refresh_button.clicked.connect(self.load_menu)
        self.refresh_button.setStyleSheet(Botones_Navegacion)
        self.menu_layout.addWidget(self.refresh_button)

        self.pagination_layout.addWidget(self.btn_anterior_menu)
        self.pagination_layout.addWidget(self.btn_siguiente_menu)
        self.pagination_layout.addStretch()
        
        self.bottom_layout.addLayout(self.pagination_layout)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.refresh_button)
        
        self.menu_layout.addLayout(self.bottom_layout)

        self.setLayout(self.menu_layout)

        # Load initial menu data
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
                edit_button.setStyleSheet(Boton_Editar)
                delete_button = QPushButton("Eliminar")
                delete_button.clicked.connect(lambda _, n=item[1]: self.delete_product(n))
                delete_button.setStyleSheet(Boton_Eliminar)

                button_layout.addWidget(edit_button)
                button_layout.addWidget(delete_button)

                self.menu_table.setCellWidget(row, 3, button_widget)

            Recargar_menu()  # Update the JSON file
        else:
            self.pagina_menu -= 1

    def add_product(self):
        category = self.category_input.text()
        name = self.name_input.text()
        price = self.price_input.text()

        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", category):
            QMessageBox.warning(
                self, "Error", "Porfavor, no ingrese caracteres invalido."
            )
            return
        elif not re.match(r"^[a-zA-ZéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", name):
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

    def edit_product(self, row):
        name = self.menu_table.item(row, 0).text()
        category = self.menu_table.item(row, 1).text()
        price = self.menu_table.item(row, 2).text()

        dialog = QDialog(self)
        dialog.setStyleSheet(Ventana_Editar)
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
        save_button.setStyleSheet(Ventana_Editar)
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
    
    def cargar_siguiente_menu(self):
        self.pagina_menu = self.siguiente(self.pagina_menu, "menu")
        self.load_menu()
    def cargar_anterior_menu(self):
        if self.pagina_menu > 0:
            self.pagina_menu = self.anterior(self.pagina_menu, "menu")
            self.load_menu()
