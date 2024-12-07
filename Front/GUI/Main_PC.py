import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer

# Importar las pestañas de la aplicación
from TAB_GUI_main import Main_Tab
from TAB_GUI_mozos import Mozos_Tab
from TAB_GUI_menu import Menu_Tab
from TAB_GUI_info import Info_Tab
from TAB_GUI_setings import Config

# Importar estilos
from Front.Static.QSS_Main_PC import Estilo_General, Estilo_app

class MainApp(QMainWindow):
    """
    Ventana principal de la aplicación MozoPlus.
    Maneja la interfaz principal y las diferentes pestañas.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MozoPlus")
        self.ajustar_tamano_pantalla()
        self.setStyleSheet(Estilo_General)

        # Configurar temporizador para actualización automática de mesas
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_mesas)
        self.timer.start(5000)  # Actualizar cada 5 segundos

        # Crear instancia de Main_Tab para la comunicación con Config
        self.main_tab = Main_Tab()
        
        # Crear instancia de Config pasando main_tab
        self.config = Config(self.main_tab)

        # Configurar el widget de pestañas
        self.setup_tabs()

    def setup_tabs(self):
        """Configura las pestañas de la aplicación"""
        self.tabs = QTabWidget()
        self.tabs.addTab(self.main_tab, "Restaurante")
        self.tabs.addTab(Mozos_Tab(), "Mozos")
        self.tabs.addTab(Menu_Tab(), "Menu")
        self.tabs.addTab(Info_Tab(), "Registro")
        
        self.setCentralWidget(self.tabs)
        self.tabs.setCornerWidget(self.config.config_button, Qt.TopRightCorner)

    def ajustar_tamano_pantalla(self):
        """Ajusta el tamaño de la ventana al tamaño de la pantalla"""
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.showMaximized()

    def actualizar_mesas(self):
        """Actualiza el estado de las mesas periódicamente"""
        if isinstance(self.main_tab, Main_Tab):
            self.main_tab.cargar_mesas()

if __name__ == "__main__":
    def exception_hook(exctype, value, tb):
        """Manejador de excepciones no capturadas"""
        print(f"Excepción no manejada: {exctype}, {value}")
        print("Traceback:")
        import traceback
        print("".join(traceback.format_tb(tb)))
        sys.__excepthook__(exctype, value, tb)
        sys.exit(1)

    # Configurar el manejador de excepciones
    sys.excepthook = exception_hook

    # Iniciar la aplicación
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(Estilo_app)
    window = MainApp()
    window.show()
    app.exec_()
