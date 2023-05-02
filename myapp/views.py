from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from myapp.forms import CustomerProfileForm, CustomerRegistrationForm,FilterForm, LoginForm
from myapp.models import Cart, Customer, Product, productImage,ProductReview
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

def home(request):
    products = Product.objects.all() 
    if request.method == "GET":
        print("get")
    elif request.method == "POST":
        price_filter = request.POST.get("price_filter")
        brand_filter = request.POST.get("brand_filter")
        discount_filter = request.POST.get("discount_filter")
        category_filter = request.POST.get("category_filter")
        print(price_filter, brand_filter, discount_filter, category_filter)


        if(price_filter == '1'):
            products = products.filter(price__range=(0, 1000))
        if(price_filter == '2'):
            products = products.filter(price__range=(1001, 5000))
        if(price_filter == '3'):
            products = products.filter(price__range=(5001, 10000))
        if(price_filter == '4'):
            products = products.filter(price__gt=10000)

        if(discount_filter == '1'):
            products = products.filter(discount_percentage__range=(0, 10))
        if(discount_filter == '2'):
            products = products.filter(discount_percentage__range=(11, 20))
        if(discount_filter == '3'):
            products = products.filter(discount_percentage__range=(21, 30))
        if(discount_filter == '4'):
            products = products.filter(discount_percentage__gt=30)

        if (brand_filter != '0'):
            brand_filter = retrive_filter("brand", brand_filter)
            products = products.filter(brand = brand_filter)

        if (category_filter != '0'):
            category_filter = retrive_filter("category", category_filter)
            products = products.filter(category = category_filter)


        print("post", products)
        print(price_filter, brand_filter, discount_filter, category_filter)
        # return HttpResponseRedirect(request.path_info)

    context = {
        'products':products,
    }
    return render(request, 'home.html',context)

def retrive_filter(filter_type, value):
    if (filter_type == "brand"):
        if (value == '1'):
            return "brand1"
        elif (value == '2'):
            return "brand2"
        elif (value == '3'):
            return "brand3"
    elif (filter_type == "category"):
        if (value == '1'):
            return "Clothing"
        elif (value == '2'):
            return "Electronics"
        elif (value == '3'):
            return "Food"
        elif (value == '4'):
            return "Grocery"
        elif (value == '5'):
            return "Stationary"
        elif (value == '6'):
            return "Footwear"
        
def retrive_price_filter(value):
    pass


def productdetail(request,pk):
    product = Product.objects.get(pk=pk)
    if request.method == "GET":
        productImages = productImage.objects.all().filter(product_id = pk)
        # print(productImages)
        discount_percentage = ((product.price-product.discounted_price)/product.price)*100
        dp = ("%.1f" % discount_percentage)
        return render(request,'productdetail.html',{'product':product,'discount_percentage':dp, 'productImages':productImages, 'pk':pk})
    
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars',3)
        content = request.POST.get('content', '')
        print(content)

        review = ProductReview.objects.create(product=product,user=request.user,stars=stars,content=content)

        # return redirect('productdetail/'+ str(pk) )
        return HttpResponseRedirect(request.path_info)


class CustomerRegistrationView(View):
    def get(self,request):
        form =CustomerRegistrationForm()
        return render(request,'registration.html',{'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # messages.success(request,'Congratulations! Registration Successfull.')
            form.save()
        # return render(request,'registration.html',{'form':form})
        return redirect('/accounts/login/')


def make_filter(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('filter/')
    else:
        form = FilterForm()
    return render(request,'home.html',{'form':form})   


class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            hometown = form.cleaned_data['hometown']
            zipcode = form.cleaned_data['zipcode']
            contact = form.cleaned_data['contact']
            state = form.cleaned_data['state']
            data = Customer(user=user,name=name,locality=locality,hometown=hometown,zipcode=zipcode,contact=contact,state=state)
            data.save()
            messages.success(request,'Your Address Updated Successfully.')
        return render(request,'profile.html',{'form':form,'active':'btn-primary'}) 


def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/cart')
    return redirect('/accounts/login/')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        # list comprehension
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_amount
            return render(request,'addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
        return render(request,'emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        # list comprehension
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount,
            }
                
            return JsonResponse(data)
        

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if (c.quantity > 1):
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 70.0
            # list comprehension
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.discounted_price)
                    amount += temp_amount

                data = {
                    'quantity':c.quantity,
                    'amount':amount,
                    'totalamount':amount + shipping_amount,
                }
                    
                return JsonResponse(data)        

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        # list comprehension
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount

            data = {
                'amount':amount,
                'totalamount':amount + shipping_amount,
            }
                
            return JsonResponse(data)

def address(request):
    data = Customer.objects.filter(user=request.user)
    return render(request, 'address.html',{'data':data,'active':'btn-primary'})


def login(request):
    return render(request, 'login.html')


def place_order(request):
    return render(request, 'checkout.html')
