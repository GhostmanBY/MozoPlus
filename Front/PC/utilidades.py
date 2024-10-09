from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QDesktopWidget
import os
import json
from PyQt5.QtWidgets import QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

def ajustar_tamano_pantalla(self):
    screen = QDesktopWidget().screenGeometry()
    self.setGeometry(0, 0, screen.width(), screen.height())
    self.showMaximized()

def set_style(self):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#F0F0F0"))
    palette.setColor(QPalette.WindowText, QColor("#333333"))
    palette.setColor(QPalette.Button, QColor("#4CAF50"))
    palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Highlight, QColor("#009688"))
    self.setPalette(palette)

    self.setStyleSheet(
        """
        QWidget {
            font-family: Arial, sans-serif;
        }
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 5px;
        }
        QPushButton {
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        QTableWidget {
            alternate-background-color: #F5F5F5;
            gridline-color: #D0D0D0;
        }
        QHeaderView::section {
            background-color: #009688;
            color: white;
            padding: 8px;
            border: 1px solid #00796B;
            font-weight: bold;
        }
        QTabWidget::pane {
            border: 1px solid #D0D0D0;
            border-radius: 5px;
        }
        QTabBar::tab {
            background-color: #E0E0E0;
            color: #333333;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
        }
    """
    )

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
            mesa_button = QPushButton(f"Mesa {mesa_num}")
            mesa_button.setFont(QFont("Arial", 14, QFont.Bold))
            mesa_button.setMinimumSize(200, 150)
            mesa_button.clicked.connect(
                lambda _, num=mesa_num: mesa_clicked(self, num)
            )

            with open(
                os.path.join(directorio_json, archivo), "r", encoding="utf-8"
            ) as file:
                mesa_data = json.load(file)

            if mesa_data.get("Disponible", True):
                mesa_button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border-radius: 20px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45A049;
                    }
                    QPushButton:pressed {
                        background-color: #3D8B40;
                    }
                """
                )
            else:
                mesa_button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border-radius: 20px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                    QPushButton:pressed {
                        background-color: #C62828;
                    }
                """
                )

            self.mesas_layout.addWidget(
                mesa_button, (mesa_num - 1) // 3, (mesa_num - 1) % 3
            )

        except ValueError:
            print(f"Error: El nombre del archivo '{archivo}' no es válido")

def mesa_clicked(self, mesa_num):
    cargar_json(self, mesa_num)

def cargar_json(self, mesa_num):
    ruta_archivo = os.path.join(base_dir, f"tmp/Mesa {mesa_num}.json")
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            pedido_json = json.load(f)
            procesar_pedido_con_json(self, pedido_json)
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
        fecha_formateada = formatear_fecha(fecha)
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
                white-space: nowrap;
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
            for categoria in menu["menu"]:
                for pedido in menu["menu"][categoria]:
                    if producto == pedido["name"]:
                        precio = pedido["price"]
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

def formatear_fecha(fecha_str):
    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        return fecha_obj.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return fecha_str