# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.template.defaulttags import NowNode
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.forms import widgets
from django.conf import settings
#RESPUESTAS JSON
import json
from django.core import serializers


from escolar.models import Docente, Curso, Alumno, MatriculaAlumnado, Campo, MatriculaDocentes, SITUACION_DOCENTE, TIPO_MATRICULA_DOCENTE, ItemCampo, DescripcionCampo
from escolar.forms import AlumnoAddForm, DivErrorList, AlumnoEditForm, CampoAddForm
from escolar.default_data.campos_default import CAMPOS_SALA_4, CAMPOS_SALA_5
from escolar.default_data.images_base64 import LOGO_PROVINCIAL, LOGO_AMPARO
#Funciones
from escolar.functions import getOrdenColor, COLORES, getColoresToPrint
##Errores
from django.http import Http404

##BASE DE DATOS
from django.db.models import Q
##MENSAJES A LA VISTA (Cuadros de alertas, info, warning, etc
from django.contrib import messages

##TIEMPOS
from datetime import date

##PARA MANDAR LOGS
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('django')
anioactual = date.today().year

#MESES:
MESES=['Enero','Febrero','Marzo',
      'Abril', 'Mayo','Junio',
      'Julio','Agosto','Septiembre',
       'Octubre','Noviembre','Diciembre'
      ]




@login_required(login_url="/loguearse")
def home(request):
    context = RequestContext(request)
    profe = None
    dire = False
    ciclo = None
    docentes=None    
    tabs_control = '0'
    
    if request.method == 'POST':
        ciclo = request.POST['ciclo']        
        logger.warning('CICLO: ' + ciclo)
    if ciclo==None:
        ciclo = date.today().year 
        
    try:
        profe =  Docente.objects.get(pk=request.user)        
    except:
        logger.warning('Usuario: no es docente')
    
    ##ES DIRE
    if (profe == None or profe.tipoDocente == 'D'):
        dire = True
        cursos = Curso.objects.filter(ciclo=ciclo)
        docentes = Docente.objects.all()
    else:
        cursos = profe.getCursos(ciclo);
        
    
    return render_to_response('homes/_h_miscursos.html', 
                              {'dire':dire,
                               'ciclo_actual':str(ciclo),
                               'cursos':cursos,                               
                               'anios_disponibles':map(str,range(2014,2021)),}, 
                              context)

@login_required(login_url="/loguearse")
def docentes(request):
    context = RequestContext(request)
    profe = None
    dire = False
    ciclo = None
    docentes=None    
    tabs_control = '0'
    
    if request.method == 'POST':
        ciclo = request.POST['ciclo']        
        logger.warning('CICLO: ' + ciclo)
    if ciclo==None:
        ciclo = date.today().year 
        
    try:
        profe =  Docente.objects.get(pk=request.user)        
    except:
        logger.warning('Usuario: no es docente')
    
    ##ES DIRE
    if (profe == None or profe.tipoDocente == 'D'):
        dire = True        
        docentes = Docente.objects.all()            
        
    
    return render_to_response('homes/_h_docentes.html', 
                              {'dire':dire,
                               'ciclo_actual':str(ciclo),                            
                               'docentes':docentes,                               
                               'anios_disponibles':map(str,range(2014,2021)),}, 
                              context)

@login_required(login_url="/loguearse")
def listados(request):
    context = RequestContext(request)
    profe = None
    dire = False
    ciclo = None
    docentes=None        
    
    if request.method == 'POST':
        ciclo = request.POST['ciclo']
        
        logger.warning('CICLO: ' + ciclo)
    if ciclo==None:
        ciclo = date.today().year
        
    try:
        profe =  Docente.objects.get(pk=request.user)        
    except:
        logger.warning('Usuario: no es docente')
    
    ##ES DIRE
    if (profe == None or profe.tipoDocente == 'D'):
        dire = True
        #TODO: Los listados que tiene la direccion    
        
    
    return render_to_response('homes/_h_listados.html', 
                              {'dire':dire,
                               'ciclo_actual':ciclo,
                              'anios_disponibles':map(str,range(2014,2021)),}, 
                              context)
    

