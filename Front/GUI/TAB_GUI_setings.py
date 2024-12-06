import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    QComboBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from Front.Static.QSS_TAB_GUI_settings import (
    Config_Style_boton, Config_Desplegable_Menu, Ventanta_de_configuracion, Ventana_Agregar_Plato
)
from Front.Static.Utils import Setting

base_dir = os.path.dirname(os.path.abspath(__file__))

class Config(Setting):
    def __init__(self):
        super().__init__()
        self.device_ip = self.get_device_ip()

        self.config_button = QToolButton(self)

        self.config_menu = QMenu(self)
    
        self.Ajustes = QAction("🔧 Ajustes", self)
        self.Ajustes_input = QLineEdit()
        
        self.Pedido_nuevo = QAction("🍽️ Agregar Pedido", self)
        self.Pedido_nuevo_input = QLineEdit()
        
        self.cubiertos_input = QLineEdit()
        self.mesas_input = QLineEdit()

        self.ip_action = QAction(f"IP del dispositivo: {self.device_ip}", self)

        self.lista_platos = []
        self.categorias = ["Ninguna"]
        self.productos_elegidos = []

        self.Menu_PC()
        self.setup_config_menu()

    def setup_config_menu(self):
        self.config_button.setText("⚙️")
        self.config_button.setFont(QFont("Arial", 14))
        self.config_button.setPopupMode(QToolButton.InstantPopup)
        self.config_button.setStyleSheet(Config_Style_boton)

        self.config_menu.setStyleSheet(Config_Desplegable_Menu)

        self.Ajustes.triggered.connect(self.Ventana_Ajustes)
        self.config_menu.addAction(self.Ajustes)
        
        self.Pedido_nuevo.triggered.connect(self.Ventana_Pedido_nuevo)
        self.config_menu.addAction(self.Pedido_nuevo)

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

    def Ventana_Pedido_nuevo(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Pedido")
        dialog.setFixedSize(400, 600)
        dialog.setStyleSheet(Ventana_Agregar_Plato)
        self.Layout = QVBoxLayout()

        # Titulo
        self.Texto_bienvenida = QLabel("Pedido Nuevo")
        self.Layout.addWidget(self.Texto_bienvenida)
        
        # Mesa y Mozo
        self.layout_HM = QHBoxLayout()
        self.texto_mesa = QLabel("Mesa N° ")
        self.Mesas = QSpinBox() #Numero de las mesas que haya
        self.Mesas.setFixedSize(50, 25)

        self.mozo = QLabel("Mozo: ")
        self.mozo_input = QLineEdit() #Nombre del mozo que antiende la mesa
        self.mozo_input.setPlaceholderText("Escribe aquí...")
        self.mozo_input.setFixedSize(150, 40)

        self.layout_HM.addWidget(self.texto_mesa)
        self.layout_HM.addWidget(self.Mesas)
        self.layout_HM.addWidget(self.mozo)
        self.layout_HM.addWidget(self.mozo_input)
        self.layout_HM.addStretch()
        self.Layout.addLayout(self.layout_HM)

        # Comensales
        self.Texto_Comensales = QLabel("Comensales")
        self.Layout.addWidget(self.Texto_Comensales)
        self.layout_HM = QHBoxLayout()
        self.adult_text = QLabel("Adultos:")
        self.adult_spin = QSpinBox() #Cantidad de comensales
        self.layout_HM.addWidget(self.adult_text)
        self.layout_HM.addWidget(self.adult_spin)

        self.niños_text = QLabel("Infantes:")
        self.niños_spin = QSpinBox() #Cantidad de comensales
        self.layout_HM.addWidget(self.niños_text)
        self.layout_HM.addWidget(self.niños_spin)
        self.Layout.addLayout(self.layout_HM)

        # Productos
        self.texto_productos = QLabel("Platos")
        self.Layout.addWidget(self.texto_productos)

        self.layout_HM = QHBoxLayout()
        self.Producto_input = QLineEdit() #Es un buscador no mas
        self.Producto_input.setPlaceholderText("Escribe aquí...")

        self.categoria = QComboBox()
        self.categoria.addItems(self.categorias)
        self.categoria.currentTextChanged.connect(self.Menu_PC)

        self.layout_HM.addWidget(self.Producto_input)
        self.layout_HM.addWidget(self.categoria)

        self.Layout.addLayout(self.layout_HM)

        # Lista de productos
        self.Lista_producto = QListWidget() #Aca se seleccionan los platos
        self.Lista_producto.addItems(self.lista_platos)
        self.Layout.addWidget(self.Lista_producto)
        self.Layout.addLayout(self.layout_HM)

        self.Producto_input.textChanged.connect(self.filtro_de_la_lista) #Funcion para usar el filtro 
        self.Lista_producto.itemClicked.connect(self.Opcion_elejida) #Aca es donde se van guardando los pedidos seleccionados (en la vairable self.productos_elejido)

        self.Extras_text = QLabel("Extra")
        self.Layout.addWidget(self.Extras_text)

        self.Extra_Entry = QTextEdit() #Aca es donde se añade la peticion del comensal
        self.Layout.addWidget(self.Extra_Entry)

        self.guardar_boton = QPushButton("Guardar") #Falta crear la funcion del boton que haga que se mandan todos los parametros en la mesa correspondiente 
        self.Layout.addWidget(self.guardar_boton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar espacio al layout
        self.Layout.addStretch()
        dialog.setLayout(self.Layout)
        dialog.exec_()

    def Menu_PC(self, text=None):
        with open(os.path.join(base_dir, "../../Docs/Menu.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
        print(text)

        if text == None:    
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
