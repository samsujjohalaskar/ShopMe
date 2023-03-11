from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from flask import redirect
from myapp.forms import CustomerRegistrationForm,FilterForm, LoginForm
from myapp.models import Product, productImage,ProductReview
from django.contrib import messages

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

# class ProductDetailView(View):
#     def get(self,request,pk):
#         product = Product.objects.get(pk=pk)
#         productImages = productImage.objects.all().filter(product_id = pk)
#         # print(productImages)
#         discount_percentage = ((product.price-product.discounted_price)/product.price)*100
#         dp = ("%.1f" % discount_percentage)
#         return render(request,'productdetail.html',{'product':product,'discount_percentage':dp, 'productImages':productImages})


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


# def filter(request,data = None):
#     if data == None:
#         brands = Product.objects.filter(brand = 'brand')
#     elif data == 'brand1' or data == 'brand2' or data == 'brand3':
#         brands = Product.objects.filter(brand = 'brand').filter(brand=data)
#     return render(request, 'filter.html',{'brands':brands})

class CustomerRegistrationView(View):
    def get(self,request):
        form =CustomerRegistrationForm()
        return render(request,'registration.html',{'form':form})
    
    def post(sel,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! Registration Successfull.')
            form.save()
        return render(request,'registration.html',{'form':form})

def profile(request):
    return render(request, 'profile.html')

def make_filter(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('filter/')
    else:
        form = FilterForm()
    return render(request,'home.html',{'form':form})    

# class ProductView(View):
#     def get(self, request):
#         clothing = Product.objects.filter(category='Clothing')
#         electronics = Product.objects.filter(category='Electronics')
#         foods = Product.objects.filter(category='Foods')
#         grocery = Product.objects.filter(category='Grocery')
#         stationary = Product.objects.filter(category='Stationary')
#         footwear = Product.objects.filter(category='Footwear')

        

#         return render(request, 'home.html',
#                       {'clothing': clothing,
#                        'electronics': electronics,
#                         'foods':foods,
#                         'grocery':grocery,
#                          'stationary':stationary,
#                            'footwear':footwear   }
#                       )


def add_to_cart(request):
    return render(request, 'addtocart.html')


def address(request):
    return render(request, 'address.html')


def login(request):
    return render(request, 'login.html')


def checkout(request):
    return render(request, 'checkout.html')