def loguearse(request):
    context = RequestContext(request)
	
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Usuario y contrasena
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Bienvenido nuevamente')
                return redirect('/')

            else:
                # An inactive account was used - no logging in!
                messages.add_message(request, messages.ERROR, 'Este usuario no está disponible!')
                return render_to_response('loguin.html', context)
        else:
            # Bad login details were provided. So we can't log the user in.            
            messages.add_message(request, messages.ERROR, 'No existe este usuario!')
            return render_to_response('login.html', context)

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
    else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object...
	
	   return render_to_response('login.html', context)

def desloguearse(request):
    logout(request)    
    context = RequestContext(request)
    messages.add_message(request, messages.SUCCESS, 'Muchas gracias!')
    return redirect('/')

#Mostrar alumnos de un curso
@login_required(login_url="/loguearse")
def mostrar_alumnos_curso(request, id_curso):
    context = RequestContext(request)    
    tabs_control='0'
    try:
        curso = Curso.objects.get(pk=id_curso)  
    except Curso.DoesNotExist:
        raise Http404("El curso no existe")
  
    matriculados = MatriculaAlumnado.objects.filter(curso=curso).exclude(activo=False)
    matriculados_inactivos = MatriculaAlumnado.objects.filter(curso=curso).exclude(activo=True)
    return render_to_response('curso/_lista_alumnos.html', 
                              {'curso':curso,
                               'matriculados':matriculados,
                               'matriculados_inactivos':matriculados_inactivos,}
                              , context)



#Mostrar alumnos de un curso
@login_required(login_url="/loguearse")
def matricular_curso(request, id_curso):
    context = RequestContext(request)    
    tabs_control='0'
    curso = Curso.objects.get(pk=id_curso)    
    lista_matriculados = MatriculaAlumnado.objects.filter(curso=curso).values_list('alumno', flat=True)
    matriculados = Alumno.objects.filter(Q(id__in = lista_matriculados))
    alumnos=Alumno.objects.filter(~Q(id__in = lista_matriculados))
    return render_to_response('curso/_matriculacion_alumnos.html', 
                              {'curso':curso,
                               'alumnos':alumnos, 
                               'matriculados':matriculados}
                              , context)


##SOLO CON AJAX!
@login_required(login_url="/loguearse")
def filter_alumnos(request):
    if request.method == 'POST':
        logger.warning('Entra: ' )        
        seleccionados = request.POST['seleccionados']
        texto_buscado = request.POST['texto_buscado']
        curso = Curso.objects.get(pk=request.POST['idx_curso'])
        logger.warning('Seleccionados: ' + seleccionados)
        lista_matriculados = MatriculaAlumnado.objects.filter(curso=curso).values_list('alumno', flat=True)
        matriculados = curso.getAlumnos()        
        id_seleccionados=[]
        try:
            for i in seleccionados.split('-'):
                id_seleccionados.append(int(i))
        except ValueError:
            pass
        
        logger.warning('ID Seleccionados: ' + str(id_seleccionados))
        if (len(texto_buscado)>=3):
            alumnos=Alumno.objects.filter(
                (Q(nombres__contains=texto_buscado) |
                Q(apellidos__contains=texto_buscado) |
                Q(dni__contains=texto_buscado) ) &
                ~Q(id__in = (lista_matriculados)) &
                ~Q(id__in = (id_seleccionados)) 
                )
        else:
            alumnos = Alumno.objects.filter(~Q(id__in = (lista_matriculados)) & ~Q(id__in = (id_seleccionados)) )     
        
        return render_to_response('curso/_matriculacion_alumnos_select.html',
                                  {'curso':curso,'alumnos':alumnos, 'matriculados':matriculados})

