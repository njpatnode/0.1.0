from django.contrib import admin
from .models import Category, Product, DataSet, DataView

class CategoryAdmin(admin.ModelAdmin):
 list_display = ['name', 'slug']
 prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
 list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
 list_filter = ['available', 'created', 'updated']
 list_editable = ['price', 'stock', 'available']
 prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

class DataSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_editable = ['name', 'code']
admin.site.register(DataSet, DataSetAdmin)

class DataViewAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'name', 'parameters', 'row_range']
    list_editable = ['dataset', 'name', 'parameters', 'row_range']
admin.site.register(DataView, DataViewAdmin)
