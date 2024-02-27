from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
from .models import Customer, OrderPlaced,Product,Cart, Report, productImage,ProductReview

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
     list_display = ['id','user','name','locality','hometown','zipcode','contact','state']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','product_info','quantity','payment_status','razor_pay_order_id']
    
    def product_info(self,obj):
        link = reverse("admin:myapp_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.name)

@admin.register(Report)
class reportAdmin(admin.ModelAdmin):
    list_display = ['id','user','email','problem','date_reported']    

@admin.register(OrderPlaced)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer_id','customer_info','product_id','product_info','quantity','date_ordered','payment_status','razor_pay_order_id','razor_pay_payment_id','razor_pay_payment_signature']    

    def customer_info(self,obj):
        link = reverse("admin:myapp_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def product_info(self,obj):
        link = reverse("admin:myapp_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.name)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','stars','content','product_info','date_added']

    def product_info(self,obj):
        link = reverse("admin:myapp_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.name)

class productImageAdmin(admin.StackedInline):
    model = productImage
    # list_display = ['id','product','images']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','images','brand','category','price','discounted_price','discount_percentage','get_rating','delivery_time','availability']
    inlines = [
            productImageAdmin,
        ]

admin.site.register(productImage)
admin.site.register(Product, ProductAdmin)