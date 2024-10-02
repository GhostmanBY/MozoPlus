import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QScrollArea, QGridLayout, QPushButton, QComboBox,
                             QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer
import random
from datetime import datetime, timedelta

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5d8f;
            }
        """)
        

class ComandaWidget(QFrame):
    def __init__(self, comanda, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(0)
        self.setMidLineWidth(0)
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            ComandaWidget {
                background-color: white;
                border-radius: 10px;
                margin: 5px;
            }
        """)

        # Add drop shadow effect
        self.setGraphicsEffect(self.create_shadow_effect())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        

        # Comanda header
        header_layout = QHBoxLayout()
        for key, value in comanda["datos"].items():
            label = QLabel(f"{key}: {value}")
            label.setStyleSheet("font-weight: bold; color: #333;")
            header_layout.addWidget(label)
        layout.addLayout(header_layout)

        # Status indicator
        self.status_label = QLabel(f"Status: {comanda['status']}")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 5px; margin-bottom: 5px;")
        layout.addWidget(self.status_label)

        # Comanda items
        for item in comanda["items"]:
            item_layout = QHBoxLayout()
            item_layout.addWidget(QLabel(item["item"]))
            item_layout.addWidget(QLabel(f"Cantidad: {item['cantidad']}"))
            item_layout.addWidget(QLabel(f"Precio: ${item['precio_unitario']}"))
            layout.addLayout(item_layout)

        # Total
        total = sum(item["cantidad"] * item["precio_unitario"] for item in comanda["items"])
        total_label = QLabel(f"Total: ${total}")
        total_label.setAlignment(Qt.AlignRight)
        total_label.setFont(QFont("Arial", 12, QFont.Bold))
        total_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        layout.addWidget(total_label)

        # Update status button
        self.update_button = StyledButton("Update Status")
        self.update_button.clicked.connect(self.cycle_status)
        layout.addWidget(self.update_button)

        self.set_status_color(comanda['status'])

    def create_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 50))
        return shadow

    def cycle_status(self):
        current_status = self.status_label.text().split(": ")[1]
        statuses = ["New", "In Progress", "Ready"]
        next_status = statuses[(statuses.index(current_status) + 1) % len(statuses)]
        self.status_label.setText(f"Status: {next_status}")
        self.set_status_color(next_status)

    def set_status_color(self, status):
        color = self.get_status_color(status)
        self.status_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {color}; margin-top: 5px; margin-bottom: 5px;")

    def get_status_color(self, status):
        return {
            "New": "#e74c3c",
            "In Progress": "#f39c12",
            "Ready": "#2ecc71"
        }.get(status, "#000000")

