from django.shortcuts import render
from .models import UserProfile,User
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    return render(request,'home.html')

def user_detail(request):
    if request.method =='POST':
        id = request.POST.get('id')
        price = request.POST.get('price')
        print(price)
        profile = UserProfile.objects.get(id = id)
        print(profile.paypal_email)
        email = profile.paypal_email
        items = "Apple I phone 12"
        host = request.get_host()
        print(host,'----------------------------')
        # paypal_receiver = "sb-bmxn710631185@business.example.com"
        paypal_receiver = email
        paypal_dict = {
        'business': paypal_receiver,
        'amount': price,
        'item_name': 'Order {}'.format(items),
        # 'invoice': str(oreder_id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
                       }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'process_payment.html', {'form': form})

    user = UserProfile.objects.all()
    return render(request,'detail.html',{'user':user})



@csrf_exempt
def payment_done(request):
    thank = True
    return render(request, 'payment_done.html',{'thank':thank})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

