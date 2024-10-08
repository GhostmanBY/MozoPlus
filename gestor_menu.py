from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QDialog, QMessageBox
from Back.Panel_Admin_Back import Cargar_Producto, Mostrar_Menu, Modificar_Menu, Eliminar_Producto
import re

def setup_menu_tab(self):
    menu_widget = QWidget()
    menu_layout = QVBoxLayout(menu_widget)

    add_product_layout = QGridLayout()
    self.category_input = QLineEdit()
    self.category_input.setPlaceholderText("Categoría")
    self.name_input = QLineEdit()
    self.name_input.setPlaceholderText("Nombre del Producto")
    self.price_input = QLineEdit()
    self.price_input.setPlaceholderText("Precio")
    add_product_button = QPushButton("Agregar Producto")
    add_product_button.clicked.connect(lambda: add_product(self))
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

    self.menu_table = QTableWidget(0, 4)
    self.menu_table.setHorizontalHeaderLabels(
        ["Nombre", "Categoría", "Precio", "Acciones"]
    )
    self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    menu_layout.addWidget(self.menu_table)

    refresh_button = QPushButton("Actualizar Menu")
    refresh_button.clicked.connect(lambda: load_menu(self))
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

    self.central_widget.addTab(menu_widget, "Gestión de Menú")

    load_menu(self)

def add_product(self):
    category = self.category_input.text()
    name = self.name_input.text()
    price = self.price_input.text()
    
    if re.search(r'[^a-zA-Z ]', name) :
        QMessageBox.warning(
            self, "Error", "Por favor, no Ingrese caracteres especiales."
        )
    elif re.search(r'[^0-9 ]', price):
        QMessageBox.warning(
            self, "Error", "Por favor, solo ingrese numeros."
        )
    elif re.search(r'[^a-zA-Z ]', category):
        QMessageBox.warning(
            self, "Error", "Por favor, no Ingrese caracteres especiales."
        )

    if category and name and price:
        try:
            price = float(price)
            Cargar_Producto(category, name, price)
            self.category_input.clear()
            self.name_input.clear()
            self.price_input.clear()
            load_menu(self)
        except ValueError:
            QMessageBox.warning(
                self, "Error", "El precio debe ser un número válido."
            )
    else:
        QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")

def load_menu(self):
    menu_items = Mostrar_Menu()
    self.menu_table.setRowCount(0)
    for row, item in enumerate(menu_items):
        self.menu_table.insertRow(row)
        self.menu_table.setItem(row, 0, QTableWidgetItem(item[1]))
        self.menu_table.setItem(row, 1, QTableWidgetItem(item[0]))
        self.menu_table.setItem(row, 2, QTableWidgetItem(str(item[2])))

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        edit_button = QPushButton("Editar")
        edit_button.clicked.connect(lambda _, r=row: edit_product(self, r))
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
        delete_button.clicked.connect(lambda _, n=item[1]: delete_product(self, n))
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

def edit_product(self, row):
    name = self.menu_table.item(row, 1).text()
    category = self.menu_table.item(row, 0).text()
    price = self.menu_table.item(row, 2).text()

    if re.search(r'[^a-zA-Z ]', name) :
        QMessageBox.warning(
            self, "Error", "Por favor, no Ingrese caracteres especiales."
        )
    elif re.search(r'[^0-9 ]', price):
        QMessageBox.warning(
            self, "Error", "Por favor, solo ingrese numeros."
        )
    elif re.search(r'[^a-zA-Z ]', category):
        QMessageBox.warning(
            self, "Error", "Por favor, no Ingrese caracteres especiales."
        )

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
        lambda: save_product_edit(self, name, category_input.text(), name_input.text(), price_input.text(), dialog)
    )
    dialog_layout.addWidget(save_button)

    dialog.setLayout(dialog_layout)
    dialog.exec_()

def save_product_edit(self, old_name, new_category, new_name, new_price, dialog):
    try:
        new_price = float(new_price)
        Modificar_Menu(old_name, "Categoria", f"'{new_category}'")
        Modificar_Menu(old_name, "Nombre", f"'{new_name}'")
        Modificar_Menu(old_name, "Precio", new_price)
        load_menu(self)
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
        Eliminar_Producto(name)
        load_menu(self)