@login_required(login_url="/loguearse")
def add_alumno(request, id_curso):
    context = RequestContext(request)  
    curso = ""
    if request.method == 'POST':
        # get data from POST request to contactform
        
        form = AlumnoAddForm(request.POST, error_class=DivErrorList)
        
        if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
            student = form.save(commit=False)
            # commit=False tells Django that "Don't send this to database yet.
            # I have more things I want to do with it."            
            student.save() # Now you can send it to DB
            messages.add_message(request, messages.SUCCESS, 'Se agregó el alumno ' + student.presentacion_completa())
            if (int(id_curso) > 0):
                matricular = MatriculaAlumnado()
                matricular.curso = Curso.objects.get(pk=id_curso)
                matricular.alumno = student
                matricular.save()
            
            if 'si_volver' in request.POST: 
                return redirect('escolar:matricular_curso', id_curso=id_curso)
            else:
                form=AlumnoAddForm(error_class=DivErrorList)
            #else:
            #    return redirect('escolar:home',{})
    else:
        #form=AlumnoAddForm(Alumno.objects.filter(pk=1).values()[0],error_class=DivErrorList)
        form=AlumnoAddForm(error_class=DivErrorList)
    if int(id_curso)>0:
        curso = Curso.objects.get(pk=id_curso)
    return render_to_response('alumno/add_alumno.html', {'form': form, 'id_curso':id_curso ,'curso':curso},context)

@login_required(login_url="/loguearse")
def edit_alumno(request, id_alumno, id_curso):
    context = RequestContext(request)  
    try:
        alumno = Alumno.objects.get(pk=id_alumno)        
    except Alumno.DoesNotExist:
        raise Http404("El alumno no existe")

    try:
        curso =  Curso.objects.get(pk=id_curso)        
    except Curso.DoesNotExist:
        curso = None

    errores = {}

    if request.method == 'POST':
        form = AlumnoEditForm(request.POST,
                instance=alumno)
        if form.is_valid():   
            messages.add_message(request, messages.SUCCESS, 'Se guardaron los cambios de: ' + alumno.presentacion_completa())
            form.save()
    else:
        form=AlumnoEditForm(error_class=DivErrorList, instance=alumno)    
    return render_to_response('alumno/edit_alumno.html', {'form':form, 'alumno': alumno, 'curso': curso},context)

@login_required(login_url="/loguearse")
def desmatricular_alumno(request, id_matricula_alumno):
    context = RequestContext(request)  
    try:
        matriculaAlumno = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)
    except MatriculaAlumnado.DoesNotExist:
        raise Http404("El alumno no existe")    
    alumno = matriculaAlumno.alumno
    errores = {}    
    if request.method == 'POST':
        if 'si_desmatricular' in request.POST: 
            matriculaAlumno.activo=False
            matriculaAlumno.save()
            messages.add_message(request, messages.SUCCESS, 'Se desmatriculo el alumno: ' + alumno.presentacion_completa())
            return redirect('escolar:mostrar_alumnos_curso', id_curso=matriculaAlumno.curso.id)
    return render_to_response('curso/desmatricular_alumno.html', {'matriculaAlumno': matriculaAlumno},context)


@login_required(login_url="/loguearse")
def eliminar_matricula_alumno(request, id_matricula_alumno):
    context = RequestContext(request)  
    try:
        matriculaAlumno = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)
    except MatriculaAlumnado.DoesNotExist:
        raise Http404("El alumno no existe")    
    curso = matriculaAlumno.curso
    alumno = matriculaAlumno.alumno
    errores = {}    
    if request.method == 'POST':
        if 'si_desmatricular' in request.POST: 
            matriculaAlumno.delete()
            messages.add_message(request, messages.SUCCESS, 'Se eliminó la matrícula del alumno: ' + alumno.presentacion_completa())
            return redirect('escolar:mostrar_alumnos_curso', id_curso=curso.id)
    return render_to_response('curso/eliminar_matricula_alumno.html', {'matriculaAlumno': matriculaAlumno},context)


@login_required(login_url="/loguearse")
def rematricular_alumno(request, id_matricula_alumno):
    context = RequestContext(request)  
    try:
        matriculaAlumno = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)
    except MatriculaAlumnado.DoesNotExist:
        raise Http404("El alumno no existe")    
    alumno = matriculaAlumno.alumno
    errores = {}    
    if request.method == 'POST':
        if 'si_rematricular' in request.POST: 
            matriculaAlumno.activo=True
            matriculaAlumno.save()
            messages.add_message(request, messages.SUCCESS, 'Se rematricula el alumno: ' + alumno.presentacion_completa())
            return redirect('escolar:mostrar_alumnos_curso', id_curso=matriculaAlumno.curso.id)
    return render_to_response('curso/rematricular_alumno.html', {'matriculaAlumno': matriculaAlumno},context)


