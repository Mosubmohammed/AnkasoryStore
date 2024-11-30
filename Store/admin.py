from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

#mix profile info with user info
class ProfileInline(admin.StackedInline):
    model = Profile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields=["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    
#unregister theold way
admin.site.unregister(User)

admin.site.register(User,UserAdmin)