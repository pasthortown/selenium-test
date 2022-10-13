from time import sleep
import random

from exceptiongroup import catch
from logger import Logger
from tester import Test
from datetime import datetime

class StepsTomaPedido:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm, logger: Logger, output_folder):
        self.tester: Test = tester
        self.output_folder = output_folder
        self.logger: Logger = logger
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def seleccionar_mesa(self, id_mesa_force = ''):
        try:
            mesas = self.tester.get_elements_by_css_class("mesa")
        except:
            mesas = []
        if (len(mesas) == 0):
            try:
                self.tester.click_button_by_id("PedidoRapido")
            except:
                pass
            return 'NO MESAS'
        id_ultima_mesa = mesas[len(mesas) - 1].get_attribute("id")
        id_mesa = mesas[random.randint(0, len(mesas) - 2)].get_attribute("id")
        if id_mesa_force != '':
            id_mesa = id_mesa_force
        self.logger.log("Mesa seleccionada: " + id_mesa)
        sleep(2)
        self.tester.click_button_by_id(id_mesa)
        sleep(2)
        try:
            self.tester.fill_textbox_by_id("cantidad","2")
            botones_dialogo = self.tester.get_elements_by_css_class("ui-button", False)
            for boton in botones_dialogo:
                if(boton.get_attribute("innerHTML") == '<span class="ui-button-text">Continuar</span>'):
                    boton.click()
                    break
        except:
            pass
        return id_ultima_mesa
    
    def solicita_datos_cliente(self):
        solicita_datos_cliente = True
        try:
            self.tester.wait_for_html_element_by_id("btn_opciones", 5)
        except:
            solicita_datos_cliente = False
        return solicita_datos_cliente

    def omitir_datos_cliente(self):
        self.tester.click_button_by_id("btn_opciones")
        sleep(2)
    
    def toma_pedido(self, num_productos):
        self.logger.log("Tomando Pedido")
        botones_productos = self.tester.get_elements_by_xpath('//div[@id="barraProducto"]/button')
        productos_ingresados = []
        for i in range(1,num_productos + 1):
            valido = False
            while(valido != True):
                index = random.randint(0, len(botones_productos) - 1)
                ingresado = False
                for a in productos_ingresados:
                    if (a == index):
                        ingresado = True
                if ingresado:
                    valido = False
                else:
                    productos_ingresados.append(index)
                    valido = True
            id_producto = botones_productos[index].get_attribute("id")
            today = datetime.now()
            self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_toma_pedido") + ".png")    
            self.logger.log("Agregando Producto: " + botones_productos[index].get_attribute("innerHTML"))
            sleep(2)
            self.tester.click_button_by_id(id_producto)
            sleep(2)
            try:
                self.tester.click_button_by_id("alertify-ok")        
            except:
                pass
            sleep(2)
            tiene_preguntas = True
            try:
                self.tester.wait_for_html_element_by_id("mdl_pcns_prgnts_sgrds", 5)
            except:
                tiene_preguntas = False
                pass
            if tiene_preguntas:
                grupos_preguntas = self.tester.get_elements_by_xpath('//div[@id="cntndr_body_prgnts_sgrds"]/div')
                for grupo in grupos_preguntas:
                    id_grupo = grupo.get_attribute('id')
                    botones_grupo = self.tester.get_elements_by_xpath('//div[@id="' + id_grupo + '"]/div/button')
                    respuestas_grupo = []
                    for boton in botones_grupo:
                        clase_css = boton.get_attribute("class")
                        if (clase_css == 'btn_descripcionPreguntas_sugeridas'):
                            respuestas_grupo.append(boton)
                    tipo_grupo = self.tester.get_elements_by_xpath('//div[@id="' + id_grupo + '"]/div[1]')[0].get_attribute("class")
                    titulo_grupo = self.tester.get_elements_by_xpath('//div[@id="' + id_grupo + '"]/div[1]/label')[0].get_attribute("innerHTML")
                    if (tipo_grupo == 'preguntasTituloOpcional'):
                        try:
                            if (len(respuestas_grupo) > 0):
                                self.logger.log("Respondiendo Pregunta: " + titulo_grupo)
                                index = random.randint(0, len(respuestas_grupo) - 1)
                                today = datetime.now()
                                self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_toma_pedido") + ".png")
                                self.logger.log("Seleccionando Respuesta: " + respuestas_grupo[index].get_attribute("innerHTML"))
                                sleep(2)
                                respuestas_grupo[index].click()
                        except:
                            pass
                    else:
                        min = int(titulo_grupo.split("Min:")[1].split("-")[0].strip())
                        max = int(titulo_grupo.split("Max:")[1].split(")")[0].strip())
                        cuenta = 0
                        while(cuenta < max):
                            try:
                                if (len(respuestas_grupo) > 0):
                                    self.logger.log("Respondiendo Pregunta: " + titulo_grupo)
                                    index = random.randint(0, len(respuestas_grupo) - 1)
                                    today = datetime.now()
                                    self.tester.capture(self.output_folder + '/proceso/' + today.strftime("%Y_%m_%d_%H_%M_%S_toma_pedido") + ".png")
                                    self.logger.log("Seleccionando Respuesta: " + respuestas_grupo[index].get_attribute("innerHTML"))
                                    sleep(2)
                                    respuestas_grupo[index].click()
                                    cuenta = cuenta + 1
                            except:
                                pass
                self.tester.click_button_by_id("btn_prgnts_sgrds_cnfrmar")