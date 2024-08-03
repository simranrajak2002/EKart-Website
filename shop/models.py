from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    subcategory=models.CharField(max_length=50)
    desc=models.CharField(max_length=200)
    price=models.IntegerField(default=0)
    pub_date=models.DateField(default='2020-08-23')
    image=models.ImageField(upload_to="shop/images")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.IntegerField(max_length=50)
    desc=models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    firstname = models.CharField(max_length=90)
    lastname = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    address2 = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111)
    payment=models.CharField(max_length=50)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id) + " " + self.update_desc[0:10]

class People(models.Model):
    email=models.CharField(max_length=3000)
    password=models.CharField(max_length=2000)
