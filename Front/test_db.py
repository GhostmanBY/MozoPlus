from customtkinter import *

letra = "Arial", 24, "bold"

root = CTk()
root.geometry("500x500")
root.title("test")

txt = CTkLabel(root, text="Registro de menu", text_color="blue", font= letra)
txt.place(rely=0.1, relx=0.5, anchor="center")



root.mainloop()