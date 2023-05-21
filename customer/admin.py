from django.contrib import admin
from customer.models import *

# Register your models here.
admin.site.register(user_details)
admin.site.register(customer_details)
admin.site.register(doctor_details)
admin.site.register(retailer_details)
admin.site.register(appointment)
admin.site.register(gallery)
admin.site.register(feedback_detail)
admin.site.register(product)
admin.site.register(cart_details)
admin.site.register(wish_details)
admin.site.register(Transaction)