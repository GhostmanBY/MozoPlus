import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QDesktopWidget

from TAB_GUI_main import Main_Tab
from TAB_GUI_mozos import Mozos_Tab
from TAB_GUI_menu import Menu_Tab
from TAB_GUI_info import Info_Tab
from TAB_GUI_setings import Config

from Front.Static.QSS_Main_PC import Estilo_General, Estilo_app
from PyQt5.QtCore import Qt, QTimer
class MainApp(QMainWindow, Config):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MozoPlus")
        self.ajustar_tamano_pantalla()
        self.setStyleSheet(Estilo_General)

        # Configurar el temporizador para actualización automática
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_mesas)
        self.timer.start(5000)  # Actualizar cada 5 segundos (5000 ms)

        self.tabs = QTabWidget()
        self.tabs.addTab(Main_Tab(), "Restaurante")
        self.tabs.addTab(Mozos_Tab(), "Mozos")
        self.tabs.addTab(Menu_Tab(), "Menu")
        self.tabs.addTab(Info_Tab(), "Registro")
        
        self.setCentralWidget(self.tabs)

        self.tabs.setCornerWidget(self.config_button, Qt.TopRightCorner)

    def ajustar_tamano_pantalla(self):
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.showMaximized()

    def actualizar_mesas(self):
        # Obtener la referencia al widget Main_Tab
        main_tab = self.tabs.widget(0)  # Obtener el primer tab (Restaurante)
        if isinstance(main_tab, Main_Tab):
            main_tab.cargar_mesas()  # Llamar al método cargar_mesas del Main_Tab

if __name__ == "__main__":
    def exception_hook(exctype, value, tb):
        print(f"Excepción no manejada: {exctype}, {value}")
        print("Traceback:")
        import traceback
        print("".join(traceback.format_tb(tb)))
        sys.__excepthook__(exctype, value, tb)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(Estilo_app)
    window = MainApp()
    window.show()
    app.exec_()
