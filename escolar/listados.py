import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from escolar.models import Docente, Curso, Alumno, MatriculaAlumnado, Campo, MatriculaDocentes
from xhtml2pdf import pisa  #INSTALAR ESTA LIBRERIA
from django.templatetags.static import static

##PARA MANDAR LOGS
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('django')

##BASE DE DATOS
from django.db.models import Q

FILE_LIST = settings.BASE_DIR+'/test.pdf'
# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/BASE_DIR
    
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path

##listados

def generar_listado_gdipe(request, anio):
    response = HttpResponse(content_type='application/pdf')
    logger.info("Levanto http")    
    response['Content-Disposition'] = 'attachment; filename="listado_gdipe.pdf"'
    cursos = Curso.objects.filter(ciclo=anio)
    lista_matriculas = MatriculaAlumnado.objects.filter(Q(curso__in = cursos))
    logger.info("Recibo cursos" + str(lista_matriculas))
    #Image
    #url = settings.BASE_DIR+ '/static/images/logo_amparo.png'
    #with open(url, "rb") as image_file:
    #    encoded_string = base64.b64encode(image_file.read())
    # Prepare context
    data = {
            'anio':anio,
           'cursos':cursos,
            'matriculas':lista_matriculas,
           }    

    # Render html content through html template with context
    template = get_template('listados/listado_gdipe.html')
    logger.info("Recibo template")
    html  = template.render(Context(data))
    logger.info("Render template")
    # Write PDF to file
    file = open(FILE_LIST, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    logger.info("Convierto pdf")
    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()
    logger.info("Meto pdf")
    response.write(pdf)
    # Don't forget to close the file handle
    #BORRO EL ARCHIVO
    if os.path.exists(FILE_LIST):
        try:
            os.remove(FILE_LIST)
        except OSError, e:
            pass
    
    return response

def generar_listado_gdipe_no(request, anio):
    
    cursos = Curso.objects.filter(ciclo=anio)
    
    #Image
    url = static('images/logo_amparo.png')
    with open(url, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    # Prepare context
    data = {
            'anio':anio,
           'cursos':cursos,
           'logo_64':encoded_string,
           }       

    # Render html content through html template with context
    template = get_template('listados/listado_gdipe.html')
    html  = template.render(Context(data))

    return HttpResponse(html)

def generar_listado_alumnos_pdf(request, id_curso):
    response = HttpResponse(content_type='application/pdf')
    
    try:
        curso = Curso.objects.get(pk=id_curso)  
    except Curso.DoesNotExist:
        raise Http404("El curso no existe")
        
    response['Content-Disposition'] = 'attachment; filename="listado_%s.pdf"' % (curso.curso_abreviado())
    matriculados = MatriculaAlumnado.objects.filter(curso=curso).exclude(activo=False)
    
    # Prepare context
    data = {'curso':curso,
           'matriculados':matriculados,
           }    

    # Render html content through html template with context
    template = get_template('listados/listado_alumnos.html')
    html  = template.render(Context(data))

    # Write PDF to file
    file = open(FILE_LIST, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()
    
    response.write(pdf)
    # Don't forget to close the file handle
    #BORRO EL ARCHIVO
    if os.path.exists(FILE_LIST):
        try:
            os.remove(FILE_LIST)
        except OSError, e:
            pass
    
    return response