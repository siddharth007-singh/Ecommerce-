from django.shortcuts import render, redirect, get_list_or_404
from datawork.models import *
from django.utils import timezone
from datawork.forms import AddressForm
import random
import string
from django.http import Http404
from django.shortcuts import render


def homepage(request):
    data = {
        "pro": Item.objects.all(),
        "cat": Category.objects.all(),
    }
    return render(request, "public/home.html", data)


def cat_filter(request, slug):
    data = {
        "pro": Item.objects.filter(category__slug=slug),
        "cat": Category.objects.all(),
    }
    return render(request, "public/home.html", data)


def product_filter(request, item_id):
    data = {
        "cat": Category.objects.all(),
        "item": Item.objects.filter(item_id = item_id),
    }
    return render(request, "public/product.html", data)


def search(request):
    if request.method == "GET":
        search_data = request.GET.get('search')

        data = {
            "pro": Item.objects.filter(title__icontains=search_data),
            "cat": Category.objects.all(),
        }
        return render(request, "public/home.html", data)
    else:
        return redirect(homepage)


def Wishlist(request):
    data = {
        # "item": Item.objects.filter(item_id = item_id),
        "cat": Category.objects.all(),
    }
    return render(request, "public/wishlist.html", data)


def addtocart(request, item_id):
    item = get_list_or_404(Item, item_id=item_id)

    orderitem, created = OrderItem.objects.get_or_create(
        item_id=item_id,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__item_id=item_id).exists():
            orderitem.qty += 1
            orderitem.save()
            #todo msg: this item is updated in your cart
            return redirect(Cart)
        else:
            order.items.add(orderitem)
            # todo msg: this item is added in your cart successfully
            return redirect(Cart)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, start_date=order_date)
        order.items.add(orderitem)
        order.save()
        # todo msg: this item wa added to your cart
        return redirect(Cart)


def buynow(request, item_id):
    item = get_list_or_404(Item, item_id=item_id)

    orderitem, created = OrderItem.objects.get_or_create(
        item_id=item_id,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__item_id=item_id).exists():
            orderitem.qty += 1
            orderitem.save()
            #todo msg: this item is updated in your cart
            return redirect(Cart)
        else:
            order.items.add(orderitem)
            # todo msg: this item is added in your cart successfully
            return redirect(Cart)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, start_date=order_date)
        order.items.add(orderitem)
        order.save()
        # todo msg: this item wa added to your cart
        return redirect(Cart)


def remove_cart(request, item_id):
    item = get_list_or_404(Item, item_id=item_id)

    orderitem, created = OrderItem.objects.get_or_create(
        item_id=item_id,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__item_id=item_id).exists():
            order_item = OrderItem.objects.filter(
                item_id=item_id,
                user=request.user,
                ordered=False
            )[0]
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                return redirect(Cart)
        else:
            return redirect(Cart)
    else:
        return redirect(Cart)


def cart_item_remove(request, item_id):
    get_id = OrderItem.objects.get(item__item_id=item_id)
    get_id.delete()
    return redirect(Cart)


def Cart(request):
    try:
        data = {
            "order": Order.objects.get(user=request.user, ordered=False)
        }
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    return render(request, "public/cart.html", data)


def checkout(request):
    form = AddressForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect("checkout")

    data = {
        "addressform": form,
        "address": Address.objects.filter(user=request.user)
    }
    return render(request, "public/checkout.html", data)


def get_ref_code(digit):
    return ''.join(random.choices(string.digits, k=digit))


def makepayment(request):

    if request.method == "POST":
        add_id = request.POST.get("address")
        address = Address.objects.get(user=request.user, address_id=add_id)

        order = Order.objects.get(user=request.user, ordered=False)
        orderitems = order.items.all()
        orderitems.update(ordered=True)

        for item in orderitems:
            item.save()

        order.ordered = True
        order.ref_code = get_ref_code(8)
        order.address = address
        order.save()
        return redirect('home')


def myorder(request):
    order = Order.objects.filter(user=request.user, ordered=True)
    data = {
        "order": order
    }
    return render(request, "public/myorder.html", data)