# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(MovieCategory)
admin.site.register(Movie)
admin.site.register(MovieDateTime)
admin.site.register(Seat)
admin.site.register(Cart)
admin.site.register(CartItems)