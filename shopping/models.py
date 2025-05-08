from django.db import models
from django.contrib.auth.models import User  # for borrower userテーブルから取得


class Product(models.Model):
    name = models.CharField(
        max_length=100, unique=True, help_text="Enter a product name."
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # store numbers with up to 2 digits after the decimal point.
    # quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Product: {self.name} Price: {self.price}"


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="baskets",  # related_nameで逆参照可能、views userinfo>historyで使用
    )
    BASKET_STATUS = (
        ("sho", "Shopping"),  # 買い物中
        ("pen", "Pending"),  # 購入申請後、staffの承認待ち
        ("con", "Confirmed"),  # staff承認済み
        ("can", "Canceled"),  # キャンセルされた状態
    )
    basket_status = models.CharField(
        max_length=3,
        choices=BASKET_STATUS,
        default="sho",
        help_text="Shopping Basket Status",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.basket_status} {self.created_at}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.basket} {self.product} {self.quantity}"

    @property  # これを書いておくと呼び出すときに()をつけなくていい、item.total_price と書ける
    def total_price(self):
        return self.product.price * self.quantity
