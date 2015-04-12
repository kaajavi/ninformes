# -*- encoding: utf-8 -*-
from django import template
from ninformes import settings
from escolar.models import Docente, Curso, MatriculaDocentes
from django.contrib.auth.models import User
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def saludo_dropdown(id_user):    
    user = User.objects.get(pk=id_user)
    docentes = Docente.objects.filter(pk=id_user)
    
    if (len(docentes)==1):
        return docentes[0].saludar()
    else:
        return "Hola " + user.username

    
@register.simple_tag
def contenido_menu(id_user):
    user = User.objects.get(pk=id_user)
    docentes = Docente.objects.filter(pk=id_user)
    docente = None
    if (len(docentes)==1):
        docente= docentes[0]
    
    
    if (docente):
        if docente.tipoDocente == 'D':
            return render_to_string('menu/menu_direccion.html',{})
        elif docente.tipoDocente == 'G':
            return render_to_string('menu/menu_gabinete.html',{})
        elif docente.tipoDocente == 'E':
            return render_to_string('menu/menu_especiales.html',{})
        else:
            return render_to_string('menu/menu_docente.html',{})
        
    else:
        return render_to_string('menu/menu_desarrollador.html',{})
    
    
@register.simple_tag
def getListadoDocentes(id_curso):
    matriculas = MatriculaDocentes.objects.filter(curso__id=id_curso)
    listado=""

    retDocentes="<ul class='list-group'>"
    if (len(matriculas)>0):
        for matricula in matriculas:
            change_url = reverse('admin:escolar_docente_change', args=(matricula.docente.id,))
            listado=listado + "<li class='list-group-item'><a href='"+change_url+"'>" + str(matricula.docente.nombreCompleto()) + " - " + matricula.tipoDocente + "</a></li>"
        retDocentes=retDocentes + listado + "</ul>"
    else:
        retDocentes = "Aún sin asignar"
    return retDocentes

@register.simple_tag
def ifdire(id_user):
    user = User.objects.get(pk=id_user)
    docentes = Docente.objects.filter(pk=id_user)
    docente = None
    if (len(docentes)==1):
        docente= docentes[0]
    
    
    if (docente):
        if docente.tipoDocente == 'D':
            return True
        else:
            return False
        
    else:
        return True