from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from myapp.forms import CustomerProfileForm, CustomerRegistrationForm, CustomerReportForm,FilterForm
from myapp.models import Cart, Customer, OrderPlaced, Product, Report, productImage,ProductReview
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
from functools import reduce
import operator
from django.core.paginator import Paginator
import razorpay
from django.conf import settings

def home(request):
    # print("home called")
    # carousel_products = OrderPlaced.objects.order_by('?')
    # carousel_products = list(OrderPlaced.objects.all())
    # change 3 to how many random items you want
    # random_carousel_items = random.sample(carousel_products, 10)

    products = Product.objects.all()
    # cart = []
    total_product = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_product = cart.count()
        
    if request.method == "GET":
        print(" ")
    elif request.method == "POST":
        total_product = 0
        price_filter = request.POST.get("price_filter")
        brand_filter = request.POST.get("brand_filter")
        discount_filter = request.POST.get("discount_filter")
        category_filter = request.POST.get("category_filter")
        # print(price_filter, brand_filter, discount_filter, category_filter)


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

        if (str(request.user) != "AnonymousUser"):
            user=request.user
            cart = Cart.objects.filter(user=user)
            for x in cart:
                total_product = total_product+1

        # print("post", products)
        # print(price_filter, brand_filter, discount_filter, category_filter)
        # return HttpResponseRedirect(request.path_info)

    context = {
        'products':products,
        'total_product':total_product
    }
    return render(request, 'home.html',context)

def retrive_filter(filter_type, value):
    if (filter_type == "brand"):
        if (value == '1'):
            return "Brand A"
        elif (value == '2'):
            return "Brand B"
        elif (value == '3'):
            return "Brand C"
        elif (value == '4'):
            return "Brand D"
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
    total_product = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_product = cart.count()
        
    if request.method == "GET":
        productImages = productImage.objects.all().filter(product_id = pk)
        # print(productImages)

        in_cart_item = False
        if request.user.is_authenticated:
            in_cart_item = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        in_order_item = False
        if request.user.is_authenticated:
            in_order_item = OrderPlaced.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        
        in_review_item = False
        if request.user.is_authenticated:
            in_review_item = ProductReview.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            
        discount_percentage = ((product.price-product.discounted_price)/product.price)*100
        dp = ("%.1f" % discount_percentage)

        data = {'product':product,
                'discount_percentage':dp,
                'productImages':productImages, 
                'pk':pk , 
                'in_cart_item':in_cart_item,
                'in_order_item':in_order_item,
                'in_review_item':in_review_item,
                'total_product':total_product
            }
        return render(request,'productdetail.html',data)
    
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
            return redirect('/accounts/login/')
        return render(request,'registration.html',{'form':form})


