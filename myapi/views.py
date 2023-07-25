from myapi.cart import Cart
from myapi.serializers import CategoriesSerializer, ProductSerializer, TagsSerializer, ProductDetailSerializer, \
    ReviewsSerializer, ProfileSerializer, AvatarSerializer, OrdersSerializer
from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, permissions, response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product as prod, Category, Product, Tags, Reviews, MyProfile, AvatarUser

User = get_user_model()


def banners(request):
    data = [
        {
            "id": prod.objects.get(id="pk"),  # "123",
            "category": prod.objects.get("category"),  # 55,
            "price": prod.objects.get("price"),  # 500.67,
            "count": prod.objects.get("count"),  # 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": prod.objects.get("title"),  # "video card",
            "description": prod.objects.get("description"),
            "freeDelivery": prod.objects.get("freeDelivery"),  # True,
            "images": [
                {
                    "src": prod.objects.get("scr"),
                    # "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": prod.objects.get("alt"),  # "any alt text",
                }
            ],
            "tags": [
                "string"
            ],
            "reviews": prod.objects.get("reviews"),  # 5,
            "rating": prod.objects.get("rating"),  # 4.6
        },
    ]
    return JsonResponse(data, safe=False)


def categories(request):
    data = [
        {
            "id": 123,
            "title": "video card",
            "image": {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
            },
            "subcategories": [
                {
                    "id": 123,
                    "title": "video card",
                    "image": {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "Image alt string"
                    }
                }
            ]
        }
    ]
    return JsonResponse(data, safe=False)


