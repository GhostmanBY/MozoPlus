import sys
import os

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
    QAction
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Front.Static.QSS_TAB_GUI_settings import (
    Config_Style_boton, Config_Desplegable_Menu, Ventanta_de_configuracion
)
from Front.Static.Utils import Setting

base_dir = os.path.dirname(os.path.abspath(__file__))

class Config(Setting):
    def __init__(self):
        super().__init__()
        self.device_ip = self.get_device_ip()

        self.config_button = QToolButton(self)

        self.config_menu = QMenu(self)
    
        self.cubiertos_action = QAction("💰 Precio de cubiertos", self)
        self.cubiertos_input = QLineEdit()
        
        self.mesas_action = QAction("🍽️ Cantidad de mesas", self)
        self.mesas_input = QLineEdit()

        self.ip_action = QAction(f"IP del dispositivo: {self.device_ip}", self)

        self.setup_config_menu()

    def setup_config_menu(self):
        self.config_button.setText("⚙️")
        self.config_button.setFont(QFont("Arial", 14))
        self.config_button.setPopupMode(QToolButton.InstantPopup)
        self.config_button.setStyleSheet(Config_Style_boton)

        self.config_menu.setStyleSheet(Config_Desplegable_Menu)

        self.cubiertos_action.triggered.connect(lambda: self.show_config_dialog("Precio de cubiertos"))
        self.config_menu.addAction(self.cubiertos_action)

        self.mesas_action.triggered.connect(lambda: self.show_config_dialog("Cantidad de mesas"))
        self.config_menu.addAction(self.mesas_action)

        reset_action = QAction("🔄 resetear mesas", self)
        reset_action.triggered.connect(self.reset_mesas)
        self.config_menu.addAction(reset_action)

        self.config_menu.addSeparator()  # Separador para la IP

        self.ip_action.setEnabled(False)  # Deshabilitar para que no sea clickeable
        self.config_menu.addAction(self.ip_action)

        self.config_button.setMenu(self.config_menu)

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
        