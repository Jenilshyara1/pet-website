from ast import Return
import email
from operator import add
from typing import _SpecialForm, Counter
from unicodedata import category
from unittest import result
from urllib.request import Request
from django.shortcuts import render, resolve_url
from retailer.models import *
from retailer.views import p_count
from doctor.views import *
from .models import *
# from .utils import *
import random
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .paytm import generate_checksum, verify_checksum
from django.conf import settings

# Create your views here.

def search(request):
    if request.method=='POST':
        pname=request.POST.get('searchproduct',None)
        if pname:
            print("-------------->Inside if")
            sproduct=product.objects.filter(productname=pname)
            return render(request,'search.html',{'searchproduct':sproduct})
        else:
            print("-------------> Inside else")
            msg="product not found"
            return render(request,'search.html',{'msg':msg})
    else:
        return render(request,'index.html')


def get_count(request):
    customer_count=customer_details.objects.filter().count()
    doctor_count=doctor_details.objects.filter().count()
    retailer_count=retailer_details.objects.filter().count()
    data = {
        'total_retailer':retailer_count,
        'total_customer':customer_count,
        'total_doctor':doctor_count
    }
    return data

def index(request):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        if user_id.role=="customer":
            products = product.objects.all()
            cid=customer_details.objects.get(user_id=user_id)
            return render(request,'index.html',{'user_details':cid,'product':products})
        elif user_id.role=="doctor":
            did=doctor_details.objects.get(user_id=user_id)
            return render(request,'doctorindex.html',{'user_details':did})
        elif user_id.role=="retailer":
            rid=retailer_details.objects.get(user_id=user_id)
            data=p_count(request.session['email'])
            productdetails=product.objects.filter(retailer_id=rid)
            rproduct=product.objects.filter(retailer_id=rid)
            return render(request,'retailerindex.html',{'user_details':rid,'data':data,'r_product':rproduct})
    else:
        return render(request,'index.html')
    
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user_id=user_details.objects.filter(email=email)
        if user_id:
            user_id=user_details.objects.get(email=email)
            if user_id.password==password:
                request.session['email']=email
                if user_id.role=="customer":
                    cid=customer_details.objects.get(user_id=user_id)
                    products=product.objects.all()
                    return render(request,'index.html',{'user_details':cid, 'product':products})
                elif user_id.role=="retailer":
                    rid=retailer_details.objects.get(user_id=user_id)
                    data=p_count(request.session['email'])
                    productdetails=product.objects.filter(retailer_id=rid)
                    rproduct=product.objects.filter(retailer_id=rid)
                    return render(request,'retailerindex.html',{'user_details':rid, 'data':data, 'r_product':rproduct})
                elif user_id.role=="doctor":
                    did=doctor_details.objects.get(user_id=user_id)
                    customer_appointment=appointment.objects.filter(doctor_id=did)
                    data=ap_count(request.session['email'])
                    return render(request,'doctorindex.html',{'user_details':did,'ap':customer_appointment,'data':data}) 
            else:
                msg="Enter correct Password"
                return render(request,'login.html',{'msg':msg})
        else:  
            if email=='richa@pet-shop.com': 
                if password=='123456':
                    request.session['richa@pet-shop.com']=email  
                    data=get_count(request)
                    return render (request,'adminindex.html',{'data':data})
                else:
                    msg="Password not matched"
                    return render(request,'login.html',{'msg':msg})
            else:        
                msg="User not registered"
                return render(request,'register.html',{'msg':msg})        
    else:
        if 'email' in request.session:
            user_id=user_details.objects.get(email=request.session['email'])
            if user_id.role=="customer":
                cid=customer_details.objects.get(user_id=user_id)
                return render(request,'index.html',{'user_details':cid})
            elif user_id.role=="retailer":
                rid=retailer_details.objects.get(user_id=user_id)
                productdetails=product.objects.filter(retailer_id=rid)
                rproduct=product.objects.filter(retailer_id=rid)
                data=p_count()
                return render(request,'retailerindex.html',{'user_details':rid, 'data':data,'r_product':productdetails})
            elif user_id.role=="doctor":
                did=doctor_details.objects.get(user_id=user_id)
                customer_appointment=appointment.objects.filter(doctor_id=did)
                data=ap_count(request.session['email'])
                return render(request,'doctorindex.html',{'user_details':did,'ap':customer_appointment,'data':data})
        else:   
            return render(request,'login.html')

