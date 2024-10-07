from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import requests
import sys
from io import BytesIO


class MainWindow(QMainWindow):
    def __init__(self):  # Corregido el método de inicialización
        super().__init__()

        # Cambiar el título de la ventana
        self.setWindowTitle("Gestión de Restaurante")

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # Etiqueta para la imagen de fondo
        self.background_label = QLabel(self.centralwidget)
        self.background_label.setScaledContents(
            True
        )  # Permitir que la imagen se escale
        self.background_label.setGeometry(
            0, 0, self.width(), self.height()
        )  # Ajustar tamaño inicial

        # Cargar la imagen de fondo desde un enlace de internet
        self.set_background_image(
            "https://cdn.pixabay.com/photo/2023/07/30/12/11/board-8158769_1280.jpg"
        )  # Reemplaza con tu enlace

        # Crear etiqueta de título
        self.title_label = QLabel(
            "Bienvenido a la Gestión de Restaurante", self.centralwidget
        )
        self.title_label.setFont(
            QFont("Lucida handwriting", 40, QFont.Bold)
        )  # Aumentar el tamaño de la fuente
        self.title_label.setStyleSheet("color: white; background: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Crear botón
        self.pushButton1 = QPushButton("Empezar día", self.centralwidget)

        # Layout para centrar el contenido
        layout = QVBoxLayout(self.centralwidget)
        layout.setAlignment(Qt.AlignCenter)  # Centrar el contenido
        layout.addWidget(self.title_label)
        layout.addWidget(self.pushButton1)

        # Establecer estilos para el botón
        self.pushButton1.setStyleSheet(self.buttonStyle())
        self.pushButton1.setAutoFillBackground(True)  # Permitir que el fondo se rellene

    def buttonStyle(self):
        return """
        QPushButton {
            background-color: rgba(76, 175, 80, 0.8); /* Fondo semitransparente */
            color: white;
            font-size: 20px;  /* Aumentar el tamaño de la fuente del botón */
            border: 2px solid rgb(0,0,0); /* Borde blanco */
            border-radius: 10px; /* Aumentar el radio de los bordes */
            padding: 15px;  /* Aumentar el relleno */
            margin: 15px;   /* Aumentar el margen */
        }
        QPushButton:hover {
            background-color: rgb(0, 0, 0); /* Amarillo al pasar el mouse */
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.8); /* Blanco al presionar */
        }
        """

    def set_background_image(self, url):
        # Descargar la imagen desde el enlace
        response = requests.get(url)
        if response.status_code == 200:  # Verificar que la solicitud fue exitosa
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)  # Cargar la imagen
            self.background_label.setPixmap(pixmap)
        else:
            print("Error al cargar la imagen:", response.status_code)

    def resizeEvent(self, event):
        # Ajustar la etiqueta de fondo al tamaño de la ventana
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # Mostrar la ventana maximizada
    sys.exit(app.exec_())