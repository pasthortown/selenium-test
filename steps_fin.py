from time import sleep
import random
from tester import Test
import math

class StepsFin:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm):
        self.tester: Test = tester
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def iniciar_desmontado_cajero(self):
        print("Iniciando Desmontado Cajero")
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        print("Usuario Asignado: " + user)
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.click_button_by_id("desmotar")
        sleep(10)
    
    def retiros(self):
        print("Retiros")
        self.tester.click_button_by_id("btn_retiroEfectivo")
        sleep(5)
        self.tester.click_button_by_id("btnEFECTIVO")
        sleep(5)
        totalEfectivo = float(self.tester.get_attribute_of_html_element_by_id("totalPosEfectivo","innerHTML"))
        denominaciones = self.buscar_denominaciones(self.tester.get_elements_by_xpath("//tr/td/input"))
        self.llenar_cantidades(totalEfectivo, denominaciones)
        sleep(2)
        self.tester.click_button_by_id("ok_BilletesEfectivo")
        sleep(2)
        self.tester.click_button_by_id("btn_okEfectivo")
        self.tester.click_button_by_id("alertify-ok")
        print("Retiros Completado")

    def buscar_denominaciones(self, elementos):
        denominaciones = []
        for element in elementos:
            id = element.get_attribute("id")
            if (id != ''):
                if (id.find("billete")>-1):
                    valor = float(element.get_attribute("value"))
                    if (valor > 0):
                        denominaciones.append({"tipo": "billete", "valor": valor, "id_cantidad": "b" + id, "cantidad": 0})
                if (id.find("moneda")>-1):
                    valor = float(element.get_attribute("value"))
                    if (valor > 0):
                        denominaciones.append({"tipo": "moneda", "valor": valor, "id_cantidad": "b" + id, "cantidad": 0})
        denominaciones = sorted(denominaciones, key=lambda i: i["valor"], reverse=True)
        return denominaciones
    
    def llenar_cantidades(self, totalEfectivo, denominaciones):
        resto = totalEfectivo * 100
        denominacion_random = None
        for denominacion in denominaciones:
            if (denominacion["tipo"]=="moneda"):
                self.tester.get_elements_by_xpath('//div[@id="div_billetesEfectivo"]/div/div[@class="jb-shortscroll-track"]/div/div[@data-dir="down"]')[0].click()
            if resto >= denominacion["valor"]:
                denominacion["cantidad"] = math.floor(resto / (denominacion["valor"]*100))
                resto = resto - (denominacion["cantidad"] * denominacion["valor"] * 100)
            if (denominacion["cantidad"] == 0 and denominacion_random == None):
                denominacion_random = denominacion
            self.tester.fill_textbox_by_id(denominacion["id_cantidad"],denominacion["cantidad"])
            sleep(1)
            self.tester.get_elements_by_css_class("keypad-enter2")[0].click()
            sleep(1)
        if (denominacion_random["tipo"]=="billete"):
            self.tester.get_elements_by_xpath('//div[@id="div_billetesEfectivo"]/div/div[@class="jb-shortscroll-track"]/div/div[@data-dir="up"]')[0].click()
        self.tester.fill_textbox_by_id(denominacion_random["id_cantidad"],denominacion_random["cantidad"])
        sleep(1)
        self.tester.get_elements_by_css_class("keypad-enter2")[0].click()
        sleep(1)