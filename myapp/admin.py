from django.contrib import admin

# Register your models here.
from .models import Customer, OrderPlaced,Product,Cart, Report, productImage,ProductReview

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
     list_display = ['id','user','name','locality','hometown','zipcode','contact','state']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Report)
class reportAdmin(admin.ModelAdmin):
    list_display = ['id','user','email','problem','date_reported']    

@admin.register(OrderPlaced)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','date_ordered']    

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id','product','user','content','date_added','stars']

class productImageAdmin(admin.StackedInline):
    model = productImage
    # list_display = ['id','product','images']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','images','brand','category','price','discounted_price','discount_percentage','delivery_time','availability']
    inlines = [
            productImageAdmin,
        ]

admin.site.register(productImage)
admin.site.register(Product, ProductAdmin)