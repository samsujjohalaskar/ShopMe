from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

# Create your models here.
state_choices = (
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh ", "Arunachal Pradesh "),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu and Kashmir ", "Jammu and Kashmir "),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),
    ("Lakshadweep", "Lakshadweep"),
    ("Delhi", "Delhi"),
    ("Puducherry", "Puducherry")
)

category_choices = (
    ('Clothing','Clothing'),
    ('Electronics','Electronics'),
    ('Food','Food'),
    ('Grocery','Grocery'),
    ('Stationary','Stationary'),
    ('Footwear','Footwear'),
)
    
class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=state_choices, max_length=50)

    def __str__(self):
        return str(self.id)
        
class Product(models.Model):
    name = models.CharField(max_length=100)
    # images = models.ImageField(upload_to='product')
    price = models.FloatField()
    brand = models.CharField(max_length=50)
    category = models.CharField(choices=category_choices,max_length=20)
    discounted_price = models.FloatField()
    discount_percentage = models.FloatField()
    delivery_time = models.DateField()
    availability = models.CharField(max_length=20)

    @property
    def discount_percentage(self):
        dp = ((self.price-self.discounted_price)/self.price)*100
        return ("%.1f" % dp)

     
    def __str__(self):
        return str(self.id)
     
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() == 0:
            return (1.5+2)
        else:
            return total/self.reviews.count()
    


class productImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos',default="")
    images = models.ImageField(upload_to ='product',default="")

    # resizing the image, you can change parameters like size and quality.
    # def save(self, *args, **kwargs):
    #    super(productImage, self).save(*args, **kwargs)
    #    img = Image.open(self.images.path)
    #    if img.height > 1125 or img.width > 1125:
    #        img.thumbnail((1125,1125))
    #    img.save(self.images.path,quality=70,optimize=True)

    def __str__(self):
        return str(self.product)

class ProductReview(models.Model):
    product = models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    content = models.TextField()
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
        

class Filter(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=state_choices, max_length=50)

    def __str__(self):
        return str(self.id)