def catalog(request):
    data = {
        "items": [
            {
                "id": prod.objects.get(id="pk"),  # "123",
                "category": prod.objects.get("category"),  # 55,
                "price": prod.objects.get("price"),  # 500.67,
                "count": prod.objects.get("count"),  # 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": prod.objects.get("title"),  # "video card",
                "description": prod.objects.get("description"),
                "freeDelivery": prod.objects.get("freeDelivery"),  # True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ],
        "currentPage": randrange(1, 4),
        "lastPage": 3
    }
    return JsonResponse(data)


def productsPopular(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
            ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
    return JsonResponse(data, safe=False)


def productsLimited(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
            ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
    return JsonResponse(data, safe=False)


def sales(request):
    data = {
        'items': [
            {
                "id": 123,
                "price": 500.67,
                "salePrice": 200.67,
                "dateFrom": "05-08",
                "dateTo": "05-20",
                "title": "video card",
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
            }
        ],
        'currentPage': randrange(1, 4),
        'lastPage': 3,
    }
    return JsonResponse(data)


def basket(request):
    if (request.method == "GET"):
        print('[GET] /api1/basket/')
        data = [
            {
                "id": 123,
                "category": 55,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            },
            {
                "id": 124,
                "category": 55,
                "price": 201.675,
                "count": 5,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "POST"):
        body = json.loads(request.body)
        id = body['id']
        count = body['count']
        print('[POST] /api1/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 13,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "DELETE"):
        body = json.loads(request.body)
        id = body['id']
        print('[DELETE] /api1/basket/')
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 11,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
                ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)


def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


def signUp(request):
    user = User.objects.create_user("mir232", "lennon@thebeatles.com", "pass232")
    user.save()
    return HttpResponse(status=200)


def signOut(request):
    logout(request)
    return HttpResponse(status=200)


def product(request, id):
    data = {
        "id": 123,
        "category": 55,
        "price": 500.67,
        "count": 12,
        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        "title": "video card",
        "description": "description of the product",
        "fullDescription": "full description of the product",
        "freeDelivery": True,
        "images": [
            {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "hello alt",
            }
        ],
        "tags": [
            {
                "id": 0,
                "name": "Hello world"
            }
        ],
        "reviews": [
            {
                "author": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "text": "rewrewrwerewrwerwerewrwerwer",
                "rate": 4,
                "date": "2023-05-05 12:12"
            }
        ],
        "specifications": [
            {
                "name": "Size",
                "value": "XL"
            }
        ],
        "rating": 4.6
    }
    return JsonResponse(data)


def tags(request):
    data = [
        {"id": 0, "name": 'tag0'},
        {"id": 1, "name": 'tag1'},
        {"id": 2, "name": 'tag2'},
    ]
    return JsonResponse(data, safe=False)


def productReviews(request, id):
    data = [
        {
            "author": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "text": "rewrewrwerewrwerwerewrwerwer",
            "rate": 4,
            "date": "2023-05-05 12:12"
        },
        {
            "author": "2Annoying Orange",
            "email": "no-reply@mail.ru",
            "text": "rewrewrwerewrwerwerewrwerwer",
            "rate": 5,
            "date": "2023-05-05 12:12"
        },
    ]
    return JsonResponse(data, safe=False)


def profile(request):
    if (request.method == 'GET'):
        data = {
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "avatar": {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "hello alt",
            }
        }
        return JsonResponse(data)

    elif (request.method == 'POST'):
        data = {
            "fullName": "Annoying Green",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "avatar": {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "hello alt",
            }
        }
        return JsonResponse(data)

    return HttpResponse(status=500)


def profilePassword(request):
    return HttpResponse(status=200)


def orders(request):
    if (request.method == 'GET'):
        data = [
            {
                "id": 123,
                "createdAt": "2023-05-05 12:12",
                "fullName": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "phone": "88002000600",
                "deliveryType": "free",
                "paymentType": "online",
                "totalCost": 567.8,
                "status": "accepted",
                "city": "Moscow",
                "address": "red square 1",
                "products": [
                    {
                        "id": 123,
                        "category": 55,
                        "price": 500.67,
                        "count": 12,
                        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                        "title": "video card",
                        "description": "description of the product",
                        "freeDelivery": True,
                        "images": [
                            {
                                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                                "alt": "Image alt string"
                            }
                        ],
                        "tags": [
                            {
                                "id": 12,
                                "name": "Gaming"
                            }
                        ],
                        "reviews": 5,
                        "rating": 4.6
                    }
                ]
            },
            {
                "id": 123,
                "createdAt": "2023-05-05 12:12",
                "fullName": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "phone": "88002000600",
                "deliveryType": "free",
                "paymentType": "online",
                "totalCost": 567.8,
                "status": "accepted",
                "city": "Moscow",
                "address": "red square 1",
                "products": [
                    {
                        "id": 123,
                        "category": 55,
                        "price": 500.67,
                        "count": 12,
                        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                        "title": "video card",
                        "description": "description of the product",
                        "freeDelivery": True,
                        "images": [
                            {
                                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                                "alt": "Image alt string"
                            }
                        ],
                        "tags": [
                            {
                                "id": 12,
                                "name": "Gaming"
                            }
                        ],
                        "reviews": 5,
                        "rating": 4.6
                    }
                ]
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == 'POST'):
        data = {
            "orderId": 123,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)


def order(request, id):
    if (request.method == 'GET'):
        data = {
            "id": 123,
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
                {
                    "id": 123,
                    "category": 55,
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "freeDelivery": True,
                    "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "Image alt string"
                        }
                    ],
                    "tags": [
                        {
                            "id": 12,
                            "name": "Gaming"
                        }
                    ],
                    "reviews": 5,
                    "rating": 4.6
                },
            ]
        }
        return JsonResponse(data)

    elif (request.method == 'POST'):
        data = {"orderId": 123}
        return JsonResponse(data)

    return HttpResponse(status=500)


def payment(request, id):
    print('qweqwewqeqwe', id)
    return HttpResponse(status=200)


def avatar(request):
    if request.method == "POST":
        print(request.FILES["avatar"])
        return HttpResponse(status=200)


class CategoriesListApiView(ListAPIView):
    """Список категорий"""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class CatalogListApiView(ListAPIView):
    """Каталог"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.query_params:
            name = self.request.query_params.get("filter[name]")
            if name:
                queryset = queryset.filter(description__icontains=name)

            min_price = self.request.query_params.get("filter[minPrice]")
            if min_price:
                queryset = queryset.filter(description__icontains=min_price)

            max_price = self.request.query_params.get("filter[maxPrice]")
            if max_price:
                queryset = queryset.filter(description__icontains=max_price)

            free_delivery = self.request.query_params.get("filter[freeDelivery]")
            if free_delivery:
                queryset = queryset.filter(description__icontains=free_delivery)

            available = self.request.query_params.get("filter[available]")
            if available:
                queryset = queryset.filter(description__icontains=available)


class PopularListApiView(ListAPIView):
    """Список популярных товаров"""

    queryset = Product.objects.prefetch_related("popular")
    serializer_class = ProductSerializer


class LimitedProductsApiView(ListAPIView):
    """Список товаров, которых мало осталось"""

    queryset = Product.objects.prefetch_related("limited")[:5]
    serializer_class = ProductSerializer


class SalesListApiView(ListAPIView):
    """Список товаров со скидкой"""

    queryset = Product.objects.prefetch_related("discount").filter(discount__gt=0)
    serializer_class = ProductSerializer


class BannersListApiView(ListAPIView):
    """Товары для баннеров на главной"""

    queryset = Product.objects.all()[:5]
    serializer_class = ProductSerializer


class TagsListApiView(ListAPIView):
    "Список тэгов"
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class ProductApiView(RetrieveAPIView):
    """Подробное описание продукта"""

    serializer_class = ProductDetailSerializer
    queryset = Product.objects.prefetch_related("images").all()


class ReviewsProductApiView(APIView):
    """Список обзоров на продукты"""

    def post(self, request, pk, *args, **kwargs):
        serializer = ReviewsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            review = Reviews(
                product=Product.objects.get(id=pk),
                author=self.request.user,
                rate=serializer.data.get("rate"),
                text=serializer.data.get("text"),
            )
            review.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = MyProfile.objects.create(user=user, first_name=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sign_out(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = MyProfile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    def post(self, request):
        profile = MyProfile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = MyProfile.objects.get(user=request.user)

        if not profile.check_password(request.data["currentPassword"]):
            raise ValueError("reset password failed")
        else:
            profile.set_password(request.data["newPassword"])
            profile.save()
        return Response("success", status=status.HTTP_200_OK)


class AvatarProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        avatar_img = request.FILES["avatar"]
        profile = MyProfile.objects.get(user=request.user)
        if profile.avatar is None:
            profile.avatar = AvatarUser.objects.create(
                src="avatar_img", alt=f"avatar{profile.user.username}"
            )
            profile.save()
        else:
            profile.avatar.src = avatar_img
            profile.avatar.save()

        serializer = AvatarSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartAPIView(APIView):
    permission_classes = [AllowAny]
    """APIView для корзины, реализация методов get, post и delete"""

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_items.append(
                {
                    "id": product.id,
                    "category": product.category.id,
                    "price": float(item["price"]),
                    "count": item["quantity"],
                    "date": product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                    "title": product.title,
                    "description": product.short_description(),
                    "freeDelivery": product.free_delivery,
                    "images": [
                        {"src": image.image.url, "alt": product.title}
                        for image in product.images.all()
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": product.reviews_count(),
                    "rating": product.average_rating(),
                }
            )
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)


class OrdersListCreateApiView(ListCreateAPIView, CartAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer



