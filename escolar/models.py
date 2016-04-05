# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static #Archivos estaticos
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date
from django.db.models.signals import post_save
#DEFINICIONES
TIPO_MATRICULA_DOCENTE=[
            ('A', u'Áulico'), 
            ('M', u'Especial - Música'),
            ('F', u'Especial - Ed. Física')            
        ]

SITUACION_DOCENTE=[
            ('T', u'Titular'), 
            ('S', u'Suplente')            
        ]
TURNOS=[
        ('M', u'Mañana'),
        ('T', u'Tarde'),
        ]

class Docente(User):
    '''
        El Modelo Docente hace referencia a los docentes de los niños
    '''
    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
    tipoDocente = models.CharField("Tipo de Docente",
        choices=(('T', u'Docente'),
                ('E', u'Especial'),                
                ('G', u'Gabinete'),
                ('D', u'Dirección')),
        max_length=1)
    sexo = models.CharField("Sexo",
        choices=(('H', u'Varón'),
                ('M', u'Mujer')),
        max_length=1, blank=True)
    
    def nombreCompleto(self):
        return self.first_name + " " + self.last_name
    
    def saludar(self):
        saludo = "Hola "
        if self.sexo == 'H':
            saludo = saludo + "profe "
        if self.sexo == 'M':
            saludo = saludo + u"seño "        
        saludo = saludo + self.first_name        
        return saludo
    
    def getCursos(self, ciclo):
        matriculas = MatriculaDocentes.objects.filter(docente=self, curso__ciclo = ciclo)
        cursos =  Curso.objects.filter(Q(id__in = matriculas.values_list('curso', flat=True)))        
        return cursos;
    
    def cursos_del_docente(self):
        matriculas = MatriculaDocentes.objects.filter(docente= self)
        listado=""

        retCursos="<ul class='list-group'>"
        if (len(matriculas)>0):
            for matricula in matriculas:
                #change_url = reverse('admin:escolar_docente_change', args=(matricula.docente.id,))
                change_url = '#'
                listado=listado + "<li class='list-group-item'><a href='"+change_url+"'>" + str(matricula.curso) + " - " + matricula.tipoDocente + "</a></li>"
            retCursos=retCursos + listado + "</ul>"
        else:
            retCursos = "Aún sin asignar"
        return retCursos
    
    cursos_del_docente.short_description = 'Cursos'
    cursos_del_docente.allow_tags = True
        

class Alumno(models.Model):

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['sexo','apellidos','nombres']
        
    apellidos = models.CharField("Apellidos", max_length=256)
    nombres = models.CharField("Nombres", max_length=256)
    dni = models.IntegerField("D.N.I.", unique=True)
    sexo = models.CharField("Sexo",
        choices=(('A', 'Varón'),
                ('Z', 'Mujer')),
        max_length=1)
    direccionPrincipal = models.CharField("Dirección Postal", max_length=256)
    fechaDeNacimiento = models.DateField('Fecha de Nacimiento')
    lugarDeNacimiento = models.CharField("Ciudad de Nacimiento", max_length=256)
    direccionSecundaria = models.CharField("Departamento",
                                           max_length=256,
                                           blank=True)
    provincia = models.CharField("Provincia de Nacimiento", max_length=256)
    pais = models.CharField("País de Nacimiento", max_length=256)
    nombreTutor = models.CharField("Nombre de Tutor Legal (completo)",
        max_length=256)
    actividadTutor = models.CharField("Actividad de Tutor Legal",
        max_length=256)
    telefonoHogar = models.CharField("Teléfono", max_length=256)
    celularPapa = models.CharField("Celular Papa", max_length=256)
    celularMama = models.CharField("Celular Mama", max_length=256)
    

    def presentacion_completa(self):
        return self.apellidos + u", " + self.nombres + u" ("+ str(self.dni) + u")"
    
    def lugaryfecha(self):
        return self.lugarDeNacimiento + ", " + self.fechaDeNacimiento.strftime('%d de %B de %Y')
    
    def sex_icon(self):
        if (self.sexo=='A'):
            url = static('images/boy.png')
        else:
            url = static('images/girl.png')
        return url
    
    def edad(self):         
        today = date.today()
        birth = self.fechaDeNacimiento
        years = ((today.year - birth.year - 1) + (1 if (today.month, today.day) >= (birth.month, birth.day) else 0))
        return years
    
    def __str__(self):
        return self.apellidos + u", " + self.nombres

