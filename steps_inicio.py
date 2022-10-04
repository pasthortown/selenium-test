from time import sleep
import random
from tester import Test

class StepsInicio:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm, passwd_user):
        self.tester: Test = tester
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
        self.passwd_usr = passwd_user
    
    def inicio_periodo(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        if (user == 'NO ASIGNADO'):
            print("Iniciando Periodo")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.click_button_by_id("btn_iniciarPeriodo")
        sleep(10)
        self.tester.click_button_by_id("btn_guardar_periodo")
        self.tester.click_button_by_id("alertify-ok")
        print("Periodo Iniciado")
    
    def asignar_cajero(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        if (user == 'NO ASIGNADO'):
            print("Asignando Cajero")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_usr)
        self.tester.click_button_by_id("validar")
        sleep(2)
        try:
            self.tester.click_button_by_id("alertify-ok")
        except:
            pass

    def login(self):
        print("Abriendo Maxpoint")
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        print("Usuario Asignado: " + user)
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_usr)
        self.tester.click_button_by_id("btn_ingresarOk")
        self.tester.click_button_by_id("alertify-ok")
        is_full_service = True
        try:
            self.tester.wait_for_html_element_by_id("PedidoRapido",5)
        except:
            is_full_service = False
            pass
        if is_full_service:
            print("Estación Full Service")
        return is_full_service