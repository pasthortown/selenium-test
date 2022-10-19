from datetime import datetime
from time import sleep
import random
from logger import Logger
from singleton import singleton
from tester import Test

@singleton
class StepsFacturacion:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm, logger: Logger, output_folder):
        self.tester: Test = tester
        self.output_folder = output_folder
        self.logger: Logger = logger
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def cobrar(self):
        self.logger.log("Cobrando")
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_facturacion") + ".png")
        self.tester.click_button_by_id("cobrar")
        sleep(5)
        cfac_id = self.tester.get_attribute_of_html_element_by_id("txtNumFactura","value", False)
        self.logger.log("Factura: " + cfac_id)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_facturacion") + ".png")
        sleep(2)
        return cfac_id

    def pago_efectivo(self):
        self.logger.log("Pago en Efectivo")
        self.tester.click_button_by_id("btnAplicarPago")
        sleep(2)

    def factura_consumidor_final(self):
        self.logger.log("Factura a Consumidor Final")
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_facturacion") + ".png")
        self.tester.click_button_by_id("btnConsumidorFinal")
        sleep(2)
    
    def factura_con_datos(self):
        self.logger.log("Factura Con Datos")
        self.tester.fill_textbox_by_id("txtClienteCI","1720364049")
        sleep(2)
        self.tester.click_button_by_id("btnBuscaCliente")
        self.tester.click_button_by_id("btnClienteConfirmarDatos")
        sleep(2)
        self.tester.click_button_by_id("alertify-cancel")
        sleep(2)
        self.tester.fill_textbox_by_id("txtClienteNombre","LUIS ALFONSO SALAZAR VACA")
        self.tester.fill_textbox_by_id("txtClienteFono","0996583107")
        self.tester.fill_textbox_by_id("txtCorreo","luissalazarvaca1986@gmail.com")
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_facturacion") + ".png")
        sleep(2)
        self.tester.click_button_by_id("btnClienteConfirmarDatosFacturar")

    def get_comprobante(self, cfac_id, tipo_comprobante, path):
        self.tester.navigate(self.url_maxpoint + 'facturacion/impresion/impresion_factura.php?cfac_id=' + cfac_id + '&tipo_comprobante=' + tipo_comprobante + '&')
        self.tester.capture(path)