from django.template import loader
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import *
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Product add成功時のメッセージ表示用
from django.contrib import messages


# ログインユーザの買い物かごの状態を取得(複数回使う共通処理)
def get_user_basket(user):
    basket = Basket.objects.filter(user=user, basket_status="sho").first()
    return basket


def get_user_basket1(user, status):
    basket = Basket.objects.filter(user=user, basket_status=status)
    return basket


def loginView(request):
    form = LoginForm()  # 空のformインスタンスを作成（クラスを呼ぶ）forms.py内にある
    msg = False
    if request.method == "POST":  # request methodがpostであれば
        form = LoginForm(request.POST)  # POSTに含まれるrequest infoを代入
        if form.is_valid():
            # builtinメソッド、空白じゃないかとか文字制限を超えていないか
            user = authenticate(
                # Django組込み関数、username,pw使ってユーザーが存在してるかを確認
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:  # 認証OKなら(userがNoneでなかったら)
                login(request, user)  # built-in function
                if user.groups.filter(name="Staff").exists():
                    # user groupでstaffに属していたらstaffページへ遷移
                    response = redirect("/staffpage")
                elif user.groups.filter(name="Customer").exists():
                    response = redirect("/mypage")
                return response
            else:
                msg = {"code": "danger", "lbl": "Failed Authentication!"}
    context = {"form": form, "msg": msg}
    return render(request, "registration/login.html", context)


def LogoutView(reqest):
    logout(reqest)
    return redirect("/login")


# ---- For Customer ------
def mypage(request):
    basket = get_user_basket(request.user)  # defined line 10
    if not basket:
        context = {}
        # passing an empty dictionary (if none item exist in the shopping cart.)
    else:
        all_items = basket.items.all()
        # 最初に取ってきたitems＋models.py>related_name="items"＋全取得
        total = sum(item.total_price for item in all_items)
        # models.py>BasketItem def total_price
        context = {
            "basket": basket,
            "items": all_items,
            "total": total,
            "created_at": basket.created_at,
        }
    return render(request, "mypage.html", context)


def get_items(baskets):
    result = []
    for basket in baskets:
        all_items = basket.items.all()
        # 最初に取ってきたitems＋models.py>related_name="items"＋全取得
        total = sum(item.total_price for item in all_items)
        # models.py>BasketItem def total_price
        result.append(
            {
                "basket": basket,
                "items": all_items,
                "total": total,
                "created_at": basket.created_at,
            }
        )
    return result


def history(request):
    basket_pending = get_user_basket1(request.user, "pen")
    basket_confirm = get_user_basket1(request.user, "con")
    basket_cancel = get_user_basket1(request.user, "can")

    if basket_pending:
        baskets_pending = get_items(basket_pending)
    else:
        baskets_pending = None
    if basket_confirm:
        baskets_confirm = get_items(basket_confirm)
    else:
        baskets_confirm = None
    if basket_cancel:
        baskets_cancel = get_items(basket_cancel)
    else:
        baskets_cancel = None
    context = {
        "baskets_pending": baskets_pending,
        "baskets_confirm": baskets_confirm,
        "baskets_cancel": baskets_cancel,
    }
    return render(request, "history.html", context)


def buy(request, pk):
    basket = Basket.objects.get(pk=pk)
    basket.basket_status = "pen"
    basket.save()
    return redirect("/mypage")


def productsList(request):
    is_customer = request.user.groups.filter(name="Customer").exists()
    products = Product.objects.all()
    num_products = Product.objects.all().count()
    context = {
        "id": id,
        "products": products,
        "num_products": num_products,
        "is_customer": is_customer,
    }
    return render(request, "product_list.html", context)


def added(request):
    basket = get_user_basket(request.user)  # defined line 10
    product_id = request.GET.get("product_id")  # htmlから送られてきたidを取得
    product = Product.objects.get(id=product_id)
    # getでidが一致するもの1件だけ取れる、filterはQuerySet（複数件）を返す

    if not basket:  # 買い物カゴが存在しなければ作成
        basket = Basket.objects.create(user=request.user, basket_status="sho")
        basket.save()

        print("Basket:", basket)
        print("Items:", basket.items.all())

    try:
        # カゴが存在していれば選択された商品がカゴにあるかをチェック
        basket_item = BasketItem.objects.get(basket=basket, product=product)
        # getを使うと1件のobjectしか受け取れない（上のproductでfilterを使うとNGになる
        basket_item.quantity += 1
        basket_item.save()
    except BasketItem.DoesNotExist:
        BasketItem.objects.create(basket=basket, product=product, quantity=1)
    return redirect("mypage")
    # 商品を追加したらmypageの一覧に飛ぶ


# ---- For Staff ------
# staffpageでのpending order/confirm/cancelで使う共通処理
def get_pending_orders():
    baskets = Basket.objects.filter(basket_status="pen")
    if baskets.exists():
        first_basket = baskets.first()
        all_items = first_basket.items.all()
        # 最初に取ってきたitems＋models.py>related_name="items"＋全取得
        total = sum(item.total_price for item in all_items)
        # models.py>BasketItem def total_price
        created_at = first_basket.created_at
    else:
        all_items = []
        total = 0
        created_at = None

    context = {
        "baskets": baskets,
        "items": all_items,
        "total": total,
        "created_at": created_at,
    }
    return context


def staffpage(request):
    # Add/Update Products
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            # builtinメソッド、空白じゃないかとか文字制限を超えていないか
            name = form.cleaned_data["name"].lower()
            price = form.cleaned_data["price"]

            if Product.objects.filter(name=name).exists():
                Product.objects.filter(name=name).update(price=price)
                messages.success(request, f"{name} price was updated. : ${price}")
                # product nameが存在していたらname入力欄にエラーを表示
            else:
                product = Product.objects.create(name=name, price=price)
                messages.success(request, f"{name} was successfully added.")
            return redirect("staffpage")

    # Pending orders
    context = get_pending_orders()
    context["form"] = form  # context_dictにformからの内容を追加

    # User一覧の取得
    users = User.objects.all()
    print(users)
    context["users"] = users  # context_dictにuser情報追加
    return render(request, "staffpage.html", context)


def basketDetail(request, pk):
    basket = Basket.objects.get(pk=pk)
    all_items = basket.items.all()
    # 最初に取ってきたitems＋models.py>related_name="items"＋全取得
    total = sum(item.total_price for item in all_items)
    # models.py>BasketItem def total_price
    created_at = basket.created_at
    context = {
        "basket": basket,
        "total": total,
        "created_at": created_at,
    }
    return render(request, "basket_detail.html", context)


def confirm(request, pk):
    basket = Basket.objects.get(pk=pk)
    basket.basket_status = "con"
    basket.save()
    return redirect("staffpage")


def cancel(request, pk):
    basket = Basket.objects.get(pk=pk)
    basket.basket_status = "can"
    basket.save()
    return redirect("staffpage")


def userinfo(request, pk):
    user = User.objects.filter(pk=pk).first()
    history = user.baskets.all()
    # models>Basket>userにあるrelated_nameで逆参照、statusに関わらず全取得

    history_data = []
    for basket in history:
        items = basket.items.all()
        basket_total = sum(item.total_price for item in items)
        history_data.append(
            {
                "basket": basket,
                "items": items,
                "total": basket_total,
                "basket_status": basket.basket_status,
                "created_at": basket.created_at,
            }
        )

    context = {
        "user": user,
        "history_data": history_data,
        "overall_total": sum(b["total"] for b in history_data),
    }
    return render(request, "userinfo.html", context)