@login_required(login_url="/loguearse")
def generar_cursos(request):
    context = RequestContext(request)      
    profe=None
    try:
        profe =  Docente.objects.get(pk=request.user)        
    except:
        logger.warning('Usuario: no es docente')        
    if (profe == None or profe.tipoDocente == 'D'):
        if request.method == 'POST':
            ciclo= request.POST['ciclo']
            dia = request.POST['dia']
            mes = request.POST['mes']
            anio = request.POST['anio']
            fecha =date(int(anio),int(mes),int(dia))
            logger.warning('Fecha Matricula: ' +  fecha.strftime("%Y-%B-%d"))
            for anio in [4,5]:
                for sala in "ABCD":
                    existente=Curso.objects.filter(sala=sala, anio=anio, ciclo=ciclo)
                    if len(existente)==0:
                        curso = Curso()
                        curso.sala = sala
                        curso.ciclo = ciclo
                        curso.anio = anio
                        curso.fechaDeMatricula=fecha
                        
                        if sala=='A' or sala=='B':
                            curso.turno = "M"
                        else:
                            curso.turno = "T"
                        curso.save()
                        logger.warning('GENERAR CURSO: Curso ' + str(anio) + " - " + sala +" GUARDADO" )
                    else:
                        curso = existente[0]
                        logger.warning('GENERAR CURSO: Curso ' + str(anio) + " - " + sala +" YA EXISTE" )
                    #TODO
                    if anio == 4:
                        campos = CAMPOS_SALA_4
                    elif anio == 5:
                        campos = CAMPOS_SALA_5
                    for orden in campos:
                        is_exist = Campo.objects.filter(Q(curso = curso) & Q(titulo = campos[orden][1]))
                        logger.warning('Generando Campo: Curso ' + str(curso) +" - Campo: " + str(orden) )
                        if len(is_exist)==0:    
                            logger.warning('Creando: Curso ' + str(curso) +" - Campo: " + str(orden) )
                            campo = Campo()
                            campo.curso = curso
                            campo.tipoDocente = campos[orden][0]
                            campo.orden = orden
                            campo.titulo = campos[orden][1]
                            campo.aprendizajes = campos[orden][2]
                            if len(campos[orden])==4:
                                campo.especial = campos[orden][3]
                            campo.save()
                        
                        
            return redirect('/')

        else:
            return render_to_response('curso/generar_cursos.html', 
                                      {'dias_disponibles':range(1,32),
                                      'meses_disponibles':MESES,
                                      'anios_disponibles':map(str,range(date.today().year,2021)),},
                                      context)
    return redirect('/')


    

@login_required(login_url="/loguearse")
def mostrar_docentes_curso(request, id_curso):
    context = RequestContext(request)    
    tabs_control='0'
    try:
        curso = Curso.objects.get(pk=id_curso)  
    except Poll.DoesNotExist:
        raise Http404("El curso no existe")
      
    docentesMatriculados = MatriculaDocentes.objects.filter(curso=curso)
    
    return render_to_response('curso/_lista_docentes.html', 
                              {'curso':curso,
                               'docentesMatriculados':docentesMatriculados,}
                              , context)

@login_required(login_url="/loguearse")
def matricular_docente(request, id_curso):
    context = RequestContext(request)        
    try:
        curso = Curso.objects.get(pk=id_curso)  
    except Curso.DoesNotExist:
        raise Http404("El curso no existe")
      
    if request.method == 'POST':
        if 'si_matricular' in request.POST: 
            docente_id= request.POST['docente_id']
            tipoDocente= request.POST['tipo_matricula']
            situacion= request.POST['situacion']            
            
            try:
                matricula = MatriculaDocentes()
                docente = Docente.objects.get(pk=docente_id)                                              
                matricula.curso = curso
                matricula.tipoDocente = tipoDocente
                matricula.situacion = situacion
                matricula.docente = docente
                matricula.save()
                messages.add_message(request, messages.SUCCESS, 'Docente '+ str(docente.nombreCompleto()) + ' matriculado')
                return redirect('escolar:mostrar_docentes_curso', id_curso=id_curso)
            except Docente.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Se produjo un error al matricular el docente. Consulte al administrador.')
    lista_matriculados = MatriculaDocentes.objects.filter(curso=curso).values_list('docente', flat=True)
    docentes = Docente.objects.filter(~Q(id__in = lista_matriculados))
    return render_to_response('curso/_matricular_docente.html', 
                              {'curso':curso,
                               'docentes':docentes,
                              'tipo_matricula':TIPO_MATRICULA_DOCENTE,
                              'situacion':SITUACION_DOCENTE}
                              , context)

