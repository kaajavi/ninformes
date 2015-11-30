# -*- encoding: utf-8 -*-
from escolar.models import Docente, Curso, Alumno, MatriculaAlumnado, Campo, MatriculaDocentes, SITUACION_DOCENTE, TIPO_MATRICULA_DOCENTE, ItemCampo


COLORES = ["FF3333", "32CD32", "6666FF", "FF3399", "FFFF33","E0E0E0",
           "FF8C00", "EE82EE", "FF4500", "BDB76B", "008000","008B8B",
           "778899","FFE4E1","B0E0E6","BDB76B","ADFF2F","8B4513","FFD700",'00FF00']

def getColoresToPrint():
    ret = "["
    for color in COLORES:
        ret =ret + '\"'+ color + '\",'
    ret = ret[:-1] + "]"
    return ret

def getOrdenColor(color):
    color = color.upper().replace('#','')    
    
    try:
        return COLORES.index(color)
    except:
        return 999


def numero_to_letras(numero):
	indicador = [("",""),("MIL","MIL"),("MILLON","MILLONES"),("MIL","MIL"),("BILLON","BILLONES")]
	entero = int(numero)
	decimal = int(round((numero - entero)*100))
	#print 'decimal : ',decimal
	contador = 0
	numero_letras = ""
	while entero >0:
		a = entero % 1000
		if contador == 0:
			en_letras = convierte_cifra(a,1).strip()
		else :
			en_letras = convierte_cifra(a,0).strip()
		if a==0:
			numero_letras = en_letras+" "+numero_letras
		elif a==1:
			if contador in (1,3):
				numero_letras = indicador[contador][0]+" "+numero_letras
			else:
				numero_letras = en_letras+" "+indicador[contador][0]+" "+numero_letras
		else:
			numero_letras = en_letras+" "+indicador[contador][1]+" "+numero_letras
		numero_letras = numero_letras.strip()
		contador = contador + 1
		entero = int(entero / 1000)

	return numero_letras

def convierte_cifra(numero,sw):
	lista_centana = ["",("CIEN","CIENTO"),"DOSCIENTOS","TRESCIENTOS","CUATROCIENTOS","QUINIENTOS","SEISCIENTOS","SETECIENTOS","OCHOCIENTOS","NOVECIENTOS"]
	lista_decena = ["",("DIEZ","ONCE","DOCE","TRECE","CATORCE","QUINCE","DIECISEIS","DIECISIETE","DIECIOCHO","DIECINUEVE"),

					("VEINTE","VEINTI"),("TREINTA","TREINTA Y "),("CUARENTA" , "CUARENTA Y "),

					("CINCUENTA" , "CINCUENTA Y "),("SESENTA" , "SESENTA Y "),

					("SETENTA" , "SETENTA Y "),("OCHENTA" , "OCHENTA Y "),

					("NOVENTA" , "NOVENTA Y ")

				]
	lista_unidad = ["",("UN" , "UNO"),"DOS","TRES","CUATRO","CINCO","SEIS","SIETE","OCHO","NUEVE"]
	centena = int (numero / 100)
	decena = int((numero -(centena * 100))/10)
	unidad = int(numero - (centena * 100 + decena * 10))
	texto_centena = ""
	texto_decena = ""
	texto_unidad = ""
	texto_centena = lista_centana[centena]
	if centena == 1:
		if (decena + unidad)!=0:
			texto_centena = texto_centena[1]
		else :
	 		texto_centena = texto_centena[0]
	#Valida las decenas
	texto_decena = lista_decena[decena]
	if decena == 1 :
		 texto_decena = texto_decena[unidad]
 	elif decena > 1 :
 		if unidad != 0 :
 			texto_decena = texto_decena[1]
 		else:
 			texto_decena = texto_decena[0]
 	#Validar las unidades
 	#print "texto_unidad: ",texto_unidad
 	if decena != 1:
 		texto_unidad = lista_unidad[unidad]
 		if unidad == 1:
 			texto_unidad = texto_unidad[sw]
 	return "{} {} {}".format(texto_centena,texto_decena,texto_unidad)

