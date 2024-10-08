from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, 
                            QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout,
                            QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess
import os
import sys
from Back.Menu_de_mesas_Back import creas_mesas, crea_mesas_tmp

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle("Gestión de Mesas")
        self.setGeometry(300, 300, 500, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', Arial;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Frame contenedor
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(20)

        # Título
        title_label = QLabel("Configuración de Mesas")
        title_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # Contenedor para el input
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
            }
        """)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)

        # Label
        label = QLabel("Número de Mesas:")
        label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 14px;
                min-width: 120px;
            }
        """)
        input_layout.addWidget(label)

        # SpinBox
        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(50)
        self.spinBox.setValue(1)
        self.spinBox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
                font-size: 14px;
                min-width: 100px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: #f0f0f0;
                border: none;
                border-left: 1px solid #CCCCCC;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
        """)
        input_layout.addWidget(self.spinBox)
        input_layout.addStretch()

        container_layout.addWidget(input_container)

        # Botón de crear
        button_container = QFrame()
        button_container.setStyleSheet("background: transparent; border: none;")
        button_layout = QHBoxLayout(button_container)
        
        create_button = QPushButton("Crear Mesas")
        create_button.setCursor(Qt.PointingHandCursor)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #009688;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
                min-width: 120px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00877a;
            }
            QPushButton:pressed {
                background-color: #00796b;
            }
        """)
        create_button.clicked.connect(self.crearMesas)
        button_layout.addWidget(create_button, alignment=Qt.AlignCenter)
        
        container_layout.addWidget(button_container)
        container_layout.addStretch()

        # Agregar el contenedor principal al layout
        main_layout.addWidget(container)

    def crearMesas(self):
        try:
            numero_mesas = self.spinBox.value()
            creas_mesas(numero_mesas)
            crea_mesas_tmp()
            self.close()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Ocurrió un error al crear las mesas: {str(e)}",
                QMessageBox.Ok
            )

if __name__ == "__main__":
    if not os.listdir("tmp"):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        subprocess.Popen(["python", "pc_front.py"])
        subprocess.Popen(["python", "Back/Api.py"])