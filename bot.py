from steps import Steps

# sleep(5)
url = "http://192.168.101.68:1883/pos/"
passwd = "159753"
productos_factura = 4
num_facturas = 2
facturas_generadas = []
steps = Steps(url)
is_full_service = steps.login(passwd)
for i in range(1,num_facturas + 1):
    if is_full_service:
        steps.seleccionar_mesa()
    solicita_datos_cliente = steps.solicita_datos_cliente()
    if solicita_datos_cliente:
        steps.omitir_datos_cliente()
    steps.toma_pedido(productos_factura)
    cfac_id = steps.cobrar()
    facturas_generadas.append(cfac_id)
    steps.pago_efectivo()
    if (i % 2):
        steps.factura_consumidor_final()
    else:
        steps.factura_con_datos()