from django.conf import settings

from .models import Product


class Cart(object):
    """Объект корзины в сессии"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            product_id = str(product.id)
            cart[product_id]["product_id"] = product_id
            cart[product_id]["price"] = float(product.price)
            cart[product_id]["total_price"] = (
                cart[product_id]["price"] * cart[product_id]["count"]
            )

        sorted_cart = sorted(cart.values(), key=lambda item: item["product_id"])

        for item in sorted_cart:
            yield item

    def __len__(self):
        return sum(item["count"] for item in self.cart.values())

    def add(self, product, count=1, override_count=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"count": 0, "price": float(product.price)}
        if override_count:
            self.cart[product_id]["count"] = count
        else:
            self.cart[product_id]["count"] += count
        self.save()

    def remove(self, product, count=1):
        product_id = str(product.id)
        if product_id in self.cart:
            if count >= self.cart[product_id]["count"]:
                del self.cart[product_id]
            else:
                self.cart[product_id]["count"] -= count
            self.save()

    def get_total_price(self):
        return round(
            sum(float(item["price"]) * item["count"] for item in self.cart.values()), 2
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
