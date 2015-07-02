from django.shortcuts import render_to_response
from django.template import RequestContext
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa  #INSTALAR ESTA LIBRERIA
from django.templatetags.static import static
from django.http import HttpResponseRedirect, HttpResponse

from escolar.models import Docente, Curso, Alumno, MatriculaAlumnado, Campo, MatriculaDocentes, SITUACION_DOCENTE, TIPO_MATRICULA_DOCENTE, ItemCampo, DescripcionCampo

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

def view_create_principal(request):
    context = RequestContext(request)                
    return render_to_response('testing/test_create_principal.html', {},context)

###para cfk
from django import forms
from ckeditor.widgets import CKEditorWidget



class ExampleCFKForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())

def test_cfkeditor(request):
    context = RequestContext(request)                
    form = ExampleCFKForm()
    return render_to_response('testing/test_cfkeditor.html', {'form':form},context)


def test_generar_informe_matricula(request):
    response = HttpResponse(content_type='application/pdf')
            
    response['Content-Disposition'] = 'attachment; filename="informe_test.pdf"'    
    from escolar.default_data.images_base64 import LOGO_PROVINCIAL
    # Prepare context
    
    matricula = MatriculaAlumnado.objects.get(pk=112)
    descrCampo = DescripcionCampo.objects.filter(matricula_alumno=matricula, semestre=1, campo__especial=False)
    descrCampoInstitucionales = DescripcionCampo.objects.filter(matricula_alumno=matricula, semestre=1, campo__especial=True)
    
    
    data = {'etapa':1,
            'matricula':matricula,
            'descrCampo':descrCampo,
            'descrCampoInstitucionales':descrCampoInstitucionales,
            'logo_provincial':LOGO_PROVINCIAL
           }    

    # Render html content through html template with context
    template = get_template('informe/_informe.html')
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