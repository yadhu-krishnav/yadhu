from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(registration)
admin.site.register(Book)
admin.site.register(customer)
admin.site.register(Cart)
admin.site.register(reviews)
admin.site.register(PasswordReset)
admin.site.register(wishlist)
admin.site.register(Multiple_Booking)
admin.site.register(order_collect)
admin.site.register(Single_Booking)
admin.site.register(Multiple_order_collect)

