from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method =='POST':
        form =  OrderCreateForm(request.POST)
        if form.is_valid:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                # print(item)
                OrderItem.objects.create(
                    order=order,
                    sensor = item['sensor'],
                    price = item['price'],
                    quantity  = item['quantity'])
                
            # Clear the cart when done.
            cart.clear()
            request.session['order_id']  = order.id
        return render(request, 'orders/order/created.html',{'order': order})
        
    else:
        form =  OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart,'form':form})                  

    
