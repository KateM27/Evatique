from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return(f"{self.firstName} {self.lastName}")
    
    def saveCust(self):
        self.save()

    def getCustByEmail(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def custExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

    def getCategories():
        return Category.objects.all()


class Product(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images')

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    # def makeOrder(self):
    #     self.save()

    def calculate_total(self):
        self.total = sum(product.subtotal() for product in self.products.all())