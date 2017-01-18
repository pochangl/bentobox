from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Order


# 訂單管理頁面
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "resNo", "ribsBox", "vegetarianBox", "vat") # 後台管理顥示的欄位


admin.site.register(Order, OrderAdmin) # 註冊管理頁面
