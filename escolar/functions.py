# -*- encoding: utf-8 -*-
from escolar.models import Docente, Curso, Alumno, MatriculaAlumnado, Campo, MatriculaDocentes, SITUACION_DOCENTE, TIPO_MATRICULA_DOCENTE, ItemCampo

def ordenarPorColor(items):
    colores = ["FF3333", "32CD32", "6666FF", "FF3399", "FFFF33","E0E0E0",
               "FF8C00", "EE82EE", "FF4500", "BDB76B", "008000","008B8B",
               "778899","FFE4E1","B0E0E6","BDB76B"]
    
    retItems = []
    
    for color in colores:
        print color
        color = "#" + color
        for item in items:
            if (item.color.upper()==color.upper()):
                retItems.append(item)
    
    return retItems
    
