from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SendMail)
admin.site.register(TokenAmountModel)
admin.site.register(EmailFilteringModel)
admin.site.register(User)