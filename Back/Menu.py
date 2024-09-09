from fpdf import FPDF
import json

# Inicializa el PDF
pdf = FPDF()
pdf.set_font("Arial", size=15)

def agregar_a_menu(pdf, nombre_plato, precio):
    """Agrega un plato al menú en el PDF."""
    pdf.cell(200, 10, txt=f"{nombre_plato} - ${precio}", ln=True, align='L')

def mostrar_menu(pdf, lista_platos):
    """Crea el archivo PDF con el menú."""
    pdf.add_page()
    pdf.cell(200, 10, txt="Menu del dia", ln=True, align='C')
    pdf.ln(10)
    for plato, precio in lista_platos:
        agregar_a_menu(pdf, plato, precio)
    pdf.output("menu.pdf")

def editar_menu(lista_platos, nombre_plato, precio):
    """Edita el precio de un plato en la lista."""
    for i, (plato, _) in enumerate(lista_platos):
        if plato == nombre_plato:
            lista_platos[i] = (nombre_plato, precio)
            break

def eliminar_de_menu(lista_platos, nombre_plato):
    """Elimina un plato de la lista."""
    lista_platos[:] = [plato for plato in lista_platos if plato[0] != nombre_plato]

def obtener_menu_en_json(lista_platos):
    """Devuelve el contenido del menu en formato json"""
    return json.dumps([{"plato": plato, "precio": precio} for plato, precio in lista_platos])

if __name__ == "__main__":
    # Lista de platos inicial
    lista_platos = [("Hamburguesa", 150), ("Pizza", 200), ("Ensalada", 100)]
    
    # Ejemplo: agregar, editar y eliminar platos
    mostrar_menu(pdf, lista_platos)
    editar_menu(lista_platos, "Hamburguesa", 180)
    eliminar_de_menu(lista_platos, "Pizza")
    
    # Muestra el menú actualizado
    pdf = FPDF()  # Reinicia el PDF para actualizarlo
    pdf.set_font("Arial", size=15)
    mostrar_menu(pdf, lista_platos)

    # Muestra el menú en formato json
    print(obtener_menu_en_json(lista_platos))

