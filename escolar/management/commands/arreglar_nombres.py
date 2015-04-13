from django.core.management.base import BaseCommand, CommandError
from escolar.models import Alumno

class Command(BaseCommand):
    def handle(self, *args, **options):
        alumnos = Alumno.objects.all()
        for alumno in Alumno.objects.all():    
            if not alumno.nombres.istitle():
                alumno.nombres = alumno.nombres.title()
                
            if not alumno.apellidos.istitle():
                alumno.apellidos = alumno.apellidos.title()
                
            if not alumno.nombreTutor.istitle():
                alumno.nombreTutor = alumno.nombreTutor.title()
                
            if not alumno.actividadTutor.istitle():
                alumno.actividadTutor = alumno.actividadTutor.title()
            
            alumno.save()
            self.stdout.write('Successfully alumno "%s"' % alumno)