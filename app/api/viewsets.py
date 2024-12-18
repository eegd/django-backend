from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.api.models import ShoppingItem
from app.api.serializers import ShoppingItemSerializer


class ShoppingItemViewSet(ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    # renderer_classes = [JSONRenderer]

    @action(detail=False, methods=["Delete"], url_path="delete-all-purchased", url_name="delete-all-purchased")
    def delete_purchased(self, request):
        ShoppingItem.objects.filter(purchased=True).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["PATCH"], url_path="mark-bulk-purchased", url_name="mark-bulk-purchased")
    def mark_bulk_purchased(self, request):
        try:
            queryset = ShoppingItem.objects.filter(id__in=request.data["shopping_items"])
            queryset.update(purchased=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
