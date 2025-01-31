from django.contrib import admin
from .models import Carrera, PDF , Firma


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'materia', 'carrera')
    search_fields = ('nombre', 'materia', 'carrera__nombre')
    list_filter = ('carrera',)

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre' , 'ocupacion')
    search_fields = ('nombre',)
