import sys
import json
import os
import re
import datetime

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ruta_raiz)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog,
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime

from Back import (
    Eliminar_empleados,
    Mostrar_Mozos,
    Alta_Mozo,
    Editar_Mozo,
)

from Front.Static.QQS_GUI_TAB_Tables import (
    Entry_input,
    Boton_Agregar,
    Estilo_Tabla,
    Botones_Navegacion,
    Boton_Editar,
    Boton_Eliminar,
    Ventana_Editar
)

from Front.Static.Utils import Utils
base_dir = os.path.dirname(os.path.abspath(__file__))

class Mozos_Tab(QWidget, Utils):
    """
    Pestaña para gestionar el personal de mozos
    """
    def __init__(self):
        super().__init__()
        self.pagina_mozos = 0

        self.mozos_widget = QWidget()
        self.mozos_layout = QVBoxLayout(self.mozos_widget)
        self.mozos_layout.setContentsMargins(10, 10, 10, 10)

        self.add_mozo_layout = QHBoxLayout()
        self.mozo_name_input = QLineEdit()
        
        self.add_mozo_button = QPushButton("Agregar Mozo")
    
        self.mozos_table = QTableWidget(0, 7)
    
        self.pagination_layout = QHBoxLayout()
    
        self.refresh_button = QPushButton("Actualizar Lista")
        
        self.bottom_layout = QHBoxLayout()
    
        self.pagination_layout = QHBoxLayout()

        #Llamar funcion
        self.setup_mozos_tab()
    
    def setup_mozos_tab(self):
        # Sección para agregar mozo
        self.mozo_name_input.setPlaceholderText("Nombre del Mozo")
        self.mozo_name_input.setStyleSheet(Entry_input)
        
        self.add_mozo_button.setStyleSheet(Boton_Agregar)
        self.add_mozo_button.clicked.connect(self.add_mozo)
        self.add_mozo_layout.addWidget(self.mozo_name_input, 3)
        self.add_mozo_layout.addWidget(self.add_mozo_button, 1)
        self.mozos_layout.addLayout(self.add_mozo_layout)

        # Tabla de Mozos
        self.mozos_table.setHorizontalHeaderLabels(["Nombre", "Código", "Hora de entrada", "Hora de salida", "Fecha", "Mesas Totales", "Acciones",])
        self.mozos_table.setStyleSheet(Estilo_Tabla)
        self.mozos_table.horizontalHeader().setStretchLastSection(True)
        self.mozos_table.verticalHeader().setDefaultSectionSize(40)
        self.mozos_table.setMinimumHeight(300)  # Establecer una altura mínima
        self.mozos_layout.addWidget(self.mozos_table)

        self.btn_anterior_mozos = QPushButton("Página Anterior", self)
        self.btn_anterior_mozos.setStyleSheet(Botones_Navegacion)
        self.btn_anterior_mozos.clicked.connect(self.cargar_anterior_mozos)
        
        self.btn_siguiente_mozos = QPushButton("Siguiente Página", self)
        self.btn_siguiente_mozos.setStyleSheet(Botones_Navegacion)
        self.btn_siguiente_mozos.clicked.connect(self.cargar_siguiente_mozos)

        # Modificar el botón de actualizar
        self.refresh_button.setStyleSheet(Botones_Navegacion)
        self.refresh_button.clicked.connect(self.update_current_view)
        self.mozos_layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.pagination_layout.addWidget(self.btn_anterior_mozos)
        self.pagination_layout.addWidget(self.btn_siguiente_mozos)
        
        self.bottom_layout.addLayout(self.pagination_layout)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.refresh_button)
        
        self.mozos_layout.addLayout(self.bottom_layout)

        self.setLayout(self.mozos_layout)

        # Cargar datos iniciales
        self.load_mozos()

    def load_mozos(self):   
        fecha_hoy = datetime.now().date()
        fecha_txt = datetime.now()

        mozos = Mostrar_Mozos(self.pagina_mozos)
        if mozos != []:
            self.mozos_table.setRowCount(0)
            self.mozos_table.setEditTriggers(QTableWidget.NoEditTriggers)
            registry_file = os.path.join(base_dir, f"../../Docs/Registro/registro_mozos_{fecha_hoy}.json")
            
            # Preparar datos del registro una sola vez
            registry_file = os.path.join(base_dir, f"../../Docs/Registro/registro_mozos_{fecha_hoy}.json")
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
            
            # Actualizar la tabla
            for row, row_data in enumerate(table_data):
                # Insertar datos en las columnas
                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(data)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.mozos_table.setItem(row, col, item)
                
                # Crear widget de botones
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.setContentsMargins(5, 2, 5, 2)
                button_layout.setSpacing(10)
                
                edit_button = QPushButton("Editar")
                edit_button.setStyleSheet(Boton_Editar)
                edit_button.clicked.connect(lambda _, r=row: self.edit_mozo(r))
                
                delete_button = QPushButton("Eliminar")
                delete_button.setStyleSheet(Boton_Eliminar)
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
            dialog.setStyleSheet(Ventana_Editar)

            layout = QVBoxLayout(dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            code_layout = QHBoxLayout()
            code_label = QLabel("Código:")
            code_input = QLineEdit(code)
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
                lambda: self.save_mozo_edit(name, name_input.text(), code, code_input.text(), dialog)
            )
            layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

            dialog.setLayout(layout)
            dialog.exec_()

    def save_mozo_edit(self, old_name, new_name, old_code, new_code, dialog):
        if old_name != new_name:
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑäëïöüÄËÏÖÜçÇ' ]+$", new_name):
                QMessageBox.warning(
                    self, "Error", "Por favor, no Ingrese caracteres especiales o Numeros en el nombre."
                )
                booN = False
            else:
                Editar_Mozo(old_name, "Nombre", new_name)
                self.load_mozos()
                booN = True
        else:
            booN = True

        if old_code != new_code:
            if not re.match(r"^[0-9a-zA-Z ]+$", new_code):
                QMessageBox.warning(
                    self, "Error", "Por favor, Solo ingrese Numeros y Letras en el codigo."
                )
                booC = False
            else:
                Editar_Mozo(new_name, "Codigo", new_code)
                self.load_mozos()
                booC = True
        else:
            booC = True

        if booN == True and booC == True:
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

    def update_current_view(self):
        self.load_mozos()
        
        # Asegurar que la tabla ocupe todo el espacio disponible
        self.mozos_table.horizontalHeader().setStretchLastSection(True)

    def cargar_siguiente_mozos(self):
        self.pagina_mozos = self.siguiente(self.pagina_mozos, "mozo")
        self.load_mozos()
        
    def cargar_anterior_mozos(self):
        print(self.pagina_mozos)
        if self.pagina_mozos > 0:
            self.pagina_mozos = self.anterior(self.pagina_mozos, "mozo")
            self.load_mozos()