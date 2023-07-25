from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.
def profile_avatar_directory_path(instance: "MyProfile", filename: str) -> str:
    return f"uploads/avatar_{instance.pk}/{filename}"


class AvatarUser(models.Model):
    """Model of Avatar for user profile"""

    src = models.ImageField(
        blank=True,
        null=True,
        upload_to=profile_avatar_directory_path,
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))
        ],
        verbose_name="someone",
    )
    alt = models.CharField(
        blank=True, max_length=500, verbose_name="someone else"
    )


class MyProfile(models.Model):
    """Model of profile of user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(blank=True, max_length=200, verbose_name="полное имя")
    email = models.CharField(
        blank=True, max_length=200, verbose_name="электронная почта"
    )
    phone = models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name="Номер телефона")
    balance = models.DecimalField(
        decimal_places=2, max_digits=12, verbose_name="баланс", default=0, blank=True
    )
    avatar = models.ForeignKey(
        AvatarUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )


class SpecificationOfProduct(models.Model):
    """Model of specifications for products"""

    name = models.CharField(max_length=128, verbose_name="size", blank=True)
    value = models.CharField(max_length=128, verbose_name="value", blank=True)


def category_image_directory_path(instance: "Category", filename: str) -> str:
    return f"categories/category_{instance.pk}/image/{filename}"


class ImageCategory(models.Model):
    src = models.ImageField(
        blank=True,
        upload_to=category_image_directory_path,
        verbose_name="изображение категории",
    )
    alt = models.CharField(
        max_length=255, blank=True, verbose_name="альтернатива картинке"
    )


class CategoryProduct(models.Model):
    title = models.TextField(max_length=50, verbose_name="название категории")
    image = models.FileField(blank=True, null=True, upload_to="uploads/")
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="название категории")
    image = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, blank=True)
    subcategory = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        blank=True,
        related_name="subcategories",
        null=True,
    )


class Tags(models.Model):
    name = models.CharField(blank=True, max_length=255, verbose_name="тег")


class Product(models.Model):
    """Model of all products"""

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="категория"
    )
    price = models.DecimalField(decimal_places=2, max_digits=12, verbose_name="цена")
    count = models.IntegerField(verbose_name="количество", default=0)
    date = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="дата создания"
    )
    title = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="название"
    )
    description = models.TextField(blank=True, max_length=2000, verbose_name="описание")
    fullDescription = models.TextField(
        blank=True, max_length=2000, verbose_name="описание"
    )
    freeDelivery = models.BooleanField(
        blank=True, default=False, verbose_name="бесплатная доставка?"
    )
    images = models.ForeignKey(
        "ProductImage",
        on_delete=models.CASCADE,
        verbose_name="изображения продукта",
        blank=True,
    )
    tags = models.ForeignKey(
        "Tags", on_delete=models.PROTECT, verbose_name="тэги", blank=True
    )
    reviews = models.IntegerField(blank=True, verbose_name="количество обзоров")
    specifications = models.ForeignKey(
        SpecificationOfProduct,
        on_delete=models.PROTECT,
        verbose_name="спецификация",
        default=None,
        blank=True,
    )
    rating = models.FloatField(blank=True, verbose_name="средний рейтинг")
    popular = models.BooleanField(
        blank=True, default=False, verbose_name="популярный продукт"
    )
    limited = models.BooleanField(
        blank=True, default=False, verbose_name="осталось мало"
    )
    discount = models.IntegerField(blank=True, default=None, verbose_name="скидка")
    discount_price = models.DecimalField(
        blank=True,
        decimal_places=2,
        max_digits=12,
        default=None,
        verbose_name="цена со скидкой",
    )


def product_image_directory_path(instance: "Product", filename: str) -> str:
    """function for create path and save items of products images"""

    return f"products/product_{instance.pk}/image/{filename}"


class ProductImage(models.Model):
    """Model of products images"""

    src = models.ImageField(
        blank=True,
        upload_to=product_image_directory_path,
        verbose_name="изображение продукта",
    )
    alt = models.CharField(
        blank=True, max_length=666, verbose_name="альтернатива картинке"
    )


class Reviews(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="название продукта",
    )
    author = models.CharField(blank=True, max_length=255, verbose_name="автор")
    email = models.CharField(
        blank=True, max_length=255, verbose_name="электронная почта"
    )
    text = models.TextField(blank=True, max_length=4096, verbose_name="текст обзора")
    rate = models.TextField(blank=True, max_length=4096, verbose_name="оценка")
    date = models.DateTimeField(
        blank=True, auto_now_add=True, max_length=4096, verbose_name="дата"
    )


class Discount(models.Model):
    discount = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="скидка"
    )


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("free", "free delivery"),
        ("express", "paid delivery"),
    ]
    PAYMENT_CHOICES = [("online", "online payment"), ("offline", "offline payment")]
    STATUS_CHOICES = [
        ("accepted", "accepted order"),
        ("rejected", "rejected order"),
        ("delivery", "order on delivery"),
        ("delivered", "order is already delivered"),
    ]

    createdAt = models.DateTimeField(blank=True, verbose_name="дата")
    fullName = models.CharField(blank=True, max_length=255, verbose_name="полное имя")
    email = models.CharField(
        blank=True, max_length=255, verbose_name="электронная почта"
    )
    phone = models.CharField(blank=True, max_length=255, verbose_name="телефон")
    deliveryType = models.CharField(
        blank=True, max_length=255, verbose_name="тип доставки"
    )
    paymentType = models.CharField(
        blank=True, max_length=255, verbose_name="тип оплаты"
    )
    totalCost = models.DecimalField(
        blank=True, decimal_places=2, max_digits=11, verbose_name="общая сумма"
    )
    status = models.CharField(blank=True, max_length=255, verbose_name="статус")
    city = models.CharField(blank=True, max_length=255, verbose_name="город")
    address = models.CharField(blank=True, max_length=255, verbose_name="адрес")
    products = models.JSONField(verbose_name="продукты", blank=True)
    # user = models.ForeignKey(
    #     MyProfile, on_delete=models.PROTECT, related_name="заказы", default=None
    # )

    def __str__(self):
        return f"Order: {self.id}"








