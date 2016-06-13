from django.contrib import admin
from .models import Category, Product, DataSet, DataView, DataTransformation, Analysis, Accordion, Panel, Slider, ColumnFilter, HospitalStay, Dropdown, Controller
from import_export.admin import ImportExportModelAdmin

class DataSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_editable = ['name', 'code']
admin.site.register(DataSet, DataSetAdmin)

class DataViewAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset']
    list_editable = ['name', 'dataset']
admin.site.register(DataView, DataViewAdmin)

class DataTransformationAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataTransformation, DataTransformationAdmin)

class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['title', 'data_view']
    list_editable = ['title', 'data_view']
admin.site.register(Analysis, AnalysisAdmin)

class AccordionAdmin(admin.ModelAdmin):
    fields = ['title', 'analysis']
    list_display, list_editable = fields, fields
admin.site.register(Accordion, AccordionAdmin)

class PanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'type']
    list_editable = ['title', 'type']
admin.site.register(Panel, PanelAdmin)

class HospitalStayAdmin(ImportExportModelAdmin):
    pass
admin.site.register(HospitalStay, HospitalStayAdmin)

class ControllerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Controller, ControllerAdmin)