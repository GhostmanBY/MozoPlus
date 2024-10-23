import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QScrollArea, QGridLayout, QPushButton, QComboBox,
                             QGraphicsDropShadowEffect, QMessageBox, QDialog, QLineEdit, QSpinBox,
                             QCheckBox, QDialogButtonBox, QListWidget, QListWidgetItem, QInputDialog)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer

class BotonEstilizado(QPushButton):
    def __init__(self, texto, padre=None):
        super().__init__(texto, padre)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5d8f;
            }
        """)

class WidgetMesa(QFrame):
    def __init__(self, datos_mesa, padre=None):
        super().__init__(padre)
        self.datos_mesa = datos_mesa
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(0)
        self.setMidLineWidth(0)
        self.setAutoFillBackground(True)
        self.setStyleSheet("""
            WidgetMesa {
                background-color: white;
                border-radius: 10px;
                margin: 5px;
            }
        """)

        self.setGraphicsEffect(self.crear_efecto_sombra())

        disposicion = QVBoxLayout(self)
        disposicion.setContentsMargins(15, 15, 15, 15)

        # Encabezado de la mesa
        disposicion_encabezado = QHBoxLayout()
        etiqueta_mesa = QLabel(f"Mesa: {datos_mesa.get('Mesa', 'N/A')}")
        etiqueta_mesa.setStyleSheet("font-weight: bold; color: #333; font-size: 18px;")
        disposicion_encabezado.addWidget(etiqueta_mesa)
        
        etiqueta_fecha_hora = QLabel(f"{datos_mesa.get('Fecha', 'N/A')} {datos_mesa.get('Hora', 'N/A')}")
        etiqueta_fecha_hora.setStyleSheet("color: #666; font-size: 14px;")
        disposicion_encabezado.addWidget(etiqueta_fecha_hora)
        
        disposicion.addLayout(disposicion_encabezado)

        # Mozo
        etiqueta_mozo = QLabel(f"Mozo: {datos_mesa.get('Mozo', 'N/A')}")
        etiqueta_mozo.setStyleSheet("font-size: 16px; margin-top: 5px;")
        disposicion.addWidget(etiqueta_mozo)

        # Botón de alternancia para disponibilidad
        self.boton_disponibilidad = QPushButton("Disponible" if datos_mesa.get('Disponible', True) else "No Disponible")
        self.boton_disponibilidad.setCheckable(True)
        self.boton_disponibilidad.setChecked(datos_mesa.get('Disponible', True))
        self.boton_disponibilidad.clicked.connect(self.alternar_disponibilidad)
        self.boton_disponibilidad.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
        """)
        disposicion.addWidget(self.boton_disponibilidad)

        # Estado del pedido
        self.etiqueta_estado = QLabel(f"Estado: {datos_mesa.get('Estado', 'Pendiente')}")
        self.etiqueta_estado.setStyleSheet("font-size: 16px; font-weight: bold;")
        disposicion.addWidget(self.etiqueta_estado)

        self.boton_cambiar_estado = BotonEstilizado("Cambiar Estado")
        self.boton_cambiar_estado.clicked.connect(self.cambiar_estado)
        disposicion.addWidget(self.boton_cambiar_estado)

        # Productos
        if datos_mesa.get('productos'):
            etiqueta_productos = QLabel("Productos:")
            etiqueta_productos.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
            disposicion.addWidget(etiqueta_productos)
            for producto in datos_mesa['productos']:
                etiqueta_producto = QLabel(f"- {producto}")
                etiqueta_producto.setStyleSheet("font-size: 16px;")
                disposicion.addWidget(etiqueta_producto)

        # Información de comensales
        info_comensales = QLabel(f"Comensales: {datos_mesa.get('cantidad_comensales', 0)}")
        info_comensales.setStyleSheet("font-size: 16px; margin-top: 10px;")
        disposicion.addWidget(info_comensales)

        comensales_infantiles = datos_mesa.get('comensales_infantiles', [False, 0])
        if comensales_infantiles[0]:
            info_infantiles = QLabel(f"Comensales infantiles: {comensales_infantiles[1]}")
            info_infantiles.setStyleSheet("font-size: 16px;")
            disposicion.addWidget(info_infantiles)

    def crear_efecto_sombra(self):
        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(15)
        sombra.setXOffset(0)
        sombra.setYOffset(5)
        sombra.setColor(QColor(0, 0, 0, 50))
        return sombra

    def alternar_disponibilidad(self):
        self.datos_mesa['Disponible'] = self.boton_disponibilidad.isChecked()
        self.boton_disponibilidad.setText("Disponible" if self.datos_mesa['Disponible'] else "No Disponible")
        self.actualizar_archivo_json()

    def cambiar_estado(self):
        estados = ["Pendiente", "En preparación", "Listo"]
        estado_actual = self.etiqueta_estado.text().split(": ")[1]
        nuevo_estado = estados[(estados.index(estado_actual) + 1) % len(estados)]
        self.etiqueta_estado.setText(f"Estado: {nuevo_estado}")
        self.datos_mesa['Estado'] = nuevo_estado
        self.actualizar_archivo_json()

    def actualizar_archivo_json(self):
        ruta_archivo = os.path.join('tmp', 'procesados', f"mesa_{self.datos_mesa['Mesa']}.json")
        try:
            with open(ruta_archivo, 'w') as f:
                json.dump(self.datos_mesa, f, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo actualizar el archivo JSON: {str(e)}")

class DialogoConfiguracion(QDialog):
    def __init__(self, mesa=None, padre=None):
        super().__init__(padre)
        self.mesa = mesa
        self.setWindowTitle("Configuración de Mesa")
        self.setModal(True)
        self.productos = self.cargar_productos()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.numero_mesa = QSpinBox(self)
        self.numero_mesa.setRange(1, 100)
        layout.addWidget(QLabel("Número de Mesa:"))
        layout.addWidget(self.numero_mesa)

        self.disponible = QCheckBox("Disponible", self)
        layout.addWidget(self.disponible)

        self.mozo = QLineEdit(self)
        layout.addWidget(QLabel("Mozo:"))
        layout.addWidget(self.mozo)

        self.cantidad_comensales = QSpinBox(self)
        self.cantidad_comensales.setRange(1, 20)
        layout.addWidget(QLabel("Cantidad de Comensales:"))
        layout.addWidget(self.cantidad_comensales)

        self.comensales_infantiles = QCheckBox("Comensales Infantiles", self)
        layout.addWidget(self.comensales_infantiles)

        self.cantidad_infantiles = QSpinBox(self)
        self.cantidad_infantiles.setRange(0, 10)
        layout.addWidget(QLabel("Cantidad de Comensales Infantiles:"))
        layout.addWidget(self.cantidad_infantiles)

        # Lista de productos
        self.lista_productos = QListWidget(self)
        layout.addWidget(QLabel("Productos:"))
        layout.addWidget(self.lista_productos)

        # Botones para editar, eliminar y añadir productos
        layout_botones = QHBoxLayout()
        self.boton_editar = QPushButton("Editar", self)
        self.boton_eliminar = QPushButton("Eliminar", self)
        self.boton_anadir = QPushButton("Añadir", self)
        layout_botones.addWidget(self.boton_editar)
        layout_botones.addWidget(self.boton_eliminar)
        layout_botones.addWidget(self.boton_anadir)
        layout.addLayout(layout_botones)

        self.boton_editar.clicked.connect(self.editar_producto)
        self.boton_eliminar.clicked.connect(self.eliminar_producto)
        self.boton_anadir.clicked.connect(self.anadir_producto)

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        if self.mesa:
            self.cargar_datos_mesa()

    def cargar_productos(self):
        try:
            with open('Front/productos.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            productos = []
            for categoria in ['comidas', 'bebidas', 'postres']:
                if categoria in data:
                    productos.extend([item['nombre'] for item in data[categoria]])
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {str(e)}")
            return []

    def cargar_datos_mesa(self):
        self.numero_mesa.setValue(self.mesa.get('Mesa', 1))
        self.disponible.setChecked(self.mesa.get('Disponible', True))
        self.mozo.setText(self.mesa.get('Mozo', ''))
        self.cantidad_comensales.setValue(self.mesa.get('cantidad_comensales', 1))
        comensales_infantiles = self.mesa.get('comensales_infantiles', [False, 0])
        self.comensales_infantiles.setChecked(comensales_infantiles[0])
        self.cantidad_infantiles.setValue(comensales_infantiles[1])
        
        # Cargar productos de la mesa
        self.lista_productos.clear()
        for producto in self.mesa.get('productos', []):
            self.lista_productos.addItem(producto)

    def obtener_datos(self):
        return {
            'Mesa': self.numero_mesa.value(),
            'Disponible': self.disponible.isChecked(),
            'Mozo': self.mozo.text(),
            'cantidad_comensales': self.cantidad_comensales.value(),
            'comensales_infantiles': [self.comensales_infantiles.isChecked(), self.cantidad_infantiles.value()],
            'productos': [self.lista_productos.item(i).text() for i in range(self.lista_productos.count())],
            'Hora': '',
            'Fecha': '',
            'Pagado': False,
            'Metodo': ''
        }

    def editar_producto(self):
        item_seleccionado = self.lista_productos.currentItem()
        if item_seleccionado:
            producto_actual = item_seleccionado.text()
            nuevo_producto, ok = QInputDialog.getItem(self, "Editar Producto", 
                                                      "Seleccione el nuevo producto:",
                                                      self.productos, 0, False)
            if ok and nuevo_producto:
                item_seleccionado.setText(nuevo_producto)

    def eliminar_producto(self):
        item_seleccionado = self.lista_productos.currentRow()
        if item_seleccionado != -1:
            self.lista_productos.takeItem(item_seleccionado)

    def anadir_producto(self):
        nuevo_producto, ok = QInputDialog.getItem(self, "Añadir Producto", 
                                                  "Seleccione el producto a añadir:",
                                                  self.productos, 0, False)
        if ok and nuevo_producto:
            self.lista_productos.addItem(nuevo_producto)

class Restaurante(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Restaurante")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)

        # Widget y disposición principal
        widget_principal = QWidget()
        self.setCentralWidget(widget_principal)
        disposicion_principal = QVBoxLayout(widget_principal)

        # Marco del título
        marco_titulo = QFrame()
        marco_titulo.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        disposicion_titulo = QHBoxLayout(marco_titulo)
        etiqueta_titulo = QLabel("Sistema de Mesas")
        etiqueta_titulo.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        disposicion_titulo.addWidget(etiqueta_titulo)

        # Botón de actualizar
        boton_actualizar = BotonEstilizado("Actualizar")
        boton_actualizar.clicked.connect(self.actualizar_mesas)
        disposicion_titulo.addWidget(boton_actualizar)

        # Botón de configuración
        boton_configuracion = BotonEstilizado("Configuración")
        boton_configuracion.clicked.connect(self.abrir_configuracion)
        disposicion_titulo.addWidget(boton_configuracion)

        # Menú desplegable de ordenación
        self.combo_ordenar = QComboBox()
        self.combo_ordenar.addItems(["Hora", "Mesa", "Disponibilidad"])
        self.combo_ordenar.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
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
        self.combo_ordenar.currentTextChanged.connect(self.ordenar_mesas)
        disposicion_titulo.addWidget(self.combo_ordenar)

        disposicion_principal.addWidget(marco_titulo)

        # Área de desplazamiento para las mesas
        self.area_desplazamiento = QScrollArea()
        self.area_desplazamiento.setWidgetResizable(True)
        self.area_desplazamiento.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        self.contenido_desplazamiento = QWidget()
        self.disposicion_desplazamiento = QGridLayout(self.contenido_desplazamiento)
        self.disposicion_desplazamiento.setSpacing(20)
        self.area_desplazamiento.setWidget(self.contenido_desplazamiento)
        disposicion_principal.addWidget(self.area_desplazamiento)

        # Obtener mesas de los archivos JSON
        self.mesas = self.obtener_mesas_de_json()

        # Mostrar mesas
        self.mostrar_mesas()

        # Configurar temporizador de actualización automática
        self.temporizador_actualizacion = QTimer(self)
        self.temporizador_actualizacion.timeout.connect(self.actualizar_mesas)
        self.temporizador_actualizacion.start(5000)  # Actualizar cada 5 segundos

    def obtener_mesas_de_json(self):
        mesas = []
        carpeta_procesados = os.path.join('tmp', 'procesados')
        try:
            archivos_actuales = set(os.listdir(carpeta_procesados))
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"No se encontró la carpeta: {carpeta_procesados}")
            return mesas

        # Detectar nuevos archivos
        nuevos_archivos = archivos_actuales - set(getattr(self, 'archivos_anteriores', set()))
        if nuevos_archivos:
            print(f"Nuevos archivos detectados: {nuevos_archivos}")
        
        for archivo in archivos_actuales:
            if archivo.endswith('.json'):
                ruta_archivo = os.path.join(carpeta_procesados, archivo)
                try:
                    with open(ruta_archivo, 'r') as f:
                        datos_mesa = json.load(f)
                        mesas.append(datos_mesa)
                except json.JSONDecodeError:
                    print(f"Error al decodificar JSON en el archivo: {archivo}")
                except Exception as e:
                    print(f"Error al leer el archivo {archivo}: {str(e)}")
        
        self.archivos_anteriores = archivos_actuales
        return mesas

    def mostrar_mesas(self):
        # Limpiar widgets existentes
        for i in reversed(range(self.disposicion_desplazamiento.count())): 
            self.disposicion_desplazamiento.itemAt(i).widget().setParent(None)

        for i, mesa in enumerate(self.mesas):
            widget_mesa = WidgetMesa(mesa)
            fila = i // 3
            columna = i % 3
            self.disposicion_desplazamiento.addWidget(widget_mesa, fila, columna)

    def actualizar_mesas(self):
        nuevas_mesas = self.obtener_mesas_de_json()
        if nuevas_mesas != self.mesas:
            self.mesas = nuevas_mesas
            self.mostrar_mesas()

    def ordenar_mesas(self, criterio):
        if criterio == "Hora":
            self.mesas.sort(key=lambda x: x.get("Hora", ""), reverse=True)
        elif criterio == "Mesa":
            self.mesas.sort(key=lambda x: x.get("Mesa", 0))
        elif criterio == "Disponibilidad":
            self.mesas.sort(key=lambda x: x.get("Disponible", True), reverse=True)
        self.mostrar_mesas()

    def abrir_configuracion(self):
        dialogo = DialogoConfiguracion(padre=self)
        if dialogo.exec_():
            nueva_mesa = dialogo.obtener_datos()
            self.agregar_mesa(nueva_mesa)

    def agregar_mesa(self, datos_mesa):
        ruta_archivo = os.path.join('tmp', 'procesados', f"mesa_{datos_mesa['Mesa']}.json")
        try:
            with open(ruta_archivo, 'w') as f:
                json.dump(datos_mesa, f, indent=2)
            self.actualizar_mesas()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar la mesa: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ventana = Restaurante()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()