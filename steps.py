from time import sleep
from tester import Test
import random

class Steps:
    def __init__(self, url):
        self.tester = Test(url)
    
    def login(self, passwd):
        print("Abriendo Maxpoint")
        user = self.tester.get_attribute_of_html_element_by_id("Respuesta_Estacion", "innerHTML")
        print("Usuario Asignado: " + user)
        self.tester.fill_textbox_by_id("usr_clave", passwd)
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

    def seleccionar_mesa(self):
        mesas = self.tester.get_elements_by_css_class("mesa")
        id_mesa = mesas[random.randint(0, len(mesas) - 1)].get_attribute("id")
        print("Mesa seleccionada: " + id_mesa)
        sleep(2)
        self.tester.click_button_by_id(id_mesa)
        sleep(2)
        self.tester.fill_textbox_by_id("cantidad","2")
        botones_dialogo = self.tester.get_elements_by_css_class("ui-button", False)
        for boton in botones_dialogo:
            if(boton.get_attribute("innerHTML") == '<span class="ui-button-text">Continuar</span>'):
                boton.click()
                break
    
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
        
    def cobrar(self):
        print("Cobrando")
        self.tester.click_button_by_id("cobrar")
        sleep(2)
        cfac_id = self.tester.get_attribute_of_html_element_by_id("txtNumFactura","value", False)
        print("Factura: " + cfac_id)
        sleep(2)

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