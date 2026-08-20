from django.contrib import admin
from .models import Vendor
from .models import License
from .models import Product


# Register your models here.
admin.site.register(Vendor)    
admin.site.register(License)
admin.site.register(Product)
