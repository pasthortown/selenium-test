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

class Executor:
    def __init__(self, url_maxpoint, passwd_adm, passwd_user):        
        self.output_folder = './resultados'
        filename = "logs" + datetime.now().strftime("_%m_%d_%y") + ".txt"
        self.tester = Test("http://www.google.com/")
        self.logger = Logger(self.output_folder, filename)
        self.steps_inicio = StepsInicio(self.tester, url_maxpoint, passwd_adm, passwd_user, self.logger, self.output_folder)
        self.steps_toma_pedido = StepsTomaPedido(self.tester, url_maxpoint, passwd_adm, self.logger, self.output_folder)
        self.steps_facturacion = StepsFacturacion(self.tester, url_maxpoint, passwd_adm, self.logger, self.output_folder)
        self.steps_anulacion = StepsAnulacion(self.tester, url_maxpoint, passwd_adm, self.logger, self.output_folder)
        self.steps_fin = StepsFin(self.tester, url_maxpoint, passwd_adm, self.logger, self.output_folder)
            
    def iniciar_periodo(self):
        try:
            self.steps_inicio.inicio_periodo()
        except:
            self.logger.log("Error al Iniciar Periodo")
    
    def asignar_cajero(self):
        try:
            self.steps_inicio.asignar_cajero()
        except:
            self.logger.log("Error al Asignar Cajero")
    
    def confirmar_fondo(self):
        try:
            self.steps_inicio.confirmar_fondo()
        except:
            self.logger.log("Error al Confirmar Fondo")
    
    def login(self):
        is_full_service = False
        try:
            is_full_service = self.steps_inicio.login()
        except:
            self.logger.log("Error al Autenticar el Usuario")
        return is_full_service
    
    def toma_pedido(self, num_facturas, productos_factura, is_full_service):
        cuenta_facturas_generadas = 0
        ultima_mesa = ''
        num_comprobantes = num_facturas * 2
        facturas_generadas = []
        tomando_pedido = True
        while tomando_pedido:
            tomando_pedido = cuenta_facturas_generadas < num_comprobantes
            try:
                if is_full_service:
                    ultima_mesa = self.steps_toma_pedido.seleccionar_mesa()
                solicita_datos_cliente = self.steps_toma_pedido.solicita_datos_cliente()
                if solicita_datos_cliente:
                    self.steps_toma_pedido.omitir_datos_cliente()
                self.steps_toma_pedido.toma_pedido(productos_factura)
                cfac_id = self.steps_facturacion.cobrar()
                facturas_generadas.append({"cfac_id": cfac_id, "tipo": "F"})
                self.steps_facturacion.pago_efectivo()
                cuenta_facturas_generadas = cuenta_facturas_generadas + 1
                if (cuenta_facturas_generadas % 2):
                    self.steps_facturacion.factura_consumidor_final()
                else:
                    self.steps_facturacion.factura_con_datos()
                if (cuenta_facturas_generadas % 2):    
                    is_full_service = self.steps_inicio.login()
                    if is_full_service:
                        self.steps_toma_pedido.seleccionar_mesa(ultima_mesa)
                    solicita_datos_cliente = self.steps_toma_pedido.solicita_datos_cliente()
                    if solicita_datos_cliente:
                        self.steps_toma_pedido.omitir_datos_cliente()
                    self.steps_anulacion.anular_factura(cfac_id)
                    if is_full_service:
                        self.steps_toma_pedido.seleccionar_mesa(ultima_mesa)
                    solicita_datos_cliente = self.steps_toma_pedido.solicita_datos_cliente()
                    if solicita_datos_cliente:
                        self.steps_toma_pedido.omitir_datos_cliente()
                    if is_full_service:
                        self.steps_anulacion.cerrar_ultima_mesa()
                    for factura in facturas_generadas:
                        if (factura["cfac_id"] == cfac_id):
                            factura["tipo"]= "N"
            except:
                self.logger.log("Error en la toma de pedido")
                tomando_pedido = False
        return facturas_generadas
    
    def print_comprobantes(self, facturas_generadas):
        for factura in facturas_generadas:
            prefix = "NC_"
            if (factura["tipo"] == "F"):
                prefix = "F_"
            try:
                self.steps_facturacion.get_comprobante(factura["cfac_id"], factura["tipo"], self.output_folder + "/documentos/ " + prefix + factura["cfac_id"] + '.png')
            except:
                pass
    
    def iniciar_desmontado_cajero(self):
        try:
            self.steps_fin.iniciar_desmontado_cajero()
        except:
            self.logger.log("Error al iniciar desmontado de cajero")

    def retiros(self):
        try:
            self.steps_fin.retiros()
        except:
            self.logger.log("Error al iniciar retiro de dinero")

    def corte_x(self):
        try:
            self.steps_fin.corte_x(self.output_folder + '/documentos/corte_x.png')
        except:
            self.logger.log("Error al generar el reporte corte en X")
    
    def retiro_fondo(self):
        try:
            self.steps_fin.retiro_fondo()
        except:
            self.logger.log("Error al retirar fondo")
    
    def desasignar_cajero(self):
        try:
            self.steps_fin.desasignar_cajero()
        except:
            self.logger.log("Error al desasignar cajero")

    def funciones_gerente(self):
        try:
            self.steps_fin.funciones_gerente()
        except:
            self.logger.log("Error al ingresar a funciones gerente")
    
    def fin_de_dia(self):
        try:
            self.steps_fin.fin_de_dia()
        except:
            self.logger.log("Error al iniciar el finalizado del dia")
    
    def desasignar_motorizados(self):
        try:
            self.steps_fin.desasignar_motorizados()
        except:
            self.logger.log("Error al desasignar motorizados")

    def cierre_periodo(self):
        try:
            self.steps_fin.cierre_periodo()
        except:
            self.logger.log("Error al cerrar periodo")