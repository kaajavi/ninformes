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
    