import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from app.models import ShoppingItem, ShoppingList


@pytest.fixture(scope="session")
def create_shopping_list():
    def _create_shopping_list(name, user):
        shopping_list = ShoppingList.objects.create(name=name)
        shopping_list.members.add(user)

        return shopping_list

    return _create_shopping_list


@pytest.fixture(scope="session")
def create_shopping_item():
    def _create_shopping_item(list_name, item_name, user):
        shopping_list = ShoppingList.objects.create(name=list_name)
        shopping_list.members.add(user)
        shopping_item = ShoppingItem.objects.create(name=item_name, purchased=False, shopping_list=shopping_list)

        return shopping_item

    return _create_shopping_item


@pytest.fixture(scope="session")
def create_user():
    def _create_user(username="user"):
        return User.objects.create_user(username=username)

    return _create_user


@pytest.fixture(scope="session")
def create_authenticated_client():
    def _create_authenticated_client(user):
        client = APIClient()
        client.force_login(user)

        return client

    return _create_authenticated_client