def register(request):
    if request.method=='POST':
        role=request.POST['role']
        fname=request.POST['tbfirstname']
        lname=request.POST['tblastname']
        email=request.POST['tbemail']
        contactno=request.POST['tbcontactno']
        password=request.POST['tbpassword']
        confirmpassword=request.POST['tbconfirmpassword']
        if confirmpassword==password:
            user_id=user_details.objects.filter(email=email)              
            if user_id:
                user_id=user_details.objects.get(email=email)
                msg="User already registerd"
                return render(request,'register.html',{'msg':msg})
            else:
                uid=user_details.objects.create(email=email,password=password,role=role)
                uid_id=user_details.objects.get(email=email)
                if role=="customer":
                    cid=customer_details.objects.create(user_id=uid_id,first_name=fname,last_name=lname,contactno=contactno)
                    # sendmail("confirmation","mail",email,{'firstname':fname, 'lastname':lname})
                    return render(request,'login.html')
                elif role=="retailer":
                    rid = retailer_details.objects.create(user_id=uid_id,first_name=fname,last_name=lname,contactno=contactno)
                    # sendmail("confirmation","mail",email,{'firstname':fname, 'lastname':lname})
                    return render(request,'login.html')
                elif role=="doctor":
                    did=doctor_details.objects.create(user_id=uid_id,first_name=fname,last_name=lname,contactno=contactno)
                    # sendmail("confirmation","mail",email,{'firstname':fname, 'lastname':lname})
                    return render(request,'login.html')             
        else:
            msg="Password and confirm password must be same"
            return render(request,'register.html',{'msg':msg})
    else:
        if 'email' in request.session:
            user_id=user_details.objects.get(email=request.session['email'])
            cid=customer_details.objects.get(user_id=user_id)
            return render(request,'index.html',{'user_details':cid})
        else:
            return render(request,'register.html')            

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return render(request,'login.html')
    else:
        return render(request,'login.html')

def profile(request):
    if 'email' in request.session:
        if request.method=='POST':
            address=request.POST['address']
            pincode=request.POST['pincode']
            city=request.POST['city']
            country=request.POST['country']
            user_id=user_details.objects.get(email=request.session['email'])
            customer_id=customer_details.objects.get(user_id=user_id)
            customer_id.address=address
            customer_id.pincode=pincode
            customer_id.city=city
            customer_id.country=country
            customer_id.save()
            return render(request,'profile.html',{'user_details':customer_id,'user_dtls':customer_id})
        else:
            user_id=user_details.objects.get(email=request.session['email'])
            customer_id=customer_details.objects.get(user_id=user_id)
            return render(request,'profile.html',{'user_details':customer_id,'user_dtls':user_id})
    else:
        return render(request,'login.html')

def forgetpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        user_id=user_details.objects.filter(email=email)
        if user_id:
            user_id=user_details.objects.get(email=email)
            otp=random.randint(111111,999999)
            user_id.otp=otp 
            user_id.save()
            # sendmail("OTP","otpmail",email,{'otp':otp})
            return render(request,'newpassword.html',{'email':email})
        else:
            msg="Email does not exist"
            return render(request,'forgetpassword.html')
    else:
        return render(request,'forgetpassword.html')

def changenewpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        otp=request.POST['otp']
        password=request.POST['password']
        cpassword=request.POST['confirmpassword']
        user_id=user_details.objects.get(email=email)
        if user_id.otp==int(otp):
            if password==cpassword:
                user_id.password=password
                user_id.save()
                return render(request,'login.html')
            else:
                msg="Password does not match"
                return render(request,'newpassword.html',{'msg':msg})
        else:
            msg="Incorrect otp"
            return render(request,'newpassword.html',{'msg':msg})
    else:
        return render(request,'newpassword.html')


