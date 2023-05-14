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

def home(request):
    # print("home called")
    products = Product.objects.all()
    # cart = []
    total_product = 0
    # print("user is: ",request.user)
    if (str(request.user) != "AnonymousUser"):
        # print("in if")
        user=request.user
        cart = Cart.objects.filter(user=user)
        # print(cart, "cart")
        # print(cart)
        for x in cart:
            # print("in loop")
            # print(x)
            total_product = total_product+1 
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

@login_required
def productdetail(request,pk):
    product = Product.objects.get(pk=pk)
    cart = Cart.objects.filter(user=request.user)
    total_product = 0
    for x in cart:
        total_product = total_product+1 
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
        # return render(request,'registration.html',{'form':form})
        return redirect('/accounts/login/')


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
        return render(request, 'checkout.html', {'add' : add, 'totalamount' : totalamount, 'cart_items':cart_items,'total_product':total_product})
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
            return render(request, 'checkout.html', {'add' : add, 'totalamount' : totalamount, 'cart_items':cart_items,'total_product':total_product})
        else:
            return redirect('/placeorder/') 

@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('cust_id')
    customer = Customer.objects.get(id=cust_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer = customer,product = c.product, quantity = c.quantity).save()
        c.delete()
    return redirect('/orders/')    

@login_required
def order_done(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    content = "You haven't Ordered Any Product Yet. "
    total_product = 0
    for x in cart:
        total_product = total_product+1
    order = OrderPlaced.objects.filter(user = user)
    if order:
        return render (request,'orders.html',{'order':order,'total_product':total_product})
    else:
        return render (request,'orders.html',{'order':order,'total_product':total_product,'content':content})

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

