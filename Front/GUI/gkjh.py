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
        
        self.Ventana_Pedido_nuevo()

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
