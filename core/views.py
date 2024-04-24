from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import PDF
import PyPDF2
import re
import json

def import_success(request):
    return render(request, 'import_success.html')


def eliminar_cabecera(texto):

    patron_eliminar = r'Carrera\s+de\sIngeniería\s+(?:en\s+)?(?:Civil|Eléctrica|Electrónica|In[ ]?formática)\s+Facultad\s+de\s+Ciencias\s+y\s+Tecnol[ ]?ogías'

    texto_sin_cabecera = re.sub(patron_eliminar, "", texto)

    return texto_sin_cabecera


def importar_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # page = pdf_reader.pages[0]
            text = ""
            # Iterar sobre todas las páginas del PDF
            for no_page in range(len(pdf_reader.pages)):
                info_page = pdf_reader._get_page(no_page)
                texto_pagina = info_page.extract_text()
                texto_sincab = eliminar_cabecera(texto_pagina)
                text += texto_sincab

            print(text)
            nombre_archivo = pdf_file.name
            materia = None
            codigo = None
            condicion = None
            curso = None
            semestre = None
            requisitos = None
            carga_horaria_semanal = None
            carga_horaria_semestral = None
            carrera = None
            fundamentacion = None
            objetivos_text = None
            contenido = None
            metodologia = None
            evaluacion = None
            bibliografia = None

            # Extraer datos del PDF
            materia_match = re.search(
                r'Nombre\s*de\s*la\s*Materia\s*:\s*(.*)', text)
            materia = materia_match.group(1).strip() if materia_match else None
            materia = re.sub(r'\.\s*$', '', materia) if materia else None

            codigo_match = re.search(r'Código\s*:\s*(.*)', text)
            codigo = codigo_match.group(1).strip().replace(
                " ", "") if codigo_match else None
            codigo = re.sub(r'\.\s*$', '', codigo) if codigo else None

            condicion_match = re.search(r'Condici(?:ó|o)n\s*:\s*(.*)', text)
            condicion = condicion_match.group(1).strip().replace(" ", "") if condicion_match else None
            condicion = re.sub(r'\.\s*$', '', condicion) if condicion else None

            curso_match = re.search(r'Curso\s*:\s*(.*)', text)
            curso = curso_match.group(1).strip().replace(
                " ", "") if curso_match else None
            curso = re.sub(r'\.\s*$', '', curso) if curso else None

            semestre_match = re.search(r'Semestre\s*:\s*(.*)', text)
            semestre = semestre_match.group(1).strip().replace(
                " ", "") if semestre_match else None
            semestre = re.sub(r'\.\s*$', '', semestre) if semestre else None

            requisitos_match = re.search(r'Requi\s*[\s]?sit\s*os\s*:\s*(.*)', text)
            requisitos = requisitos_match.group(1).strip() if requisitos_match else None
            requisitos = re.sub(r'\.\s*$', '', requisitos) if requisitos else None
            if 'Pre-Requisito' in text:
                requisitos_match = re.search(r'Pre-Requisito\s*:\s*(.*)', text)
                requisitos = requisitos_match.group(1).strip() if requisitos_match else None
                requisitos = re.sub(r'\.\s*$', '', requisitos) if requisitos else None
            carga_horaria_semanal_match = re.search(
                r'Carga\s+horaria\s+semanal\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semanal = carga_horaria_semanal_match.group(
                1).strip() if carga_horaria_semanal_match else None
            carga_horaria_semanal = re.sub(
                r'\.\s*$', '', carga_horaria_semanal) if carga_horaria_semanal else None

            carga_horaria_semestral_match = re.search(
                r'Carga\s+horaria\s+semestral\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semestral = carga_horaria_semestral_match.group(
                1).strip() if carga_horaria_semestral_match else None
            carga_horaria_semestral = re.sub(
                r'\.\s*$', '', carga_horaria_semestral) if carga_horaria_semestral else None
            if 'Carga horaria' in text and carga_horaria_semestral is None:
                carga_horaria_semanal_match = re.search(
                    r'Carga\s+horaria\s*:\s*(.*)', text, re.IGNORECASE)
                carga_horaria_semanal = carga_horaria_semanal_match.group(
                    1).strip() if carga_horaria_semanal_match else None
                carga_horaria_semanal = re.sub(
                    r'\.\s*$', '', carga_horaria_semanal) if carga_horaria_semanal else None
            if 'Total' in text and carga_horaria_semestral is None:
                carga_horaria_semestral_match = re.search(
                    r'Total\s*:\s*(.*)', text, re.IGNORECASE)
                carga_horaria_semestral = carga_horaria_semestral_match.group(
                    1).strip() if carga_horaria_semestral_match else None
                carga_horaria_semestral = re.sub(
                    r'\.\s*$', '', carga_horaria_semestral) if carga_horaria_semestral else None
            carrera_match = re.search(r'Carrera\s*:\s*(.*)', text)
            carrera = carrera_match.group(1).strip() if carrera_match else None
            carrera = re.sub(r'\.\s*$', '', carrera) if carrera else None

            fundamentacion_match = re.search(
                r'FUNDAMENTACIÓN\s*(?:\. )?(.*?)(?=III.|$)', text, re.DOTALL)
            fundamentacion = fundamentacion_match.group(
                1).strip() if fundamentacion_match else None
            if 'FUNDAME NTACIÓN' in text :
                fundamentacion_match = re.search(
                    r'FUNDAME NTACIÓN\s*(?:\. )?(.*?)(?=III.|$)', text, re.DOTALL)
                fundamentacion = fundamentacion_match.group(
                    1).strip() if fundamentacion_match else None
            objetivos_match = re.search(
                r'OBJETI(?:\s+)?VOS\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)
            objetivos_text = objetivos_match.group(1).strip() if objetivos_match else None

            if 'CONTENIDO' in text:
                contenido_match = re.search(r'CONTENIDO\s*(?:\. )?(.*?)(?=V. |$)', text, re.DOTALL)
                contenido = contenido_match.group(1).strip() if contenido_match else None
                # Aquí puedes realizar cualquier otra acción relacionada con el contenido
            elif 'CONTEN IDO' in text:
                contenido_match = re.search(r'CONTEN IDO\s*(?:\. )?(.*?)(?=V. |$)', text, re.DOTALL)
                contenido = contenido_match.group(1).strip() if contenido_match else None
                # Aquí puedes realizar cualquier otra acción relacionada con el contenido
            elif 'CONT ENIDO' in text:
                contenido_match = re.search(r'CONT ENIDO\s*(?:\. )?(.*?)(?=V. |$)', text, re.DOTALL)
                contenido = contenido_match.group(1).strip() if contenido_match else None
                # Aquí puedes realizar cualquier otra acción relacionada con el contenido
            else:
                contenido = None



            patron_metodologia = r'METODO(?:LOG[ ]?)?(?:[IÍÍ]A| LOG[ ]ÍA)\s*(?:\. )?(\w+)(?=VI\.|Carrera\.|/Z)\.'

            metodologia_match = re.search(patron_metodologia, text, re.DOTALL)
            metodologia = metodologia_match.group(1).strip() if metodologia_match else None

            if 'METODOLOG ÍA' in text:
                metodologia_match = re.search(r'METODOLOG ÍA\s*(?:\. )?(.*?)(?=VI. |$)', text, re.DOTALL)
                metodologia = metodologia_match.group(1).strip() if metodologia_match else None
            elif 'METODO LOG ÍA' in text:
                metodologia_match = re.search(r'METODO LOG ÍA\s*(?:\. )?(.*?)(?=VI. |$)', text, re.DOTALL)
                metodologia = metodologia_match.group(1).strip() if metodologia_match else None
            elif 'METODOLOGIA' in text:
                metodologia_match = re.search(r'METODOLOGIA\s*(?:\. )?(.*?)(?=VI. |$)', text, re.DOTALL)
                metodologia = metodologia_match.group(1).strip() if metodologia_match else None
            elif 'METODOLOGÍA' in text:
                metodologia_match = re.search(r'METODOLOGÍA\s*(?:\. )?(.*?)(?=VI. |$)', text, re.DOTALL)
                metodologia = metodologia_match.group(1).strip() if metodologia_match else None

            elif 'ESTRATEGIAS METODOLÓGICAS' or 'ESTRATEGIAS METODOLOGICAS' in text and metodologia is None:
                metodologia_match = re.search(r'ESTRATEGIAS METODOLÓGICAS\s*(?:\. )?(.*?)(?=VI. |$)', text, re.DOTALL)
   
                if metodologia_match is None:
                    metodologia_match = re.search(r'ESTRATEGIAS METODOLOGICAS\s*(?:\. )?(.*?)(?=VI. |$)', text,
                                                  re.DOTALL)
                metodologia = metodologia_match.group(1).strip() if metodologia_match else None
                evaluacion_match = re.search(
                    r'EVALUACIÓN\s*(?:\. )?(.*?)(?=BIBLIOGRAFÍA|VIII\.|\Z)', text, re.DOTALL)
                evaluacion = evaluacion_match.group(
                    1).strip() if evaluacion_match else None
            evaluacion_match = re.search(
                r'EVALUACIÓN\s*(?:\. )?(.*?)(?=BIBLIOGRAFÍA|VII\.|\Z)', text, re.DOTALL)
            evaluacion = evaluacion_match.group(
                1).strip() if evaluacion_match else None

            bibliografia_match = re.search(
                r'BIBLIOGRAFÍA\s*(?:\. )?(.*?)(?=\Z)', text, re.DOTALL)
            bibliografia = bibliografia_match.group(
                1).strip() if bibliografia_match else None



            # Guardar en la base de datos
            pdf = PDF(nombre=nombre_archivo, materia=materia,
                      carrera=carrera, codigo=codigo, objetivos=objetivos_text,
                      fundamentacion=fundamentacion, contenido=contenido, metodologia=metodologia,
                      evaluacion=evaluacion, bibliografia=bibliografia, condicion=condicion,
                      curso=curso, semestre=semestre, requisitos=requisitos,
                      carga_Horaria_Semanal=carga_horaria_semanal, carga_Horaria_Semestral=carga_horaria_semestral)
            pdf.save()

        return redirect('import_success')
    return render(request, 'import_pdf.html')


def menu(request):
    return render(request, 'menu.html', )

def programa(request):
    id = request.GET.get('Materia')
    pdf = PDF.objects.get(id=id)
    return render(request, 'programa.html', {'pdf': pdf})



def get_materiasf(request, codcarrera):
    materias = list(PDF.objects.filter(codigo__icontains=codcarrera).values())
    if (len(materias) > 0):
        data = {'message': "Success", 'materias': materias}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