@login_required(login_url="/loguearse")
def desmatricular_docente(request, id_matricula):
    context = RequestContext(request)        
    try:
        matriculaDocente = MatriculaDocentes.objects.get(pk=id_matricula)  
        curso = matriculaDocente.curso
        docente = matriculaDocente.docente
    except MatriculaDocentes.DoesNotExist:
        raise Http404("La matricula no existe")
      
    if request.method == 'POST':
        if 'si_desmatricular' in request.POST: 
            matriculaDocente.delete()
            messages.add_message(request, messages.SUCCESS, 'Docente '+ str(docente.nombreCompleto()) + ' desmatriculado')
            return redirect('escolar:mostrar_docentes_curso', id_curso=curso.id)
            
    return render_to_response('curso/desmatricular_docente.html', {'matriculaDocente': matriculaDocente},context)

@login_required(login_url="/loguearse")
def matricular_alumnos(request):    
    context = RequestContext(request)      
    profe=None
    try:
        profe =  Docente.objects.get(pk=request.user)        
    except:
        logger.warning('Usuario: no es docente')            
    logger.warning('Método:' + request.method)   
    correcto = False;
    if (profe == None or profe.tipoDocente == 'D' or profe.tipoDocente == 'T'):
        if request.method == 'POST':            
            cont_add = 0
            cont_err = 0
            id_curso = request.POST['id_curso']
            curso = Curso.objects.get(pk=id_curso)
            
            for id_alumno in eval(request.POST['input_matricular']):
                try:                    
                    alumno = Alumno.objects.get(pk=id_alumno)
                    matricula = MatriculaAlumnado()
                    matricula.curso = curso
                    matricula.alumno = alumno
                    matricula.save()                    
                    cont_add+=1
                except:
                    cont_err+=1
            if (cont_add>0):
                messages.add_message(request, messages.SUCCESS, 'Se agregaron ' + str(cont_add) + ' alumnos.')
            if (cont_err>0):
                messages.add_message(request, messages.WARNING, 'No se pudieron agregar ' + str(cont_err) + ' alumnos.')
            return redirect('escolar:matricular_curso', id_curso=id_curso)
            
    return redirect('/')



##CAMPO - MANEJO DEL CAMPOS
@login_required(login_url="/loguearse")
def mostrar_campo(request, id_campo):
    context = RequestContext(request)
    try:        
        campo = Campo.objects.get(pk=id_campo)
    except Campo.DoesNotExist:
        raise Http404("El curso no existe")
    
    return render_to_response('campo/home_campo.html', {'campo':campo}, context)
   
@login_required(login_url="/loguearse")
def add_campo(request, id_curso):
    context = RequestContext(request)  
    try:
        curso = Curso.objects.get(pk=id_curso)        
    except Curso.DoesNotExist:
        raise Http404("El curso no existe")    
    
    if request.method == 'POST':
        form = CampoAddForm(request.POST)
        
        if form.is_valid():            
            form.save()
            return redirect('escolar:mostrar_campo', id_campo = form.instance.id)
    else:
        form = CampoAddForm(instance=None)   
    form.fields['curso'].choices=((curso.id, curso),)
    for n in form.fields['curso'].choices:
        logger.warning(n)
    
    #form.fields['curso'].value = curso
    logger.warning(form.fields['curso'])
    return render(request, 'campo/add_campo.html', {'curso':curso,'form':form})


