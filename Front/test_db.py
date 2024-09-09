from customtkinter import *
import requests

def function(codigo):
    response = requests.post(f"{BASE_API}/verificar/{codigo}")
    
    # Asegúrate de que la respuesta sea exitosa
    response.raise_for_status()
    
    # Convierte la respuesta JSON a un diccionario de Python
    data = response.json()
    
    print(data['verificado'])


BASE_API = "http://127.0.0.1:8000"

letra = "Arial", 24, "bold"

root = CTk()
root.geometry("500x500")
root.title("test")

codigo = CTkEntry(root, width=150, height=50, placeholder_text="Codigo")
codigo.pack()

boot = CTkButton(root, width=100, height=50, text="login", command= lambda: function(codigo.get()))
boot.pack()

root.mainloop()