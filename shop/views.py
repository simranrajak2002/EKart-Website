from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate, People
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from math import ceil
import json,smtplib


# Create your views here.


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)
    # return HttpResponse("Shop")

def searchMatch(query, item):
    # '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def tracker(request):
    return render(request, 'shop/tracker.html')


def contact(request):
    if request.method == "POST": 
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/productView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        firstname = request.POST.get('firstname', '')
        lastname=request.POST.get('lastname')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        address2 = request.POST.get('address2', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zipcode', '')
        phone = request.POST.get('phone', '')
        payment=request.POST.get('payment1','')
        order = Orders(items_json=items_json, firstname=firstname, lastname=lastname, email=email, address=address, address2=address2, state=state, zip_code=zip_code, phone=phone, payment=payment)
        # print(items_json)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        server = smtplib.SMTP('smtp.gmail.com', 587)
        subject="Ordered Successfully"
        body=f"""Dear {firstname}, \n Your order has been submitted successfully. Your order ID is {id}.\n Use this order id to track your order.\n """
        message=f'Subject: {subject} \n\n {body}'
        server.starttls()
        server.login('myfunkycart@gmail.com', 'lsvhcvjwcryjmbpc')
        server.sendmail('myfunkycart@gmail.com', email, message)
        server.quit()
        
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        cancel=request.POST.get('cancel','c')
        track=request.POST.get('track','t')
        if(track=='track'):
            try:
                order = Orders.objects.filter(order_id=orderId, email=email)
                if len(order) > 0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append(
                            {'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps([updates, order[0].items_json], default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{}')
            except Exception as e:
                return HttpResponse(f'exception {e}')
        if(cancel=='cancel'):
            try:
                order=Orders.objects.filter(order_id=orderId,email=email)
                if len(order)>0:
                    deleteOrderUpdate = OrderUpdate.objects.filter(order_id=orderId)
                    for i in deleteOrderUpdate:
                        i.delete()
                    cancelOrder=Orders.objects.get(order_id=orderId)
                    # print(deleteOrderUpdate)
                    # cancelOrder.delete()
                update = OrderUpdate(order_id=orderId, update_desc="Your Order has been Cancelled Successfully. Your Money will be returned soon. Thanks for ordering with us..")
                update.save()
                updated=OrderUpdate.objects.get(order_id=orderId)
                updates=[]
                updates.append({'text': updated.update_desc, 'time': updated.timestamp})
                response = json.dumps([updates, order[0].items_json], default=str)
                cancelOrder.delete()
                return HttpResponse(response)
                
            except Exception as e:
                return HttpResponse(f'exception {e}')

    return render(request, 'shop/tracker.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if len(username)>10:
            messages.error(request,"Username cannot be greater than 10 characters")
            return redirect('/shop/register/')
        if not username.isalnum():
            messages.error(request,"Username must only contains alphabates and number")
        if password!=password2:
            messages.error(request,"Password does not match")
            return redirect('/shop/register/')

        user=User.objects.create_user(username,email,password)
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        people = People(email=email,password=password2)
        people.save()
        messages.success(request,"Your FunkyCart account has been created")
        return redirect('/shop/')
    else:
        return render(request,"register.html")

def hlogin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully Logged In")
            return redirect('/shop/')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('/shop/')
    return redirect('/shop/register/')

def hlogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/shop/')
    return redirect('/shop/register/')

def forgotpass(request):
    return render(request,'shop/forgotpass.html')