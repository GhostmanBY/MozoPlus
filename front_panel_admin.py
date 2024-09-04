import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QSplitter)
from PyQt5.QtCore import Qt, QTimer, QTime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Gestión de Mesas")
        self.setGeometry(100, 100, 800, 400)

        self.mesa_buttons = []
        self.tiempos = []
        self.pedidos = ["pedido_mesa_1.txt", "pedido_mesa_2.txt", 
                        "pedido_mesa_3.txt", "pedido_mesa_4.txt"]
        
        self.initUI()
        
    def initUI(self):
        # Layout principal
        main_layout = QHBoxLayout()
        
        # Layout de las mesas
        mesa_layout = QVBoxLayout()
        for i in range(4):
            btn = QPushButton(f'Mesa {i + 1}')
            btn.setFixedSize(150, 150)  
            btn.setStyleSheet("background-color: grey")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.mesa_clicked(idx))
            self.mesa_buttons.append(btn)
            mesa_layout.addWidget(btn)
            self.tiempos.append(QTime(0, 0, 0))
        
        # Barra lateral
        self.pedido_view = QTextEdit()
        self.pedido_view.setReadOnly(True)
        
        cerrar_mesa_btn = QPushButton("Cerrar Mesa")
        cerrar_mesa_btn.clicked.connect(self.cerrar_mesa)

        side_layout = QVBoxLayout()
        side_layout.addWidget(self.pedido_view)
        side_layout.addWidget(cerrar_mesa_btn)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.create_widget(mesa_layout))
        splitter.addWidget(self.create_widget(side_layout))
        
        main_layout.addWidget(splitter)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Temporizador para actualizar los colores de los botones
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_buttons)
        self.timer.start(1000)  # Cada segundo
        
    def create_widget(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def mesa_clicked(self, index):
        """Evento cuando se hace clic en un botón de mesa"""
        self.pedido_view.clear()
        try:
            with open(self.pedidos[index], 'r') as file:
                self.pedido_view.setText(file.read())
                self.mesa_buttons[index].setStyleSheet("background-color: green")
        except FileNotFoundError:
            self.pedido_view.setText("Pedido no encontrado.")
    
    def cerrar_mesa(self):
        """Cerrar la mesa seleccionada"""
        for i, btn in enumerate(self.mesa_buttons):
            if btn.isChecked():
                btn.setChecked(False)
                btn.setStyleSheet("background-color: red")
                self.tiempos[i] = QTime(0, 0, 0)  # Resetear el tiempo
                break
    
    def update_buttons(self):
        """Actualizar colores de los botones según el tiempo"""
        for i, btn in enumerate(self.mesa_buttons):
            if btn.isChecked():
                self.tiempos[i] = self.tiempos[i].addSecs(1)
                if self.tiempos[i] < QTime(0, 1, 0):  # Menos de 1 minuto
                    btn.setStyleSheet("background-color: green")
                elif QTime(0, 1, 0) <= self.tiempos[i] < QTime(0, 5, 0):  # Entre 1 y 5 minutos
                    btn.setStyleSheet("background-color: orange")
                else:
                    btn.setStyleSheet("background-color: red")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
