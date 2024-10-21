from rest_framework import generics

from app.api.permission import (
    AllShoppingItemsShoppingListMembersOnly,
    ShoppingItemShoppingListMembersOnly,
    ShoppingListMembersOnly
)

from app.api.models import ShoppingItem, ShoppingList
from app.api.serializers import ShoppingItemSerializer, ShoppingListSerializer
from utils.pagination import LargerResultsSetPagination


class ListAddShoppingList(generics.ListCreateAPIView):
    serializer_class = ShoppingListSerializer

    def perform_create(self, serializer):
        shopping_list = serializer.save()
        shopping_list.members.add(self.request.user)

        return shopping_list

    def get_queryset(self):
        members = self.request.user
        queryset = ShoppingList.objects.filter(members=members)

        return queryset


class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [ShoppingListMembersOnly]


class ListAddShoppingItem(generics.ListCreateAPIView):
    serializer_class = ShoppingItemSerializer
    permission_classes = [AllShoppingItemsShoppingListMembersOnly]
    pagination_class = LargerResultsSetPagination

    def get_queryset(self):
        shopping_list = self.kwargs["pk"]
        queryset = ShoppingItem.objects.filter(shopping_list=shopping_list).order_by("purchased")

        return queryset


class ShoppingItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [ShoppingItemShoppingListMembersOnly]
    lookup_url_kwarg = "item_pk"