class Curso(models.Model):

    class Meta:        
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-anio','sala']
    ciclo = models.CharField('Ciclo Lectivo',
        choices=((str(x), x) for x in range(2014,2021)),
        max_length=4)
    fechaDeMatricula = models.DateField('Fecha de Matricula')
    anio = models.CharField('Año',
        choices=((str(x), x) for x in range(2,6)),
        max_length=1)
    sala = models.CharField("Sala",
        choices=(('A', 'A'),
                ('B', 'B'),
                ('C', 'C'),
                ('D', 'D'),
                ('E', 'E'),
                ('F', 'F')),
        max_length=1) 
    turno = models.CharField("Turno",
        choices=TURNOS,
        max_length=10)    
    
    
    def getDocentes(self):
        lista_matriculados = MatriculaDocentes.objects.filter(curso=self).values_list('docente', flat=True)
        docentes = Docente.objects.filter(Q(id__in = lista_matriculados))
        return docentes

    def getMatriculasAlumnos(self):
        return self.matriculas_alumno.filter(activo=True)
    
    def getAlumnos(self):
        lista_matriculados = MatriculaAlumnado.objects.filter(curso=self, activo=True).values_list('alumno', flat=True)
        alumnos = Alumno.objects.filter(Q(id__in = lista_matriculados))
        return alumnos
    
    def getCantidadAlumnos(self):
        return len(self.getAlumnos())
    
    def print_curso(self):
        return u"Sala de " + self.anio + u" años - División: " + self.sala + u" - Turno: "+self.turno+u" - (Año " +self.ciclo+u")" 
    
    def turno_str(self):    
        for value in TURNOS:
            if (value[0]==self.turno):
                return value[1]
        return ""
    
    def docentes_del_curso(self):
        matriculas = MatriculaDocentes.objects.filter(curso= self)
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
    
    def getMatriculasDocentes(self):        
        matriculas = MatriculaDocentes.objects.filter(curso=self)
        return matriculas
    
    def getCampos(self):
        campos = Campo.objects.filter(curso=self)
        return campos
    
    def curso_abreviado(self):
        return str(self.anio) + u'_' + str(self.sala)
    
    def __unicode__(self):
        return u'Sala de ' + self.anio + u' años - División: ' + self.sala + u' - Turno: '+self.turno_str()+u' - (Año ' +self.ciclo+ u')'   

    def toString(self):
        return u'Sala de ' + self.anio + u' años - División: ' + self.sala + u' - Turno: '+self.turno_str()+u' - (Año ' +self.ciclo+ u')'   
    
    print_curso.short_description = 'Curso'
    print_curso.allow_tags = True
    docentes_del_curso.short_description = 'Docentes'
    docentes_del_curso.allow_tags = True
    
    
class Campo(models.Model):
    class Meta:
        verbose_name = 'Campo'
        verbose_name_plural = 'Campos'
        ordering = ['orden']
    curso = models.ForeignKey('Curso')    
    tipoDocente = models.CharField("Tipo de docente",
        choices = TIPO_MATRICULA_DOCENTE,
        max_length=10)
    orden = models.IntegerField("Orden", default=0)
    titulo = models.CharField("Título del campo", max_length=256)
    descripcion = models.TextField("Descripción del Campo", max_length=256, blank=True, null=True)
    aprendizajes = models.TextField("Aprendizajes", blank=True, null=True)        
    especial = models.BooleanField('Extra Curricular', default=False)
    def getTipoCampo(self):        
        for value in TIPO_MATRICULA_DOCENTE:
            if (value[0]==self.tipoDocente):
                return value[1]
        return ""
    
    def __str__(self):
        return self.titulo
    
    def aprendizajes_to_html(self):
        ap_array = self.aprendizajes.split('\n')
        ret = "<ul>"
        for arr in ap_array:
            if (len(arr)>5):
                ret = ret + "<li>" + arr + "</li>"
        ret = ret + "</ul>"
        return ret


class ItemCampo(models.Model):
    class Meta:
        verbose_name = 'Item Campo'
        verbose_name_plural = 'Items Campo'
        ordering = ['orden']
    campo = models.ForeignKey('Campo')
    item = models.TextField("Item")
    semestre = models.IntegerField('Semestre', default=3)
    color = models.CharField("Color", max_length=8)   
    orden = models.IntegerField('Orden', default=1)
    
    
class MatriculaAlumnado(models.Model):

    class Meta:
        verbose_name = 'Matricula Alumno'
        verbose_name_plural = 'Matriculación Alumnado'
        ordering = ['curso', 'alumno']
        
    curso = models.ForeignKey('Curso', related_name="matriculas_alumno")
    alumno = models.ForeignKey('Alumno')    
    activo = models.BooleanField('Activo', default=True)
    obs_p_etapa = models.TextField("observaciones primera etapa", blank= True, default="")
    obs_s_etapa = models.TextField("observaciones segunda etapa", blank= True, default="")    
    numMatricula = models.IntegerField('Número de Matrícula', default=0)
    def __str__(self):
        return str(self.alumno) + "  - " + str(self.curso)
    

class DescripcionCampo(models.Model):
    class Meta:
        ordering = ['campo']
        
    campo = models.ForeignKey('Campo')    
    matricula_alumno = models.ForeignKey('MatriculaAlumnado', default = 1)    
    descripcion = models.TextField("Descripción", blank= True, default = "")
    semestre = models.IntegerField('Semestre', default=1)
        
    def toString(self):        
        return str(self.campo)
    
    def __str__(self):
        return str(self.campo.titulo)
    
class MatriculaDocentes(models.Model):

    class Meta:
        verbose_name = 'Matricula Docentes'
        verbose_name_plural = 'Matriculaciones a Docentes'
    curso = models.ForeignKey('Curso')    
    docente = models.ForeignKey('Docente')
    tipoDocente = models.CharField("Tipo de docente",
        choices = TIPO_MATRICULA_DOCENTE,
        max_length=10)
    situacion = models.CharField("Situación",
        choices = SITUACION_DOCENTE,
        max_length=10)
    
    def situacion_str(self):    
        for value in SITUACION_DOCENTE:
            if (value[0]==self.situacion):
                return value[1]
        return "" 
        
    def tipoDocente_str(self):    
        for value in TIPO_MATRICULA_DOCENTE:
            if (value[0]==self.tipoDocente):
                return value[1]
        return ""
        
    
    def __str__(self):
        return str(self.docente) + "  - " + str(self.curso)

    



