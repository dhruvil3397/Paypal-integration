from django.db.models import query
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, response
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.   
def index(request): 
    allProds = []
    catprods = Product.objects.values('category')
    print(catprods)
   

    cats = {item['category'] for item in catprods}
    print(cats)

    for cat in cats:
       prod = Product.objects.filter(category = cat)
       n = len(prod)
       nSlides = n//4 + ceil((n/4)-(n//4))
       allProds.append([prod,range(1,nSlides),nSlides])
    print(allProds)

    params = {'allProds':allProds}
    return render(request,"shop/index.html", params)

def searchmatch(query,item):
    '''return True only if query matches the item'''
    if query in item.category.lower() or query in item.type.lower() or query in item.brand.lower() or query in item.model.lower():
        return True
    else :
        False

def search(request):
    query = request.GET.get('search')
    print(query)
    allProds = []
    catprods = Product.objects.values('category')
    print(catprods)
   

    cats = {item['category'] for item in catprods}
    print(cats)

    for cat in cats:
        prodtemp = Product.objects.filter(category = cat)
        prod = [item for item in prodtemp if searchmatch(query,item)]
        print('______________________________')
        print(prod)
        print('______________________________')
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4)) 
        if len(prod) != 0:
            allProds.append([prod,range(1,nSlides),nSlides])
      
    print(allProds)

    params = {'allProds':allProds,"msg":""}
    if len(allProds)==0 or len(query)<2:
        params={'msg':"Please make sure to enter relevant search query"}

    return render(request,"shop/search.html", params)
    


def about(request): 
    return render(request,'shop/about.html')
def contact(request):
    thank = False
    if request.method == "POST":
        name =  request.POST.get('name','default')
        email =  request.POST.get('email','default')
        phone =  request.POST.get('phone','default')
        message =  request.POST.get('message','default')
        # params = {'name':name,'email':email,'phone':phone,'message':message}
        contact = Contact(name = name,email = email,phone = phone,message = message)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{'thank':thank})
    

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id','')
        email =  request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id = order_id,email = email)
            if len(order) >0:
                update = OrderUpdate.objects.filter(order_id = order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success","updates": updates,"items_json" : order[0].items_json}, default = str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"No Items"}')
        except: 
            return HttpResponse('{"status":"error"}')

    return render(request,'shop/tracker.html')



def productview(request,myid):
    # fetch the products using the id
    product = Product.objects.filter(id = myid)
    print(product)
    return render(request,'shop/products.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items_json','')
        amount = request.POST.get('amount','')
        name =  request.POST.get('name','')
        email =  request.POST.get('email','')
        address =  request.POST.get('address1','') + " " + request.POST.get('address2','')
        phone =  request.POST.get('phone','')
        city =  request.POST.get('city','')
        state =  request.POST.get('state','')
        zip_code =  request.POST.get('zip_code','')
        order = Orders(items_json = items_json,amount = amount,name =name,email = email,address =address,phone= phone,city = city, state= state,zip_code= zip_code)
        order.save()
        thank = True
        id = order.order_id
        update = OrderUpdate(order_id=id,update_desc= "The Order has been placed")
        update.save()

        
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        host = request.get_host()
        print(host,'----------------------------')
        # paypal_receiver = "dhruvillr@gmail.com"
        paypal_dict = {
        # 'business': paypal_receiver,
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount,
        'item_name': 'Order {}'.format(items_json),
        'invoice': str(id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
                       }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'shop/process_payment.html', {'form': form})

    return render(request,'shop/checkout.html')


@csrf_exempt
def payment_done(request):
    thank = True
    return render(request, 'shop/payment_done.html',{'thank':thank})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'shop/payment_cancelled.html')