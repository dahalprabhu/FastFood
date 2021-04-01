from django.contrib import admin
from .models import Resturants
from .models import FoodItems
from .models import Order
from .models import OrderItem
from .models import ShippingAddress
from .models import Customer




# Register your models here.

admin.site.register(Resturants)
admin.site.register(FoodItems)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Customer)




