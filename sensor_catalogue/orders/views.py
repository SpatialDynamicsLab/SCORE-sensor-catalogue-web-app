from django.shortcuts import render,redirect
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart

def create_order(request):
    cart = Cart(request)
    if request.method =='POST':
        form =  OrderCreateForm(request.POST)
        # form = CreateOrderForm(request.POST)
        if form.is_valid:
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                print(item)
                OrderItem.objects.create(
                    order=order,
                    sensor = item['sensor'],
                    price = item['price'],
                    quantity  = item['quantity'])
                
            # Clear the cart when done.
            cart.clear()
        return render(request, 'orders/order/created.html',{'order': order})
        
    else:
        # form = CreateOrderForm()
        form =  OrderCreateForm()

    # return render(request, 'orders/order/checkout.html', {'cart':cart,'form':form}) 
    return render(request, 'orders/order/create.html', {'cart':cart,'form':form})                  

    
