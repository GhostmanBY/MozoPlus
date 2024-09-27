import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSplitter,
    QSizePolicy,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve

base_dir = os.path.dirname(os.path.abspath(__file__))


class GradientButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(130, 130)
        self.setMaximumSize(150, 150)
        self.setCursor(Qt.PointingHandCursor)
        self.is_available = True

        # Aplicar sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

    def set_available(self, available):
        self.is_available = available
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_available:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#4CAF50"))
            gradient.setColorAt(1, QColor("#45a049"))
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#F44336"))
            gradient.setColorAt(1, QColor("#D32F2F"))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class RestaurantInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Restaurante")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F0F4F8;
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

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_main_tab()

    def setup_main_tab(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(20)

        # Sección izquierda para mesas
        mesas_widget = QWidget()
        mesas_layout = QVBoxLayout(mesas_widget)
        mesas_layout.setContentsMargins(0, 0, 0, 0)

        titulo_mesas = QLabel("Mesas del Restaurante")
        titulo_mesas.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #FFFFFF;
            border-radius: 10px;
        """
        )
        shadow = QGraphicsDropShadowEffect(titulo_mesas)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        titulo_mesas.setGraphicsEffect(shadow)
        mesas_layout.addWidget(titulo_mesas)

        busqueda_mesas = QLineEdit()
        busqueda_mesas.setPlaceholderText("Buscar mesa...")
        busqueda_mesas.setStyleSheet(
            """
            QLineEdit {
                padding: 12px;
                border: 1px solid #E0E0E0;
                border-radius: 25px;
                font-size: 16px;
                background-color: #FFFFFF;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
            }
        """
        )
        shadow = QGraphicsDropShadowEffect(busqueda_mesas)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        busqueda_mesas.setGraphicsEffect(shadow)
        mesas_layout.addWidget(busqueda_mesas)

        mesas_scroll = QScrollArea()
        mesas_scroll.setWidgetResizable(True)
        mesas_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mesas_content = QWidget()
        self.mesas_layout = QGridLayout(mesas_content)
        self.mesas_layout.setSpacing(20)
        mesas_scroll.setWidget(mesas_content)

        mesas_scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #FFFFFF;
                border: none;
                border-radius: 10px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect(mesas_scroll)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        mesas_scroll.setGraphicsEffect(shadow)

        mesas_layout.addWidget(mesas_scroll)

        # Sección derecha para pedidos y registro
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_widget.setStyleSheet(
            """
            QWidget {
                background-color: #FFFFFF;
                border-radius: 10px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect(right_widget)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        right_widget.setGraphicsEffect(shadow)

        # Área de pedidos
        pedidos_widget = QWidget()
        pedidos_layout = QVBoxLayout(pedidos_widget)
        pedidos_label = QLabel("Datos del pedido")
        pedidos_label.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #F0F4F8;
            border-radius: 5px;
        """
        )
        pedidos_layout.addWidget(pedidos_label)

        self.json_input = QTextEdit()
        self.json_input.setFont(QFont("Courier New", 12))
        self.json_input.setPlaceholderText("Datos del pedido se mostrarán aquí")
        self.json_input.setStyleSheet(
            """
            QTextEdit {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
                background-color: #FFFFFF;
                selection-background-color: #81C784;
            }
        """
        )
        self.json_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.json_input.setReadOnly(True)
        pedidos_layout.addWidget(self.json_input)

        procesar_button = QPushButton("Actualizar Registro")
        procesar_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect(procesar_button)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        procesar_button.setGraphicsEffect(shadow)
        procesar_button.clicked.connect(self.cargar_mesas)
        pedidos_layout.addWidget(procesar_button)

        right_layout.addWidget(pedidos_widget)

        main_layout.addWidget(mesas_widget, 6)
        main_layout.addWidget(right_widget, 4)

        self.central_widget.addTab(main_widget, "Restaurante")

        self.cargar_mesas()

    def crear_boton_mesa(self, mesa_num, disponible):
        mesa_button = GradientButton(f"Mesa {mesa_num}")
        mesa_button.set_available(disponible)

        info_label = QLabel(
            f"Mesa {mesa_num}\n{'Disponible' if disponible else 'Ocupada'}"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            border-radius: 20px;
            padding: 10px;
        """
        )
        info_label.hide()

        layout = QVBoxLayout(mesa_button)
        layout.addWidget(info_label)

        def mostrar_info():
            info_label.show()

        def ocultar_info():
            info_label.hide()

        mesa_button.enterEvent = lambda e: mostrar_info()
        mesa_button.leaveEvent = lambda e: ocultar_info()

        mesa_button.clicked.connect(lambda _, num=mesa_num: self.mesa_clicked(num))
        return mesa_button

    def cargar_mesas(self):
        directorio_json = os.path.join(base_dir, "tmp")
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
                with open(
                    os.path.join(directorio_json, archivo), "r", encoding="utf-8"
                ) as file:
                    mesa_data = json.load(file)

                disponible = mesa_data.get("Disponible", True)
                mesa_button = self.crear_boton_mesa(mesa_num, disponible)

                self.mesas_layout.addWidget(
                    mesa_button, (mesa_num - 1) // 3, (mesa_num - 1) % 3
                )

            except ValueError:
                print(f"Error: El nombre del archivo '{archivo}' no es válido")

    def mesa_clicked(self, mesa_num):
        self.cargar_json(mesa_num)

    def cargar_json(self, mesa_num):
        ruta_archivo = os.path.join(base_dir, f"tmp/Mesa {mesa_num}.json")
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                pedido_json = json.load(f)
                self.procesar_pedido_con_json(pedido_json)
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"Error: No se pudo cargar el archivo JSON para la Mesa {mesa_num}")

    def procesar_pedido_con_json(self, pedido_json):
        with open(os.path.join(base_dir, "Docs/Menu.json"), "r", encoding="utf-8") as f:
            menu = json.load(f)

        mesa = pedido_json.get("Mesa", "")
        fecha = pedido_json.get("Fecha", "")
        hora = pedido_json.get("Hora", "")
        mozo = pedido_json.get("Mozo", "")
        productos = pedido_json.get("productos", [])
        cantidad_comensales = pedido_json.get("cantidad_comensales", 0)
        comensales_infantiles = pedido_json.get("comensales_infantiles", [False, 0])

        estado = "Disponible" if pedido_json.get("Disponible", True) else "Ocupada"

        if productos or cantidad_comensales > 0 or any(comensales_infantiles):
            fecha_formateada = self.formatear_fecha(fecha)
            comanda_texto = f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .comanda {{
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    padding: 30px;
                    width: 100%;
                    box-sizing: border-box;
                }}
                h2 {{
                    color: #2E7D32;
                    text-align: center;
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                .info {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-between;
                    font-size: 14px;
                    margin-bottom: 20px;
                }}
                .info p {{
                    margin: 5px 0;
                    flex: 1 1 40%;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                    font-size: 14px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #2E7D32;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .total {{
                    font-weight: bold;
                    background-color: #E8F5E9;
                }}
            </style>
            <div class="comanda">
                <h2>COMANDA MESA: {mesa}</h2>
                <div class="info">
                    <p><strong>Fecha:</strong> {fecha}</p>
                    <p><strong>Hora:</strong> {hora}</p>
                    <p><strong>Mozo:</strong> {mozo}</p>
                    <p><strong>Comensales:</strong> {cantidad_comensales} (Infantiles: {comensales_infantiles[1]})</p>
                </div>

                <table>
                    <tr>
                        <th>Item</th>
                        <th>Cant.</th>
                        <th>Precio</th>
                        <th>Total</th>
                    </tr>
            """

            total_general = 0
            for producto in productos:
                for categoria in menu:
                    for pedido in menu[categoria]:
                        if producto == pedido["Nombre"]:
                            precio = pedido["Precio"]
                            total = precio
                            total_general += total
                            comanda_texto += f"""
                            <tr>
                                <td>{producto}</td>
                                <td>1</td>
                                <td>${precio:.2f}</td>
                                <td>${total:.2f}</td>
                            </tr>
                            """

            comanda_texto += f"""
                <tr class="total">
                    <td colspan="3">Total General:</td>
                    <td>${total_general:.2f}</td>
                </tr>
            </table>
            </div>
            """
        else:
            comanda_texto = f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .comanda-vacia {{
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    padding: 30px;
                    width: 100%;
                    box-sizing: border-box;
                    text-align: center;
                }}
                h2 {{
                    color: #2E7D32;
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                .icon {{
                    font-size: 48px;
                    color: #9E9E9E;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 16px;
                    color: #616161;
                    margin: 10px 0;
                    line-height: 1.5;
                }}
                .estado {{
                    font-size: 18px;
                    font-weight: bold;
                    color: {('#4CAF50' if estado == 'Disponible' else '#F44336')};
                    margin-top: 20px;
                }}
            </style>
            <div class="comanda-vacia">
                <h2>MESA {mesa}</h2>
                <div class="icon">📋</div>
                <p>No hay pedidos registrados para esta mesa.</p>
                <p>Esta mesa está actualmente:</p>
                <p class="estado">{estado.upper()}</p>
            </div>
            """

        self.json_input.setHtml(comanda_texto)

    def formatear_fecha(self, fecha_str):
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
            return fecha_obj.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return fecha_str


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ventana = RestaurantInterface()
    ventana.showMaximized()
    sys.exit(app.exec_())
