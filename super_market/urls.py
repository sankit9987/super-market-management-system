from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('index', views.index1,name="index1"),
    path('login', views.Login,name="login"),
    path('register', views.register,name="register"),
    path('logout', views.user_logout,name="user_logout"),


    #user
    path('user/index', views.user_index,name="user_index"),
    path('user/cart', views.cart,name="cart"),
    path('user/register/employee', views.employee,name="employee"),
    path('product-detail/<int:id>', views.product,name="product"),
    path('payment:<int:id>', views.payment,name="payment"),

    #HR
    path('hr/view-application/<int:id>', views.view_application,name="view_application"),
    path('hr/application', views.application,name="application"),
    path('delete-application/<int:id>', views.delete_application,name="delete_application"),

    #billing
    # path('billing/', views.billing,name="billing"),


    #Employee
    path('item-to-pack', views.item_to_pack,name="item_to_pack"),
    path('pay/<int:id>', views.pay,name="pay"),

    #Admin
    path('add-product', views.add_product,name="add_product"),
    path('sale-detail', views.sale_detail,name="sale_detail"),
    path('admin-index', views.admin_index,name="admin_index"),
    path('view-product', views.view_product,name="view_product"),
    path('delete-product/<int:id>', views.delete_product,name="delete_product"),
    path('view-product-detail/<int:id>', views.view_product_detail,name="view_product_detail"),

]