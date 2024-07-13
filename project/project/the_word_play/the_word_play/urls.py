"""
URL configuration for the_word_play project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about',views.about),
    path('log',views.log),
    path('delivery_reg', views.delivery_reg),
    path('user_regs',views.user_regs),
    path('login',views.login),
    path('user_reg',views.user_reg),
    path('delivery_regs',views.delivery_regs),
    path('logout',views.logout),
    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),

    ######################## user ###################3
    path('user_home', views.user_home),
    path('user_carts', views.user_carts),
    path('user_profile', views.user_profile),
    path('user_profile_update', views.user_profile_update),
    path('update_user_profile',views.update_user_profile),
    path('user_status', views.user_status),
    path('user_wish',views.user_wish),
    path('view_product',views.view_product),
    path('user_review/<int:id>', views.user_review),
    path('search',views.search),
    path('book_data/<int:id>', views.book_data),
    path('add_cart/<int:id>',views.addcart),
    path('cart/increment/<int:cart_id>/', views.increment_quantity, name='increment_quantity'),
    path('cart/decrement/<int:cart_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('remove/<int:id>', views.remove_cart),
    path('wish/<int:id>',views.wish),
    path('remove_wish/<int:id>', views.remove_wish),
    path('checkout',views.checkout),
    ##########payment#############3
    path('single_pay/<int:id>',views.single_pay),
    path('razor/<int:price>', views.razor),
    path('single_booking/<int:id>',views.single_booking),
    path('single_cash_on_delivery/<int:id>',views.single_cash_on_delivery),
    path('order_cancel/<uuid:id>',views.order_cancel),
    path('mul_order_cancel/<uuid:id>', views.mul_order_cancel),
    path('mul_cash_on_delivery',views.mul_cash_on_delivery),
    path('mul_pay',views.mul_pay),
    path('success',views.success),
    ##############book view
    path('Fiction', views.Fiction),
    path('Non_Fiction', views.Non_Fiction),
    path('Novel', views.Novel),
    path('Romance', views.Romance),
    path('Biography', views.Biography),
    path('Autobiography', views.Autobiography),
    path('Mystery', views.Mystery),
    path('Poetry_Books', views.Poetry_Books),
    path('Thrillers', views.Thrillers),
    path('Spiritual_Books', views.Spiritual_Books),
    path('Cook_Books', views.Cook_Books),
    path('History_Books', views.History_Books),
    path('other_book',views.other_book),

    ###############################  admin  #############
    path('admin_home',views.admin_home),
    path('admin_book', views.admin_book),
    path('admin_add_book', views.admin_add_book),
    path('admin_employee_view', views.admin_employee_view),
    path('admin_order_history', views.admin_order_history),
    path('admin_user_view', views.admin_user_view),
    path('add_book',views.add_book),
    path('admin_edit_book/<int:id>',views.admin_edit_book),
    path('logout_admin',views.logout_admin),
    path('admin_book_edit/<int:id>',views.admin_book_edit),
    path('remove_book/<int:id>',views.remove_book),
    path('ad_book_data/<int:id>',views.ad_book_data),
    path('emp_approve/<int:id>',views.emp_approve),
    path('emp_remove/<int:id>',views.emp_remove),
    path('user_remove/<str:id>',views.user_remove),
    path('admin_search',views.admin_search),
    path('new_order',views.new_order),
    path('ship_single/<uuid:id>', views.ship_single),
    path('ship_mul/<uuid:id>', views.ship_mul),

    ###############################  employee  #############
    path('delivery_home', views.delivery_home),
    path('delivery_collected_order', views.delivery_collected_order),
    path('delivery_order', views.delivery_Order),
    path('delivery_profile', views.delivery_profile),
    path('delivery_profile_edit', views.delivery_profile_edit),
    path('delivery_edit_profile',views.delivery_edit_profile),
    path('collect_order/<uuid:id>',views.collect_order),
    path('delivery/<uuid:id>',views.delivery),
    path('mul_collect_order/<uuid:id>', views.mul_collect_order),
    path('mul_delivery/<uuid:id>', views.mul_delivery),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)