from rest_framework import generics, status
from rest_framework.response import Response

from app.api.permission import (
    AllShoppingItemsShoppingListMembersOnly,
    ShoppingItemShoppingListMembersOnly,
    ShoppingListMembersOnly
)

from app.api.models import ShoppingItem, ShoppingList
from app.api.serializers import AddMemberSerializer, RemoveMemberSerializer, ShoppingItemSerializer, ShoppingListSerializer
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


class ShoppingListAddMembers(generics.UpdateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = AddMemberSerializer
    permission_classes = [ShoppingListMembersOnly]

    def update(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        serializer = self.get_serializer(shopping_list, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [ShoppingListMembersOnly]


class ShoppingListRemoveMembers(generics.UpdateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = RemoveMemberSerializer
    permission_classes = [ShoppingListMembersOnly]

    def update(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        serializer = self.get_serializer(shopping_list, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
