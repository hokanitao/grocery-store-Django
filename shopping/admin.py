from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product
from .models import Basket
from .models import BasketItem

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)  # 既存の UserAdmin をいったん解除


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "is_staff", "display_groups")

    def display_groups(self, obj):
        return ", ".join(group.name for group in obj.groups.all())


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        # "quantity"
    )


class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "basket_status", "created_at")


# @admin.register(Basket)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_basket_status",
        "basket_user",
        "product_name",
        "product_price",
        "quantity",
        "created_at",
    )

    def basket_user(self, obj):
        return obj.basket.user

    @admin.display(description="Basket Status")  # admin pageでの表示名指定
    def get_basket_status(self, obj):
        return obj.basket.get_basket_status_display()

    def product_name(self, obj):
        return obj.product.name

    def product_price(self, obj):
        return obj.product.price


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketItem, BasketItemAdmin)
# admin.site.register(Group)
