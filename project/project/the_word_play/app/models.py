from django.db import models
import uuid
# Create your models here.

class registration(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    phone=models.IntegerField()
    address=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    license=models.FileField()
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    accoundnumber=models.CharField(max_length=50)
    status=models.IntegerField(default=0)

class Book(models.Model):
    book_id=models.AutoField(primary_key=True)
    book_name=models.CharField(max_length=50)
    author=models.CharField(max_length=25)
    category=models.CharField(max_length=15)
    description=models.CharField(max_length=150)
    price=models.IntegerField()
    quantity=models.IntegerField()
    image=models.FileField()
class customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    address = models.CharField(max_length=50)
    username = models.CharField(max_length=30,primary_key=True)
    password = models.CharField(max_length=20)
    city= models.CharField(max_length=50)
    pincode= models.IntegerField()
    def _str_(self) -> str:
        return self.username
class Cart(models.Model):
    product_details=models.ForeignKey(Book,on_delete=models.CASCADE)
    user_details=models.ForeignKey(customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField()
class wishlist(models.Model):
    product_details = models.ForeignKey(Book,on_delete=models.CASCADE)
    user_details = models.ForeignKey(customer,on_delete=models.CASCADE)
class reviews(models.Model):
    user_details=models.ForeignKey(customer,on_delete=models.CASCADE)
    product_details = models.ForeignKey(Book,on_delete=models.CASCADE)
    review = models.CharField(max_length=250)

class PasswordReset(models.Model):
    user=models.ForeignKey(customer,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)




class Single_Booking(models.Model):
        user_details = models.ForeignKey(customer, on_delete=models.CASCADE)
        product_details = models.ForeignKey(Book, on_delete=models.CASCADE)
        name = models.CharField(max_length=20, null=False)
        email = models.EmailField(null=False)
        phone = models.CharField(max_length=10, null=False)
        address = models.TextField(null=False)
        city = models.CharField(max_length=20, null=False)
        pincode = models.CharField(max_length=10, null=False)
        status = models.CharField(max_length=150, default='Pending')
        qty=models.IntegerField(default=1)
        total_price = models.IntegerField(null=False, default=0)
        payment_mode = models.CharField(max_length=150, null=False, default='razo')
        order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID for unique order ID

        def __str__(self):
            return f"Booking {self.order_id} - {self.name}"
class order_collect(models.Model):
    order_details = models.ForeignKey(Single_Booking, on_delete=models.CASCADE)
    delivery_details = models.ForeignKey(registration, on_delete=models.CASCADE)
    date = models.DateField()

class Multiple_Booking(models.Model):
        user_details = models.ForeignKey(customer, on_delete=models.CASCADE)
        Cart_details = models.JSONField()
        name = models.CharField(max_length=20, null=False)
        email = models.EmailField(null=False)
        phone = models.CharField(max_length=10, null=False)
        address = models.TextField(null=False)
        city = models.CharField(max_length=20, null=False)
        pincode = models.CharField(max_length=10, null=False)
        status = models.CharField(max_length=150, default='Pending')
        total_price = models.IntegerField(null=False, default=0)
        payment_mode = models.CharField(max_length=150, null=False, default='razo')
        order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID for unique order ID

        def __str__(self):
            return f"Booking {self.order_id} - {self.name}"

class Multiple_order_collect(models.Model):
    order_details = models.ForeignKey(Multiple_Booking, on_delete=models.CASCADE)
    delivery_details = models.ForeignKey(registration, on_delete=models.CASCADE)
    date = models.DateField()