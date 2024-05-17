from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ('id', 'category', 'name', 'price', 'get_image','quantity')
    list_display_links = ('id', 'category', 'name', 'price', 'get_image','quantity')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

    def get_image(self,product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="50" height="50" />')