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
                        <p><strong>Comensales:</strong> {cantidad_comensales} (Infantiles: {comensales_infantiles})</p>
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

def Comanda_Vacia_HTML (Comanda_Vacia_Style, mesa, estado, aclaraciones):
    Comanda_Vacia_HTML = f"""
                <style>
                    {Comanda_Vacia_Style}
                </style><div class="comanda-vacia">
                <h2>MESA {mesa}</h2>
                <div class="icon">📋</div>
                <p>No hay pedidos registrados para esta mesa.</p>
                <p>Esta mesa está actualmente:</p>
                <p class="estado">{estado.upper()}</p>
                <div class="aclaraciones">
                    <p><strong>Aclaraciones:</strong> {aclaraciones if aclaraciones else "No hay aclaraciones sobre el pedido"}</p>
                </div>
            </div>
            """
    return Comanda_Vacia_HTML