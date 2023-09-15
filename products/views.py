import json

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from products.forms import ProductForm
from products.models import Brand, Category, Product
from products.functions import generate_form_errors
# Create your views here.


@login_required(login_url="/users/login/")
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            if not Brand.objects.filter(user=request.user).exists():
                brand = Brand.objects.create(
                    user=request.user, name=request.user.username)
            else:
                brand = request.user.brand
            instance = form.save(commit=False)
            instance.brand = brand
            instance.save()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(
                    title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title": "Successfully submitted",
                "message": "Successfully submitted",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/"
            }
        else:
            error_message = generate_form_errors(form)
            response_data = {
                "title": "form validation error",
                "message": str(error_message),
                "status": "error",
                "stable": "yes",
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        form = ProductForm()
        context = {
            "form": form,
            "title": "Add a new Product"

        }
        return render(request, "products/create.html", context=context)


@login_required(login_url="/users/login/")
def my_products(request):
    instances = Product.objects.filter(brand__user=request.user, is_deleted=False)

    context = {
        "title": "My Products",
        "instances": instances
    }
    return render(request, "products/my_products.html", context=context)

@login_required(login_url="/users/login/")
def delete_product(request, id):
    instance = get_object_or_404(Product, id=id)
    instance.is_deleted = True
    instance.delete()

    response_data = {
        "title": "successfully deleted",
        "message": "post deleted successfully",
        "status": "success"
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/users/login/")
def edit_product(request, id):
    instance = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            instance = form.save(commit=False)

            instance.save()
            instance.categories.clear()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(
                    title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title": "Successfully submitted",
                "message": "Successfully submitted",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/"
            }
        else:
            error_message = generate_form_errors(form)
            response_data = {
                "title": "form validation error",
                "message": str(error_message),
                "status": "error",
                "stable": "yes",
            }
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    else:
        category_string = ""
        for category in instance.categories.all():
            category_string += f"{category.title},"
        form = ProductForm(instance=instance, initial={
                        "tags": category_string[:-1]})
        context = {
            "title": "Create a new Product",
            'form': form,
        }
        return render(request, "products/create.html", context=context)