@login_required(login_url="/loguearse")
def add_item_campo(request, id_campo, semestre):
    context = RequestContext(request)  
    try:
        campo = Campo.objects.get(pk=id_campo)        
    except Campo.DoesNotExist:
        raise Http404("El campo no existe")        
    if request.method == 'POST':
        try:
            item = ItemCampo.objects.get(pk=int(request.POST['item_id']))
            item.delete()
        except:
            item = ItemCampo()
            item.campo=campo
            item.item = request.POST['item']
            item.color = request.POST['color']
            item.semestre = semestre
            item.orden = getOrdenColor(item.color)
            item.save()
                
    items = ItemCampo.objects.filter(Q(campo=campo) & Q(semestre=semestre))
    return render(request, 'campo/principal/agregar_item.html', {'campo':campo,'semestre':semestre,'items':items, 'colores':getColoresToPrint})

@login_required(login_url="/loguearse")
def mostrar_campos_curso(request, id_curso):
    context = RequestContext(request)        
    profe = None
    matricula_profe = None
    campos = None
    try:
        curso = Curso.objects.get(pk=id_curso)  
    except Curso.DoesNotExist:
        raise Http404("El curso no existe")
    
    try:
        profe =  Docente.objects.get(pk=request.user)   
        matricula_profe = MatriculaDocentes.objects.filter(Q(curso=curso) & Q(docente=profe))[0]  
        if (matricula_profe != None):
            campos = Campo.objects.filter(Q(curso=curso) & Q(tipoDocente=matricula_profe.tipoDocente))
        elif (profe.tipoDocente == 'G' or profe.tipoDocente == 'D'):
            campos = Campo.objects.filter(Q(curso=curso))
    except:
        logger.warning('Usuario: no es docente')        
    
    if (request.user.is_superuser):
        campos = Campo.objects.filter(Q(curso=curso))                
    
    return render_to_response('curso/_lista_campos.html', 
                              {'curso':curso,
                               'campos':campos,
                              }
                              , context)


@login_required(login_url="/loguearse")
def edit_orden_campo(request):                
    context = RequestContext(request)        
    campo = None
    if request.method == 'POST':
        campo = Campo.objects.get(pk=request.POST['id_campo'])
        campo.orden = request.POST['nvo_orden']
        campo.save()
    else:
        return None
    profe = None
    matricula_profe = None
    campos = None
    
    curso = campo.curso
    
    try:
        profe =  Docente.objects.get(pk=request.user)   
        matricula_profe = MatriculaDocentes.objects.filter(Q(curso=curso) & Q(docente=profe))[0]  
        if (matricula_profe != None):
            campos = Campo.objects.filter(Q(curso=curso) & Q(tipoDocente=matricula_profe.tipoDocente))
        elif (profe.tipoDocente == 'G' or profe.tipoDocente == 'D'):
            campos = Campo.objects.filter(Q(curso=curso))
    except:
        logger.warning('Usuario: no es docente')        
    
    if (request.user.is_superuser):
        campos = Campo.objects.filter(Q(curso=curso))                
    
    return render_to_response('campo/_tabla_campos.html', 
                              {'curso':curso,
                               'campos':campos,
                              }
                              , context)


@login_required(login_url="/loguearse")
def edit_informe(request, id_matricula_alumno, etapa):
    context = RequestContext(request)
    docente = 'A'
    try:
        matricula = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)        
        #campos = Campo.objects.filter(curso=matricula.curso) #TODO FILTRAR SOLO LOS CAMPOS DEL PROFE
    except:
        raise Http404("Error")     
        
    try:
        
        profe =  Docente.objects.get(pk=request.user)                   
        
        if (profe.tipoDocente == 'G' or profe.tipoDocente == 'D'):            
            campos = Campo.objects.filter(Q(curso=matricula.curso))   
            docente = 'A'
        else:
            matricula_profe = MatriculaDocentes.objects.filter(Q(curso=matricula.curso) & Q(docente=profe))[0]
            campos = Campo.objects.filter(Q(curso=matricula.curso) & Q(tipoDocente=matricula_profe.tipoDocente))
            if (len(campos)==1):
                docente = 'E'
                return redirect('escolar:edit_descripcion_campo', 
                                id_matricula_alumno=id_matricula_alumno,
                                id_campo = campos[0].id,
                               etapa=etapa)    
            docente = 'A'
            
    except:
        logger.warning('Usuario: no es docente')
        docente = 'A'
    
    
    if (request.user.is_superuser):
        campos = Campo.objects.filter(Q(curso=matricula.curso))    
    
    for campo in campos:
        DescripcionCampo.objects.get_or_create(campo=campo, matricula_alumno= matricula, semestre=etapa)
    
    return render_to_response('informe/home_informe.html', 
                              {'curso': matricula.curso,
                               'matricula': matricula,
                               'campos':campos,
                               'etapa':int(etapa),    
                               'docente':docente,
                               'obs':'-',
                              } 
                              , context)

