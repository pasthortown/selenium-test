from time import sleep
import random
from tester import Test

class StepsFacturacion:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm):
        self.tester: Test = tester
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def cobrar(self):
        print("Cobrando")
        self.tester.click_button_by_id("cobrar")
        sleep(2)
        cfac_id = self.tester.get_attribute_of_html_element_by_id("txtNumFactura","value", False)
        print("Factura: " + cfac_id)
        sleep(2)
        return cfac_id

    def pago_efectivo(self):
        print("Pago en Efectivo")
        self.tester.click_button_by_id("btnAplicarPago")
        sleep(2)

    def factura_consumidor_final(self):
        print("Factura a Consumidor Final")
        self.tester.click_button_by_id("btnConsumidorFinal")
        sleep(2)
    
    def factura_con_datos(self):
        print("Factura Con Datos")
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
        sleep(2)
        self.tester.click_button_by_id("btnClienteConfirmarDatosFacturar")

    def get_comprobante(self, cfac_id, tipo_comprobante, path):
        self.tester.navigate(self.url_maxpoint + 'facturacion/impresion/impresion_factura.php?cfac_id=' + cfac_id + '&tipo_comprobante=' + tipo_comprobante + '&')
        self.tester.capture(path)