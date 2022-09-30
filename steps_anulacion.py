from time import sleep
import random
from tester import Test

class StepsAnulacion:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm):
        self.tester: Test = tester
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def anular_factura(self, cfac_id):
        print("Iniciando Anulación de Factura")
        self.tester.click_button_by_id("boton_sidr")
        self.tester.click_button_by_id("btn_transacciones")
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        sleep(2)
        self.tester.click_button_by_id("boton_sidr")
        self.tester.click_button_by_id("cuentasCerradas")
        self.tester.fill_textbox_by_id("parBusqueda", cfac_id)
        self.tester.get_elements_by_css_class("keypad-enter2")[0].click()
        sleep(2)
        self.tester.get_elements_by_xpath('//li[@id="' + cfac_id + '"]')[0].click()
        self.tester.click_button_by_id("anularOrden")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.get_elements_by_css_class("btnVirtualOKpq")[0].click()
        self.tester.select_option_dropdown("motivosAnulacion","No existe cambio")
        self.tester.fill_textbox_by_id("motivoObservacion", "Pruebas QA")
        sleep(2)
        self.tester.click_button_by_id("btn_ok_teclado")
        print("Llenando Datos de Cliente")
        sleep(2)
        self.tester.fill_textbox_by_id("txtClienteCI","1720364049")
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        sleep(2)
        self.tester.click_button_by_id("btnClienteConfirmarDatos")
        sleep(2)
        self.tester.click_button_by_id("alertify-cancel")
        sleep(2)
        self.tester.fill_textbox_by_id("txtClienteNombre","LUIS ALFONSO SALAZAR VACA")
        self.tester.fill_textbox_by_id("txtClienteFono","0996583107")
        self.tester.fill_textbox_by_id("txtCorreo","luissalazarvaca1986@gmail.com")
        sleep(2)
        self.tester.click_button_by_id("btnClienteAnularFactura")
        sleep(4)
        self.tester.get_elements_by_css_class("botonPago")[0].click()
        sleep(4)
        self.tester.click_button_by_id("alertify-ok")
        sleep(2)
        self.tester.navigate(self.url_maxpoint)
        print("Factura Anulada: " + cfac_id)
        sleep(2)
    
    def cerrar_ultima_mesa(self):
        self.tester.click_button_by_id("Volver")
        sleep(4)