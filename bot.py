import random
import sys
from steps_anulacion import StepsAnulacion
from steps_facturacion import StepsFacturacion
from steps_fin import StepsFin
from steps_inicio import StepsInicio
from steps_toma_pedido import StepsTomaPedido
from tester import Test
from logger import Logger
from datetime import datetime

today = datetime.now()
output = './resultados'
filename = "logs" + today.strftime("_%m_%d_%y") + ".txt"
logger = Logger(output, filename)
passwd_adm= sys.argv[1]
passwd_user = sys.argv[2]
url_maxpoint = "http://" + sys.argv[3] + "/pos/"
num_facturas = int(sys.argv[4])
productos_factura = int(sys.argv[5])

cuenta_facturas_generadas = 0
ultima_mesa = ''
num_comprobantes = num_facturas * 2
facturas_generadas = []
tester = Test("http://www.google.com/")
steps_inicio = StepsInicio(tester, url_maxpoint, passwd_adm, passwd_user, logger, output)
steps_toma_pedido = StepsTomaPedido(tester, url_maxpoint, passwd_adm, logger, output)
steps_facturacion = StepsFacturacion(tester, url_maxpoint, passwd_adm, logger, output)
steps_anulacion = StepsAnulacion(tester, url_maxpoint, passwd_adm, logger, output)
steps_fin = StepsFin(tester, url_maxpoint, passwd_adm, logger, output)

try:
    steps_inicio.inicio_periodo()
except:
    logger.log("Error al Iniciar Periodo")
try:
    steps_inicio.asignar_cajero()
except:
    logger.log("Error al Asignar Cajero")
try:
    steps_inicio.confirmar_fondo()
except:
    logger.log("Error al Confirmar Fondo")
    
try:
    is_full_service = steps_inicio.login()
except:
    logger.log("Error al Autenticar el Usuario")

tomando_pedido = True
while tomando_pedido:
    tomando_pedido = cuenta_facturas_generadas < num_comprobantes
    try:
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
            is_full_service = steps_inicio.login()
            if is_full_service:
                steps_toma_pedido.seleccionar_mesa(ultima_mesa)
            solicita_datos_cliente = steps_toma_pedido.solicita_datos_cliente()
            if solicita_datos_cliente:
                steps_toma_pedido.omitir_datos_cliente()
            steps_anulacion.anular_factura(cfac_id)
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
    except:
        logger.log("Error en la toma de pedido")
        tomando_pedido = False
        
for factura in facturas_generadas:
    prefix = "NC_"
    if (factura["tipo"] == "F"):
        prefix = "F_"
    try:
        steps_facturacion.get_comprobante(factura["cfac_id"], factura["tipo"], output + "/documentos/ " + prefix + factura["cfac_id"] + '.png')
    except:
        pass

try:
    steps_fin.iniciar_desmontado_cajero()
except:
    logger.log("Error al iniciar desmontado de cajero")
try:
    steps_fin.retiros()
except:
    logger.log("Error al iniciar retiro de dinero")
try:
    steps_fin.corte_x(output + '/documentos/corte_x.png')
except:
    logger.log("Error al generar el reporte corte en X")
try:
    steps_fin.iniciar_desmontado_cajero()
except:
    logger.log("Error al continuar desmontado de cajero")
try:
    steps_fin.retiro_fondo()
except:
    logger.log("Error al retirar fondo")
try:
    steps_fin.desasignar_cajero()
except:
    logger.log("Error al desasignar cajero")
try:
    steps_fin.funciones_gerente()
except:
    logger.log("Error al ingresar a funciones gerente")
try:
    steps_fin.fin_de_dia()
except:
    logger.log("Error al iniciar el finalizado del dia")
try:
    steps_fin.desasignar_motorizados()
except:
    logger.log("Error al desasignar motorizados")
try:
    steps_fin.cierre_periodo()
except:
    logger.log("Error al cerrar periodo")