from django.contrib import admin

# Register your models here.
from .models import People, Product,Contact,Orders,OrderUpdate
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(People)
