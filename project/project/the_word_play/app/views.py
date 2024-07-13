from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import *
import random
from django.contrib import messages
from datetime import date
import uuid
import razorpay
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from itertools import chain


# Create your views here.
def index(re):
    return render(re,'home.html')
def log(re):
    return render(re,'login.html')
def about(re):
    return render(re,'about.html')
def user_reg(re):
    return render(re,'user_register.html')
def delivery_reg(re):
    return render(re,'delivery register.html')


def user_regs(re):
    if re.method=='POST':
        name=re.POST['name']
        email=re.POST['email']
        phone=re.POST['phone']
        address = re.POST['address']
        city = re.POST['city']
        pincode = re.POST['pincode']
        username=re.POST['username']
        password=re.POST['password']
        if customer.objects.filter(username=username).exists() or registration.objects.filter(username=username).exists():
                messages.error(re, 'Username already exists')
        else:
            data=customer.objects.create(name=name,email=email,phone=phone,address=address,city=city,pincode=pincode,username=username,password=password)
            data.save()
            messages.success(re, 'Account created')
            z=data.email
            message=f'''{name}We are thrilled to have you as part of our community.You can explore an extensive collection of books across all genres and subjects. Whether youre looking for the latest bestseller, a timeless classic, or a hidden gem, you can find and buy any book you want here.

Warm regards,
The Word Play Team'''
            send_mail('Congrats !!!', message,'settings.EMAIL_HOST_USER',[z],fail_silently=False)
        return render(re, 'login.html')
    return render(re,'login.html')


