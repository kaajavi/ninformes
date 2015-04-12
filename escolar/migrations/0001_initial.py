# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apellidos', models.CharField(max_length=256, verbose_name=b'Apellidos')),
                ('nombres', models.CharField(max_length=256, verbose_name=b'Nombres')),
                ('dni', models.IntegerField(unique=True, verbose_name=b'D.N.I.')),
                ('sexo', models.CharField(max_length=1, verbose_name=b'Sexo', choices=[(b'A', b'Var\xc3\xb3n'), (b'Z', b'Mujer')])),
                ('direccionPrincipal', models.CharField(max_length=256, verbose_name=b'Direcci\xc3\xb3n Postal')),
                ('direccionSecundaria', models.CharField(max_length=256, verbose_name=b'Direcci\xc3\xb3n Postal secundaria', blank=True)),
                ('fechaDeNacimiento', models.DateField(verbose_name=b'Fecha de Nacimiento')),
                ('lugarDeNacimiento', models.CharField(max_length=256, verbose_name=b'Ciudad de Nacimiento')),
                ('provincia', models.CharField(max_length=256, verbose_name=b'Provincia de Nacimiento')),
                ('pais', models.CharField(max_length=256, verbose_name=b'Pa\xc3\xads de Nacimiento')),
                ('nombreTutor', models.CharField(max_length=256, verbose_name=b'Nombre de Tutor Legal (completo)')),
                ('actividadTutor', models.CharField(max_length=256, verbose_name=b'Actividad de Tutor Legal')),
                ('telefonoHogar', models.CharField(max_length=256, verbose_name=b'Tel\xc3\xa9fono')),
                ('celularPapa', models.CharField(max_length=256, verbose_name=b'Celular Papa')),
                ('celularMama', models.CharField(max_length=256, verbose_name=b'Celular Mama')),
            ],
            options={
                'ordering': ['sexo', 'apellidos', 'nombres'],
                'verbose_name': 'Alumno',
                'verbose_name_plural': 'Alumnos',
            },
        ),
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoDocente', models.CharField(max_length=10, verbose_name=b'Tipo de docente', choices=[(b'A', b'A\xc3\xbalico'), (b'M', b'Especial - M\xc3\xbasica'), (b'F', b'Especial - Ed. F\xc3\xadsica')])),
                ('titulo', models.CharField(max_length=256, verbose_name=b'T\xc3\xadtulo del campo')),
                ('descripcion', models.TextField(max_length=256, verbose_name=b'Descripci\xc3\xb3n del Campo')),
                ('items_a_evaluar', models.TextField(verbose_name=b'Items a evaluar', blank=True)),
                ('borrador_pe', models.TextField(verbose_name=b'Borrador Primera Etapa', blank=True)),
                ('borrador_se', models.TextField(verbose_name=b'Borrador Segunda Etapa', blank=True)),
            ],
            options={
                'verbose_name': 'Campo',
                'verbose_name_plural': 'Campos',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ciclo', models.CharField(max_length=4, verbose_name=b'Ciclo Lectivo', choices=[(b'2014', 2014), (b'2015', 2015), (b'2016', 2016), (b'2017', 2017), (b'2018', 2018), (b'2019', 2019), (b'2020', 2020)])),
                ('fechaDeMatricula', models.DateField(verbose_name=b'Fecha de Matricula')),
                ('anio', models.CharField(max_length=1, verbose_name=b'A\xc3\xb1o', choices=[(b'2', 2), (b'3', 3), (b'4', 4), (b'5', 5)])),
                ('sala', models.CharField(max_length=1, verbose_name=b'Sala', choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'D', b'D'), (b'E', b'E'), (b'F', b'F')])),
                ('turno', models.CharField(max_length=10, verbose_name=b'Turno', choices=[(b'Ma\xc3\xb1ana', b'Ma\xc3\xb1ana'), (b'Tarde', b'Tarde')])),
            ],
            options={
                'ordering': ['anio', 'sala'],
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tipoDocente', models.CharField(max_length=1, verbose_name=b'Tipo de Docente', choices=[(b'T', b'Docente'), (b'E', b'Especial'), (b'G', b'Gabinete'), (b'D', b'Direcci\xc3\xb3n')])),
                ('sexo', models.CharField(blank=True, max_length=1, verbose_name=b'Sexo', choices=[(b'H', b'Var\xc3\xb3n'), (b'M', b'Mujer')])),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MatriculaAlumnado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activo', models.BooleanField(default=True, verbose_name=b'Activo')),
                ('alumno', models.ForeignKey(to='escolar.Alumno')),
                ('curso', models.ForeignKey(to='escolar.Curso')),
            ],
            options={
                'verbose_name': 'Matricula Alumno',
                'verbose_name_plural': 'Matriculaci\xf3n Alumnado',
            },
        ),
        migrations.CreateModel(
            name='MatriculaDocentes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoDocente', models.CharField(max_length=10, verbose_name=b'Tipo de docente', choices=[(b'A', b'A\xc3\xbalico'), (b'M', b'Especial - M\xc3\xbasica'), (b'F', b'Especial - Ed. F\xc3\xadsica')])),
                ('situacion', models.CharField(max_length=10, verbose_name=b'Situaci\xc3\xb3n', choices=[(b'T', b'Titular'), (b'S', b'Suplente')])),
                ('curso', models.ForeignKey(to='escolar.Curso')),
                ('docente', models.ForeignKey(to='escolar.Docente')),
            ],
            options={
                'verbose_name': 'Matricula Docentes',
                'verbose_name_plural': 'Matriculaciones a Docentes',
            },
        ),
        migrations.AddField(
            model_name='campo',
            name='curso',
            field=models.ForeignKey(to='escolar.Curso'),
        ),
    ]
