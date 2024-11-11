import sys
import os
import multiprocessing
import uvicorn
from PyQt5.QtWidgets import QApplication

# Importar las rutas necesarias
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar los módulos necesarios
from Front.pc_front import RestaurantInterface
from Back.Api import app

def run_api():
    """Ejecuta el servidor API FastAPI"""
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")

def run_frontend():
    """Ejecuta la interfaz gráfica PyQt"""
    app_qt = QApplication(sys.argv)
    window = RestaurantInterface()
    window.showMaximized()
    sys.exit(app_qt.exec_())

if __name__ == '__main__':
    try:
        # Iniciar API en un proceso separado
        api_process = multiprocessing.Process(target=run_api)
        api_process.start()

        # Ejecutar el frontend en el proceso principal
        run_frontend()
    except KeyboardInterrupt:
        print("Cerrando aplicación...")
    finally:
        # Asegurar que el proceso de la API se termine cuando se cierre la aplicación
        if 'api_process' in locals():
            api_process.terminate()
            api_process.join()
