# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from escolar.models import MatriculaAlumnado, Campo, Curso, Docente, Alumno
from django.forms.extras.widgets import SelectDateWidget

from django.contrib.admin.widgets import AdminDateWidget 

from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __unicode__(self):              # __unicode__ on Python 2
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="alert alert-danger">%s</div>' % ''.join(['<div class="alert-danger">%s</div>' % e for e in self])

class DocenteChangeForm(UserChangeForm):
    class Meta:
	   model = Docente
	   fields = ('first_name', 'last_name', 'email', 'username', 'tipoDocente','sexo')

class DocenteAddForm(UserCreationForm):  
    class Meta:
	   model = Docente
	   fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'tipoDocente','sexo')  
        
        


class AlumnoAddForm(forms.ModelForm):
    #your_name = forms.CharField(label='Your name', max_length=100)
    error_css_class = 'alert alert-danger'
    #required_css_class = 'alert alert-danger'
    class Meta:
        model = Alumno       
        exclude = ('',)         

    def __init__(self, *args, **kwargs):
        super(AlumnoAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if (field.required):
                field.widget.attrs['placeholder'] = 'Requerido'
                field.label = '* ' + field.label       

class AlumnoEditForm(forms.ModelForm):
    #your_name = forms.CharField(label='Your name', max_length=100)
    error_css_class = 'alert alert-danger'
    #required_css_class = 'alert alert-danger'
    class Meta:
        model = Alumno       
        exclude = ('',)         

    def __init__(self, *args, **kwargs):
        super(AlumnoEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if (field.required):
                field.widget.attrs['placeholder'] = 'Requerido'
                field.label = '* ' + field.label    
    
class CampoAddForm(forms.ModelForm):
    error_css_class = 'alert alert-danger'
    #required_css_class = 'alert alert-danger'
    class Meta:
        model = Campo       
        exclude = ('descripcion','default_anio','default_sala', 'orden')         

    def __init__(self, *args, **kwargs):
        super(CampoAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if (field.required):
                field.widget.attrs['placeholder'] = 'Requerido'
                field.label = '* ' + field.label    