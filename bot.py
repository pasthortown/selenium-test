import sys
from executor import Executor

passwd_adm= sys.argv[1]
passwd_user = sys.argv[2]
url_maxpoint = "http://" + sys.argv[3] + "/pos/"
num_facturas = int(sys.argv[4])
productos_factura = int(sys.argv[5])

executor = Executor(url_maxpoint, passwd_adm, passwd_user)
executor.iniciar_periodo()
executor.asignar_cajero()
executor.confirmar_fondo()
is_full_service = executor.login()
facturas_generadas = executor.toma_pedido(num_facturas, productos_factura, is_full_service)
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