class Cocina(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cocina - Sistema de Comandas")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)

        # Initialize database
        self.init_db()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Title frame
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_frame)
        title_label = QLabel("Sistema de Comandas")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)

        # Add refresh button
        refresh_button = StyledButton("Refresh")
        refresh_button.clicked.connect(self.refresh_comandas)
        title_layout.addWidget(refresh_button)

        # Add sorting dropdown
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Time", "Table", "Status"])
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.sort_combo.currentTextChanged.connect(self.sort_comandas)
        title_layout.addWidget(self.sort_combo)

        main_layout.addWidget(title_frame)

        # Scroll area for comandas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Fetch comandas from database
        self.comandas = self.fetch_comandas_from_db()

        # Display comandas
        self.display_comandas()

        # Set up auto-refresh timer
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_comandas)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds

    def init_db(self):
        self.conn = sqlite3.connect('comandas.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comandas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                hora TEXT,
                mesa TEXT,
                mozo TEXT,
                items TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

        # Check if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM comandas")
        count = self.cursor.fetchone()[0]

        # If the table is empty, add pre-loaded orders
        if count == 0:
            self.add_preloaded_orders()

    def add_preloaded_orders(self):
        items = [
            [{"item": "Hamburguesa", "cantidad": 1, "precio_unitario": 500},
             {"item": "Papas fritas", "cantidad": 1, "precio_unitario": 200}],
            [{"item": "Pizza", "cantidad": 1, "precio_unitario": 600}],
            [{"item": "Ensalada Caesar", "cantidad": 1, "precio_unitario": 400},
             {"item": "Agua mineral", "cantidad": 1, "precio_unitario": 100}],
            [{"item": "Spaghetti Bolognese", "cantidad": 1, "precio_unitario": 450},
             {"item": "Vino tinto", "cantidad": 1, "precio_unitario": 300}],
            [{"item": "Pollo a la parrilla", "cantidad": 1, "precio_unitario": 550},
             {"item": "Ensalada mixta", "cantidad": 1, "precio_unitario": 250}],
            [{"item": "Tacos de carne", "cantidad": 3, "precio_unitario": 200},
             {"item": "Guacamole", "cantidad": 1, "precio_unitario": 150}],
            [{"item": "Sushi variado", "cantidad": 1, "precio_unitario": 700},
             {"item": "Sake", "cantidad": 1, "precio_unitario": 350}],
            [{"item": "Paella", "cantidad": 2, "precio_unitario": 400},
             {"item": "Sangría", "cantidad": 1, "precio_unitario": 300}],
            [{"item": "Lasagna", "cantidad": 1, "precio_unitario": 480},
             {"item": "Tiramisú", "cantidad": 1, "precio_unitario": 200}],
            [{"item": "Churrasco", "cantidad": 1, "precio_unitario": 600},
             {"item": "Papas al horno", "cantidad": 1, "precio_unitario": 180}]
        ]

        mozos = ["Juan", "Maria", "Carlos", "Ana", "Pedro"]
        statuses = ["New", "In Progress", "Ready"]

        base_time = datetime.now() - timedelta(hours=2)  # Start 2 hours ago

        for i in range(10):
            fecha = (base_time + timedelta(minutes=i*15)).strftime("%d/%m/%Y")
            hora = (base_time + timedelta(minutes=i*15)).strftime("%H:%M")
            mesa = str(random.randint(1, 20))
            mozo = random.choice(mozos)
            order_items = items[i]
            status = random.choice(statuses)

            self.cursor.execute('''
                INSERT INTO comandas (fecha, hora, mesa, mozo, items, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (fecha, hora, mesa, mozo, str(order_items), status))

        self.conn.commit()

    def fetch_comandas_from_db(self):
        self.cursor.execute('''
            SELECT * FROM comandas ORDER BY id DESC LIMIT ?
        ''', (self.get_max_visible_comandas(),))
        rows = self.cursor.fetchall()
        comandas = []
        for row in rows:
            comanda = {
                "id": row[0],
                "datos": {
                    "Fecha": row[1],
                    "Hora": row[2],
                    "Mesa": row[3],
                    "Mozo": row[4]
                },
                "items": eval(row[5]),  # Convert string representation of list to actual list
                "status": row[6]
            }
            comandas.append(comanda)
        return comandas

    def get_max_visible_comandas(self):
        # Calculate how many comandas can fit on the screen
        # This is a simple estimation and might need adjustment
        available_height = self.height() - 100  # Subtract some height for margins and title
        comanda_height = 200  # Estimated height of a comanda widget
        return (available_height // comanda_height) * 3  # Multiply by 3 for 3 columns

    def display_comandas(self):
        # Clear existing widgets
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        for i, comanda in enumerate(self.comandas):
            comanda_widget = ComandaWidget(comanda)
            row = i // 3
            col = i % 3
            self.scroll_layout.addWidget(comanda_widget, row, col)

    def refresh_comandas(self):
        self.comandas = self.fetch_comandas_from_db()
        self.display_comandas()

    def sort_comandas(self, sort_by):
        if sort_by == "Time":
            self.comandas.sort(key=lambda x: x["datos"]["Hora"], reverse=True)
        elif sort_by == "Table":
            self.comandas.sort(key=lambda x: int(x["datos"]["Mesa"]))
        elif sort_by == "Status":
            self.comandas.sort(key=lambda x: x["status"])
        self.display_comandas()

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = Cocina()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()