from django.core.management.base import BaseCommand, CommandError
from escolar.models import Alumno

class Command(BaseCommand):
    def handle(self, *args, **options):
        alumnos = Alumno.objects.all()
        #for alumno in Alumno.objects.all():    
        #alumnos.delete() Por las dudas lo bajo a este comando