from django.urls import path, include

from products import views


app_name = "products"

urlpatterns = [
    path('create/', views.create, name='create'),
    path('my_products/', views.my_products, name='my_products'),
    path('delete/<int:id>/', views.delete_product, name="delete_product"),
    path('edit/<int:id>/', views.edit_product, name="edit_product"),

    

]
