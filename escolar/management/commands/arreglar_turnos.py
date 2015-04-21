from django.core.management.base import BaseCommand, CommandError
from escolar.models import Curso

class Command(BaseCommand):
    def handle(self, *args, **options):        
        for curso in Curso.objects.all():
            if curso.sala=='A' or curso.sala=='B':
                curso.turno = "M"
            else:
                curso.turno = "T"
            
            curso.save()
            self.stdout.write('Successfully curso "%s"' % curso)