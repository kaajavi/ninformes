from django import template
from ninformes import settings
from escolar.models import Alumno, MatriculaAlumnado, Curso, Docente
from django.contrib.auth.models import User

from django.template.loader import render_to_string

register = template.Library()



@register.simple_tag
def class_curso(anio, seccion):
    ret= "gray"
    if (seccion == 'A'):
        ret = "red"
    elif (seccion == 'B'):
        ret = "green"
    elif (seccion == 'C'):
        ret = "blue"
    elif (seccion == 'D'):
        ret = "yellow"
    if (anio=='4'):
        ret = ret+"-live"
    return ret


@register.simple_tag
def menu_curso(option, curso, id_user):
    user = User.objects.get(pk=id_user)
    docentes = Docente.objects.filter(pk=id_user)
    gestor = True
    if (len(docentes)==1):
        if docentes[0].tipoDocente != 'D':
            gestor = False
    
    return render_to_string('curso/_c_menu.html',{'disabled':option, 'curso':curso, 'gestor':gestor })
    