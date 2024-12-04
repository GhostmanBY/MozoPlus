import sys
import json
import os
import socket

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QMessageBox

from Back.Menu_de_mesas_Back import (
    creas_mesas, crea_mesas_tmp
)
from Front.GUI.TAB_GUI_main import Main_Tab
from Front.Static.QSS_TAB_GUI_info import *

base_dir = os.path.dirname(os.path.abspath(__file__))

class Utils():
    def siguiente(self, pagina = 0, tab = ""):
        if tab.lower() == "mozo":
            pagina += 1
            return pagina
        elif tab.lower() == "menu":
            pagina += 1
            return pagina
    def anterior(self, pagina = 0, tab = ""):
        if tab.lower() == "mozo":
            pagina -= 1
            return pagina
        elif tab.lower() == "menu":
            pagina -= 1
            return pagina
        
class Setting(Main_Tab):
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

   