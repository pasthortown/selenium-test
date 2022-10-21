import os
from executor import Executor
from reporter import Reporter

passwd_adm=  os.getenv('PASSWD_ADM')
passwd_user = os.getenv('PASSWD_USER')
url_maxpoint = "http://" + os.getenv('IP_PUERTO_MAXPOINT') + "/pos/"
num_facturas = int(os.getenv('NUM_FACTURAS'))
productos_factura = int(os.getenv('NUM_PRODUCTOS_FACTURA'))

executor = Executor(url_maxpoint, passwd_adm, passwd_user)
reporter = Reporter()

executor.iniciar_periodo()
executor.asignar_cajero()
executor.confirmar_fondo()
is_full_service = executor.login()

cuenta_facturas_generadas = 0
num_comprobantes = num_facturas * 2
facturas_generadas = []
tomando_pedido = True
while tomando_pedido:
    tomando_pedido = cuenta_facturas_generadas < num_comprobantes
    result = executor.generar_factura(productos_factura, is_full_service, cuenta_facturas_generadas % 2)
    cuenta_facturas_generadas = cuenta_facturas_generadas + 1
    if (result['factura']['cfac_id'] != 'ERROR'):
        facturas_generadas.append(result['factura'])
        if (cuenta_facturas_generadas % 2):    
            anulada = executor.anular_factura(is_full_service, result['ultima_mesa'], result['factura']['cfac_id'])
            if (anulada):
                for factura in facturas_generadas:
                    if (factura["cfac_id"] == result['factura']['cfac_id']):
                        factura["tipo"]= "N"

executor.print_comprobantes(facturas_generadas)
executor.iniciar_desmontado_cajero()
executor.retiros()
executor.corte_x()
executor.iniciar_desmontado_cajero()
executor.retiro_fondo()
executor.desasignar_cajero()
executor.funciones_gerente()
executor.fin_de_dia()
executor.desasignar_motorizados()
executor.cierre_periodo()
reporter.build_report()