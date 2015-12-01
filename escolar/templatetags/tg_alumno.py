from django import template
from ninformes import settings

from escolar.models import Alumno, MatriculaAlumnado, Curso

register = template.Library()


#Deprecated
@register.simple_tag
def select_matriculando(idx_alumno=None, idx_curso=None, seleccionados=[]):
    alumno = Alumno.objects.get(pk=idx_alumno)
    curso = Curso.objects.get(pk=idx_curso)
    
    if  (len(MatriculaAlumnado.objects.filter(curso=curso, alumno=alumno))<=0 and
         str(alumno.id) not in seleccionados):
        return "<option value='"+str(idx_alumno)+"'>"+str(alumno.presentacion_completa())+"</option>"
    else:
        return "<option value='"+str(idx_alumno)+"' selected=\"True\" disabled=''>"+str(alumno.presentacion_completa())+"</option>"
    
@register.filter
def adjust_dni(dni):
    return "{:,}".format(int(dni)).replace(',','.')

@register.filter
def zerofill_2(val):
    return "{}".format(val).zfill(2)
