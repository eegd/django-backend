from django.urls import path, include
from rest_framework import routers

from shopping_list.api.views import (
    AddShoppingItem,
    ListAddShoppingList,
    ShoppingItemDetail,
    ShoppingListDetail,
)

# from shopping_list.api.viewsets import ShoppingItemViewSet


# router = routers.DefaultRouter()
# router.register("shopping-items", ShoppingItemViewSet, basename="shopping-items")

# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("shopping-lists/", ListAddShoppingList.as_view(), name="all-shopping-lists"),
    path("shopping-lists/<uuid:pk>/", ShoppingListDetail.as_view(), name="shopping-list-detail"),
    path("shopping-lists/<uuid:pk>/shopping-items/", AddShoppingItem.as_view(), name="add-shopping-item"),
    path("shopping-lists/<uuid:pk>/shopping-items/<uuid:item_pk>/", ShoppingItemDetail.as_view(), name="shopping-item-detail"),
]