@login_required(login_url="/loguearse")
def edit_descripcion_campo(request, id_matricula_alumno, id_campo, etapa):
    context = RequestContext(request)
    #try:        
    campo = Campo.objects.get(pk=id_campo)
    matricula = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)               
    descripcion = DescripcionCampo.objects.get_or_create(campo=campo, matricula_alumno= matricula, semestre=etapa)
    try:        
        profe =  Docente.objects.get(pk=request.user)   
        
        matricula_profe = MatriculaDocentes.objects.filter(Q(curso=matricula.curso) & Q(docente=profe))[0]
        
        
        if (profe.tipoDocente == 'G' or profe.tipoDocente == 'D'):            
            campos = Campo.objects.filter(Q(curso=matricula.curso))   
            docente = 'A'
        else:
            campos = Campo.objects.filter(Q(curso=matricula.curso) & Q(tipoDocente=matricula_profe.tipoDocente))
            docente = 'E'
            
    except:
        logger.warning('Usuario: no es docente')
        docente = 'A'
    
    if (request.user.is_superuser):
        campos = Campo.objects.filter(Q(curso=matricula.curso))    
    items = ItemCampo.objects.filter(Q(campo=campo) & Q(semestre=etapa))
    #TODO: Ordenar items
           
    
    return render_to_response('informe/descripcion_campo.html', 
                              {'descripcion':descripcion[0],                                                      
                               'curso': matricula.curso,
                               'matricula': matricula,
                               'campos':campos,
                               'docente':docente,
                               'items':items,
                               'etapa':etapa,
                               'colores':getColoresToPrint(),
                              }
                              , context)

@login_required(login_url="/loguearse")
def update_descripcion_campo(request):
    context = RequestContext(request)
    if request.method == 'POST':
        desc = DescripcionCampo.objects.get(pk=int(request.POST['id_descripcion']))
        desc.descripcion = request.POST['descripcion']
        desc.save()
        return HttpResponse("Se guardo correctamente")
    else:
        return HttpResponse("Error al guardarse")
    
@login_required(login_url="/loguearse")
def update_observaciones(request):
    context = RequestContext(request)
    if request.method == 'POST':
        matricula = MatriculaAlumnado.objects.get(pk=int(request.POST['id_matricula']))
        obse = request.POST['descripcion'] 
        etapa = int(request.POST['etapa'])
        if (etapa == 1):
            matricula.obs_p_etapa = obse
            logger.warning(obse)
        elif (etapa == 2):
            matricula.obs_s_etapa = obse
        matricula.save()
        return HttpResponse("Se guardo correctamente")
    else:
        return HttpResponse("Error al guardarse")
    
@login_required(login_url="/loguearse")
def update_aprendizaje(request):
    context = RequestContext(request)
    if request.method == 'POST':
        Campo.objects.filter(pk=int(request.POST['id_campo'])).update(aprendizajes = request.POST['aprendizajes'])        
        return HttpResponse(Campo.objects.get(pk=int(request.POST['id_campo'])).aprendizajes_to_html())
    else:
        return HttpResponse("Error al guardarse")
    
    
@login_required(login_url="/loguearse")
def view_informe_matricula(request, id_matricula_alumno, etapa):
    context = RequestContext(request)       
    # Prepare context
    
    matricula = MatriculaAlumnado.objects.get(pk=id_matricula_alumno)
    descrCampo = DescripcionCampo.objects.filter(matricula_alumno=matricula, semestre=etapa, campo__especial=False)
    descrCampoInstitucionales = DescripcionCampo.objects.filter(matricula_alumno=matricula, semestre=etapa, campo__especial=True)
    
    
    data = {'etapa':int(etapa),
            'matricula':matricula,
            'descrCampo':descrCampo,
            'descrCampoInstitucionales':descrCampoInstitucionales,
            'logo_provincial':LOGO_PROVINCIAL
           }                

    return render_to_response('informe/view_informe.html', data, context)




