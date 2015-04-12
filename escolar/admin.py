# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy



# Register your models here.
from escolar.models import MatriculaAlumnado, MatriculaDocentes, Campo, Curso, Docente, Alumno
from escolar.forms import DocenteChangeForm, DocenteAddForm      
        
class DocenteAdmin(admin.ModelAdmin):
    form = DocenteChangeForm
    add_form = DocenteAddForm
    list_display = ('last_name', 'first_name','username','email')
    search_fields = ('last_name', 'first_name','username')
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return DocenteAddForm
        else:
            return DocenteChangeForm
    def save_model(self, request, obj, form, change):
        if not change:
            if (obj.tipoDocente == 'D'):
                obj.is_staff = True
        obj.save()
        
        
        
class CursoAdmin(admin.ModelAdmin):
    list_filter = ('ciclo','sala','anio')
    list_display = ('print_curso', 'docentes_del_curso',)
    
        
admin.site.register(Curso, CursoAdmin)
admin.site.register(Alumno)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(MatriculaAlumnado)
admin.site.register(Campo)
admin.site.register(MatriculaDocentes)
