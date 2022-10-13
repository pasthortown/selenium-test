from datetime import datetime
from time import sleep
import random
from logger import Logger
from tester import Test
import math

class StepsFin:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm, logger: Logger, output_folder):
        self.tester: Test = tester
        self.output_folder = output_folder
        self.logger: Logger = logger
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def iniciar_desmontado_cajero(self):
        self.logger.log("Iniciando Desmontado Cajero")
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        self.logger.log("Usuario Asignado: " + user)
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.click_button_by_id("desmotar")
        sleep(10)
    
    def retiros(self):
        self.logger.log("Retiros")
        self.tester.click_button_by_id("btn_retiroEfectivo")
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
        sleep(5)
        self.tester.click_button_by_id("btnEFECTIVO")
        sleep(5)
        totalEfectivo = float(self.tester.get_attribute_of_html_element_by_id("totalPosEfectivo","innerHTML"))
        denominaciones = self.buscar_denominaciones(self.tester.get_elements_by_xpath("//tr/td/input"))
        self.llenar_cantidades(totalEfectivo, denominaciones)
        sleep(2)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
        self.tester.click_button_by_id("ok_BilletesEfectivo")
        sleep(2)
        self.tester.click_button_by_id("btn_okEfectivo")
        self.tester.click_button_by_id("alertify-ok")
        self.logger.log("Retiros Completado")

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
    
    def corte_x(self, path):
        self.iniciar_desmontado_cajero()
        self.logger.log("Realizando Corte en X")
        self.tester.click_button_by_id("btn_impresionCorteX")
        ctrc_id = self.tester.get_attribute_of_html_element_by_id("IDControlEstacion","value", False)
        usr_id = self.tester.get_attribute_of_html_element_by_id("hid_usuario","value", False)
        usr_id_admin = self.tester.get_attribute_of_html_element_by_id("hid_usuario","value", False)
        self.tester.navigate(self.url_maxpoint +"corte_caja/impresion_Corte_X.php?ctrc_id=" + ctrc_id + "&usr_id=" + usr_id + "&usr_id_admin=" + usr_id_admin + "&tipoReporte=CorteX")
        self.tester.capture(path)
        self.logger.log("Corte en X - Ejecutado")
        sleep(1)

    def retiro_fondo(self):
        self.logger.log("Retirando Fondo")
        self.tester.click_button_by_id("btn_corteCaja")
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        sleep(5)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
        self.tester.click_button_by_id("btn_cash")
        sleep(2)
        self.tester.fill_textbox_by_id("usr_claveAdmin", self.passwd_adm)
        botones = self.tester.get_elements_by_css_class("btnVirtualOKpq")
        for boton in botones:
            if boton.get_attribute("innerHTML") == 'OK':
                boton.click()
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        self.logger.log("Fondo Retirado")
        sleep(5)

    def desasignar_cajero(self):
        self.logger.log("Iniciando Desmontado de Cajero")
        self.tester.click_button_by_id("btn_corteCaja")
        sleep(2)
        self.tester.click_button_by_id("btnTEFECTIVO")
        sleep(2)
        cantidades = self.tester.get_elements_by_xpath('//tr/td/input[@class="form-control hasKeypad"]')
        cantidades[0].click()
        cantidades[0].clear()
        cantidades[0].send_keys("0")
        sleep(1)
        self.tester.click_button_by_id("ok")
        sleep(2)
        self.tester.click_button_by_id("btn_okgeneral")
        sleep(2)
        self.tester.click_button_by_id("alertify-ok")
        sleep(5)
        try:
            self.tester.click_button_by_id("alertify-ok")
            sleep(5)
        except:
            pass
        try:
            self.tester.fill_textbox_by_id("txtArea","Pruebas QA - Desmontado cajero")
            today = datetime.now()
            self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
            self.tester.click_button_by_id("btn_okmotivo")
            sleep(30)
            self.tester.click_button_by_id("alertify-ok")
            sleep(5)
        except:
            pass
        self.logger.log("Cajero Desmontado")
    
    def funciones_gerente(self):
        self.tester.navigate(self.url_maxpoint )
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        if (user == 'NO ASIGNADO'):
            self.logger.log("Iniciando Cierre de Periodo")
        self.tester.fill_textbox_by_id("usr_clave", self.passwd_adm)
        self.tester.click_button_by_id("btn_ingreso_Admin")
        try:
            self.tester.click_button_by_id("alertify-ok")
        except:
            pass
        sleep(5)

    def fin_de_dia(self):   
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png") 
        botones_funciones_gerente = self.tester.get_elements_by_xpath('//input[@class="btnFuncionGerente boton"]')
        for boton in botones_funciones_gerente:
            if (boton.get_attribute("value")=="Fin de Dia"):
                boton.click()
                break
        sleep(5)

    def desasignar_motorizados(self):
        self.logger.log("Desasignando Motorizados")
        motorizados_asignados = self.tester.get_elements_by_xpath('//div[@id="motorizados"]/div/input[@class="btn btn-primary"]')
        motorizados_desmontados = motorizados_asignados[0].get_attribute("value") == 'Ningún Motorizado Asignado'
        while motorizados_desmontados != True:
            for motorizado in motorizados_asignados:
                motorizado.click()
                today = datetime.now()
                self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
                self.tester.click_button_by_id("alertify-ok")
                sleep(2)
                break
            motorizados_asignados = self.tester.get_elements_by_xpath('//div[@id="motorizados"]/input[@class="btn btn-primary"]')
            motorizados_desmontados = motorizados_asignados[0].get_attribute("value") == 'Ningún Motorizado Asignado'
        self.logger.log("Motorizados Desasignados")
    
    def cierre_periodo(self):
        self.logger.log("Cerrando Periodo")
        self.tester.click_button_by_id("btn_aceptar")
        self.tester.click_button_by_id("alertify-ok")
        sleep(5)
        try:
            self.tester.click_button_by_id("alertify-ok")
            sleep(10)
        except:
            pass
        try:
            self.tester.click_button_by_id("alertify-ok")
            sleep(10)
        except:
            pass
        try:
            self.tester.click_button_by_id("alertify-ok")
            sleep(10)
        except:
            pass
        self.tester.navigate(self.url_maxpoint)
        today = datetime.now()
        self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_cierre_dia") + ".png")
        self.logger.log("Periodo Cerrado")