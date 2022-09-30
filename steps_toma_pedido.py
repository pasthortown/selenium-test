from time import sleep
import random
from tester import Test

class StepsTomaPedido:
    def __init__(self, tester: Test, url_maxpoint, passwd_adm):
        self.tester: Test = tester
        self.url_maxpoint = url_maxpoint
        self.passwd_adm = passwd_adm
    
    def seleccionar_mesa(self, id_mesa_force = ''):
        mesas = self.tester.get_elements_by_css_class("mesa")
        id_ultima_mesa = mesas[len(mesas) - 1].get_attribute("id")
        id_mesa = mesas[random.randint(0, len(mesas) - 2)].get_attribute("id")
        if id_mesa_force != '':
            id_mesa = id_mesa_force
        print("Mesa seleccionada: " + id_mesa)
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
        print("Tomando Pedido")
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
            print("Agregando Producto: " + botones_productos[index].get_attribute("innerHTML"))
            sleep(2)
            self.tester.click_button_by_id(id_producto)
            sleep(2)
            self.tester.click_button_by_id("alertify-ok")
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
                                print("Respondiendo Pregunta: " + titulo_grupo)
                                index = random.randint(0, len(respuestas_grupo) - 1)
                                print("Seleccionando Respuesta: " + respuestas_grupo[index].get_attribute("innerHTML"))
                                sleep(2)
                                respuestas_grupo[index].click()
                        except:
                            pass
                self.tester.click_button_by_id("btn_prgnts_sgrds_cnfrmar")