def productdetail(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        proid=product.objects.filter(id=pk)
        return render(request,'productdetail.html',{'user_details':cid,'product':proid})
    else:
        return render(request,'login.html')
     
def bookappointment(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        did=doctor_details.objects.get(id=pk)
        return render(request,'bookappointment.html',{'user_details':cid,'d_id':did})
    else:
        return render(request,'login.html')

def bookap(request):
    if request.method=='POST':
        d_id=request.POST['d_id']
        firstname=request.POST['apfirstname']
        lastname=request.POST['aplastname']
        contact_no=request.POST['apcontactno']
        ap_date=request.POST['apdate']
        ap_time=request.POST['aptime']
        doctors=doctor_details.objects.all()
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        did=doctor_details.objects.get(id=d_id)
        appointmentid=appointment.objects.create(doctor_id=did,firstname=firstname,lastname=lastname,contactnumber=contact_no,date=ap_date,time=ap_time)
        return render(request,'doctor.html',{'user_details':cid,'alldoctors':doctors})
    else:
        if 'email' in request.session:
            user_id=user_details.objects.get(email=request.session['email'])
            cid=customer_details.objects.get(user_id=user_id)
            return render(request,'bookappointment.html',{'user_details':cid})
        else:
            return render(request,'login.html')


# sendmail("confirmation","mail",email,{'firstname':fname, 'lastname':lname})
def doctor(request):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        doctors=doctor_details.objects.all()
        return render(request,'doctor.html',{'alldoctors':doctors,'user_details':cid})
    else:
        return render(request,'login.html')
    

def doctordetail(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        doctorid=doctor_details.objects.filter(id=pk)
        return render(request,'doctordetail.html',{'doctors':doctorid,'user_details':cid})
    else:
        return render(request,'login.html')


def feedback(request):
    if 'email' in request.session:
        if request.method=='POST':
            user_id=user_details.objects.get(email=request.session['email'])
            cid=customer_details.objects.get(user_id=user_id)
            feedback_name=request.POST['feedback_name']
            cfeedback=request.POST['cfeedback']
            f_id=feedback_detail.objects.create(f_name=feedback_name,c_feedback=cfeedback)
            return render(request,'feedback.html',{'user_details':cid,'user_dtls':cid})
        else:
            user_id=user_details.objects.get(email=request.session['email'])
            customer_id=customer_details.objects.get(user_id=user_id)
            return render(request,'feedback.html',{'user_details':customer_id,'user_dtls':customer_id})
    else:
        return render(request,'login.html')

def addtocart(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        pid=product.objects.get(id=pk)
        p=int(pid.price)
        addto=cart_details.objects.filter(product_id=pid,user_id=user_id)
        if addto:
            addto=cart_details.objects.filter(user_id=user_id)
            total_amount=0
            for i in addto:
                total_amount=total_amount+i.total_price
            return render(request,'addtocart.html',{'user_details':cid,'pid':pid,'addto':addto,'totalamount':total_amount})
        else:
            addto=cart_details.objects.create(product_id=pid,user_id=user_id,total_price=p,qty=1)
            addto=cart_details.objects.filter(user_id=user_id)
            total_amount=0
            for i in addto:
                total_amount=total_amount+i.total_price
            return render(request,'addtocart.html',{'user_details':cid,'pid':pid,'addto':addto,'totalamount':total_amount})
    else:
        return render(request,'login.html')

def update_qty(request):
    if request.method=="POST":
        user_id=user_details.objects.get(email=request.session['email'])
        cart_id = request.POST['cart_id']
        qty = request.POST['qty']
        price = request.POST['price']
        print("----------------",price)
        if(cart_details.objects.filter(id=cart_id)):
            qty=int(qty)
            cart = cart_details.objects.get(id=cart_id)
            total=int(qty)*int(price)
            print("---------------",total)
            cart.total_price = total
            cart.qty=int(qty)
            cart.save()
            all_items = cart_details.objects.filter(user_id=user_id)
            subtotal=0
            for i in all_items:
                subtotal=subtotal+i.total_price
            data={
                'status':'updated',
                'total':total,
                'sub_total':subtotal,
            }
            return JsonResponse(data)
    
def cart(request):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    addto=cart_details.objects.filter(user_id=user_id)
    total_amount=0
    for i in addto:
        total_amount=total_amount+i.total_price
    return render(request,'addtocart.html',{'user_details':cid,'addto':addto,'totalamount':total_amount})

def wishlist(request):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    wish=wish_details.objects.filter(user_id=user_id)
    return render(request,'wishlist.html',{'user_details':cid,'wish':wish})

def addtowish(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        pid=product.objects.get(id=pk)
        p=int(pid.price)
        wish=wish_details.objects.filter(user_id=user_id)
        if wish:
            wish=wish_details.objects.filter(user_id=user_id)
            addto=cart_details.objects.filter(product_id=pid,user_id=user_id)
            return render(request,'wishlist.html',{'user_details':cid,'pid':pid,'wish':wish})
        else:
            wish=wish_details.objects.create(product_id=pid,user_id=user_id)
            wish=wish_details.objects.filter(user_id=user_id)
            return render(request,'wishlist.html',{'user_details':cid,'pid':pid,'wish':wish})
    else:
        return render(request,'login.html')


def about(request):
    return render(request,'about.html')





def gallerypicture(request):
    if request.method=="POST":
        user_id=user_details.objects.get(email=request.session['email'])
        cid=customer_details.objects.get(user_id=user_id)
        gallery_image=request.FILES['galleryimage']
        gi = gallery.objects.all()
        if gallery_image in gi:
            msg="Images already uploaded"
            return render(request,'gallerypicture.html',{'user_details':cid,'img':gi})
        else:
            image_id=gallery.objects.create(customer_id=cid,g_image=gallery_image)
            img=gallery.objects.all()
            return render(request,'gallerypicture.html',{'user_details':cid,'img':img})
    else:
        if 'email' in request.session:
            user_id=user_details.objects.get(email=request.session['email'])
            cid=customer_details.objects.get(user_id=user_id)
            img=gallery.objects.all()
            return render(request,'gallerypicture.html',{'user_details':cid,'img':img})
        else:
            return render(request,'login.html')

def c_food(request):
    user_id=user_details.objects.get(email=request.session['email'])
    products = product.objects.filter(category='Food')
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'c_food.html',{'user_details':cid,'product':products})
    
def c_acc(request):
    user_id=user_details.objects.get(email=request.session['email'])
    products = product.objects.filter(category='Accesories')
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'c_acc.html',{'user_details':cid,'product':products})

def c_dog(request):
    user_id=user_details.objects.get(email=request.session['email'])
    products = product.objects.filter(category='Dog')
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'c_acc.html',{'user_details':cid,'product':products})

def c_cat(request):
    user_id=user_details.objects.get(email=request.session['email'])
    products = product.objects.filter(category='cat')
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'c_cat.html',{'user_details':cid,'product':products})

def c_bird(request):
    user_id=user_details.objects.get(email=request.session['email'])
    products = product.objects.filter(category='Birds')
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'c_bird.html',{'user_details':cid,'product':products})

