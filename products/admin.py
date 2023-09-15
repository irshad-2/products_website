from django.contrib import admin
from products.models import Product, Category, Brand

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "brand")


admin.site.register(Product)

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


admin.site.register(Brand, BrandAdmin)
