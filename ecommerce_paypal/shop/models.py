from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = 'shop/images')

    def __str__(self) -> str:
        return self.category
        
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    message = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)   
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=15)
    phone = models.IntegerField()


    def __str__(self) -> str:
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=100)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.update_desc[0:7] + "..." 