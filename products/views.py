from django.http import HttpResponse

def product_list(request):
    return HttpResponse("This is the product list page.")

def product_detail(request, product_id):
    return HttpResponse(f"This is the detail page for product ID {product_id}.")