from django import forms
from .models import Product


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,  # required=Trueは必須にする
        label="Enter Username",
        widget=forms.TextInput(  # HTML input type="text"
            attrs={
                "class": "form-control",  # HTML classに該当
                "name": "username",  # HTML nameに該当
                "placeholder": "Enter Username",  # HTML placeholderに該当
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="Enter Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password",
                "placeholder": "Enter Password",
            }
        ),
    )


class AddProductForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        label="Enter Product Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "name",
                "placeholder": "(e.g. apple)",
            }
        ),
    )
    price = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=True,
        label="Enter Product Price",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "(e.g. 10.99)",
                "min": "0",  # 最小値を0にしてマイナスの入力を防ぐ
                "step": "0.01",  # 0.01刻みで調整（小数点第2位まで）
            }
        ),
    )
