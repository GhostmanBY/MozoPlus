import sys
import json
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QLineEdit,
    QMessageBox,
    QSizePolicy,
    QFrame
)
from PyQt5.QtCore import Qt
from Back.Panel_Admin_Back import (
    Mostrar_Mozos,
    obtener_resumen_por_fecha,
)

from Front.Static.QSS_TAB_GUI_info import *

base_dir = os.path.dirname(os.path.abspath(__file__))

class Info_Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout(self.info_widget)

        self.header_frame = QFrame()
    
        self.header_layout = QVBoxLayout(self.header_frame)
    
        self.title_label = QLabel("Resumen de Registros")
        
        self.search_container = QWidget()
        self.search_layout = QHBoxLayout(self.search_container)
        
        self.fecha_container = QWidget()
        self.fecha_layout = QHBoxLayout(self.fecha_container)
        
        self.fecha_label = QLabel("📅")
        self.fecha_label.setStyleSheet(Icon_Label_Style)

        self.fecha_input = QLineEdit()
        
        self.mozo_container = QWidget()
        self.mozo_layout = QHBoxLayout(self.mozo_container)

        self.mozo_label = QLabel("👤")
        self.mozo_label.setStyleSheet(Icon_Label_Style)

        self.mozo_input = QLineEdit()

        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
    
        self.search_button = QPushButton("🔍 Buscar")

        self.load_button = QPushButton("📋 Ver Todos")
    
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        #Llamar funcion
        self.setup_info_tab()

    def setup_info_tab(self):
        self.info_layout.setContentsMargins(20, 20, 20, 20)
        self.info_layout.setSpacing(15)

        # Título y búsqueda en el mismo frame
        self.header_frame.setStyleSheet(Header_Frame_Style)
        self.header_layout.setSpacing(10)

        # Título
        self.title_label.setStyleSheet(Title_Label_Style)
        self.header_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Contenedor para los controles de búsqueda
        self.search_layout.setContentsMargins(10, 0, 10, 0)
        self.search_layout.setSpacing(20)

        # Fecha
        self.fecha_layout.setContentsMargins(0, 0, 0, 0)
        self.fecha_layout.setSpacing(10)
        
        self.fecha_input.setPlaceholderText("Buscar por fecha...")
        self.fecha_input.setStyleSheet(Search_Input_Style)
        self.fecha_layout.addWidget(self.fecha_label)
        self.fecha_layout.addWidget(self.fecha_input)

        # Mozo
        self.mozo_layout.setContentsMargins(0, 0, 0, 0)
        self.mozo_layout.setSpacing(10)
        
        self.mozo_input.setPlaceholderText("Buscar por mozo...")
        self.mozo_input.setStyleSheet(Search_Input_Style)
        self.mozo_layout.addWidget(self.mozo_label)
        self.mozo_layout.addWidget(self.mozo_input)

        # Botones
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(10)

        self.search_button.setStyleSheet(Search_Button_Style)
        self.search_button.clicked.connect(self.buscar_resumen)

        self.load_button.setStyleSheet(Load_Button_Style)
        self.load_button.clicked.connect(lambda: self.load_summary(None))

        self.buttons_layout.addWidget(self.search_button)
        self.buttons_layout.addWidget(self.load_button)

        # Agregar todos los elementos al layout de búsqueda
        self.search_layout.addWidget(self.fecha_container)
        self.search_layout.addWidget(self.mozo_container)
        self.search_layout.addWidget(self.buttons_container)
        self.search_layout.addStretch()

        self.header_layout.addWidget(self.search_container)
        self.info_layout.addWidget(self.header_frame)

        # Área de scroll (sin cambios en el código existente)
        self.scroll_area.setStyleSheet(resumen_estilo_scroll)
        
        # Configurar el scroll area y su contenido
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.MinimumExpanding
        )
        
        # Ajustar márgenes y espaciado
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(10, 10, 10, 50)  # Aumentar margen inferior
        
        # Asegurar que el layout principal dé prioridad al scroll area
        self.info_layout.addWidget(self.scroll_area, stretch=1)  # Añadir stretch=1
        self.info_layout.setStretchFactor(self.scroll_area, 1)
        
        # Ajustar el tamaño mínimo del widget de contenido
        self.scroll_content.setMinimumWidth(self.scroll_area.width())
        
        self.info_layout.addWidget(self.scroll_area)
        self.info_layout.setStretch(0, 0)
        self.info_layout.setStretch(1, 1)

        self.setLayout(self.info_layout)

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
            # Si registro es una lista vacía, mostrar mensaje
            if not registro:
                no_data_label = QLabel("No se encontraron registros")
                no_data_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
                no_data_label.setAlignment(Qt.AlignCenter)
                self.scroll_layout.addWidget(no_data_label)
                return
            registros = registro

        # Si no hay registros, mostrar mensaje
        if not registros:
            no_data_label = QLabel("No se encontraron registros")
            no_data_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
            no_data_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(no_data_label)
            return

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
            fecha_layout.setContentsMargins(10, 10, 10, 10)  # Reducir márgenes
            fecha_layout.setSpacing(8)  # Reducir espaciado

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

                        Precio_frame = QFrame()
                        Precio_layout = QVBoxLayout(Precio_frame)
                        
                        productos = entry.get('productos', [])
                        total = 0
                        with open(os.path.join(base_dir, "../../Docs/Menu.json"), "r", encoding="utf-8") as f:
                            menu = json.load(f)
                            for producto in productos:
                                for categoria in menu["menu"]:
                                    for item in menu["menu"][categoria]:
                                        if producto == item["name"]:
                                            total += item["price"]

                        total_label = QLabel(f"💰 Total: ${total:.2f}")
                        total_label.setStyleSheet(Detail_Total_Style)
                        total_label.setWordWrap(True)
                        Precio_layout.addWidget(total_label)
                        entry_layout.addWidget(Precio_frame)
                        fecha_layout.addWidget(entry_frame)

            self.scroll_layout.addWidget(fecha_frame)

        # Añadir un widget espaciador al final para empujar el contenido hacia arriba
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_layout.addWidget(spacer)

    def get_summary_records(self):
        """Obtiene todos los registros del historial."""
        resumen = {}
        docs_dir = os.path.join(base_dir, "../../Docs/Registro")
        
        # Verificar si el directorio existe
        if not os.path.exists(docs_dir):
            return resumen

        # Obtener la lista de mozos
        data = Mostrar_Mozos()
        mozos = [mozo[1] for mozo in data]  # Extraer solo los nombres de los mozos

        # Procesar todos los archivos de registro
        for filename in os.listdir(docs_dir):
            if filename.endswith('.json'):
                # Extraer la fecha y el nombre del mozo del nombre del archivo
                parts = filename.replace('.json', '').split('_')
                if len(parts) >= 2:
                    fecha = parts[0]
                    mozo_name = '_'.join(parts[1:])  # Manejar nombres con guiones bajos
                    
                    # Verificar si el archivo corresponde a un mozo activo
                    if mozo_name in mozos:
                        filepath = os.path.join(docs_dir, filename)
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                entries = json.load(f)
                                
                                if fecha not in resumen:
                                    resumen[fecha] = []
                                    
                                    for entry in entries:
                                        resumen[fecha].append({
                                            "mozo": mozo_name,
                                            "mesa": entry.get("Mesa", ""),
                                            "hora": entry.get("Hora", ""),
                                            "hora_cierre": entry.get("Hora_cierre", ""),
                                            "productos": entry.get("productos", []),
                                        })
                        except Exception as e:
                            print(f"Error al cargar el archivo {filename}: {str(e)}")

        return resumen

    def buscar_resumen(self):
        fecha = self.fecha_input.text() if self.mozo_input.text() else None
        mozo = self.mozo_input.text() if self.mozo_input.text() else None

        # Llamar a la función para obtener el resumen por fecha y mozo
        resumen = obtener_resumen_por_fecha(fecha, mozo)

        if resumen:
            self.load_summary(resumen)
        else:
            QMessageBox.warning(self, "Búsqueda", "No se encontraron registros para los criterios especificados.")
