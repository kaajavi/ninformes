from django.conf.urls import patterns, include, url
from django.views.generic.edit import UpdateView
from ninformes import settings
from escolar.models import Alumno

urlpatterns = patterns('',
                       url(r'^$', 'escolar.views.home', name='home'),
                       url(r'^generar_cursos/$', 'escolar.views.generar_cursos', name='generar_cursos'),
                       url(r'^listados/$', 'escolar.views.listados', name='listados'),
                       url(r'^docentes/$', 'escolar.views.docentes', name='docentes'),
                       url(r'^loguearse/$', 'escolar.views.loguearse', name='loguearse'),
                       url(r'^desloguearse/$', 'escolar.views.desloguearse', name='desloguearse'),
                       #CURSO
                       url(r'^curso/(?P<id_curso>\d+)/$', 'escolar.views.mostrar_alumnos_curso', name='mostrar_alumnos_curso'),
                       url(r'^curso/miscampos/(?P<id_curso>\d+)/$', 'escolar.views.mostrar_campos_curso', name='mostrar_campos_curso'),
                       url(r'^curso/matricular/(?P<id_curso>\d+)/$', 'escolar.views.matricular_curso', name='matricular_curso'),
                       url(r'^curso/docentes/(?P<id_curso>\d+)/$', 'escolar.views.mostrar_docentes_curso', name='mostrar_docentes_curso'),
                       url(r'^curso/docente/matricular/(?P<id_curso>\d+)/$', 'escolar.views.matricular_docente', name='matricular_docente'),
                       url(r'^curso/docente/desmatricular/(?P<id_matricula>\d+)/$', 'escolar.views.desmatricular_docente', name='desmatricular_docente'), 
                       url(r'^curso/matricular_multiple/', 'escolar.views.matricular_alumnos', name='matricular_alumnos'),                
                       url(r'^curso/alumno/desmatricular/(?P<id_matricula_alumno>\d+)/$', 'escolar.views.desmatricular_alumno', name='desmatricular_alumno'),
                       url(r'^curso/alumno/matricula/eliminar/(?P<id_matricula_alumno>\d+)/$', 'escolar.views.eliminar_matricula_alumno', name='eliminar_matricula_alumno'),
                       url(r'^curso/alumno/rematricular/(?P<id_matricula_alumno>\d+)/$', 'escolar.views.rematricular_alumno', name='rematricular_alumno'),
                       #ALUMNO
                       url(r'^alumno/filtrar/', 'escolar.views.filter_alumnos', name='filtrar_alumnos'),
                       url(r'^alumno/editar/(?P<id_alumno>\d+)/(?P<id_curso>\d+)/$', 'escolar.views.edit_alumno', name="editar_alumno"), 
                       url(r'^alumno/agregar/(?P<id_curso>\d+)/$', 'escolar.views.add_alumno', name='agregar_alumno'),
                       ##CAMPOS
                       url(r'^campo/(?P<id_campo>\d+)/$', 'escolar.views.mostrar_campo', name='mostrar_campo'),       
                       ##LISTADOS
                       url(r'^listados/curso/(?P<id_curso>\d+)/$', 'escolar.listados.generar_listado_alumnos_pdf', name='generar_listado_alumnos_pdf'),
                       url(r'^listados/gdipe/(?P<anio>\d+)/$', 'escolar.listados.generar_listado_gdipe', name='generar_listado_gdipe'),
                      )
##LISTADOS - EN OTRO ARCHIVO
#urlpatterns += patterns(

#)
#url(r'^listados/curso/(?P<id_curso>\d+)/$', 'escolar.views.generate_PDF', name='generate_PDF'), 