def delivery_regs(re):
    if re.method=='POST':
        name=re.POST['name']
        email=re.POST['email']
        phone=re.POST['phone']
        address = re.POST['address']
        location = re.POST['location']
        license = re.FILES['license']
        accoundnumber=re.POST['accoundnumber']
        username=re.POST['username']
        password=re.POST['password']

        if customer.objects.filter(username=username).exists() or registration.objects.filter(username=username).exists():
            messages.error(re, 'Username already exists')
        else:
            data=registration.objects.create(name=name,email=email,phone=phone,address=address,location=location,license=license,accoundnumber=accoundnumber,username=username,password=password)
            data.save()
            messages.success(re, 'Request Sent')
            z=data.email
            message=f'''Hello {name},

            Thank you for submitting your resume for the delivery job position at The Word Play.

            We have successfully received your application and our team is currently reviewing your credentials. Your application status is currently pending. Once we have completed our review, we will send you a confirmation email with the next steps.

            Thank you for your interest in joining our team. We appreciate your patience during this process and look forward to potentially working with you.

            Best regards,

            The Word Play Team'''
            send_mail('Congrats !!!', message,'settings.EMAIL_HOST_USER',[z],fail_silently=False)
        return render(re,'login.html')
    return render(re,'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user is a customer
        try:
            customer_data = customer.objects.get(username=username)
            if customer_data.password == password:
                request.session['user'] = username
                return redirect(user_home)  # Update with your user home view name
        except customer.DoesNotExist:
            pass  # Skip to next check

        # Check if the user is an admin
        if username == 'admin' and password == 'Admin@123':
            request.session['admin'] = username
            return redirect(admin_home)  # Update with your admin home view name

        # Check if the user is a registered employee
        try:
            registration_data = registration.objects.get(username=username)
            if registration_data.password == password:
                if registration_data.status != 0:
                    request.session['emp'] = username
                    return redirect(delivery_home)  # Update with your delivery home view name
                else:
                    messages.add_message(request, messages.INFO, "Request pending")
            else:
                messages.add_message(request, messages.INFO, "Invalid password")
        except registration.DoesNotExist:
            messages.add_message(request, messages.INFO, "Invalid username")

    return render(request, 'login.html')



def logout(re):
    if 'emp' in re.session or 'user' in re.session:
        re.session.flush()
    return render(re, 'login.html')



def forgot_password(re):
    if re.method == 'POST':
        email = re.POST.get('email')
        try:
            user = customer.objects.get(email=email)
        except:
            messages.info(re,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            messages.add_message(re, messages.SUCCESS, "Reset Mail Send Successfully")
        except:
            messages.info(re,"Network connection failed")
            return redirect(forgot_password)

    return render(re, 'forgot.html')

def reset_password(re, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if re.method == 'POST':
        new_password = re.POST.get('newpassword')
        repeat_password = re.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(re, 'reset-pass.html',{'token':token})





##################### user  #################################
def user_home(re):
    if 'user' in re.session:
        datas = Cart.objects.filter(user_details=re.session['user'])
        return render(re,'user/home.html',{'d1':datas})

def view_product(re):
    if 'user' in re.session:
        user = customer.objects.get(username=re.session['user'])
        datas = Cart.objects.filter(user_details=user)
        data =Book.objects.all()
        return render(re, 'user/book.html', {'Data': data,'d1': datas})


def book_data(re,id):
    if 'user' in re.session:
        datas = Cart.objects.filter(user_details=re.session['user'])
        data=Book.objects.get(pk=id)
        rev=reviews.objects.filter(product_details__pk=id)
        a=False
        if data.quantity>0:
            a=True
    return render(re, 'user/book data.html',{'Data':data,'a':a,'d1':datas,'rev': rev})
def user_review(re,id):
    if 'user' in re.session:
        if re.method=='POST':
            msg = re.POST.get('msg', '')
            book=Book.objects.get(pk=id)
            u=customer.objects.get(username=re.session['user'])
            reviews.objects.create(user_details=u,product_details=book,review=msg)
            b=book.pk
    return redirect(book_data,b)

def user_profile(re):
    if 'user' in re.session:
        data = customer.objects.get(username=re.session['user'])
        datas = Cart.objects.filter(user_details=re.session['user'])
        return render(re,'user/profile.html',{'Data':data,'d1':datas})
    return render(re,'user/profile.html')


def user_profile_update(re):
    if 'user' in re.session:
        data = customer.objects.get(username=re.session['user'])
        datas = Cart.objects.filter(user_details=re.session['user'])
        return render(re,'user/profile_update.html',{'Data':data,'d1':datas})
def update_user_profile(re):
    if 'user' in re.session:
        if re.method=='POST':
            name=re.POST['name']
            Number=re.POST['Number']
            email=re.POST['email']
            address=re.POST['address']
            city=re.POST['city']
            pincode=re.POST['pincode']
            customer.objects.filter(username=re.session['user']).update(name=name,phone=Number,email=email,address=address,city=city,pincode=pincode)
            messages.success(re, ' Update successfully')
        return redirect(user_profile)

def user_status(re):
    if 'user' in re.session:
        d1=Cart.objects.all()
        a=Single_Booking.objects.filter(user_details__username=re.session['user'])
        b=Multiple_Booking.objects.filter(user_details__username=re.session['user'])
    return render(re,'user/order status.html',{'Data':a,'data':b,'d1':d1})

def user_carts(re):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        b=Cart.objects.filter(user_details=u)
        # c=Book.objects.get(book_name=b.product_details.book_name)
        qty=1
        total=0
        for i in b:
            total+=i.product_details.price*i.quantity
            # Book.quantity-=i.quantity
            # c.save()
        return render(re,'user/cart.html',{'Data':b,'total':total})
def addcart(re,id):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        item=Book.objects.get(pk=id)
        v = Cart.objects.all()
        b = 0
        for i in v:
            if item.book_name == i.product_details.book_name:
                b=1
                i.quantity+=1
                i.save()
                item.quantity -= 1
                item.save()
        if b == 0:
            Cart.objects.create(product_details=item,user_details=u,total_price=item.price)
            item.quantity-=1
            item.save()
            messages.success(re,'Cart added successfully')
        return redirect(view_product)
def remove_cart(re,id):
    data=Cart.objects.get(pk=id)
    a=data.product_details
    a.quantity+=data.quantity
    a.save()
    data.delete()
    return redirect(user_carts)
def wish(re,id):
        if 'user' in re.session:
            u = customer.objects.get(username=re.session['user'])
            item = Book.objects.get(pk=id)
            v=wishlist.objects.all()
            b=0
            for i in v:
                if item.book_name==i.product_details.book_name:
                    b=1
            if b==0:
                wishlist.objects.create(product_details=item, user_details=u)
                messages.success(re, 'Wishlist added successfully')
            return redirect(view_product)

def user_wish(re):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        b=wishlist.objects.filter(user_details=u)
        datas = Cart.objects.filter(user_details=re.session['user'])
        return render(re,'user/wishlist.html',{'Data':b,'d1':datas})
def remove_wish(re,id):
    data=wishlist.objects.get(pk=id)
    data.delete()
    return redirect(user_wish)
def search(re):
    if re.method=='POST':
          b_name=re.POST['bookname']
          if b_name!='':
            data=Book.objects.filter(book_name=b_name)
          else:
              data = Book.objects.all()
          return render(re, 'user/book.html', {'Data': data})
    return redirect(view_product)

def Fiction(re):
        data = Book.objects.filter(category='Fiction')
        return render(re, 'user/book.html', {'Data': data})

def Non_Fiction(re):
        data = Book.objects.filter(category='Non-Fiction')
        return render(re, 'user/book.html', {'Data': data})

def Novel(re):
    data = Book.objects.filter(category='Novel')
    return render(re, 'user/book.html', {'Data': data})

def Romance(re):
    data = Book.objects.filter(category='Romance')
    return render(re, 'user/book.html', {'Data': data})

def Biography(re):
    data = Book.objects.filter(category='Biography')
    return render(re, 'user/book.html', {'Data': data})


def Autobiography(re):
    data = Book.objects.filter(category='Autobiography')
    return render(re, 'user/book.html', {'Data': data})

def Mystery(re):
    data = Book.objects.filter(category='Mystery')
    return render(re, 'user/book.html', {'Data': data})


def Poetry_Books(re):
    data = Book.objects.filter(category='Poetry Books')
    return render(re, 'user/book.html', {'Data': data})

def Thrillers(re):
    data = Book.objects.filter(category='Thrillers')
    return render(re, 'user/book.html', {'Data': data})


def Spiritual_Books(re):
    data = Book.objects.filter(category='Spiritual Books')
    return render(re, 'user/book.html', {'Data': data})

def Cook_Books(re):
    data = Book.objects.filter(category='Cook Books')
    return render(re, 'user/book.html', {'Data': data})

def History_Books(re):
    data = Book.objects.filter(category='History Books')
    return render(re, 'user/book.html', {'Data': data})

def other_book(re):
    data=Book.objects.all()
    l=[]
    for i in data:
        if i.category not in ['Fiction', 'Non-Fiction','Novel','Romance','Biography','Autobiography','Mystery','Poetry Books','Thrillers','Spiritual Books','Cook Books', 'History Books']:
            l.append(i)
    return render(re, 'user/book.html', {'Data': l})


def increment_quantity(re, cart_id):
    cart_item =Cart.objects.get(pk=cart_id)
    product = cart_item.product_details
    if product.quantity > 0:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * product.price
        product.quantity -= 1
        cart_item.save()
        product.save()
    else:
        messages.warning(re, 'No more available stock.')

    return redirect(user_carts)

def decrement_quantity(re, cart_id):
    cart_item = Cart.objects.get(pk=cart_id)
    product = cart_item.product_details

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.quantity * product.price
        product.quantity += 1  # Increment product quantity
        cart_item.save()
        product.save()  # Save product details
    else:
        messages.warning(re, 'Quantity cannot be less than 1.')

    return redirect(user_carts)
def checkout(re):
    if 'user' in re.session:
        data=customer.objects.get(username=re.session['user'])
        b = Cart.objects.filter(user_details=re.session['user'])
        total = 0
        for i in b:
            total += i.product_details.price * i.quantity
        return render(re,'user/checkout.html',{'Data':data,'data':b,'total':total,'a':True})






# ---------------------------- RAZOR PAY ---------------------------

def razor(request, price):
    if 'user' in request.session:
        amount = price * 100
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, "user/payment.html", {'amount': amount,'payment':payment})


def single_pay(re,id):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        book = Book.objects.get(pk=id)
        if re.method == "POST":
            Name = re.POST['name']
            Mobile_Number = re.POST['Number']
            email = re.POST['email']
            address = re.POST['address']
            city = re.POST['city']
            pincode = re.POST['pincode']
            order_id = uuid.uuid4()
            qty = re.POST['qty']
            amount = book.price*int(qty)
            Single_Booking.objects.filter(status='Pending',user_details=u).update(status='Payment Error')
            Single_Booking.objects.create(order_id=order_id,user_details=u, product_details=book,name=Name, phone=Mobile_Number,email=email, address=address,qty=qty, city=city, pincode=pincode,total_price=amount,payment_mode='Razor')
            book.quantity-=int(qty)
            book.save()
            return redirect(razor,amount)
        return redirect(view_product)
def single_cash_on_delivery(re,id):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        book = Book.objects.get(pk=id)
        if re.method == "POST":
            Name = re.POST['name']
            Mobile_Number = re.POST['Number']
            email = re.POST['email']
            address = re.POST['address']
            city = re.POST['city']
            pincode = re.POST['pincode']
            order_id = uuid.uuid4()
            qty=re.POST['qty']
            amount = int(book.price)*int(qty)
            Single_Booking.objects.create(order_id=order_id,user_details=u, product_details=book,name=Name, phone=Mobile_Number,email=email, address=address, city=city, pincode=pincode,qty=qty,total_price=amount,payment_mode='Cash on Delivery',status='Order Success')
            book.quantity-=int(qty)
            book.save()
            return render(re,'user/success.html')
        return redirect(view_product)
def mul_cash_on_delivery(re):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        b = Cart.objects.filter(user_details=u)
        total=0
        cart_items = []

        for i in b:
            total += i.product_details.price * i.quantity
            cart_items.append({
                'product_id': i.product_details.pk,
                'product_name': i.product_details.book_name,
                'quantity': i.quantity,
                'price': i.product_details.price,
            })
        if re.method == "POST":
            Name = re.POST['name']
            Mobile_Number = re.POST['Number']
            email = re.POST['email']
            address = re.POST['address']
            city = re.POST['city']
            pincode = re.POST['pincode']
            order_id = uuid.uuid4()
            Multiple_Booking.objects.create(order_id=order_id,user_details=u, Cart_details=cart_items,name=Name, phone=Mobile_Number,email=email, address=address, city=city, pincode=pincode,total_price=total,payment_mode='Cash on Delivery',status='Order Success')
            b.delete()
        return render(re,'user/success.html')
    return redirect(view_product)
def mul_pay(re):
    if 'user' in re.session:
        u=customer.objects.get(username=re.session['user'])
        b = Cart.objects.filter(user_details=u)
        total = 0
        cart_items = []
        for i in b:
            total += i.product_details.price * i.quantity
            cart_items.append({
                'product_id': i.product_details.pk,
                'product_name': i.product_details.book_name,
                'quantity': i.quantity,
                'price': i.product_details.price,
            })
        if re.method == "POST":
            Name = re.POST['name']
            Mobile_Number = re.POST['Number']
            email = re.POST['email']
            address = re.POST['address']
            city = re.POST['city']
            pincode = re.POST['pincode']
            order_id = uuid.uuid4()
            Multiple_Booking.objects.filter(status='Pending',user_details=u).update(status='Payment Error')
            Multiple_Booking.objects.create(order_id=order_id,user_details=u, Cart_details=cart_items,name=Name, phone=Mobile_Number,email=email, address=address, city=city, pincode=pincode,total_price=total,payment_mode='Razor')
            b.delete()
            return redirect(razor,total)
        return redirect(view_product)
def order_cancel(re,id):
    a=Single_Booking.objects.get(pk=id)
    a.delete()
    return redirect(user_status)
def mul_order_cancel(re,id):
    a=Multiple_Booking.objects.get(pk=id)
    a.delete()
    return redirect(user_status)
def single_booking(re,id):
    if 'user' in re.session:
            book=Book.objects.get(pk=id)
            data=customer.objects.get(username=re.session['user'])
            if re.method=='POST':
                b=False
                qty=re.POST['qty']
                if int(book.quantity)>=int(qty):
                      b=True
                total=int(book.price)*int(qty)
            return render(re, 'user/checkout.html', {'Data': data, 'book': book,'total':total,'a':False,'qty':qty,'b':b})


def success(re):
    if 'user' in re.session:
        data = customer.objects.get(username=re.session['user'])
        Single_Booking.objects.filter(status='Pending',user_details=data).update(status='Order Success')
        Multiple_Booking.objects.filter(status='Pending',user_details=data).update(status='Order Success')
    return render(re,'user/success.html')

############################## admin #######################################
def admin_home(re):
    return render(re,'admin/home.html')
def admin_book(re):
    if 'admin' in re.session:
        d = Book.objects.all()
        return render(re, 'admin/book.html', {'Data': d})
    return render(re, 'admin/book.html')
def admin_add_book(re):
    return render(re,'admin/add book.html')
def admin_employee_view(re):
    if 'admin' in re.session:
        d = registration.objects.all()
        l=[]
        for i in d:
            if i.status!=0:
                l.append(i)
        return render(re, 'admin/employee_view.html', {'Data':d,'l':l})
    return render(re, 'admin/employee_view.html')

def ad_book_data(re,id):
        d = reviews.objects.filter(product_details__pk=id)
        data=Book.objects.get(pk=id)
        return render(re, 'admin/book data.html',{'Data':data,'rev':d})



def admin_order_history(re):
        a = order_collect.objects.all()
        b=Multiple_order_collect.objects.all()
        return render(re,'admin/order history.html', {'Data': a,'data':b})

def admin_user_view(re):
        d = customer.objects.all()
        return render(re, 'admin/user view.html', {'Data':d})
def add_book(re):
    if re.method=='POST':
        b_name=re.POST['b_name']
        Author=re.POST['author']
        Category=re.POST['category']
        Description=re.POST['description']
        Price=re.POST['price']
        Quantity=re.POST['quaty']
        Image=re.FILES['image']
        data = Book.objects.create(book_name=b_name, author=Author, category=Category, description=Description, price=Price, quantity=Quantity, image=Image)
        data.save()
        messages.success(re, 'Book added successfully')
        return render(re,'admin/add book.html')
    return redirect(admin_add_book)
def admin_book_edit(re,id):
    if 'admin' in re.session:
        item=Book.objects.get(pk=id)
        return render(re, 'admin/edit book.html',{'Data':item})
def admin_edit_book(re,id):
    if 'admin' in re.session:
        if re.method == 'POST':
            b_name = re.POST['b_name']
            Author = re.POST['author']
            Category = re.POST['category']
            Description = re.POST['description']
            Price = re.POST['price']
            Quantity = re.POST['quaty']
            if 'image' in re.FILES:
                image = re.FILES['image']
            else:
                # Handle case where no new image was uploaded (retain existing image)
                book = Book.objects.get(pk=id)
                image = book.image
            Book.objects.filter(pk=id).update(book_name=b_name, author=Author, category=Category,description=Description, price=Price, quantity=Quantity, image=image)
            return redirect(admin_book)
def logout_admin(re):
    if 'admin' in re.session:
        re.session.flush()
        return render(re, 'login.html')

def remove_book(re,id):
    if 'admin' in re.session:
        data=Book.objects.get(pk=id)
        data.delete()
        return redirect(admin_book)
def emp_approve(re,id):
    if 'admin' in re.session:
        registration.objects.filter(pk=id).update(status=1)
        data=registration.objects.get(pk=id)
        z = data.email
        message = f'''Dear {data.name},
        We are thrilled to inform you that your request to become a delivery partner with The Word Play has been approved!

Welcome to our team! Your role is crucial in ensuring that our customers receive their orders promptly and efficiently. We are confident that your dedication and commitment will significantly contribute to our success.
        Warm regards,
        The Word Play Team'''
        send_mail(' Welcome to The Word Play! Your Delivery Partner Request is Approved', message, 'settings.EMAIL_HOST_USER', [z], fail_silently=False)
        return redirect(admin_employee_view)
def emp_remove(re,id):
    if 'admin' in re.session:
        data = registration.objects.get(pk=id)
        z = data.email
        message = f'''Dear {data.name},
                Thank you for your interest in becoming a delivery partner with [Company Name]. We appreciate the time and effort you put into your application.
                After careful consideration, we regret to inform you that we will not be moving forward with your application at this time.
                If you have any questions or need further information, please do not hesitate to reach out to us at thewordplaybooks@gmail.com .
                Thank you once again for your interest in partnering with us. We wish you all the best in your future endeavors.

Sincerely,
The Word Play Team
'''
        send_mail(' Update on Your Delivery Partner Application with The Word Play', message,'settings.EMAIL_HOST_USER', [z], fail_silently=False)

        data.delete()
    return redirect(admin_employee_view)
def user_remove(re,id):
        data=customer.objects.get(username=id)
        data.delete()
        return redirect(admin_user_view)
def admin_search(re):
    if re.method=='POST':
          b_name=re.POST['bookname']
          if b_name!='':
            data=Book.objects.filter(book_name=b_name)
          else:
              data = Book.objects.all()
          return render(re, 'admin/book.html', {'Data': data})
    return render(view_product)
def new_order(re):
        a=Single_Booking.objects.filter(status='Order Success')
        b=Multiple_Booking.objects.filter(status='Order Success')
        return render(re,'admin/neworder.html',{'Data':a ,'data':b})

def ship_single(re,id):
    Single_Booking.objects.filter(pk=id).update(status='Shipped')
    return redirect(new_order)
def ship_mul(re,id):
    Multiple_Booking.objects.filter(pk=id).update(status='Shipped')
    return redirect(new_order)







############################## employee #######################################
def delivery_home(re):
    return render(re,'delivery/home.html')
def delivery_collected_order(re):
    if 'emp' in re.session:
        d=order_collect.objects.filter(delivery_details__username=re.session['emp'])
        c=Multiple_order_collect.objects.filter(delivery_details__username=re.session['emp'])
        a=[]
        b=[]
        for i in d:
            if i.order_details.status=='Ready to Delivery':
                a.append(i)
        for i in c:
            if i.order_details.status=='Ready to Delivery':
                b.append(i)
        return render(re,'delivery/collected order.html',{'Data':a,'data':b})
    return render(re,'delivery/collected order.html')

def delivery_Order(re):
    if 'emp' in re.session:
        a=registration.objects.get(username=re.session['emp'])
        b=Single_Booking.objects.all()
        near=[]
        l=[]
        mu = Multiple_Booking.objects.all()
        n = []
        long = []
        for i in mu:
            if i.status == 'Shipped':
                if i.city == a.location:
                    n.append(i)
                else:
                    long.append(i)
            else:
                pass
        for i in b:
                if i.status == 'Shipped':
                    if i.city==a.location:
                        near.append(i)
                    else:
                        l.append(i)
                else:
                    pass
        return render(re,'delivery/Order.html',{'Data':near,'Data1':l,'d':n,'d1':long})

def collect_order(re,id):
        u=registration.objects.get(username=re.session['emp'])
        b=Single_Booking.objects.get(pk=id)
        order_collect.objects.create(order_details=b,delivery_details=u,date=date.today())
        Single_Booking.objects.filter(pk=id).update(status='Ready to Delivery')
        return redirect(delivery_Order)
def mul_collect_order(re,id):

        u=registration.objects.get(username=re.session['emp'])
        b=Multiple_Booking.objects.get(pk=id)
        Multiple_order_collect.objects.create(order_details=b,delivery_details=u,date=date.today())
        Multiple_Booking.objects.filter(pk=id).update(status='Ready to Delivery')
        return redirect(delivery_Order)
def delivery(re,id):
        data=Single_Booking.objects.filter(pk=id).update(status='Deliverd')
        order_collect.objects.filter(order_details=data).update(date=date.today())
        return redirect(delivery_collected_order)
def mul_delivery(re,id):

        data=Multiple_Booking.objects.filter(pk=id).update(status='Deliverd')
        Multiple_order_collect.objects.filter(order_details=data).update(date=date.today())
        return redirect(delivery_collected_order)
def delivery_profile(re):
    if 'emp' in re.session:
        data = registration.objects.get(username=re.session['emp'])
    return render(re,'delivery/profile.html',{'Data':data})
def delivery_profile_edit(re):
    if 'emp' in re.session:
        data = registration.objects.get(username=re.session['emp'])
    return render(re, 'delivery/profile edit.html', {'Data': data})

def delivery_edit_profile(re):
    if 'emp' in re.session:
        if re.method=='POST':
            name=re.POST['name']
            phone=re.POST['phone']
            email=re.POST['email']
            address=re.POST['address']
            location=re.POST['location']
            accoundnumber=re.POST['accoundnumber']
            if 'license' in re.FILES:
                license=re.FILES['license']
            else:
                # Handle case where no new image was uploaded (retain existing image)
                data = registration.objects.get(username=re.session['emp'])
                license = data.license

            registration.objects.filter(username=re.session['emp']).update(name=name,phone=phone,email=email,address=address,location=location,accoundnumber=accoundnumber,license=license)
            messages.success(re, ' Update successfully')
    return redirect(delivery_profile)
