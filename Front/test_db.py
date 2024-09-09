from customtkinter import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Back.Panel_Admin_Back import Alta_Mozo, Mostrar_Mozos

def function(name, plaza):
    nombre.place_forget()
    Plaza.place_forget()
    boot.place_forget()

    categorias = ["ID", "Nombre", "Codigo", "Plaza"]

    for i in range(len(categorias)):
        categorias[i] = CTkLabel(root, width=150, height=50, font=letra, text=categorias[i])
        categorias[i].place(relx = 0.2, rely = 0.2*(i+1), anchor="center")

        
        

    Alta_Mozo(name, plaza)


letra = "Arial", 24, "bold"

root = CTk()
root.geometry("500x500")
root.title("test")

data = Mostrar_Mozos()
print(data)

nombre = CTkEntry(root, width=150, height=50, placeholder_text="Nombre")
nombre.place(relx= 0.5, rely=0.2, anchor="center")

Plaza = CTkEntry(root, width=150, height=50, placeholder_text="Numero de plaza")
Plaza.place(relx= 0.5, rely=0.4, anchor="center")

boot = CTkButton(root, width=100, height=50, text="login", command= lambda: function(nombre.get(), Plaza.get()))
boot.place(relx= 0.5, rely=0.6, anchor="center")

root.mainloop()