import email
from django import views
from django.shortcuts import render 
from customer.views import *
from customer.models import *
from retailer.views import *

# Create your views here.
def adminindex(request):
    email='richa@pet-shop.com'
    if 'richa@pet-shop.com' in request.session:
        data=get_count(request )
        return render(request,'adminindex.html',{'data':data})
    else:
        return render(request,'login.html')


def adminlogout(request):
    if 'richa@pet-shop.com' in request.session:
        del request.session['richa@pet-shop.com']
        return render(request,'login.html')
    else:
        return render(request,'login.html')


def add_doctor(request):
    return render(request,'add_doctor.html')

def addretailr(request):
    return render(request,'addretailr.html')

def allretailer(request):
    return render(request,'allretailer.html')

def alldoctors(request):
    if 'richa@pet-shop.com' in request.session:
        alldoctors=doctor_details.objects.all()
        return render(request,'alldoctors.html',{'doctors':alldoctors})
    else:
        return render(request,'login.html')

def allretailers(request):
    if 'richa@pet-shop.com' in request.session:
        allretailer=retailer_details.objects.all()
        return render(request,'allretailers.html',{'retailers':allretailer})
    else:
        return render(request,'login.html')

def delete_doctor(request,pk): 
        doctor_id=doctor_details.objects.get(id=pk)
        doctor_id.delete()
        alldoctors=doctor_details.objects.all()
        return render(request,'alldoctors.html',{'doctors':alldoctors})

def delete_retailer(request,pk):
        retailer_id=retailer_details.objects.get(id=pk)
        retailer_id.delete()
        allretailer=retailer_details.objects.all()
        return render(request,'allretailers.html',{'retailers':allretailer})


def vf(request):
    feedback=feedback_detail.objects.all()
    return render(request,'vf.html',{'c_vf':feedback})

def delete_vf(request,pk):
    fid=feedback_detail.objects.get(id=pk)
    fid.delete()
    feedback=feedback_detail.objects.all()
    return render(request,'vf.html',{'c_vf':feedback})

def retailer_product(request):
    return render(request,'retailer_product.html')


