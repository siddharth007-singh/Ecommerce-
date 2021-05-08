from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.brand_name


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="product/")
    price = models.FloatField()
    discount_price = models.FloatField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    od_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)  # shows that this ort already ordered or not
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.qty} of {self.item.title}"

    def total_price(self):
        return self.qty * self.item.price

    def total_discount_price(self):
        return self.qty * self.item.discount_price

    def final_price(self):
        if self.item.discount_price:
            return self.total_discount_price()
        else:
            return self.total_price()

    def total_saving(self):
        return self.total_price() - self.total_discount_price()


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    pincode = models.IntegerField()
    locality = models.CharField(max_length=200)
    CITY_CHOICES = (("PUR", "Purnea"), ("PAT", "Patna"), ("BHGA", "Bhagalpur"), ("KTR", "Katihar"))
    city = models.CharField(max_length=10, choices=CITY_CHOICES)
    state = models.CharField(max_length=20)
    alt_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Cupon(models.Model):
    cupon_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=200, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    coupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    def get_total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        return total

    def get_total_saving(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_saving()

        return total

    def get_actual_total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price()

        return total