import os

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
        


   