def make_filter(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('filter/')
    else:
        form = FilterForm()
    return render(request,'home.html',{'form':form,})   

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        cart = Cart.objects.filter(user=request.user)
        total_product = 0
        for x in cart:
            total_product = total_product+1 
        return render(request,'profile.html',{'form':form,'active':'btn-primary','total_product':total_product})

    def post(self,request):
        cart = Cart.objects.filter(user=request.user)
        total_product = 0
        for x in cart:
            total_product = total_product+1
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
        return render(request,'profile.html',{'form':form,'active':'btn-primary','total_product':total_product}) 

@method_decorator(login_required,name='dispatch')
class ReportView(View):
    def get(self,request):
        form = CustomerReportForm()
        cart = Cart.objects.filter(user=request.user)
        total_product = 0
        for x in cart:
            total_product = total_product+1 
        return render(request,'help_support.html',{'form':form,'active':'btn-primary','total_product':total_product})

    def post(self,request):
        form = CustomerReportForm(request.POST)
        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']
            problem = form.cleaned_data['problem']
            data = Report(user=user,email=email,problem=problem)
            data.save()
            messages.success(request,'Problem Reported Successfully.')
        return render(request,'help_support.html',{'form':form,'active':'btn-primary'}) 


@login_required
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/cart')
    return redirect('/accounts/login/')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        total_product = 0
        for x in cart:
            total_product = total_product+1
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
            return render(request,'addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount,'total_product':total_product})
        return render(request,'emptycart.html',{'total_product':total_product})

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

@login_required
def address(request):
    data = Customer.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    content = "No Address Found! Please add Address."
    total_product = 0
    for x in cart:
        total_product = total_product+1
    if data:    
        return render(request, 'address.html',{'data':data,'active':'btn-primary','total_product':total_product})
    else:
        return render(request, 'address.html',{'content':content,'active':'btn-primary','total_product':total_product})


def login(request):
    return render(request, 'login.html')

@login_required
def place_order(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = user)
    content = "Please Add Address Before Ordering Products."
    cart = Cart.objects.filter(user=request.user)
    total_product = 0
    for x in cart:
        total_product = total_product+1
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if add:
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount  
            totalamount = amount + shipping_amount   
        client = razorpay.Client(auth = (settings.KEY, settings.TEST))
        payment = client.order.create({'amount' : totalamount * 100, 'currency' : 'INR', 'payment_capture' : 1})
        for cart in cart:
            cart.razor_pay_order_id = payment['id']
            cart.payment_status = payment['status']
            cart.save()     
        return render(request, 'checkout.html', {'payment' : payment, 'add' : add, 'totalamount' : totalamount, 'cart_items':cart_items,'total_product':total_product})
    return render(request, 'checkout.html', {'content':content,'add' : add, 'totalamount' : totalamount, 'cart_items':cart_items,'total_product':total_product})


@login_required
def buy_now(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.filter(user = user,product=product)
        cart = Cart.objects.filter(user=request.user)
        total_product = 0
        for x in cart:
            total_product = total_product+1
        if not cart_item:
            Cart(user=user,product=product).save()
            add = Customer.objects.filter(user = user)
            cart_items = Cart.objects.filter(user = user)
            amount = 0.0
            shipping_amount = 70.0
            totalamount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.discounted_price)
                    amount += temp_amount  
                totalamount = amount + shipping_amount    
            return redirect('/placeorder/')
        else:
            return redirect('/placeorder/') 

@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('cust_id')
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    customer = Customer.objects.get(id=cust_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer = customer,product = c.product, quantity = c.quantity,razor_pay_order_id = razorpay_order_id, razor_pay_payment_id = razorpay_payment_id, razor_pay_payment_signature = razorpay_signature, payment_status = "succes").save()
        c.delete()
    return redirect('/orders/')    

@login_required
def order_done(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    content = "You haven't Ordered Any Product Yet."
    total_product = cart.count()
    
    order_list = OrderPlaced.objects.filter(user=user).order_by('-date_ordered')
    paginator = Paginator(order_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if order_list.exists():
        return render(request, 'orders.html', {'page_obj': page_obj, 'total_product': total_product})
    else:
        return render(request, 'orders.html', {'content': content, 'total_product': total_product})
    
@login_required
def product_search(request):
    query = request.GET['query']
    cart = Cart.objects.filter(user=request.user)
    total_product = 0
    for x in cart:
        total_product = total_product+1
    content = "No Product Found! Please Search By Name,Brand or Category."
    products = Product.objects.filter(Q(name__icontains = query)|Q(category__icontains = query)|Q(brand__icontains = query))
    if products:
        return render (request,'product_search.html',{'products':products,'total_product':total_product})
    else:
        return render (request,'product_search.html',{'content':content,'total_product':total_product})

def categories(request):
    total_product = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_product = cart.count()
    return render(request, 'categories.html', {'total_product': total_product})

def products(request, category=None):
    total_product = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_product = cart.count()
        
    products = Product.objects.all()
    if request.method == "GET":
        category_filter = request.GET.getlist('category')
        price_filter = request.GET.getlist('price')
        brand_filter = request.GET.getlist('brand')

        if category_filter:
            category_ranges = {
                '1': ("Clothing"),
                '2': ("Electronics"),
                '3': ("Food"),
                '4': ("Grocery"),
                '5': ("Stationary"),
                '6': ("Footwear"),
            }
            if category_filter:
                categories = [category_ranges[key] for key in category_filter]
                products = products.filter(category__in=categories)
            
        if price_filter:
            price_ranges = {
                '0': (0,500),
                '1': (501, 1000),
                '2': (1001, 5000),
                '3': (5001, 10000),
                '4': (10001, float('inf'))
            }
            price_queries = [Q(price__range=price_ranges[key]) for key in price_filter]
            products = products.filter(reduce(operator.or_, price_queries))
            
        if brand_filter:
            brand_ranges = {
                '1': ("Brand A"),
                '2': ("Brand B"),
                '3': ("Brand C"),
                '4': ("Brand D"),
            }
            if brand_filter:
                brands = [brand_ranges[key] for key in brand_filter]
                products = products.filter(brand__in=brands)  
                
    paginator = Paginator(products, 20)  # Show 10 products per page
    page_number = request.GET.get('page')
    products_actual = paginator.get_page(page_number) 
    
    total_count = paginator.count
    start_index = products_actual.start_index()
    end_index = products_actual.end_index()
        
    context = {
        'products': products_actual,
        'start_index': start_index,
        'end_index': end_index,
        'total_count': total_count,
        'total_product': total_product, #cart products for a logged in user
        'category_filter': category_filter,  # Pass filter parameters to the template
        'price_filter': price_filter,
        'brand_filter': brand_filter,
    }        
            
    return render(request, 'products.html', context)

def about(request):
    total_product = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        total_product = cart.count()
    return render(request, 'about.html', {'total_product': total_product})