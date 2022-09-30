import random
from steps_anulacion import StepsAnulacion
from steps_facturacion import StepsFacturacion
from steps_fin import StepsFin
from steps_inicio import StepsInicio
from steps_toma_pedido import StepsTomaPedido
from tester import Test

url_maxpoint = "http://192.168.101.68:1883/pos/"
passwd = "159753"
passwd_adm= "123"
productos_factura = 3
num_facturas = 4
facturas_generadas = []
tester = Test("http://www.google.com/")
steps_inicio = StepsInicio(tester, url_maxpoint, passwd_adm)
steps_toma_pedido = StepsTomaPedido(tester, url_maxpoint, passwd_adm)
steps_facturacion = StepsFacturacion(tester, url_maxpoint, passwd_adm)
steps_anulacion = StepsAnulacion(tester, url_maxpoint, passwd_adm)
steps_fin = StepsFin(tester, url_maxpoint, passwd_adm)

is_full_service = steps_inicio.login(passwd)
cuenta_facturas_generadas = 0
ultima_mesa = ''
num_comprobantes = num_facturas * 2
while cuenta_facturas_generadas < num_comprobantes:
    if is_full_service:
        ultima_mesa = steps_toma_pedido.seleccionar_mesa()
    solicita_datos_cliente = steps_toma_pedido.solicita_datos_cliente()
    if solicita_datos_cliente:
        steps_toma_pedido.omitir_datos_cliente()
    steps_toma_pedido.toma_pedido(productos_factura)
    cfac_id = steps_facturacion.cobrar()
    facturas_generadas.append({"cfac_id": cfac_id, "tipo": "F"})
    steps_facturacion.pago_efectivo()
    cuenta_facturas_generadas = cuenta_facturas_generadas + 1
    if (cuenta_facturas_generadas % 2):
        steps_facturacion.factura_consumidor_final()
    else:
        steps_facturacion.factura_con_datos()
    if (cuenta_facturas_generadas % 2):    
        steps_anulacion.anular_factura(cfac_id)
        is_full_service = steps_inicio.login(passwd)
        if is_full_service:
            steps_toma_pedido.seleccionar_mesa(ultima_mesa)
        solicita_datos_cliente = steps_toma_pedido.solicita_datos_cliente()
        if solicita_datos_cliente:
            steps_toma_pedido.omitir_datos_cliente()
        if is_full_service:
            steps_anulacion.cerrar_ultima_mesa()
        for factura in facturas_generadas:
            if (factura["cfac_id"] == cfac_id):
                factura["tipo"]= "N"
        
for factura in facturas_generadas:
    folder = "notas_credito"
    if (factura["tipo"] == "F"):
        folder = "facturas"
    steps_facturacion.get_comprobante(factura["cfac_id"], factura["tipo"], './resultados/' + folder + '/' + factura["cfac_id"] + '.png')

steps_fin.iniciar_desmontado_cajero()
steps_fin.retiros()