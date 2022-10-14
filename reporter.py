from datetime import datetime
from io import BytesIO
import pdfkit
import jinja2
import base64
import qrcode
import os

def build_image_tag(image):
    return 'data:image/png;base64, ' + image

def get_images(path):
    archivos = os.listdir(path)
    toReturn = []
    for archivo in archivos:
        try:    
            if (archivo.split('.')[1] == 'png'):
                with open(path + archivo, "rb") as imagen:
                    b64_string = base64.b64encode(imagen.read())
                    toReturn.append(build_image_tag(b64_string.decode("utf-8")))
        except:
            pass
    return toReturn

def get_text(path):
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

def generate_pdf(template_name, params_in, output):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
    params = params_in
    template = env.get_template(template_name)
    html_processed = template.render(params)
    pdfkit.from_string(html_processed, output)

def generate_qr(toEncode):
    buffered = BytesIO()
    img = qrcode.make(toEncode)
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

proceso = get_images('./resultados/proceso/')
documentos = get_images('./resultados/documentos/')
evidencias_proceso = proceso + documentos
pasos = get_text('./resultados/')
dia = datetime.now().strftime("%d")
mes = datetime.now().strftime("%m")
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
fecha = dia + ' de ' + meses[int(mes) - 1] + ' del ' + datetime.now().strftime("%Y")
titulo = 'Reporte de pruebas de regresión'
params = {
    "qr": generate_qr(titulo + ', QA - ' + fecha),
    "titulo": titulo,
    "fecha": fecha,
    "pasos": pasos,
    "evidencias_proceso": evidencias_proceso
}

generate_pdf('reporte.html', params, 'salida2.pdf')