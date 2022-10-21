from datetime import datetime
from io import BytesIO
import pdfkit
import jinja2
import base64
import qrcode
import os

class Reporter:

    def __init__(self):
        self.filename = datetime.now().strftime("%Y_%m_%d") + "_pruebas_regresion.pdf"

    def build_image_tag(self, image):
        return 'data:image/png;base64, ' + image

    def get_images(self, path):
        archivos = os.listdir(path)
        toReturn = []
        for archivo in archivos:
            try:    
                if (archivo.split('.')[1] == 'png'):
                    with open(path + archivo, "rb") as imagen:
                        b64_string = base64.b64encode(imagen.read())
                        toReturn.append(self.build_image_tag(b64_string.decode("utf-8")))
            except:
                pass
        return toReturn

    def get_text(self, path):
        archivos = os.listdir(path)
        toReturn = []
        for archivo in archivos:
            try:
                if (archivo.split('.')[1] == 'txt'):
                    with open(path + archivo, "rb") as documento:
                        lines = documento.read().splitlines()
                        for line in lines:
                            toReturn.append(line.decode("utf-8"))
            except:
                pass
        return toReturn

    def generate_pdf(self, template_name, params_in, output):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
        params = params_in
        template = env.get_template(template_name)
        html_processed = template.render(params)
        pdfkit.from_string(html_processed, output)

    def generate_qr(self, toEncode):
        buffered = BytesIO()
        img = qrcode.make(toEncode)
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str.decode('utf-8')

    def build_report(self):
        proceso = self.get_images('./resultados/proceso/')
        documentos = self.get_images('./resultados/documentos/')
        evidencias_proceso = proceso + documentos
        pasos = self.get_text('./resultados/')
        dia = datetime.now().strftime("%d")
        mes = datetime.now().strftime("%m")
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        fecha = dia + ' de ' + meses[int(mes) - 1] + ' del ' + datetime.now().strftime("%Y")
        titulo = 'Reporte de pruebas de regresión'
        params = {
            "qr": self.generate_qr(titulo + ', QA - ' + fecha),
            "titulo": titulo,
            "fecha": fecha,
            "pasos": pasos,
            "evidencias_proceso": evidencias_proceso
        }
        
        self.generate_pdf('reporte.html', params, '/output/' + self.filename)