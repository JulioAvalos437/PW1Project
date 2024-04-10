from django.db import models

class PDF(models.Model):
    nombre = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    condicion = models.CharField(max_length=30,null=True,blank=True)
    curso = models.CharField(max_length=20,null=True,blank=True)
    semestre = models.CharField(max_length=20,null=True,blank=True)
    requisitos = models.CharField(max_length=100,null=True,blank=True)
    carga_Horaria_Semanal = models.CharField(max_length=50,null=True,blank=True)
    carga_Horaria_Semestral = models.CharField(max_length=50,null=True,blank=True)
    profesor =  models.CharField(max_length=100,null=True,blank=True)
    objetivos = models.TextField(null=True,blank=True)
    contenido = models.TextField(null=True,blank=True)
    metodologia = models.TextField(null=True,blank=True)
    evaluacion = models.TextField(null=True,blank=True)
    bibliografia = models.TextField(null=True,blank=True)
    fundamentacion = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.archivo
