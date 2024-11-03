from typing import List

from rest_framework import serializers

from app.api.models import ShoppingItem, ShoppingList, User


class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ["members"]

    def update(self, instance, validated_data):
        for member in validated_data["members"]:
            instance.members.add(member)
            instance.save()

        return instance


class RemoveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ["members"]

    def update(self, instance, validated_data):
        for member in validated_data["members"]:
            instance.members.remove(member)
            instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = ["id", "name", "purchased", "shopping_list"]
        read_only_fields = ["id", "shopping_list"]

    def create(self, validated_data, **kwargs):
        shopping_list_id = self.context["request"].parser_context["kwargs"]["pk"]

        try:
            shopping_list = ShoppingList.objects.get(id=shopping_list_id)
        except:
            raise serializers.ValidationError("The specified shopping list does not exist")

        if shopping_list.shopping_items.filter(name=validated_data["name"], purchased=False):  # type: ignore
            raise serializers.ValidationError("There's already this item on the list")

        validated_data["shopping_list_id"] = shopping_list_id
        return super().create(validated_data)


class ShoppingListSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    unpurchased_items = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = ["id", "name", "unpurchased_items", "members"]

    def get_unpurchased_items(self, obj) -> List:
        return [{"name": shopping_item.name} for shopping_item in obj.shopping_items.filter(purchased=False)]
