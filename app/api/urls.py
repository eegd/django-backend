from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from app.api.views import (
    ListAddShoppingItem,
    ListAddShoppingList,
    ShoppingItemDetail,
    ShoppingListAddMembers,
    ShoppingListDetail,
    ShoppingListRemoveMembers,
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest-framework")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("shopping-lists/", ListAddShoppingList.as_view(), name="all-shopping-lists"),
    path("shopping-lists/<uuid:pk>/", ShoppingListDetail.as_view(), name="shopping-list-detail"),
    path('shopping-lists/<uuid:pk>/add-members/', ShoppingListAddMembers.as_view(), name="shopping-list-add-members"),
    path("shopping-lists/<uuid:pk>/remove-members/", ShoppingListRemoveMembers.as_view(), name="shopping-list-remove-members"),
    path("shopping-lists/<uuid:pk>/shopping-items/", ListAddShoppingItem.as_view(), name="list-add-shopping-item"),
    path("shopping-lists/<uuid:pk>/shopping-items/<uuid:item_pk>/", ShoppingItemDetail.as_view(), name="shopping-item-detail"),
]
