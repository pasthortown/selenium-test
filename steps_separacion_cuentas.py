from datetime import datetime
from time import sleep
from logger import Logger
from singleton import singleton
from tester import Test


@singleton
class StepsSeparacionCuentas:
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

    def separar_cuentas(self):
        # 17 | click | id=boton_sidr | 
        self.tester.get_element_by_id("boton_sidr").click()
        # 18 | click | id=separarCuentas | 
        self.tester.get_element_by_id("separarCuentas").click()
        # 19 | click | id=alertify-ok | 
        self.tester.get_element_by_id("alertify-ok").click()
        # 20 | click | id=split_acumulado | 
        self.tester.get_element_by_id("split_acumulado").click()
        # 21 | click | css=#D4AA433E-F36B-1410-8AC1-00839939A349 > .listaproductosDesc | 
        self.tester.get_elements_by_css_class("#D4AA433E-F36B-1410-8AC1-00839939A349 > .listaproductosDesc").click()
        # 22 | click | id=id2 | 
        self.tester.get_element_by_id("id2").click()
        # 23 | click | id=btn_facturarCuenta | 
        self.tester.get_element_by_id("btn_facturarCuenta").click()
        # 24 | click | css=#btnAplicarPago > b | 
        self.tester.get_elements_by_css_class("#btnAplicarPago > b").click()
        # 26 | click | id=btnConsumidorFinal | 
        self.tester.get_element_by_id("btnConsumidorFinal").click()
        # 27 | click | id=alertify-ok | 
        self.tester.get_element_by_id("alertify-ok").click()
        # 28 | click | id=btn_facturarCuenta | 
        self.tester.get_element_by_id("btn_facturarCuenta").click()
        # 29 | click | css=#btnAplicarPago > b | 
        self.tester.get_elements_by_css_class("#btnAplicarPago > b").click()
        # 31 | click | id=rdo_pasaporte | 
        self.tester.get_element_by_id("rdo_pasaporte").click()
        # 32 | type | id=txtClienteCI | 139931082
        self.tester.get_element_by_id("txtClienteCI").send_keys("139931082")
        # 33 | click | id=btnClienteConfirmarDatos | 
        self.tester.get_element_by_id("btnClienteConfirmarDatos").click()
        # 34 | click | id=alertify-ok | 
        self.tester.get_element_by_id("alertify-ok").click()
        # 35 | click | id=alertify-ok | 
        self.tester.get_element_by_id("alertify-ok").click()