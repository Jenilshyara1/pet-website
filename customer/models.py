from ast import mod
from pdb import main
from pickle import TRUE
from re import L
from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class user_details(models.Model):
    email=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    otp=models.IntegerField(default=4567)

class customer_details(models.Model):
    user_id=models.ForeignKey(user_details,on_delete=CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contactno=models.BigIntegerField()
    address=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    city=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,null=True)

class doctor_details(models.Model):
    user_id=models.ForeignKey(user_details,on_delete=CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    d_degree=models.CharField(max_length=100,null=True)
    contactno=models.BigIntegerField()
    address=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    city=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,null=True)
    d_picture=models.FileField(upload_to="media",default="none")

class retailer_details(models.Model):
    user_id=models.ForeignKey(user_details,on_delete=CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contactno=models.BigIntegerField()
    address=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    city=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,null=True)

class appointment(models.Model):
    doctor_id=models.ForeignKey(doctor_details,on_delete=CASCADE,null=True)
    firstname=models.CharField(max_length=100,null=True)
    lastname=models.CharField(max_length=100,null=True)
    contactnumber=models.BigIntegerField()
    date=models.DateField()
    time=models.TimeField()

class gallery(models.Model):
    customer_id=models.ForeignKey(customer_details,on_delete=CASCADE,null=True)
    g_image=models.FileField(upload_to="media/gallery")
    like=models.IntegerField(default=0)


class product(models.Model):
    retailer_id=models.ForeignKey(retailer_details,on_delete=CASCADE,default=1)
    productname=models.CharField(max_length=100)
    price=models.BigIntegerField()
    description=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    picture=models.FileField(upload_to="media",blank=True)

class feedback_detail(models.Model):
    f_name=models.CharField(max_length=100,null=True)
    c_feedback=models.CharField(max_length=100,null=True)

class cart_details(models.Model):
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(user_details,on_delete=models.CASCADE,null=True)
    total_price=models.IntegerField(null=True)
    qty=models.IntegerField(null=True)

class wish_details(models.Model):
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(user_details,on_delete=models.CASCADE,null=True)


class Transaction(models.Model):
    made_by = models.ForeignKey(user_details, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    

class images(models.Model):
    image1=models.FileField(upload_to="media/gallery")
    image2=models.FileField(upload_to="media/gallery")
