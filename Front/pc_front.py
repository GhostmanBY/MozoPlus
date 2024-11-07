import sys
import json
import os
import re
import socket
import datetime
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

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
    QDialog,
    QSizePolicy,
    QFrame,
    QComboBox,
    QToolBar,
    QToolButton,
    QMenu,
    QAction,
    QFileDialog
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QCursor
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
    obtener_resumen_por_fecha,
)
from Front.QSS_Pc_Front import *
from Front.HTML_Pc_Front import (
    Coamnda_HTML,
    Comanda_Vacia_HTML
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

        # Inicializar los atributos de entrada para la búsqueda
        self.fecha_input = QLineEdit()
        self.fecha_input.setPlaceholderText("YYYY-MM-DD")
        self.mozo_input = QLineEdit()
        self.mozo_input.setPlaceholderText("Nombre del Mozo")

        # Configurar la interfaz principal
        self.setup_main_tab()
        self.setup_mozos_tab()
        self.setup_menu_tab()
        self.setup_info_tab()

        # Configurar el temporizador para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cargar_mesas)
        self.timer.start(5000)  # Actualizar cada 5 segundos (5000 ms)

        self.device_ip = self.get_device_ip()  # Obtener la IP del dispositivo

        """Configura un menú desplegable para las opciones de configuración."""
        self.setup_config_menu()

    def get_device_ip(self):
        """Obtiene la dirección IP del dispositivo."""
        try:
            # Conectar a un servidor DNS público para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"Error al obtener la IP: {e}")
            return "IP no disponible"

    def setup_info_tab(self):
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(15)

        # Título y búsqueda en el mismo frame
        header_frame = QFrame()
        header_frame.setStyleSheet(Header_Frame_Style)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(10)

        # Título
        title_label = QLabel("Resumen de Registros")
        title_label.setStyleSheet(Title_Label_Style)
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Contenedor para los controles de búsqueda
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 0, 10, 0)
        search_layout.setSpacing(20)

        # Fecha
        fecha_container = QWidget()
        fecha_layout = QHBoxLayout(fecha_container)
        fecha_layout.setContentsMargins(0, 0, 0, 0)
        fecha_layout.setSpacing(10)
        
        fecha_label = QLabel("📅")
        fecha_label.setStyleSheet(Icon_Label_Style)
        self.fecha_input.setPlaceholderText("Buscar por fecha...")
        self.fecha_input.setStyleSheet(Search_Input_Style)
        fecha_layout.addWidget(fecha_label)
        fecha_layout.addWidget(self.fecha_input)

        # Mozo
        mozo_container = QWidget()
        mozo_layout = QHBoxLayout(mozo_container)
        mozo_layout.setContentsMargins(0, 0, 0, 0)
        mozo_layout.setSpacing(10)
        
        mozo_label = QLabel("👤")
        mozo_label.setStyleSheet(Icon_Label_Style)
        self.mozo_input.setPlaceholderText("Buscar por mozo...")
        self.mozo_input.setStyleSheet(Search_Input_Style)
        mozo_layout.addWidget(mozo_label)
        mozo_layout.addWidget(self.mozo_input)

        # Botones
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)

        search_button = QPushButton("🔍 Buscar")
        search_button.setStyleSheet(Search_Button_Style)
        search_button.clicked.connect(self.buscar_resumen)

        load_button = QPushButton("📋 Ver Todos")
        load_button.setStyleSheet(Load_Button_Style)
        load_button.clicked.connect(lambda: self.load_summary(None))

        buttons_layout.addWidget(search_button)
        buttons_layout.addWidget(load_button)

        # Agregar todos los elementos al layout de búsqueda
        search_layout.addWidget(fecha_container)
        search_layout.addWidget(mozo_container)
        search_layout.addWidget(buttons_container)
        search_layout.addStretch()

        header_layout.addWidget(search_container)
        info_layout.addWidget(header_frame)

        # Área de scroll (sin cambios en el código existente)
        self.scroll_area.setStyleSheet("""
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
        """)
        
        # Asegurar que el contenido sea scrolleable
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        
        # Ajustar márgenes y espaciado
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(10, 10, 10, 30)  # Aumentar margen inferior
        
        info_layout.addWidget(self.scroll_area)
        info_layout.setStretch(0, 0)
        info_layout.setStretch(1, 1)

        self.central_widget.addTab(info_widget, "Resumen")

    def buscar_resumen(self):
        fecha = self.fecha_input.text() if self.mozo_input.text() else None
        mozo = self.mozo_input.text() if self.mozo_input.text() else None

        # Llamar a la función para obtener el resumen por fecha y mozo
        resumen = obtener_resumen_por_fecha(fecha, mozo)

        if resumen:
            print(f"resumen: {resumen}")
            self.load_summary(resumen)
        else:
            QMessageBox.warning(self, "Búsqueda", "No se encontraron registros para los criterios especificados.")

    def load_summary(self, registro=None):
        # Limpiar el layout existente
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Cargar registros
        if registro is None:
            registros = self.get_summary_records()
        else:
            registros = registro

        # Estilo para los frames de fecha
        fecha_frame_style = Summary_Fecha_Frame_Style

        # Estilo para las etiquetas de fecha
        fecha_label_style = Summary_Fecha_Label_Style

        # Estilo para los frames de entrada
        entry_frame_style = Summary_Entry_Frame_Style

        # Estilo para las etiquetas de información
        info_label_style = Summary_Info_Label_Style

        for fecha, data in registros.items():
            fecha_frame = QFrame()
            fecha_frame.setStyleSheet(fecha_frame_style)
            fecha_layout = QVBoxLayout(fecha_frame)

            fecha_label = QLabel(f"📅 {fecha}")
            fecha_label.setStyleSheet(fecha_label_style)
            fecha_layout.addWidget(fecha_label)

            for entry in data:
                if isinstance(entry, dict):
                    entry_frame = QFrame()
                    entry_frame.setStyleSheet(entry_frame_style)
                    entry_frame.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor al pasar por encima
                    entry_layout = QVBoxLayout(entry_frame)

                    # Guardar los datos en el frame para acceder a ellos al hacer clic
                    entry_frame.entry_data = entry
                    
                    # Conectar el evento de clic
                    entry_frame.mousePressEvent = lambda e, data=entry: self.show_detailed_info(data)

                    # Información del mozo
                    mozo_label = QLabel(f"👤 Mozo: {entry.get('mozo', 'Desconocido')}")
                    mozo_label.setStyleSheet(info_label_style)
                    entry_layout.addWidget(mozo_label)

                    # Información de la mesa
                    mesa_label = QLabel(f"🍽️ Mesa: {entry.get('mesa', 'Desconocida')}")
                    mesa_label.setStyleSheet(info_label_style)
                    entry_layout.addWidget(mesa_label)

                    # Horarios
                    horarios_frame = QFrame()
                    horarios_layout = QHBoxLayout(horarios_frame)
                    
                    hora_apertura = QLabel(f"🕐 Apertura: {entry.get('hora', 'No especificada')}")
                    hora_cierre = QLabel(f"🕒 Cierre: {entry.get('hora_cierre', 'No especificada')}")
                    
                    hora_apertura.setStyleSheet(info_label_style)
                    hora_cierre.setStyleSheet(info_label_style)
                    
                    horarios_layout.addWidget(hora_apertura)
                    horarios_layout.addWidget(hora_cierre)
                    entry_layout.addWidget(horarios_frame)

                    # Productos y total
                    if 'productos' in entry:
                        productos_frame = QFrame()
                        productos_layout = QVBoxLayout(productos_frame)
                        
                        productos_label = QLabel("📋 Productos:")
                        productos_label.setStyleSheet(info_label_style)
                        productos_layout.addWidget(productos_label)

                        pedido_tmp = []
                        pedido_final = []
                        for producto in entry['productos']:
                            if producto not in pedido_tmp:
                                cantidad = entry['productos'].count(producto)
                                pedido = f"• {producto} (x{cantidad})"
                                pedido_final.append(pedido)
                                pedido_tmp.append(producto)

                        productos_detalle = QLabel("\n".join(pedido_final))
                        productos_detalle.setStyleSheet(Summary_Productos_Detalle_Style)
                        productos_detalle.setWordWrap(True)
                        productos_layout.addWidget(productos_detalle)
                        entry_layout.addWidget(productos_frame)

                    fecha_layout.addWidget(entry_frame)

            self.scroll_layout.addWidget(fecha_frame)

        # Añadir un espaciador al final
        self.scroll_layout.addStretch()

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
        add_product_button.setStyleSheet(Agregar_Plato_boton)

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
        self.menu_table.setStyleSheet(Tablas_Menu)
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        menu_layout.addWidget(self.menu_table)

        menu_pagination_layout = QHBoxLayout()
        
        self.btn_anterior_menu = QPushButton("Página Anterior", self)
        self.btn_anterior_menu.setStyleSheet(Paginas_atras_adelante_reset)
        self.btn_anterior_menu.clicked.connect(self.cargar_anterior_menu)
        
        self.btn_siguiente_menu = QPushButton("Siguiente Página", self)
        self.btn_siguiente_menu.setStyleSheet(Paginas_atras_adelante_reset)
        self.btn_siguiente_menu.clicked.connect(self.cargar_siguiente_menu)
        
        menu_pagination_layout.addWidget(self.btn_anterior_menu)
        menu_pagination_layout.addWidget(self.btn_siguiente_menu)
        menu_pagination_layout.addStretch()  # Esto empujará los botones hacia la izquierda
        
        menu_layout.addLayout(menu_pagination_layout)

        # Refresh button
        refresh_button = QPushButton("Actualizar Menu")
        refresh_button.clicked.connect(self.load_menu)
        refresh_button.setStyleSheet(Paginas_atras_adelante_reset)
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
                edit_button.setStyleSheet(boton_editar_Plato)
                delete_button = QPushButton("Eliminar")
                delete_button.clicked.connect(lambda _, n=item[1]: self.delete_product(n))
                delete_button.setStyleSheet(boton_eliminar_PLato)

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
        save_button.setStyleSheet(Guardar_cambios_Plato)
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
        self.mozo_name_input.setStyleSheet(Entry_name_mozo)
        add_mozo_button = QPushButton("Agregar Mozo")
        add_mozo_button.setStyleSheet(Agregar_Mozo)
        add_mozo_button.clicked.connect(self.add_mozo)
        add_mozo_layout.addWidget(self.mozo_name_input, 3)
        add_mozo_layout.addWidget(add_mozo_button, 1)
        mozos_layout.addLayout(add_mozo_layout)

        # Tabla de Mozos
        self.mozos_table = QTableWidget(0, 7)
        self.mozos_table.setHorizontalHeaderLabels(["Nombre", "Código", "Hora de entrada", "Hora de salida", "Fecha", "Mesas Totales", "Acciones",])

        self.mozos_table.setStyleSheet(Tablas_Mozo)
        self.mozos_table.horizontalHeader().setStretchLastSection(True)
        self.mozos_table.verticalHeader().setDefaultSectionSize(40)
        self.mozos_table.setMinimumHeight(300)  # Establecer una altura mínima
        mozos_layout.addWidget(self.mozos_table)

        pagination_layout = QHBoxLayout()
    
        self.btn_anterior_mozos = QPushButton("Página Anterior", self)
        self.btn_anterior_mozos.setStyleSheet(Paginas_atras_adelante_reset)
        self.btn_anterior_mozos.clicked.connect(self.cargar_anterior_mozos)
        
        self.btn_siguiente_mozos = QPushButton("Siguiente Página", self)
        self.btn_siguiente_mozos.setStyleSheet(Paginas_atras_adelante_reset)
        self.btn_siguiente_mozos.clicked.connect(self.cargar_siguiente_mozos)
        
        pagination_layout.addWidget(self.btn_anterior_mozos)
        pagination_layout.addWidget(self.btn_siguiente_mozos)
        pagination_layout.addStretch()  # Esto empujará los botones hacia la izquierda
        
        mozos_layout.addLayout(pagination_layout)

        # Modificar el botón de actualizar
        self.refresh_button = QPushButton("Actualizar Lista")
        self.refresh_button.setStyleSheet(Paginas_atras_adelante_reset)
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
                edit_button.setStyleSheet(Boton_Editar_mozo)
                edit_button.clicked.connect(lambda _, r=row: self.edit_mozo(r))
                
                delete_button = QPushButton("Eliminar")
                delete_button.setStyleSheet(Boton_eliminar_Mozo)
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
            dialog.setStyleSheet(Ventanta_de_editar_Mozo)

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
        self.setStyleSheet(Estilo_General)

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
        mesas_scroll.setStyleSheet(Frame_Scroll_mesas)

        # Sección derecha para pedidos y registro
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Estilo para el widget derecho
        right_widget.setStyleSheet(right_widget_style)

        # Área de pedidos
        pedidos_widget = QWidget()
        pedidos_layout = QVBoxLayout(pedidos_widget)
        pedidos_label = QLabel("Datos del pedido:")
        pedidos_layout.addWidget(pedidos_label)

        # Estilo para las etiquetas
        pedidos_label.setStyleSheet(pedidos_label_Style)

        self.json_input = QTextEdit()
        self.json_input.setFont(QFont("Courier New", 12))
        self.json_input.setPlaceholderText("Datos del pedido se mostrarán aquí")
        self.json_input.setStyleSheet(Placeholder_text_pedido)
        self.json_input.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.json_input.setReadOnly(True)
        pedidos_layout.addWidget(self.json_input)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(pedidos_widget)
        right_layout.addWidget(splitter)

        # Estilo para el QSplitter
        splitter.setStyleSheet(splitter_style)

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
                
                # Configurar los eventos de clic
                mesa_button.clicked.connect(lambda checked, num=mesa_num: self.cargar_json(num))  # Clic izquierdo
                mesa_button.setContextMenuPolicy(Qt.CustomContextMenu)
                mesa_button.customContextMenuRequested.connect(
                    lambda pos, num=mesa_num: self.mostrar_historial_mesa(num)
                )  # Clic derecho

                with open(
                    os.path.join(directorio_json, archivo), "r", encoding="utf-8"
                ) as file:
                    mesa_data = json.load(file)

                if mesa_data.get("Disponible", True):
                    mesa_button.setStyleSheet(Mesas_True)
                else:
                    mesa_button.setStyleSheet(Mesas_False)

                self.mesas_layout.addWidget(
                    mesa_button, (mesa_num - 1) // 3, (mesa_num - 1) % 3
                )

            except ValueError:
                print(f"Error: El nombre del archivo '{archivo}' no es válido")

    def mostrar_historial_mesa(self, mesa_num):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Historial Mesa {mesa_num}")
        dialog.setMinimumSize(800, 600)  # Aumentar el tamaño mínimo
        layout = QVBoxLayout(dialog)

        # Estilo para el diálogo
        dialog.setStyleSheet(Ventana_de_historial_mesa)

        # Título
        title_label = QLabel(f"Historial de Comandas - Mesa {mesa_num}")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Crear un área de desplazamiento para la tabla
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Tabla de historial
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Fecha", "Hora", "Mozo", "Total", "Acciones"])
        
        # Configurar la tabla
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Cargar historial
        historial = self.cargar_historial_mesa(mesa_num)
        table.setRowCount(len(historial))

        for row, comanda in enumerate(historial):
            # Configurar altura de fila
            table.setRowHeight(row, 50)

            # Crear y configurar items
            fecha_item = QTableWidgetItem(comanda['fecha'])
            hora_item = QTableWidgetItem(comanda['hora'])
            mozo_item = QTableWidgetItem(comanda['mozo'])
            total_item = QTableWidgetItem(f"${comanda['total']:.2f}")

            # Alinear texto al centro
            for item in [fecha_item, hora_item, mozo_item, total_item]:
                item.setTextAlignment(Qt.AlignCenter)

            # Agregar items a la tabla
            table.setItem(row, 0, fecha_item)
            table.setItem(row, 1, hora_item)
            table.setItem(row, 2, mozo_item)
            table.setItem(row, 3, total_item)

            # Crear widget contenedor para el botón
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(10, 5, 10, 5)
            cell_layout.setAlignment(Qt.AlignCenter)

            # Botón de exportar
            export_button = QPushButton("📄 Exportar")
            export_button.setFixedSize(130, 40)
            export_button.setStyleSheet(Boton_Exportar_comadna)

            # Menú de exportación
            export_menu = QMenu()
            export_menu.setStyleSheet(Exportar_menu)

            pdf_action = QAction("Exportar como PDF", self)
            pdf_action.triggered.connect(lambda checked, c=comanda: self.export_comanda(c, self.cargar_menu(), "pdf"))
            
            txt_action = QAction("Exportar como TXT", self)
            txt_action.triggered.connect(lambda checked, c=comanda: self.export_comanda(c, self.cargar_menu(), "txt"))

            export_menu.addAction(pdf_action)
            export_menu.addAction(txt_action)
            
            export_button.clicked.connect(
                lambda: export_menu.exec_(export_button.mapToGlobal(export_button.rect().bottomLeft()))
            )
            
            cell_layout.addWidget(export_button)
            table.setCellWidget(row, 4, cell_widget)

        scroll_layout.addWidget(table)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        dialog.exec_()

    def export_comanda(self, pedido_json, menu, formato):
        try:
            # Obtener la ubicación donde guardar el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"Comanda_Mesa_{pedido_json['Mesa']}_{timestamp}"
            
            if formato == "pdf":
                file_filter = "PDF Files (*.pdf)"
                default_name += ".pdf"
            else:
                file_filter = "Text Files (*.txt)"
                default_name += ".txt"

            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Comanda",
                default_name,
                file_filter
            )

            if filename:
                if formato == "pdf":
                    self.export_to_pdf(pedido_json, menu, filename)
                else:
                    self.export_to_txt(pedido_json, menu, filename)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar: {str(e)}"
            )

    def export_to_txt(self, pedido_json, menu, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Escribir encabezado
                f.write(f"{'='*50}\n")
                f.write(f"COMANDA MESA {pedido_json['Mesa']}\n")
                f.write(f"{'='*50}\n\n")

                # Información básica
                f.write(f"Fecha: {pedido_json['fecha']}\n")
                f.write(f"Hora: {pedido_json['hora']}\n")
                f.write(f"Mozo: {pedido_json['mozo']}\n")
                f.write(f"Comensales: {pedido_json.get('cantidad_comensales', 0)} ")
                f.write(f"(Infantiles: {pedido_json.get('comensales_infantiles', 0)})\n\n")

                # Aclaraciones
                if pedido_json.get('Extra'):
                    f.write("ACLARACIONES:\n")
                    f.write(f"{pedido_json['Extra']}\n\n")

                # Productos
                f.write(f"{'-'*50}\n")
                f.write(f"{'Producto':<30}{'Cant.':<8}{'Precio':<10}{'Total':<10}\n")
                f.write(f"{'-'*50}\n")

                total_general = 0
                producto_tmp = []
                
                for producto in pedido_json['productos']:
                    if producto not in producto_tmp:
                        cantidad = pedido_json['productos'].count(producto)
                        for categoria in menu["menu"]:
                            for item in menu["menu"][categoria]:
                                if producto == item["name"]:
                                    precio = item["price"]
                                    total = precio * cantidad
                                    total_general += total
                                    f.write(f"{producto:<30}{cantidad:<8}${precio:<9.2f}${total:<9.2f}\n")
                                    producto_tmp.append(producto)

                f.write(f"{'-'*50}\n")
                f.write(f"{'TOTAL GENERAL:':<48}${total_general:.2f}\n")
                f.write(f"{'-'*50}\n")

            QMessageBox.information(
                self,
                "Exportación Exitosa",
                f"La comanda ha sido exportada como archivo de texto en:\n{filename}"
            )

        except Exception as e:
            raise Exception(f"Error al exportar a TXT: {str(e)}")

    def export_to_pdf(self, pedido_json, menu, filename):
        try:
            # Crear el documento PDF con el filename proporcionado
            doc = SimpleDocTemplate(
                filename,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Preparar los elementos del documento
            elements = []
            styles = getSampleStyleSheet()
            
            # Estilo personalizado para el título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2E7D32'),
                spaceAfter=30,
                alignment=1
            )

            # Título
            elements.append(Paragraph(f"Comanda Mesa {pedido_json['Mesa']}", title_style))
            
            # Información básica
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                textColor=colors.HexColor('#333333')
            )
            
            elements.append(Paragraph(f"<b>Fecha:</b> {pedido_json['fecha']}", info_style))
            elements.append(Paragraph(f"<b>Hora:</b> {pedido_json['hora']}", info_style))
            elements.append(Paragraph(f"<b>Mozo:</b> {pedido_json['mozo']}", info_style))
            elements.append(Paragraph(f"<b>Comensales:</b> {pedido_json.get('cantidad_comensales', 0)} (Infantiles: {pedido_json.get('comensales_infantiles', 0)})", info_style))
            
            elements.append(Spacer(1, 20))

            # Aclaraciones
            if pedido_json.get('Extra'):
                elements.append(Paragraph("<b>Aclaraciones:</b>", info_style))
                aclaraciones_style = ParagraphStyle(
                    'Aclaraciones',
                    parent=styles['Normal'],
                    fontSize=12,
                    textColor=colors.HexColor('#FF5722'),
                    backColor=colors.HexColor('#FFF3E0'),
                    borderPadding=10,
                    spaceAfter=20
                )
                elements.append(Paragraph(pedido_json['Extra'], aclaraciones_style))

            # Tabla de productos
            if pedido_json.get('productos'):
                data = [['Producto', 'Cantidad', 'Precio', 'Total']]
                total_general = 0
                producto_tmp = []
                
                for producto in pedido_json['productos']:
                    if producto not in producto_tmp:
                        cantidad = pedido_json['productos'].count(producto)
                        for categoria in menu["menu"]:
                            for item in menu["menu"][categoria]:
                                if producto == item["name"]:
                                    precio = item["price"]
                                    total = precio * cantidad
                                    total_general += total
                                    data.append([
                                        producto,
                                        str(cantidad),
                                        f"${precio:.2f}",
                                        f"${total:.2f}"
                                    ])
                                    producto_tmp.append(producto)

                # Agregar el total general
                data.append(['Total General', '', '', f"${total_general:.2f}"])

                # Crear y estilizar la tabla
                table = Table(data, colWidths=[220, 80, 80, 80])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8F5E9')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ]))
                
                elements.append(table)

            # Generar el PDF
            doc.build(elements)
            
            QMessageBox.information(
                self,
                "Exportación Exitosa",
                f"La comanda ha sido exportada como PDF en:\n{filename}"
            )

        except Exception as e:
            raise Exception(f"Error al exportar a PDF: {str(e)}")

    def cargar_historial_mesa(self, mesa_num):
        historial = []
        registro_dir = os.path.join(base_dir, "../Docs/Registro")
        
        # Verificar si el directorio existe
        if not os.path.exists(registro_dir):
            return historial

        # Obtener todos los archivos de registro
        for filename in os.listdir(registro_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(registro_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        registros = json.load(f)
                        
                        # Procesar cada registro
                        for registro in registros:
                            if str(registro.get('Mesa')) == str(mesa_num):
                                # Calcular el total
                                total = 0
                                productos = registro.get('productos', [])
                                menu_data = self.cargar_menu()
                                
                                for producto in productos:
                                    for categoria in menu_data["menu"]:
                                        for item in menu_data["menu"][categoria]:
                                            if producto == item["name"]:
                                                total += item["price"]

                                historial.append({
                                    'fecha': registro.get('Fecha', ''),
                                    'hora': registro.get('Hora', ''),
                                    'mozo': registro.get('Mozo', ''),
                                    'total': total,
                                    'productos': productos,
                                    'Mesa': mesa_num,
                                    'cantidad_comensales': registro.get('cantidad_comensales', 0),
                                    'comensales_infantiles': registro.get('comensales_infantiles', 0),
                                    'Extra': registro.get('Extra', '')
                                })
                except Exception as e:
                    print(f"Error al cargar el archivo {filename}: {str(e)}")

        # Ordenar el historial por fecha y hora (más reciente primero)
        historial.sort(key=lambda x: f"{x['fecha']} {x['hora']}", reverse=True)
        return historial

    def cargar_menu(self):
        """Carga y retorna los datos del menú"""
        menu_path = os.path.join(base_dir, "../Docs/Menu.json")
        try:
            with open(menu_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar el menú: {str(e)}")
            return {"menu": {}}

    def setup_config_menu(self):
        self.config_button = QToolButton(self)
        self.config_button.setText("⚙️")
        self.config_button.setFont(QFont("Arial", 14))
        self.config_button.setPopupMode(QToolButton.InstantPopup)
        self.config_button.setStyleSheet(Config_Style_boton)

        config_menu = QMenu(self)
        config_menu.setStyleSheet(Config_Desplegable_Menu)

        cubiertos_action = QAction("💰 Precio de cubiertos", self)
        cubiertos_action.triggered.connect(lambda: self.show_config_dialog("Precio de cubiertos"))
        config_menu.addAction(cubiertos_action)

        mesas_action = QAction("🍽️ Cantidad de mesas", self)
        mesas_action.triggered.connect(lambda: self.show_config_dialog("Cantidad de mesas"))
        config_menu.addAction(mesas_action)

        reset_action = QAction("🔄 resetear mesas", self)
        reset_action.triggered.connect(self.reset_mesas)
        config_menu.addAction(reset_action)

        config_menu.addSeparator()  # Separador para la IP

        ip_action = QAction(f"IP del dispositivo: {self.device_ip}", self)
        ip_action.setEnabled(False)  # Deshabilitar para que no sea clickeable
        config_menu.addAction(ip_action)

        self.central_widget.setCornerWidget(self.config_button, Qt.TopRightCorner)
        self.config_button.setMenu(config_menu)

    def show_config_dialog(self, config_type):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configurar {config_type}")
        dialog.setFixedSize(420, 270)
        layout = QVBoxLayout(dialog)

        dialog.setStyleSheet(Ventanta_de_configuracion)

        icon_label = QLabel()
        if config_type == "Precio de cubiertos":
            icon_label.setText("💰")
            input_widget = self.cubiertos_input
        elif config_type == "Cantidad de mesas":  # Cantidad de mesas
            icon_label.setText("🍽️")
            input_widget = self.mesas_input

        icon_label.setStyleSheet("font-size: 48px; margin-right: 15px;")

        header_layout = QHBoxLayout()
        header_layout.addWidget(icon_label)
        header_layout.addWidget(QLabel(f"{config_type}"))
        layout.addLayout(header_layout)

        input_widget.setPlaceholderText(f"Ingrese {config_type.lower()}")
        layout.addWidget(input_widget)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(lambda: self.save_config(config_type, dialog))
        layout.addWidget(save_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        dialog.setLayout(layout)
        dialog.exec_()

    def reset_mesas(self):
                # Crear el cuadro de diálogo de advertencia
        warning_message = QMessageBox(self)
        warning_message.setIcon(QMessageBox.Warning)
        warning_message.setWindowTitle("Advertencia")
        warning_message.setText("si continua se borrara toda la informacion de las mesas")
        warning_message.setInformativeText("¿Deseas continuar?")
        
        # Agregar botones de continuar y cancelar
        continue_button = warning_message.addButton("Continuar", QMessageBox.AcceptRole)
        cancel_button = warning_message.addButton("Cancelar", QMessageBox.RejectRole)
        
        # Mostrar el cuadro de diálogo y esperar respuesta
        warning_message.exec_()

        # Verificar cuál botón se presionó
        if warning_message.clickedButton() == continue_button:
            if os.path.exists(os.path.join(base_dir, "../Docs/Config.json")):
                with open(os.path.join(base_dir, "../Docs/Config.json"), "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
            
            self.update_mesas_count(config[1]['cantidad_mesas'])
            
        elif warning_message.clickedButton() == cancel_button:
            self.close()  # Cerrar el widget actual si se presiona "Cancelar"

    
    def save_config(self, config_type, dialog):
        try:
            if config_type == "Precio de cubiertos":
                precio_cubiertos = self.cubiertos_input.text()
                if os.path.exists(os.path.join(base_dir, "../Docs/Config.json")):
                    with open(os.path.join(base_dir, "../Docs/Config.json"), "r", encoding="utf-8") as f:
                        config = json.load(f)
                else:
                    config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
                
                config[0]["precio_cubiertos"] = "$" + str(precio_cubiertos)
            
            elif config_type == "Cantidad de mesas":
                cantidad_mesas = int(self.mesas_input.text())
                if os.path.exists(os.path.join(base_dir, "../Docs/Config.json")):
                    with open(os.path.join(base_dir, "../Docs/Config.json"), "r", encoding="utf-8") as f:
                        config = json.load(f)
                else:
                    config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
                
                config[1]["cantidad_mesas"] = cantidad_mesas
                self.update_mesas_count(cantidad_mesas)

            with open(os.path.join(base_dir, "../Docs/Config.json"), "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            QMessageBox.information(dialog, "Configuración Guardada", "La configuración ha sido guardada exitosamente.")
            dialog.accept()
        except ValueError:
            QMessageBox.warning(dialog, "Error", "Por favor, ingrese un valor válido.")

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

    def cargar_json(self, mesa_num):
        """Carga y muestra la comanda actual de una mesa específica"""
        ruta_archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa_num}.json")
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                pedido_json = json.load(f)
                self.procesar_pedido_con_json(pedido_json)
        except Exception as e:
            print(f"Error al cargar JSON para Mesa {mesa_num}: {str(e)}")

    def procesar_pedido_con_json(self, pedido_json):
        """Procesa y muestra la comanda en la interfaz"""
        with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)
        with open(os.path.join(base_dir, "../Docs/config.json"), "r", encoding="utf-8") as f:
            config = json.load(f)
            precio_cubiertos = config[0].get("precio_cubiertos", 0)

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
            comanda_texto = Coamnda_HTML(
                comanda_style=Comanda_Style,
                mesa=mesa,
                fecha=fecha,
                hora=hora,
                mozo=mozo,
                cantidad_comensales=cantidad_comensales,
                comensales_infantiles=comensales_infantiles,
                aclaraciones=aclaraciones if aclaraciones else "No hay aclaraciones sobre el pedido"
            )
            total_general = 0
            producto_tmp = []
            for producto in productos:
                cantidad = 0
                for categoria in menu["menu"]:
                    for pedido in menu["menu"][categoria]:
                        if producto == pedido["name"]:
                            if producto not in producto_tmp:
                                cantidad += productos.count(producto)
                                Precio_producto = pedido["price"] * cantidad
                                producto_tmp.append(producto)
                                total_general += Precio_producto 
                                
                                
                                comanda_texto += f"""
                                <tr>
                                    <td>{producto}</td>
                                    <td>{cantidad}</td>
                                    <td>${pedido["price"]:.2f}</td>
                                    <td>${Precio_producto:.2f}</td>
                                </tr>
                                """
            total_general += float(precio_cubiertos[1:])
            comanda_texto += f"""
                <tr class="total">
                    <td colspan="2">Total General:</td>
                    <td>${float(precio_cubiertos[1:])}</td>
                    <td>${total_general:.2f}</td>
                </tr>
            </table>
            </div>
            """
        else:
            comanda_texto = Comanda_Vacia_HTML(
                Comanda_Vacia_Style=Comanda_Vacia_Style,
                mesa=mesa,
                estado=estado.upper(),
            )

        self.json_input.setHtml(comanda_texto)

    def show_detailed_info(self, entry_data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Detalles de la Comanda")
        dialog.setMinimumWidth(500)
        dialog.setMaximumHeight(700)  # Limitar altura máxima
        
        # Crear un scroll area para contener todo el contenido
        scroll = QScrollArea(dialog)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
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
        """)

        # Widget contenedor principal
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Encabezado
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel(f"Mesa {entry_data.get('mesa', 'N/A')}")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #8B4513;
            padding-bottom: 10px;
            border-bottom: 2px solid #DEB887;
        """)
        header_layout.addWidget(title)

        # Información básica
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        mozo_label = QLabel(f"👤 Mozo: {entry_data.get('mozo', 'N/A')}")
        fecha_label = QLabel(f"📅 Fecha: {entry_data.get('fecha', 'N/A')}")
        hora_apertura = QLabel(f"🕐 Hora de apertura: {entry_data.get('hora', 'N/A')}")
        hora_cierre = QLabel(f"🕒 Hora de cierre: {entry_data.get('hora_cierre', 'N/A')}")

        info_layout.addWidget(mozo_label)
        info_layout.addWidget(fecha_label)
        info_layout.addWidget(hora_apertura)
        info_layout.addWidget(hora_cierre)

        # Productos
        productos_frame = QFrame()
        productos_layout = QVBoxLayout(productos_frame)
        
        productos_title = QLabel("📋 Productos:")
        productos_title.setStyleSheet("font-weight: bold;")
        productos_layout.addWidget(productos_title)

        productos = entry_data.get('productos', [])
        if productos:
            producto_tmp = []
            for producto in productos:
                if producto not in producto_tmp:
                    cantidad = productos.count(producto)
                    producto_label = QLabel(f"• {producto} (x{cantidad})")
                    producto_label.setStyleSheet("margin-left: 20px;")
                    productos_layout.addWidget(producto_label)
                    producto_tmp.append(producto)
        else:
            productos_layout.addWidget(QLabel("No hay productos registrados"))

        # Calcular total
        total = 0
        with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)
            for producto in productos:
                for categoria in menu["menu"]:
                    for item in menu["menu"][categoria]:
                        if producto == item["name"]:
                            total += item["price"]

        total_label = QLabel(f"💰 Total: ${total:.2f}")
        total_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2E7D32;
            margin-top: 10px;
            padding: 10px;
            background-color: #E8F5E9;
            border-radius: 5px;
        """)

        # Agregar todos los elementos al layout principal
        layout.addWidget(header_frame)
        layout.addWidget(info_frame)
        layout.addWidget(productos_frame)
        layout.addWidget(total_label)

        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
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
        """)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        # Establecer el widget principal en el scroll area
        scroll.setWidget(main_widget)

        # Layout del diálogo
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(scroll)

        dialog.exec_()

if __name__ == "__main__":
    def exception_hook(exctype, value, tb):
        print(f"Excepción no manejada: {exctype}, {value}")
        print("Traceback:")
        import traceback
        print("".join(traceback.format_tb(tb)))
        sys.__excepthook__(exctype, value, tb)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(Estilo_app)

    ventana = RestaurantInterface()
    ventana.showMaximized()
    sys.exit(app.exec_())