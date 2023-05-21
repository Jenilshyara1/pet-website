from django.shortcuts import render
from django.shortcuts import render, resolve_url

from customer.models import retailer_details
from .models import *
import random
from customer.models import *
from customer.views import *

# Create your views here.

def retailerindex(request):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        rid=retailer_details.objects.get(user_id=user_id)
        rproduct=product.objects.filter(retailer_id=rid)
        data=p_count(request.session['email'])
        return render(request,'retailerindex.html',{'user_details':rid,'data':data,'r_product':rproduct})
    else:
        return render(request,'login.html')

def retailerprofile(request):
    if 'email' in request.session:
        if request.method=='POST':
            address=request.POST['address']
            pincode=request.POST['pincode']
            city=request.POST['city']
            country=request.POST['country']
            user_id=user_details.objects.get(email=request.session['email'])
            retailer_id=retailer_details.objects.get(user_id=user_id)
            retailer_id.address=address
            retailer_id.pincode=pincode
            retailer_id.city=city
            retailer_id.country=country
            retailer_id.save()
            return render(request,'retailerprofile.html',{'user_details':retailer_id,'user_dtls':retailer_id})
        else:
            user_id=user_details.objects.get(email=request.session['email'])
            retailer_id=retailer_details.objects.get(user_id=user_id)
            return render(request,'retailerprofile.html',{'user_details':retailer_id,'user_dtls':retailer_id})
    else:
        return render(request,'login.html')

def addproduct(request):
    if 'email' in request.session:
        if request.method=="POST":
            user_id=user_details.objects.get(email=request.session['email'])
            rid=retailer_details.objects.get(user_id=user_id) 
            product_name=request.POST['tbproductname']
            p_category=request.POST['tbcategory']
            p_description=request.POST['tbdescription']
            p_price=request.POST['tbprice']
            p_quantity=request.POST['tbquantity']
            picture=request.FILES['upload']
            
            pid=product.objects.create(retailer_id=rid,productname=product_name,price=p_price,description=p_description,quantity=p_quantity,category=p_category,picture=picture) 
            return render(request,'addproduct.html', {'user_details':rid})
        else:
            return render(request,'addproduct.html' )
    else:
        return render(request,'login.html')

def p_count(email):
    user_id=user_details.objects.get(email=email)
    rid=retailer_details.objects.get(user_id=user_id) 

    product_count=product.objects.filter(retailer_id=rid).count()
    data= {
        'total_product' : product_count
    }
    return data

def rproductdetail(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        retailer_id=retailer_details.objects.get(user_id=user_id)
        product_id=product.objects.filter(id=pk)
        return render(request,'rproductdetail.html',{'user_details':retailer_id,'product':product_id})                
    else:
        return render(request,'login.html')

def delete_product(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        retailer_id=retailer_details.objects.get(user_id=user_id)
        pid=product.objects.get(id=pk)
        rproduct=product.objects.filter(retailer_id=retailer_id)
        pid.delete()
        data=p_count(request.session['email'])
        return render(request,'retailerindex.html',{'user_details':retailer_id,'product':pid,'r_product':rproduct,'data':data}) 
    else:
        return render(request,'login.html')

def paymenthistory(request):
    if 'email' in request.session:
        return render(request,'paymenthistory.html')
    else:
        return render(request,'login.html')

def orders(request):
    if 'email' in request.session:
        return render(request,'orders.html')
    else:
        return render(request,'login.html')

