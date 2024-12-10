import sys
import os
import json
import asyncio
from Back.models import ValorInput

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Back.Menu_de_mesas_Back import guardar_mesa
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDialog,
    QToolButton,
    QMenu,
    QAction,
    QListWidget,
    QSpinBox,
    QTextEdit,
    QComboBox,
    QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from Front.Static.QSS_TAB_GUI_settings import (
    Config_Style_boton, Config_Desplegable_Menu, Ventanta_de_configuracion, Ventana_Agregar_Plato, Ventana_productos
)
from Front.Static.Settings import Setting

base_dir = os.path.dirname(os.path.abspath(__file__))

class Config(Setting):
    def __init__(self, main_tab):
        super().__init__(main_tab)
        self.main_tab = main_tab
        self.mesa_num = None
        
        # Conectar la señal
        self.main_tab.mesa_seleccionada.connect(self.actualizar_mesa)

        self.device_ip = self.get_device_ip()

        self.config_button = QToolButton(self)

        self.config_menu = QMenu(self)
    
        self.Ajustes = QAction("🔧 Ajustes", self)
        self.Ajustes_input = QLineEdit()
        
        self.Pedido_nuevo = QAction("🍽️ Agregar Pedido", self)
        self.Pedido_nuevo_input = QLineEdit()
        
        self.editar_mesa = QAction("🗒️ Editar Mesa", self)

        self.mozo_add = QAction("👨‍🍳 Agregar Mozo", self)
        self.mozo_add_input = QLineEdit()

        self.producto_add = QAction("🍽️ Agregar Producto", self)

        self.cubiertos_input = QLineEdit()
        self.cubiertos_input.setPlaceholderText(f"Precio de cubiertos: {self.load_cubiertos_price()}")
        self.mesas_input = QLineEdit()
        self.mesas_input.setPlaceholderText(f"Cantidad de mesas: {self.load_mesas_count()}")

        self.ip_action = QAction(f"IP del dispositivo: {self.device_ip}", self)

        self.lista_platos = []
        self.categorias = ["Ninguna"]
        self.productos_elegidos = []

        self.Vista = 0  # Inicializar la variable Vista

        self.Menu_PC()
        self.setup_config_menu()


    def setup_config_menu(self):
        self.config_button.setText("⚙️")
        self.config_button.setFont(QFont("Arial", 14))
        self.config_button.setPopupMode(QToolButton.InstantPopup)
        self.config_button.setStyleSheet(Config_Style_boton)

        self.config_menu.setStyleSheet(Config_Desplegable_Menu)

        self.config_menu.clear()
        # Ajustes
        if self.Vista == 0:
            self.Ajustes.triggered.connect(self.Ventana_Ajustes)
            self.config_menu.addAction(self.Ajustes)
            
            self.Pedido_nuevo.triggered.connect(lambda: self.Ventana_Pedido_nuevo("nuevo"))
            self.config_menu.addAction(self.Pedido_nuevo)

            self.editar_mesa.triggered.connect(lambda: self.Ventana_Pedido_nuevo("editar"))
            self.config_menu.addAction(self.editar_mesa)
        elif self.Vista == 1:
            self.mozo_add.triggered.connect(lambda: self.show_config_dialog("Mozo"))
            self.config_menu.addAction(self.mozo_add)
        elif self.Vista == 2:
            self.producto_add.triggered.connect(self.Nuevo_Menu)
            self.config_menu.addAction(self.producto_add)
        

        self.config_menu.addSeparator()  # Separador para la IP

        self.ip_action.setEnabled(False)  # Deshabilitar para que no sea clickeable
        self.config_menu.addAction(self.ip_action)

        self.config_button.setMenu(self.config_menu)

    def Ventana_Ajustes(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("🔧 Ajustes")
        dialog.setFixedSize(300, 250)
        dialog.setStyleSheet(Ventanta_de_configuracion)

        layout = QVBoxLayout(dialog)
        
        boton_Mesas = QPushButton("🍴 Cantidad de mesas")
        boton_Mesas.clicked.connect(lambda: self.show_config_dialog("Cantidad de mesas"))
        layout.addWidget(boton_Mesas)

        boton_Precio_Cubiertos = QPushButton("💰 Precio de Cubiertos")
        boton_Precio_Cubiertos.clicked.connect(lambda: self.show_config_dialog("Precio de cubiertos"))
        layout.addWidget(boton_Precio_Cubiertos)
        
        boton_Reset_mesas = QPushButton("🔁 Reiniciar mesas")
        boton_Reset_mesas.clicked.connect(self.reset_mesas)
        layout.addWidget(boton_Reset_mesas)

        layout.addStretch()

        dialog.setLayout(layout)
        dialog.exec_()

    def show_config_dialog(self, config_type):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configurar {config_type}")
        dialog.setFixedSize(420, 270)
        layout = QVBoxLayout(dialog)

        dialog.setStyleSheet(Ventanta_de_configuracion)

        icon_label = QLabel()
        if config_type == "Precio de cubiertos":
            icon_label.setText("💰")
            self.input_widget = self.cubiertos_input
        elif config_type == "Cantidad de mesas":  # Cantidad de mesas
            icon_label.setText("🍽️")
            self.input_widget = self.mesas_input
        elif config_type == "Mozo":
            icon_label.setText("👨‍🍳")
            self.input_widget = self.mozo_add_input

        icon_label.setStyleSheet("font-size: 48px; margin-right: 15px;")

        header_layout = QHBoxLayout()
        header_layout.addWidget(icon_label)
        header_layout.addWidget(QLabel(f"{config_type}"))
        layout.addLayout(header_layout)

        self.input_widget.setPlaceholderText(f"Ingrese {config_type.lower()}")
        layout.addWidget(self.input_widget)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(lambda: self.save_config(config_type, self.input_widget.text() ,dialog))
        layout.addWidget(save_button, alignment=Qt.AlignCenter)

        layout.addStretch()

        dialog.setLayout(layout)
        dialog.exec_()

    def Nuevo_Menu(self):
        dialog = QDialog(self)
        dialog.setStyleSheet(Ventana_productos)
        dialog.setFixedSize(300, 450)
        dialog.setWindowTitle("Nuevo Producto")
        dialog_layout = QVBoxLayout(dialog)

        category_input = QLineEdit()
        name_input = QLineEdit()
        price_input = QLineEdit()

        dialog_layout.addWidget(QLabel("Categoría:"))
        dialog_layout.addWidget(category_input)
        dialog_layout.addWidget(QLabel("Nombre:"))
        dialog_layout.addWidget(name_input)
        dialog_layout.addWidget(QLabel("Precio:"))
        dialog_layout.addWidget(price_input)

        save_button = QPushButton("Guardar")
        save_button.setStyleSheet(Ventana_productos)
        save_button.clicked.connect( lambda: self.add_product(category_input.text(), name_input.text(), price_input.text()))
        dialog_layout.addWidget(save_button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def Ventana_Pedido_nuevo(self, modo="nuevo"):
        """
        Crea una ventana de pedido
        modo: "nuevo" para un nuevo pedido, "editar" para editar uno existente
        """
        def guardar(mesa, categorias: list, values: list):
            i = 0
            while i < len(values):
                for categoria in categorias:
                    valor_input = ValorInput(categoria=categoria, valor=values[i])
                    asyncio.run(guardar_mesa(mesa, input=valor_input))
                    i += 1
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Pedido" if modo == "nuevo" else "Editar Pedido")
        dialog.setFixedSize(400, 600)
        dialog.setStyleSheet(Ventana_Agregar_Plato)
        self.Layout = QVBoxLayout()

        # Titulo
        self.Texto_bienvenida = QLabel("Pedido Nuevo" if modo == "nuevo" else "Editar Pedido")
        self.Layout.addWidget(self.Texto_bienvenida)
        
        # Mesa y Mozo
        self.layout_mesa_mozo = QHBoxLayout()
        self.texto_mesa = QLabel("Mesa N° ")
        self.Mesas = QSpinBox() #Numero de las mesas que haya
        self.Mesas.setFixedSize(50, 25)
        
        # Si estamos en modo editar, deshabilitar el cambio de mesa
        self.Mesas.setEnabled(False)

        self.mozo = QLabel("Mozo: ")
        self.mozo_input = QLineEdit() #Nombre del mozo que antiende la mesa
        self.mozo_input.setPlaceholderText("Escribe aquí...")
        self.mozo_input.setFixedSize(150, 40)

        self.layout_mesa_mozo.addWidget(self.texto_mesa)
        self.layout_mesa_mozo.addWidget(self.Mesas)
        self.layout_mesa_mozo.addWidget(self.mozo)
        self.layout_mesa_mozo.addWidget(self.mozo_input)
        self.layout_mesa_mozo.addStretch()
        self.Layout.addLayout(self.layout_mesa_mozo)

        # Comensales
        self.Texto_Comensales = QLabel("Comensales")
        self.Layout.addWidget(self.Texto_Comensales)
        self.layout_comensales = QHBoxLayout()
        self.adult_text = QLabel("Adultos:")
        self.adult_spin = QSpinBox() #Cantidad de comensales
        self.layout_comensales.addWidget(self.adult_text)
        self.layout_comensales.addWidget(self.adult_spin)

        self.niños_text = QLabel("Infantes:")
        self.niños_spin = QSpinBox() #Cantidad de comensales
        self.layout_comensales.addWidget(self.niños_text)
        self.layout_comensales.addWidget(self.niños_spin)
        self.Layout.addLayout(self.layout_comensales)

        # Productos
        self.texto_productos = QLabel("Platos")
        self.Layout.addWidget(self.texto_productos)

        self.layout_busqueda = QHBoxLayout()
        self.Producto_input = QLineEdit()
        self.Producto_input.setPlaceholderText("Escribe aquí...")

        self.categoria = QComboBox()
        self.categoria.addItems(self.categorias)
        self.categoria.currentTextChanged.connect(self.Menu_PC)

        self.layout_busqueda.addWidget(self.Producto_input)
        self.layout_busqueda.addWidget(self.categoria)

        self.Layout.addLayout(self.layout_busqueda)

        # Lista de productos
        self.Lista_producto = QListWidget()
        self.Lista_producto.addItems(self.lista_platos)
        self.Layout.addWidget(self.Lista_producto)
        
        self.Producto_input.textChanged.connect(self.filtro_de_la_lista) #Funcion para usar el filtro 
        self.Lista_producto.itemClicked.connect(self.Opcion_elejida) #Aca es donde se van guardando los pedidos seleccionados (en la vairable self.productos_elejido)

        self.Extra_text = QLabel("Extra")
        self.Layout.addWidget(self.Extra_text)

        self.Extra_Entry = QTextEdit() #Aca es donde se añade la peticion del comensal
        self.Layout.addWidget(self.Extra_Entry)

        self.guardar_boton = QPushButton("Actualizar" if modo == "editar" else "Guardar")
        self.guardar_boton.clicked.connect(lambda: guardar(self.Mesas.value(), categorias=["Mesa","productos", "cantidad_comensales", "comensales_infantiles", "Mozo","Extra"], values=[str(self.Mesas.value()), self.productos_elegidos, str(self.adult_spin.value()), str(self.niños_spin.value()), self.mozo_input.text(), self.Extra_Entry.toPlainText()]))
        self.Layout.addWidget(self.guardar_boton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar espacio al layout
        self.Layout.addStretch()
        dialog.setLayout(self.Layout)

        # Si es modo editar, cargar los datos existentes
        if modo == "editar":
            Json_mesa = os.path.join(base_dir, f"../../tmp/Mesa {self.mesa_num}.json")

            with open(Json_mesa, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            if data["Disponible"] == False:
                self.Mesas.setValue(int(self.mesa_num))
                self.mozo_input.setText(data["Mozo"])
                self.adult_spin.setValue(int(data["cantidad_comensales"]))
                self.niños_spin.setValue(int(data["comensales_infantiles"])) # Convert to integer
                self.productos_elegidos = data["productos"]
                self.Extra_Entry.setText(data["Extra"])
                self.Marcar()     
            else: 
                QMessageBox.warning(
                    self,
                    "Error Editar",
                    "La mesa que quieres editar no contiene un pedido"
                )
        dialog.exec_()

    def Menu_PC(self, text=None):
        with open(os.path.join(base_dir, "../../Docs/Menu.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
        print(text)

        if text == None or text == "Ninguna":    
            for categoria in data["menu"]:
                self.categorias.append(categoria)
                for producto in data["menu"][categoria]:
                    self.lista_platos.append(producto["name"])
        else:
            self.lista_platos = []
            for producto in data["menu"][text]:
                self.lista_platos.append(producto["name"])
            self.Lista_producto.clear()
            self.Lista_producto.addItems(self.lista_platos)
            self.Marcar()

    def filtro_de_la_lista(self, text):
        # Filtrar elementos según el texto
        if text == "":  # Si el campo de texto está vacío, mostrar toda la lista
            self.Lista_producto.clear()
            self.Lista_producto.addItems(self.lista_platos)
        else:
            filtered_items = [item for item in self.lista_platos if text.lower() in item.lower()]
            self.Lista_producto.clear()
            self.Lista_producto.addItems(filtered_items)
        # Actualizar el color de fondo de los elementos seleccionados
        self.Marcar()

    def Opcion_elejida(self, item):
        # Alternar la selección de un ítem: agregarlo o quitarlo de la lista de productos elegidos
        if item.text() not in self.productos_elegidos:
            self.productos_elegidos.append(item.text())  # Agregar a la lista si no está
        else:
            self.productos_elegidos.remove(item.text())  # Quitar de la lista si ya está

        # Actualizar el color de fondo de los elementos seleccionados
        self.Marcar()

    def Marcar(self):
        # Resaltar en verde los elementos que están en productos_elegidos
        for i in range(self.Lista_producto.count()):
            item = self.Lista_producto.item(i)
            if item.text() in self.productos_elegidos:
                item.setBackground(QColor(144, 238, 144))  # Resaltado en verde
            else:
                item.setBackground(QColor(255, 255, 255))  # Fondo blanco para los no seleccionados

    def actualizar_mesa(self, numero_mesa):
        """Recibe el número de mesa seleccionada"""
        self.mesa_num = numero_mesa
    def actualizar_tab(self, tabIndex):
        """Actualiza la pestaña activa"""
        self.Vista = tabIndex  # Almacena el índice de la pestaña activa
        self.setup_config_menu()