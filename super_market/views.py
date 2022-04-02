from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        p = Product.objects.all()
        return render(request, "index.html",{'p':p})
    else:
        return redirect("user_index")

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect("login")

def Login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = username,password=password)
            if user:
                login(request, user)
                if request.user.is_hr:
                    return redirect("application")
                elif request.user.is_superuser:
                    return redirect("admin_index")
                elif request.user.is_staff:
                    return redirect("item_to_pack")
                else:
                    return redirect("user_index")
            else:
                messages.error(request, "Please check email and password!!!")
                return redirect("login")
        return render(request, "login.html")
    else:
        return redirect("index")

def index1(request):
    return render(request, "index1.html")

def register(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            name = request.POST['name']
            number = request.POST['number']
            zip = request.POST['zip']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            user = User.objects.filter(email=email)
            if user:
                messages.error(request, "User already exits!!!")
            else:
                u = User.objects.create_user(email=email, password=password,mobile_no=number,state=state,zip=zip,name=name,Address=address,Address2=address2,city=city)
                u.is_user = True
                u.save()
                return redirect("login")
        return render(request, "registration.html")
    else:
        return redirect("index")


@login_required(login_url='login')
def user_index(request):
    product = Product.objects.all()
    return render(request, "user/index.html",{'product':product})


@login_required(login_url='login')
def cart(request):
    c =Cart.objects.filter(user=request.user)
    return render(request, "user/add-to-cart.html",{'c':c})

@login_required(login_url='login')
def ucart(request):
    if request.method=="POST":
        p = request.POST['p']
        p = Product.objects.get(id=p)
        Cart.objects.create(user=request.user,product=p)
        return redirect("user_index")

@login_required(login_url='login')
def employee(request):
    if request.method=='POST':
        email = request.POST['email']
        Experience = request.POST['Experience']
        job_type = request.POST['job_type']
        user = User.objects.get(email=email)
        if user:
            user.status = "pending"
            user.experience=Experience
            user.job_type = job_type
            user.save()
            messages.success(request, "Application Send")
            return redirect("employee")
        else:
            u = User.objects.create_user(email=email, password=password,mobile_no=number,state=state,zip=zip,name=name,Address=address,Address2=address2,city=city)
            u.is_user = True
            u.is_staff = True
            u.save()
            return redirect("index")
    return render(request, "user/register-as-employee.html")

@login_required(login_url='login')
def product(request,id):
    pro = Product.objects.get(id=id)
    return render(request, "user/product-detail.html",{'p':pro})

@login_required(login_url='login')
def payment(request,id):
    if request.method=='POST':
        name = request.POST['cardname']
        expmonth = request.POST['expmonth']
        expyear = request.POST['expyear']
        cardnumber = request.POST['cardnumber']
        cvv = request.POST['cvv']
        p = Product.objects.get(id=id)
        Payment.objects.create(product=p,name=name,expmonth=expmonth,expyear=expyear,cvv=cvv,cardnumber=cardnumber,status='unpacked')
        return redirect("user_index")
    p = Product.objects.get(id=id)
    return render(request, "user/payment.html",{'p':p})

@login_required(login_url='login')
def application(request):
    if request.user.is_hr:
        user = User.objects.filter(status='pending')
        return render(request, "HR/application.html",{'user':user})
    else:
        return redirect("user_index")

@login_required(login_url='login')
def view_application(request,id):
    if request.user.is_hr:
        user = User.objects.get(id=id)
        return render(request, "HR/view-application.html",{'user':user})
    else:
        return redirect("user_index")


@login_required(login_url='login')
def delete_application(request,id):
    if request.user.is_hr:
        user = User.objects.get(id=id)
        user.status = 'reject'
        user.save()
        return redirect("application")
    else:
        return redirect("user_index")

@login_required(login_url='login')
def item_to_pack(request):
    if request.user.is_staff:
        p = Payment.objects.filter(status='unpacked')
        return render(request, "Employee/items-to-pack.html",{'pay':p})
    else:
        return redirect("user_index")

@login_required(login_url='login')
def pay(request,id):
    if request.user.is_staff:
        p = Payment.objects.get(id=id)
        p.status = 'packed'
        p.save()
        return redirect("item_to_pack")
    else:
        return redirect("user_index")

@login_required(login_url='login')
def add_product(request):
    if request.user.is_superuser:
        if request.method=='POST':
            name = request.POST['name']
            description = request.POST['description']
            stock = request.POST['stock']
            image = request.FILES['image']
            cost = request.POST['cost']
            Product.objects.create(name=name,description=description,image=image,price=cost)
            return redirect("view_product")
        return render(request, "hod/add-item.html")
    else:
        return redirect("user_index")
    


@login_required(login_url='login')
def view_product(request):
    if request.user.is_superuser:
        p = Product.objects.all()
        return render(request, "hod/item-detail.html",{'p':p})
    else:
        return redirect("user_index")


def delete_product(request,id):
    if request.user.is_superuser:
       p = Product.objects.get(id=id)
       p.delete()
       return redirect("view_product")
    else:
        return redirect("user_index")


def view_product_detail(request,id):
    if request.user.is_superuser:
        p = Product.objects.get(id=id)
        if request.method=='POST':
            name = request.POST['name']
            description = request.POST['description']
            cost = request.POST['cost']
            Product.objects.filter(id=id).update(name=name,price=cost,description=description)
            return redirect("view_product")
        return render(request, "hod/edit-item.html",{'p':p})
    else:
        return redirect("user_index")


def sale_detail(request):
    if request.user.is_superuser:
        p = Payment.objects.all()
        return render(request, "hod/sales-detail.html",{"p":p})
    else:
        return redirect("user_index")


def admin_index(request):
    if request.user.is_superuser:
        return render(request,"hod/index.html")
    else:
        return redirect("user_index")