from datetime import datetime
from time import sleep
import random
from logger import Logger
from tester import Test

class StepsInicio:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm, passwd_user, logger: Logger, output_folder):
        self.tester: Test = tester
        self.output_folder = output_folder
        self.logger: Logger = logger
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
        self.passwd_usr = passwd_user
    
    def inicio_periodo(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        if (user == 'NO ASIGNADO'):
            self.logger.log("Iniciando Periodo")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.click_button_by_id("btn_iniciarPeriodo")
        sleep(10)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_inicio_periodo") + '.png')
        sleep(1)
        self.tester.click_button_by_id("btn_guardar_periodo")
        self.tester.click_button_by_id("alertify-ok")
        self.logger.log("Periodo Iniciado")
    
    def asignar_cajero(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        if (user == 'NO ASIGNADO'):
            self.logger.log("Asignando Cajero")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_usr)
        self.tester.click_button_by_id("validar")
        esperando_validaciones = True
        while(esperando_validaciones):
            style = self.tester.get_element_by_id("mdl_rdn_pdd_crgnd",False).get_attribute("style")
            sleep(5)
            if (style == "display: none;"):
                esperando_validaciones = False
        try:
            self.tester.click_button_by_id("alertify-ok")
        except:
            pass
        self.tester.fill_textbox_by_id("usr_claveAdmin", self.passwd_adm)
        botones = self.tester.get_elements_by_css_class("btnVirtualOKpq")
        for boton in botones:
            if (boton.get_attribute("innerHTML") == "OK"):
                boton.click()
                break
        sleep(2)
        pad_numerico = self.tester.get_elements_by_xpath('//table[@id="tabla_credencialesAdminfondo"]/tbody/tr/td/button')
        for boton in pad_numerico:
            if (boton.get_attribute("innerHTML") == "2"):
                boton.click()
                break
        sleep(1)
        for boton in pad_numerico:
            if (boton.get_attribute("innerHTML") == "5"):
                boton.click()
                break
        sleep(1)
        for boton in pad_numerico:
            if (boton.get_attribute("innerHTML") == "OK"):
                boton.click()
                break
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        sleep(10)

    def confirmar_fondo(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        self.logger.log("Asignando Cajero: " + user)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cajero_asignado") + '.png')
        sleep(1)
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_usr)
        self.tester.click_button_by_id("btn_ingresarOk")
        sleep(5)
        self.tester.click_button_by_id("alertify-ok")
        sleep(10)
        self.logger.log("Cajero Asignado: " + user)
        self.tester.navigate(self.url_maxpoint )

    def login(self):
        self.logger.log("Abriendo Maxpoint")
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        self.logger.log("Usuario Asignado: " + user)
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_usr)
        self.tester.click_button_by_id("btn_ingresarOk")
        try:
            self.tester.click_button_by_id("alertify-ok")
        except:
            pass
        try:
            self.tester.click_button_by_id("alertify-ok")
        except:
            pass
        is_full_service = True
        try:
            self.tester.wait_for_html_element_by_id("PedidoRapido",5)
        except:
            is_full_service = False
            pass
        if is_full_service:
            self.logger.log("Estación Full Service")
        return is_full_service