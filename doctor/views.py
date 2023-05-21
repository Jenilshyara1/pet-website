from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from customer.models import *
from customer.views import *

# Create your views here.
def doctorindex(request):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        did=doctor_details.objects.get(user_id=user_id)
        customer_appointment=appointment.objects.filter(doctor_id=did)
        data=ap_count(request.session['email'])
        return render(request,'doctorindex.html',{'user_details':did,'ap':customer_appointment,'data':data})
    else:
        return render(request,'login.html')

def doctorprofile(request):
    if 'email' in request.session:
        if request.method=='POST':
            address=request.POST['address']
            pincode=request.POST['pincode']
            degree=request.POST['degree']
            city=request.POST['city']
            country=request.POST['country']
            profilepic=request.FILES['profileimage']
            user_id=user_details.objects.get(email=request.session['email'])
            doctor_id=doctor_details.objects.get(user_id=user_id)
            doctor_id.address=address
            doctor_id.d_degree=degree
            doctor_id.pincode=pincode
            doctor_id.d_picture=profilepic
            doctor_id.city=city
            doctor_id.country=country
            doctor_id.save()
            print("-------------------------------------",doctor_id.d_degree)
            return render(request,'doctorprofile.html',{'user_details':doctor_id,'user_dtls':doctor_id})
        else:
            user_id=user_details.objects.get(email=request.session['email'])
            doctor_id=doctor_details.objects.get(user_id=user_id)
            return render(request,'doctorprofile.html',{'user_details':doctor_id,'user_dtls':doctor_id})
    else:
        return render(request,'login.html')

def decline(request,pk):
    if 'email' in request.session:
        user_id=user_details.objects.get(email=request.session['email'])
        # doctor_id=doctor_details.objects.get(user_id=user_id)
        did=doctor_details.objects.get(user_id=user_id)
        customer_appointment=appointment.objects.get(id=pk)
        customer_appointment.delete()
        cid=appointment.objects.filter(doctor_id=did)
        return render(request,'doctorindex.html',{'user_details':did,'ap':cid})
    else:
        return render(request,'login.html')

def ap_count(email):
    user_id=user_details.objects.get(email=email)
    did=doctor_details.objects.get(user_id=user_id) 
    a_count=appointment.objects.filter(doctor_id=did).count()
    data = { 'total_ap' : a_count  }
    return data
