from .models import customer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.contrib import messages
from django.db.models.functions import ExtractHour
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import item
import pyrebase
import datetime
import time
from datetime import datetime

config = {
    "apiKey": "AIzaSyDCdeMINxVCsGu38B-qc05yrk1rW99Yq94",
    "authDomain": "customertracker-378d4.firebaseapp.com",
    "databaseURL": "https://customertracker-378d4-default-rtdb.firebaseio.com/Persons",
    "projectId": "customertracker-378d4",
    "storageBucket": "customertracker-378d4.appspot.com",
    "messagingSenderId": "724650362302",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4f8wx%40customertracker-378d4.iam.gserviceaccount.com",
    "appId": "1:724650362302:web:7b7c079d409f17ab67e5ef",
    "serviceAccount": "E:\Major project\customertracker\core\serviceAccountCredentials.json"
}

# here we are doing firebase authentication
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


@login_required(login_url="/auth/login/")
def index(request):
    if(request.user):
        all_customers = customer.objects.all()
        all_items = item.objects.all()

        city1_customers = customer.objects.filter(city__city='ludhiana')
        city2_customers = customer.objects.filter(city__city='chandigarh')
        trending_items = customer.objects.values('item').annotate(
            count=Count('item')).order_by('item').reverse()
        revenue_items = customer.objects.values('item').annotate(
            sum=Sum('price')).order_by('item').reverse()
        data = []
        data.append(city1_customers.count())
        data.append(city2_customers.count())
        labels = ['city A', 'city B']
        # data = customer_data.filter(city)
        # customer_data.filter.filter()
        context = {
            'all_customers': all_customers,
            'city1_customers': city1_customers,
            'city2_customers': city2_customers,
            'data': data,
            'labels': labels,
            'trending_items': trending_items,
            'revenue_items': revenue_items,
            'all_items': all_items

        }

    # Render the HTML template index.html with the data i
        return render(request, 'index.html', context=context)
    else:
        return redirect('/auth/login')


def chart(request):
    citywise_customers = customer.objects.all().annotate(cityc=Count('city'))
    city1_customers = citywise_customers.filter(city__city='ludhiana')
    city2_customers = citywise_customers.filter(city__city='chandigarh')
    city1item1 = customer.objects.filter(
        city__city='ludhiana', item__item='school bag')
    city1item2 = customer.objects.filter(
        city__city='ludhiana', item__item='hand bag')
    city1item3 = customer.objects.filter(
        city__city='ludhiana', item__item='travelling bag')
    city2item1 = customer.objects.filter(
        city__city='chandigarh', item__item='school bag')
    city2item2 = customer.objects.filter(
        city__city='chandigarh', item__item='hand bag')
    city2item3 = customer.objects.filter(
        city__city='chandigarh', item__item='travelling bag')

    labels = [str(x)+':00 hours' for x in range(1, 13)]
    itemlabels = ['school bag', 'hand bag', 'travelling bag']
    hourwise_customers1 = city1_customers.annotate(hour=ExtractHour(
        'timestamp')).values('hour').annotate(c=Count('id')).values('hour', 'c')
    hourwise_customers2 = city2_customers.annotate(hour=ExtractHour(
        'timestamp')).values('hour').annotate(c=Count('id')).values('hour', 'c')
    hourwisedata1 = [x['c'] for x in hourwise_customers1]
    hourwisedata2 = [x['c'] for x in hourwise_customers2]
    context = {
        'hourwise_customers1': hourwisedata1,
        'hourwise_customers2': hourwisedata2,
        'labels': labels,
        'city1item1': city1item1.count(),
        'city1item2': city1item2.count(),
        'city1item3': city1item3.count(),
        'itemlables': itemlabels,
        'city2item1': city2item1.count(),
        'city2item2': city2item2.count(),
        'city2item3': city2item3.count()
    }
    return render(request, 'chartjs.html', context=context)


def table(request):
    now = datetime.now()
    date = now.strftime("%b-%d-%Y")
    print(date)
    name = database.child('Dec-09-2021').get().val()
    data = []
    if name is None:
        return render(request, 'basic-table.html')

    for key, value in name.items():
        print('time', key, 'in', value['text_in'])
        time = key
        customer_entering = value['text_in']
        customer_leaving = value['text_out']
        customer_staying = value['remaining']
        data.append({'time': time, 'customer_entering': customer_entering,
                     'customer_leaving': customer_leaving, 'customer_staying': customer_staying})
        context = {
            "data": data
        }
    return render(request, 'basic-table.html',  context)


def addsale(request):
    if request.method == 'POST':

        form = CustomerForm(request.POST)

        if form.is_valid():

            form.save()
            itemName = item.objects.get(pk=request.POST.get('item'))
            itemName.stock = int(itemName.stock)
            int(request.POST.get('quantity'))
            itemName.save()
            messages.success(request, ' submssion successful')

            return redirect('/add')
        else:
            return HttpResponse(form.errors.as_json())
    else:
        form = CustomerForm()
        context = {
            'form': form,
        }

    return render(request, 'basic-elements.html', context)
