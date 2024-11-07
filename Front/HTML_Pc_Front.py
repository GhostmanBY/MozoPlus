def Coamnda_HTML(comanda_style, mesa, fecha, hora, mozo, cantidad_comensales, comensales_infantiles, aclaraciones):
    Coamnda_HTML = f"""
                <style>
                    {comanda_style}
                </style>
                <div class="comanda">
                    <h2>COMANDA MESA: {mesa}</h2>
                    <div class="info">
                        <p><strong>Fecha:</strong> {fecha}</p>
                        <p><strong>Hora:</strong> {hora}</p>
                        <p><strong>Mozo:</strong> {mozo}</p>
                        <p><strong>Comensales Adultos:</strong> {cantidad_comensales}</p>
                        <p><strong>Comensales Infantiles:</strong>  {comensales_infantiles}</p>
                    </div>
                    <div class="aclaraciones">
                        <p><strong>Aclaraciones:</strong> {aclaraciones if aclaraciones else "No hay aclaraciones sobre el pedido"}</p>
                    </div>

                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Cant.</th>
                            <th>Precio</th>
                            <th>Total</th>
                        </tr>
            """
    return Coamnda_HTML

def Comanda_Vacia_HTML (Comanda_Vacia_Style, mesa, estado):
    Comanda_Vacia_HTML = f"""
                <style>
                    {Comanda_Vacia_Style}
                </style><div class="comanda-vacia">
                <h2>MESA {mesa}</h2>
                <div class="icon">📋</div>
                <p>No hay pedidos registrados para esta mesa.</p>
                <p>Esta mesa está actualmente:</p>
                <p class="estado">{estado.upper()}</p>
            </div>
            """
    return Comanda_Vacia_HTML

def Detail_Info_HTML(mesa, mozo, fecha, hora_apertura, hora_cierre, productos, total):
    productos_html = ""
    if productos:
        producto_tmp = []
        for producto in productos:
            if producto not in producto_tmp:
                cantidad = productos.count(producto)
                productos_html += f"• {producto} (x{cantidad})<br>"
                producto_tmp.append(producto)
    else:
        productos_html = "No hay productos registrados"

    return f"""
    <div class="detail-info">
        <h2>Mesa {mesa}</h2>
        <div class="info-basic">
            <p>👤 Mozo: {mozo}</p>
            <p>📅 Fecha: {fecha}</p>
            <p>🕐 Hora de apertura: {hora_apertura}</p>
            <p>🕒 Hora de cierre: {hora_cierre}</p>
        </div>
        <div class="productos">
            <h3>📋 Productos:</h3>
            <div class="productos-lista">
                {productos_html}
            </div>
        </div>
        <div class="total">
            💰 Total: ${total:.2f}
        </div>
    </div>
    """