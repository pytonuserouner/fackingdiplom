from django.db.models import Avg
from rest_framework import serializers

from .models import Order, ImageCategory, Category, Tags, SpecificationOfProduct, Reviews, ProductImage, Product, \
    MyProfile, AvatarUser


class OrdersSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField(method_name="get_createdAt")
    fullName = serializers.SerializerMethodField(method_name="get_fullName")
    email = serializers.SerializerMethodField(method_name="get_email")
    phone = serializers.SerializerMethodField(method_name="get_phone")
    deliveryType = serializers.SerializerMethodField(method_name="get_deliveryType")
    paymentType = serializers.SerializerMethodField(method_name="get_paymentType")
    totalCost = serializers.SerializerMethodField(method_name="get_totalCost")

    class Meta:
        model = Order
        fields = (
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
        )

    def get_createdAt(self, obj):
        return obj.created_at

    def get_fullName(self, obj):
        return obj.user.profile.fullName

    def get_email(self, obj):
        return obj.user.profile.email

    def get_phone(self, obj):
        return str(obj.user.profile.phone)

    def get_deliveryType(self, obj):
        return obj.delivery_type

    def get_paymentType(self, obj):
        return obj.payment_type

    def get_totalCost(self, obj):
        return obj.total_cost


class CategoryImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = ImageCategory
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class CategoriesSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name="get_image")
    subcategories = serializers.SerializerMethodField(method_name="get_subcategories")

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "image",
            "subcategories",
        )

    def get_subcategories(self, obj):
        subcategories = [
            {
                "id": subcategory.id,
                "title": subcategory.title,
                "image": {
                    "src": (subcategory.image.url or ""),
                    "alt": subcategory.title,
                },
            }
            for subcategory in obj.subcategories.all()
        ]
        return subcategories

    def get_image(self, obj):
        return {"src": (obj.image.url or ""), "alt": obj.title}


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["name"]


class SpecificationOfProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOfProduct
        fields = ["name", "value"]


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            "author",
            "email",
            "text",
            "rate",
            "date",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField(method_name="get_scr")

    class Meta:
        model = ProductImage
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src



# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ["category", "price", "count", "date", "title", "description", "fullDescription", "freeDelivery", "images", "tags", "reviews", "specifications", "rating", "popular", "limited", "discount", "discount_price"]


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer()
    tags = TagsSerializer()
    reviews = ReviewsSerializer()
    rating = serializers.SerializerMethodField(method_name="get_rating")
    salePrice = serializers.SerializerMethodField(method_name="get_sale_price")
    fullDescription = serializers.SerializerMethodField(
        method_name="get_full_description"
    )
    specifications = SpecificationOfProductSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "salePrice",
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
        )
        extra_kwargs = {
            "freeDelivery": {"source": "free_delivery"},
            "description": {"source": "short_description"},
            "count": {"source": "quantity"},
        }

    def get_sale_price(self, obj):
        if not obj.discount:
            return None
        return round(obj.price - obj.price / 100 * obj.discount, 2)

    def get_full_description(self, obj):
        return obj.full_description

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(rating=Avg("rate"))
        return avg_rating["rating"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer()
    tags = serializers.SerializerMethodField(method_name="get_tags")
    reviews = serializers.SerializerMethodField(method_name="get_reviews")
    rating = serializers.SerializerMethodField(method_name="get_rating")
    salePrice = serializers.SerializerMethodField(method_name="get_sale_price")

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "salePrice",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )
        extra_kwargs = {
            "freeDelivery": {"source": "free_delivery"},
            "description": {"source": "short_description"},
            "count": {"source": "quantity"},
        }

    def get_tags(self, obj):
        tags = [
            {
                "id": tag.id,
                "name": tag.name,
            }
            for tag in obj.tags.all()
        ]
        return tags

    def get_reviews(self, obj):
        if not obj.reviews:
            return 0
        reviews = obj.reviews.count()
        return reviews

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(rating=Avg("rate"))
        return avg_rating["rating"]

    def get_sale_price(self, obj):
        if not obj.discount:
            return None
        return round(obj.price - obj.price / 100 * obj.discount, 2)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        fields = ["user", "fullName", "email", "phone", "balance", "avatar"]


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = AvatarUser
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = MyProfile
        fields = [
            "fullName",
            "email",
            "phone",
            "avatar",
        ]