# def likephoto(request,pk):
#         user_id=user_details.objects.get(email=request.session['email'])
#         cid=customer_details.objects.get(user_id=user_id)
#         img=gallery.objects.all()
#         gid=gallery.objects.get(id=pk)
#         n=gid.like
#         print("---------------",type(n))
#         if request.method=="POST":
#             n+=1
#             gid.like=n
#             gid.save()
#             return render(request,'gallerypicture.html',{'user_details':cid,'img':img})
#         else:
#             return render(request,'gallerypicture.html',{'user_details':cid,'img':img})

def delet_cp(request,pk):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    cart_id=cart_details.objects.get(id=pk)
    cart_id.delete()
    addto=cart_details.objects.filter(user_id=user_id)
    return render(request,'addtocart.html',{'user_details':cid,'addto':addto})

def delwish(request,pk):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    wish_id=wish_details.objects.get(id=pk)
    wish_id.delete()
    wish=wish_details.objects.filter(user_id=user_id)
    return render(request,'wishlist.html',{'user_details':cid,'wish':wish})

def check(request):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    return render(request,'checkout.html',{'user_details':cid})

def checkout(request):
        pass

def amount(request):
    user_id=user_details.objects.get(email=request.session['email'])
    cid=customer_details.objects.get(user_id=user_id)
    addto=cart_details.objects.filter(user_id=user_id)
    total_amount=0
    for i in addto:
        total_amount=total_amount+i.total_price
    return render(request,'checkout.html',{'user_details':cid,'totalamount':total_amount})


# @csrf_exempt
# def callback(request):
#     if request.method == 'POST':
#         received_data = dict(request.POST)
#         paytm_params = {}
#         paytm_checksum = received_data['CHECKSUMHASH'][0]   
#         for key, value in received_data.items():
#             if key == 'CHECKSUMHASH':
#                 paytm_checksum = value[0]
#             else:
#                 paytm_params[key] = str(value[0])
#         # Verify checksum
#         is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
#         if is_valid_checksum:
#             received_data['message'] = "Checksum Matched"
#         else:
#             received_data['message'] = "Checksum Mismatched"
#             return render(request, 'callback.html', context=received_data)
#         return render(request, 'callback.html', context=received_data)


# def initiate_payment(request):
#     if request.method == "GET":
#         print("Inside if")
#         return render(request, 'pay.html')
#     else:
#         print("Inside else")
#         username =request.session['email'] 
#         amount = int(request.POST['amount'])
#         user_id = user_details.objects.get(email=username)
#         transaction = Transaction.objects.create(made_by=user_id, amount=amount)
#         transaction.save()
#         merchant_key = settings.PAYTM_SECRET_KEY

#         params = (
#             ('MID', settings.PAYTM_MERCHANT_ID),
#             ('ORDER_ID', str(transaction.order_id)),
#             ('CUST_ID', str(transaction.made_by.email)),
#             ('TXN_AMOUNT', str(transaction.amount)),
#             ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
#             ('WEBSITE', settings.PAYTM_WEBSITE),
#             # ('EMAIL', request.user.email),
#             # ('MOBILE_N0', '9911223388'),
#             ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
#             ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
#             # ('PAYMENT_MODE_ONLY', 'NO'),
#         )
#         for i in params:
#             print("*"*20,i)
#         paytm_params = dict(params)
#         checksum = generate_checksum(paytm_params, merchant_key)

#         transaction.checksum = checksum
#         transaction.save()

#         paytm_params['CHECKSUMHASH'] = checksum
#         print('SENT: ', checksum)
#         return render(request, 'redirect.html', context=paytm_params)

def orderhistory(request):
    return render(request,'orderhistory.html')

# # def order_history(request):
# #     pass


