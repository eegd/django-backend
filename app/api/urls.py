from django.urls import include, path
# from rest_framework import routers

from app.api.views import (
    ListAddShoppingItem,
    ListAddShoppingList,
    ShoppingItemDetail,
    ShoppingListDetail,
)
# from app.api.viewsets import ShoppingItemViewSet


# router = routers.DefaultRouter()
# router.register("shopping-items", ShoppingItemViewSet, basename="shopping-items")

# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest-framework")),
    path("shopping-lists/", ListAddShoppingList.as_view(), name="all-shopping-lists"),
    path("shopping-lists/<uuid:pk>/", ShoppingListDetail.as_view(), name="shopping-list-detail"),
    path("shopping-lists/<uuid:pk>/shopping-items/", ListAddShoppingItem.as_view(), name="list-add-shopping-item"),
    path("shopping-lists/<uuid:pk>/shopping-items/<uuid:item_pk>/", ShoppingItemDetail.as_view(), name="shopping-item-detail"),
]
