import sys
import json
import os
import asyncio

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ruta_raiz)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QGridLayout, QSplitter, QScrollArea, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from Static.QSS_TAB_GUI_main import (
    Frame_Scroll_mesas, right_widget_style, pedidos_label_Style, Placeholder_text_pedido,
    splitter_style, Mesas_True, Mesas_False, Comanda_Style, Comanda_Vacia_Style)

from Static.HTML_Pc_Front import (Coamnda_HTML, Comanda_Vacia_HTML)

from Back import cerrar_mesa

base_dir = os.path.dirname(os.path.abspath(__file__))

class Main_Tab(QWidget):
    """
    Pestaña principal que muestra las mesas y los detalles de los pedidos.
    Permite la visualización y gestión de las mesas del restaurante.
    """
    # Señal para comunicar la mesa seleccionada
    mesa_seleccionada = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.mesas_scroll = QScrollArea()
        
        self.mesas_widget = QWidget()

        # Sección derecha para pedidos y registro
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
    
        self.pedidos_widget = QWidget()
        self.pedidos_layout = QVBoxLayout(self.pedidos_widget)

        self.pedidos_label = QLabel("Datos del pedido:")
    
        self.json_input = QTextEdit()

        self.mesa_actual = None  # Agregar variable para tracking

        #Llamar la funcion
        self.setup_main_tab()
    
    def setup_main_tab(self):

        # Sección izquierda para mesas
        self.mesas_scroll.setWidgetResizable(True)
        self.mesas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mesas_layout = QGridLayout(self.mesas_widget)
        self.mesas_layout.setSpacing(20)

        self.mesas_scroll.setWidget(self.mesas_widget)

        # Estilo para el QScrollArea (mesas_scroll)
        self.mesas_scroll.setStyleSheet(Frame_Scroll_mesas)

        # Estilo para el widget derecho
        self.right_widget.setStyleSheet(right_widget_style)

        # Área de pedidos
        self.pedidos_layout.addWidget(self.pedidos_label)

        # Estilo para las etiquetas
        self.pedidos_label.setStyleSheet(pedidos_label_Style)

        self.json_input.setFont(QFont("Courier New", 12))
        self.json_input.setPlaceholderText("Datos del pedido se mostrarán aquí")
        self.json_input.setStyleSheet(Placeholder_text_pedido)
        self.json_input.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.json_input.setReadOnly(True)
        self.pedidos_layout.addWidget(self.json_input)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.pedidos_widget)
        self.right_layout.addWidget(splitter)

        # Estilo para el QSplitter
        splitter.setStyleSheet(splitter_style)

        self.main_layout.addWidget(self.mesas_scroll, 6)
        self.main_layout.addWidget(self.right_widget, 4)

        self.setLayout(self.main_layout)

        self.cargar_mesas()

    def cargar_mesas(self):
        # Limpiar el layout de mesas existente
        for i in reversed(range(self.mesas_layout.count())): 
            self.mesas_layout.itemAt(i).widget().setParent(None)
        
        directorio_json = os.path.join(base_dir, "../../tmp")
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
                #mesa_button.customContextMenuRequested.connect(lambda pos, num=mesa_num: self.mostrar_historial_mesa(num))  # Clic derecho
                
                
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

    def cargar_json(self, mesa_num):
        """Carga y muestra la comanda actual de una mesa específica"""
        self.mesa_actual = mesa_num  # Guardar mesa seleccionada
        self.mesa_seleccionada.emit(mesa_num)  # Emitir señal
        ruta_archivo = os.path.join(base_dir, f"../../tmp/Mesa {mesa_num}.json")
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                pedido_json = json.load(f)
                self.procesar_pedido_con_json(pedido_json)
        except Exception as e:
            print(f"Error al cargar JSON para Mesa {mesa_num}: {str(e)}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_X:  # Detectar la tecla "X"
            self.confirmar_cierre_mesa()

    def confirmar_cierre_mesa(self):
        """Muestra un cuadro de diálogo para confirmar el cierre de la mesa."""
        reply = QMessageBox.question(
            self,
            "Confirmar Cierre",
            "¿Está seguro de que desea cerrar la mesa?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            if self.mesa_actual is not None:  # Asegúrate de que hay una mesa seleccionada
                # Usar un QTimer para ejecutar la función asíncrona
                QTimer.singleShot(0, lambda: self.cerrar_mesa_async(self.mesa_actual))
            else:
                QMessageBox.warning(self, "Error", "No hay mesa seleccionada para cerrar.")

    def cerrar_mesa_async(self, mesa_num):
        """Función asíncrona para cerrar la mesa."""
        # Usar un bucle de eventos para ejecutar la coroutine
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cerrar_mesa(mesa_num))  # Llama a la función para cerrar la mesa
        QMessageBox.information(self, "Cierre de Mesa", "La mesa ha sido cerrada.")

    def procesar_pedido_con_json(self, pedido_json):
        """Procesa y muestra la comanda en la interfaz"""
        with open(os.path.join(base_dir, "../../Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)
        with open(os.path.join(base_dir, "../../Docs/config.json"), "r", encoding="utf-8") as f:
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