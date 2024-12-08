import sys
import json
import os
import re
import socket

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ruta_raiz)

from PyQt5.QtWidgets import QMessageBox

from Back import (
    creas_mesas, crea_mesas_tmp, Alta_Mozo
)
from Front.GUI.TAB_GUI_main import Main_Tab
from Front.GUI.TAB_GUI_mozos import Mozos_Tab
from Front.Static.QSS_TAB_GUI_info import *

base_dir = os.path.dirname(os.path.abspath(__file__))


class Setting(Main_Tab, Mozos_Tab):
    def __init__(self, main_tab):
        super().__init__()
        self.main_tab = main_tab
    def save_config(self, config_type, valor_config ,dialog):
        try:
            if config_type == "Precio de cubiertos":
                self.precio_cubiertos = valor_config
                if os.path.exists(os.path.join(base_dir, "../../Docs/Config.json")):
                    with open(os.path.join(base_dir, "../../Docs/Config.json"), "r", encoding="utf-8") as f:
                        self.config = json.load(f)
                else:
                    self.config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
    
                self.config[0]["precio_cubiertos"] = "$" + str(self.precio_cubiertos)
            
            elif config_type == "Cantidad de mesas":
                self.cantidad_mesas = int(valor_config)
                if os.path.exists(os.path.join(base_dir, "../../Docs/Config.json")):
                    with open(os.path.join(base_dir, "../../Docs/Config.json"), "r", encoding="utf-8") as f:
                        self.config = json.load(f)
                else:
                    self.config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
                
                self.config[1]["cantidad_mesas"] = self.cantidad_mesas
                self.update_mesas_count(self.cantidad_mesas)

            elif config_type == "Mozo":
                self.mozo = valor_config

                name = self.mozo
                if re.search(r'[^a-zA-Z ]', name):
                    QMessageBox.warning(
                        self, "Error", "Por favor, no Ingrese caracteres especiales."
                    )

                if name:
                    response =Alta_Mozo(name)
                    if response:
                        QMessageBox.warning(
                            self, "Mozo no agregado", "Nombre de Mozo duplicado, por favor intente otro nombre"
                        )
                    self.load_mozos()
                else:
                    QMessageBox.warning(
                        self, "Error", "Por favor, ingrese un nombre para el mozo."
                    )
            if not config_type == "Mozo":
                with open(os.path.join(base_dir, "../../Docs/Config.json"), "w", encoding="utf-8") as f:
                    json.dump(self.config, f, indent=4)

            QMessageBox.information(dialog, "Configuración Guardada", "La configuración ha sido guardada exitosamente.")
            dialog.accept()
        except ValueError:
            QMessageBox.warning(dialog, "Error", "Por favor, ingrese un valor válido.")

    def update_mesas_count(self, new_count):
        # Actualizar la cantidad de mesas en el sistema
        creas_mesas(new_count)  # Asegúrate de que esta función esté correctamente implementada en la API
        crea_mesas_tmp()  # Asegúrate de que esta función también esté correctamente implementada
        self.cargar_mesas()  # Recargar las mesas en la interfaz
        

    def reset_mesas(self):
        # Crear el cuadro de diálogo de advertencia
        warning_message = QMessageBox(self)
        warning_message.setIcon(QMessageBox.Warning)
        warning_message.setWindowTitle("Advertencia")
        warning_message.setText("si continua se borrara toda la informacion de las mesas")
        warning_message.setInformativeText("¿Deseas continuar?")
        
        # Agregar botones de continuar y cancelar
        continue_button = warning_message.addButton("Continuar", QMessageBox.AcceptRole)
        cancel_button = warning_message.addButton("Cancelar", QMessageBox.RejectRole)
        
        # Mostrar el cuadro de diálogo y esperar respuesta
        warning_message.exec_()

        # Verificar cuál botón se presionó
        if warning_message.clickedButton() == continue_button:
            if os.path.exists(os.path.join(base_dir, "../Docs/Config.json")):
                with open(os.path.join(base_dir, "../Docs/Config.json"), "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                config = [{"precio_cubiertos": 0}, {"cantidad_mesas": 0}]
            
            self.update_mesas_count(config[1]['cantidad_mesas'])
            
        elif warning_message.clickedButton() == cancel_button:
            self.close()  # Cerrar el widget actual si se presiona "Cancelar"

    def get_device_ip(self):
        """Obtiene la dirección IP del dispositivo."""
        try:
            # Conectar a un servidor DNS público para obtener la IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"Error al obtener la IP: {e}")
            return "IP no disponible"