@login_required(login_url="/loguearse")
def render_copy_items(request, ciclo):
    context = RequestContext(request)    
    data = {'cursos': Curso.objects.filter(ciclo=ciclo)}

    return render_to_response('campo/principal/copy_items.html', data, context)

@login_required(login_url="/loguearse")
def get_campos_curso(request):
    id_curso=request.POST['id_curso']
    curso=Curso.objects.get(pk=id_curso)
    #campos = Campo.objects.filter(curso=curso).values('id', 'titulo')
    #json_campos = serializers.serialize('json', objectQuerySet, fields=('fileName','id'))
    json_campos = serializers.serialize("json", Campo.objects.filter(curso=curso), fields=('id', 'titulo'))
    return HttpResponse(json_campos)

@login_required(login_url="/loguearse")
def copy_items(request):
    context = RequestContext(request)       
    # Prepare context
    if request.method == 'POST':           
        id_curso_from=request.POST['from']
        id_curso_to=request.POST['to']
        semestre=int(request.POST['semestre'])
        campo = int(request.POST['campo'])
        curso_from=Curso.objects.get(pk=id_curso_from)
        curso_to=Curso.objects.get(pk=id_curso_to)
        if (campo ==0):
            for campo_from in curso_from.getCampos():
                items_from = ItemCampo.objects.filter(Q(campo=campo_from) & Q(semestre=semestre))
                if (Campo.objects.filter(curso=curso_to,titulo = campo_from.titulo).exists()):
                    campo_to = Campo.objects.filter(curso=curso_to,titulo = campo_from.titulo)[0]
                else:
                    continue
                #items_to = ItemCampo.objects.filter(Q(campo=campo_to) & Q(semestre=semestre))


                for item_from in items_from:            
                    if not ItemCampo.objects.filter(Q(campo=campo_to) & Q(item=item_from.item) & Q(semestre=semestre) & Q(color=item_from.color)).exists():
                        item_to = ItemCampo(campo = campo_to,item = item_from.item, semestre=semestre, color=item_from.color)
                        item_to.orden = getOrdenColor(item_from.color)
                        item_to.save()
            messages.add_message(request, messages.SUCCESS, 'Items Copiados')
        else:
            campo_from = Campo.objects.get(pk=campo)
            
            items_from = ItemCampo.objects.filter(Q(campo=campo_from) & Q(semestre=semestre))
            if (Campo.objects.filter(curso=curso_to,titulo = campo_from.titulo).exists()):
                campo_to = Campo.objects.filter(curso=curso_to,titulo = campo_from.titulo)[0]
                for item_from in items_from:            
                    if not ItemCampo.objects.filter(Q(campo=campo_to) & Q(item=item_from.item) & Q(semestre=semestre) & Q(color=item_from.color)).exists():
                        item_to = ItemCampo(campo = campo_to,item = item_from.item, semestre=semestre, color=item_from.color)
                        item_to.orden = getOrdenColor(item_from.color)
                        item_to.save()
            messages.add_message(request, messages.SUCCESS, 'Copiados los items del campo ' + campo_from.titulo)
                    
        return redirect('/')
    return HttpResponse("PROBLEMAS! NO POST")


@login_required(login_url="/loguearse")
def renumerarMatriculas(request, ciclo):
    cursos = Curso.objects.filter(ciclo=ciclo)
    lista_matriculas = MatriculaAlumnado.objects.filter(Q(curso__in = cursos))
    count=0
    for matricula in lista_matriculas:
        count = count + 1
        matricula.numMatricula = count
        matricula.save()
    messages.add_message(request, messages.SUCCESS, 'Matriculas año ' + str(ciclo) +" renumeradas.")   
    return redirect('escolar:home',{})

@login_required(login_url="/loguearse")
def regenerarOrdenColores(request):
    items = ItemCampo.objects.all()
    for item in items:
        item.orden = getOrdenColor(item.color)
        item.save()
    return HttpResponse("SE CAMBIO EL ORDEN DE LOS ITEMS")