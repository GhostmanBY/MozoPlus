from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QLabel,QHeaderView
import os
import json
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from Back.Panel_Admin_Back import Alta_Mozo, Mostrar_Mozos, Editar_Mozo, Eliminar_empleados
from datetime import date

base_dir = os.path.dirname(os.path.abspath(__file__))
fecha_hoy = date.today().strftime("%Y-%m-%d")

def setup_mozos_tab(self):
    mozos_widget = QWidget()
    mozos_layout = QVBoxLayout(mozos_widget)
    mozos_layout.setContentsMargins(10, 10, 10, 10)

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
    add_mozo_button.clicked.connect(lambda: add_mozo(self))
    add_mozo_layout.addWidget(self.mozo_name_input, 3)
    add_mozo_layout.addWidget(add_mozo_button, 1)
    mozos_layout.addLayout(add_mozo_layout)

    self.toggle_view_button = QPushButton("Registro de Mozos")
    self.toggle_view_button.setStyleSheet(
        """
        QPushButton {
            background-color: #2196F3;
            color: white;
            padding: 5px 15px;
            border: none;
            border-radius: 3px;
            font-size: 14px;
            min-width: 150px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
    """
    )
    self.toggle_view_button.clicked.connect(lambda: toggle_mozo_view(self))
    mozos_layout.addWidget(self.toggle_view_button)

    self.mozos_table = QTableWidget(0, 4)
    self.mozos_table.setHorizontalHeaderLabels(
        ["ID", "Nombre", "Código", "Acciones"]
    )
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
    self.mozos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.mozos_table.verticalHeader().setDefaultSectionSize(40)
    self.mozos_table.setMinimumHeight(300)
    mozos_layout.addWidget(self.mozos_table)

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
    self.refresh_button.clicked.connect(lambda: update_current_view(self))
    mozos_layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

    self.central_widget.addTab(mozos_widget, "Gestión de Mozos")

    load_mozos(self)

def toggle_mozo_view(self):
    if self.toggle_view_button.text() == "Registro de Mozos":
        self.toggle_view_button.setText("Código de Mozos")
        self.mozos_table.setColumnCount(5)
        self.mozos_table.setHorizontalHeaderLabels(["Mozo", "Hora de entrada", "Hora de salida", "Fecha", "Mesas Totales"])
        load_mozo_registry(self)
    else:
        self.toggle_view_button.setText("Registro de Mozos")
        self.mozos_table.setColumnCount(4)
        self.mozos_table.setHorizontalHeaderLabels(["ID", "Nombre", "Código", "Acciones"])
        load_mozos(self)

def load_mozo_registry(self):
    current_width = self.mozos_table.width()
    current_height = self.mozos_table.height()
    
    self.mozos_table.setRowCount(0)
    registry_file = os.path.join(base_dir, f"Docs/registro_mozos_{fecha_hoy}.json")
    
    if os.path.exists(registry_file):
        with open(registry_file, "r", encoding="utf-8") as file:
            datos_registro = json.load(file)
            
        for fila, registro in enumerate(datos_registro):
            mozo = list(registro.keys())[0]
            detalles = registro[mozo]

            entrada = detalles.get("Horario_entrada", "")
            salida = detalles.get("Horario_salida", "")
            mesas_totales = str(detalles.get("Mesas totales", ""))
            fecha_disc = detalles.get("Fecha", "")

            self.mozos_table.insertRow(fila)
            item_mozo = QTableWidgetItem(mozo)
            item_mozo.setTextAlignment(Qt.AlignCenter)
            self.mozos_table.setItem(fila, 0, item_mozo)

            item_entrada = QTableWidgetItem(entrada)
            item_entrada.setTextAlignment(Qt.AlignCenter)
            self.mozos_table.setItem(fila, 1, item_entrada)

            item_salida = QTableWidgetItem(salida)
            item_salida.setTextAlignment(Qt.AlignCenter)
            self.mozos_table.setItem(fila, 2, item_salida)

            item_fecha_disc = QTableWidgetItem(fecha_disc)
            item_fecha_disc.setTextAlignment(Qt.AlignCenter)
            self.mozos_table.setItem(fila, 3, item_fecha_disc)

            item_mesas_totales = QTableWidgetItem(mesas_totales)
            item_mesas_totales.setTextAlignment(Qt.AlignCenter)
            self.mozos_table.setItem(fila, 4, item_mesas_totales)
    else:
        print(f"El archivo {registry_file} no existe.")

    self.mozos_table.setFixedWidth(current_width)
    self.mozos_table.setFixedHeight(current_height)
    
    self.mozos_table.resizeColumnsToContents()
    self.mozos_table.resizeRowsToContents()

def update_current_view(self):
    if self.toggle_view_button.text() == "Código de Mozos":
        load_mozo_registry(self)
    else:
        load_mozos(self)
    
    self.mozos_table.horizontalHeader().setStretchLastSection(True)
    self.mozos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

def add_mozo(self):
        name = self.mozo_name_input.text()
        if re.search(r'[^a-zA-Z ]', name):
            QMessageBox.warning(
                self, "Error", "Por favor, no Ingrese caracteres especiales."
            )

        if name:
            Alta_Mozo(name)
            self.mozo_name_input.clear()
            self.load_mozos()
        else:
            QMessageBox.warning(
                self, "Error", "Por favor, ingrese un nombre para el mozo."
            )

def load_mozos(self):
    mozos = Mostrar_Mozos()
    self.mozos_table.setRowCount(0)
    for row, mozo in enumerate(mozos):
        self.mozos_table.insertRow(row)
        self.mozos_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.mozos_table.setItem(row, 1, QTableWidgetItem(mozo[1]))
        self.mozos_table.setItem(row, 2, QTableWidgetItem(mozo[2]))

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(5, 2, 5, 2)
        button_layout.setSpacing(10)

        edit_button = QPushButton("Editar")
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
        edit_button.clicked.connect(lambda _, r=row: edit_mozo(self, r))

        delete_button = QPushButton("Eliminar")
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
        delete_button.clicked.connect(lambda _, n=mozo[1]: delete_mozo(self, n))

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addStretch()

        self.mozos_table.setCellWidget(row, 3, button_widget)

    self.mozos_table.resizeColumnsToContents()
    self.mozos_table.setColumnWidth(0, 50)
    self.mozos_table.setColumnWidth(3, 200)

def edit_mozo(self, row):
    name = self.mozos_table.item(row, 1).text()
    code = self.mozos_table.item(row, 0).text()

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
        lambda: save_mozo_edit(self, name, name_input.text(), dialog)
    )
    layout.addWidget(save_button, alignment=Qt.AlignCenter)

    dialog.setLayout(layout)
    dialog.exec_()

def save_mozo_edit(self, old_name, new_name, dialog):
    if old_name != new_name:
        Editar_Mozo(old_name, "Nombre", new_name)
        load_mozos(self)
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
        load_mozos(self)