from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request): 
    uid = request.session["uid"] 
    charge = request.session["charge"] 
    quantity = Order.objects.all()
    obj_count = 0
    total = 0
    for obj in quantity:
        obj_count += obj.quantity_ordered
        total += obj.total_price
    context = {
        "product": Product.objects.get(id=uid),
        "quantity": Order.objects.all(),
        "num": obj_count,
        "total": total,
        "charge": charge
    }
    return render(request, "store/checkout.html", context)

def process(request):
    uid = int(request.POST["uid"])
    item = Product.objects.get(id=uid,)
    quantity_from_form = int(request.POST["quantity"])
    price_item = float(item.price)
    total_charge = quantity_from_form * price_item
    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    request.session["uid"] = uid 
    request.session["charge"] = total_charge

    return redirect("/checkout")

# =============================== Provided Solutions ================================

# from django.shortcuts import render,redirect
# from .models import Order, Product
# from django.db.models import Sum

# def index(request):
#     context = {
#         "all_products": Product.objects.all()
#     }
#     return render(request, "store/index.html", context)

# def checkout(request):
#     last = Order.objects.last()
#     price=last.total_price
#     full_order = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
#     full_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
#     context = {
#         'orders':full_order,
#         'total':full_price,
#         'bill':price,
#     }
#     return render(request, "store/checkout.html",context)

# def purchase(request):
#     if request.method == 'POST':
#         this_product = Product.objects.filter(id=request.POST["id"])
#         if not this_product:
#             return redirect('/')
#         else:
#             quantity = int(request.POST["quantity"])
#             total_charge = quantity*(float(this_product[0].price))
#             Order.objects.create(quantity_ordered=quantity, total_price=total_charge)
#             return redirect('/checkout')
#     else:
#         return redirect('/')