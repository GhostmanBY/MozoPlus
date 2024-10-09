import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QScrollArea, QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QLineEdit, QLabel, QHBoxLayout, QGridLayout, QFrame, QTextEdit, QSizePolicy, QSplitter
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from datetime import datetime, date

# Importar funciones de gestión de mesas
from Back.Menu_de_mesas_Back import ver_mesas, abrir_mesa, cerrar_mesa, restaurar_mesa

fecha_hoy = date.today().strftime("%Y-%m-%d")

from gestor_mozos import setup_mozos_tab, load_mozos, add_mozo, edit_mozo, delete_mozo, toggle_mozo_view, update_current_view
from gestor_menu import setup_menu_tab, add_product, load_menu, edit_product, delete_product
from utilidades import ajustar_tamano_pantalla, set_style, cargar_mesas, mesa_clicked, cargar_json, procesar_pedido_con_json, formatear_fecha

base_dir = os.path.dirname(os.path.abspath(__file__))

class RestaurantInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Restaurante")
        ajustar_tamano_pantalla(self)
        set_style(self)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.setup_main_tab()
        setup_mozos_tab(self)
        setup_menu_tab(self)
        self.setup_info_tab()

    def setup_info_tab(self):
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)

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

                fecha_layout.addWidget(entry_frame)

            self.scroll_layout.addWidget(fecha_frame)

    def get_summary_records(self):
        resumen = {}
        docs_dir = os.path.join(base_dir, "Docs/Registro")
        for filename in os.listdir(docs_dir):
            if filename.endswith(".json"):
                mozo_name = filename.replace(f"{fecha_hoy}_", "").replace(".json", "")
                date_str = filename.replace(f"_{mozo_name}", "").replace(".json", "")

                with open(
                    os.path.join(docs_dir, filename), "r", encoding="utf-8"
                ) as file:
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

    def setup_main_tab(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        mesas_scroll = QScrollArea()
        mesas_scroll.setWidgetResizable(True)
        mesas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mesas_widget = QWidget()
        self.mesas_layout = QGridLayout(mesas_widget)
        self.mesas_layout.setSpacing(20)

        mesas_scroll.setWidget(mesas_widget)

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

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        right_widget.setStyleSheet(
            """
            QWidget {
                background-color: #FAFAFA;
                border-radius: 10px;
            }
        """
        )

        pedidos_widget = QWidget()
        pedidos_layout = QVBoxLayout(pedidos_widget)
        pedidos_label = QLabel("Datos del pedido:")
        pedidos_layout.addWidget(pedidos_label)

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

        procesar_button = QPushButton("Actualizar Registro")
        procesar_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )
        procesar_button.clicked.connect(lambda: cargar_mesas(self))
        pedidos_layout.addWidget(procesar_button)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(pedidos_widget)
        right_layout.addWidget(splitter)

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

        cargar_mesas(self)

    def mesa_clicked(self, mesa_num):
        mesa_clicked(self, mesa_num)

    def cargar_json(self, mesa_num):
        cargar_json(self, mesa_num)

    def procesar_pedido_con_json(self, pedido_json):
        procesar_pedido_con_json(self, pedido_json)

    def formatear_fecha(self, fecha_str):
        return formatear_fecha(fecha_str)

if __name__ == "__main__":
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