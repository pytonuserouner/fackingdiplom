from django.contrib import admin

from .models import Order, MyProfile, AvatarUser, Reviews, Tags, Category, ImageCategory, Product, ProductImage, \
    SpecificationOfProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "createdAt",
        "fullName",
        "email",
        "phone",
        "deliveryType",
        "paymentType",
        "totalCost",
        "status",
        "city",
        "address",
        "products",
    ]


@admin.register(SpecificationOfProduct)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]

    class Meta:
        verbose_name = "Спецификация"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "category",
        "price",
        "count",
        "date",
        "title",
        "description",
        "fullDescription",
        "freeDelivery",
        "images",
        "tags",
        "reviews",
        "specifications",
        "rating",
    ]


@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author",)


@admin.register(AvatarUser)
class AvatarUserAdmin(admin.ModelAdmin):
    list_display = [
        "src",
        "alt",
    ]


@admin.register(MyProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "fullName",
        "email",
        "phone",
        "balance",
        "avatar",
    ]




