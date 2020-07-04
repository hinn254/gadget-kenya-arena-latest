from django.db import models
from django.conf import  settings
from django. shortcuts import reverse
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('OP','Oppo'),
    ('NO','Nokia'),
    ('SM','Samsung'),
    ('TC','Tecno'),
    ('ON','Oneplus'),
    ('VI','Vivo'),
    ('RM','RealMe'),
    ('VI','Vivo'),
    ('IN','Infinix'),
    ('HU','Huawei'),
    ('HT','Htc'),
    ('IP','iPhone'),
    ('RE','Redmi'),
    ('TA','Tablet'),
    ('CO','Computer'),
    ('AC','Accessory'),

)
LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),

)

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    RAM = models.CharField(max_length=100)
    Internal_storage = models.CharField(max_length=100)
    battery_capacity = models.CharField(max_length=100)
    primary_camera = models.CharField(max_length=100)
    front_camera = models.CharField(max_length=100)
    network_type = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    screen_size = models.CharField(max_length=100)
    sim_card_slots = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'slug':self.slug})

    def get_add_to_cart(self):
        return reverse('core:add_to_cart', kwargs={'slug':self.slug})
       
    def get_remove_from_cart(self):
        return reverse('core:remove_from_cart', kwargs={'slug':self.slug})
       

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
      
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


    def __str__(self):
        return self.user.username


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email_address = models.EmailField()
    country = CountryField(multiple=False)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username

