import pytest

from django.urls import reverse
from rest_framework import status

from app.models import ShoppingList


@pytest.mark.django_db
def test_valid_shopping_list_is_created(create_user, create_authenticated_client):
    client = create_authenticated_client(user=create_user())
    url = reverse("all-shopping-lists")
    data = {"name": "Groceries"}

    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.get().name == "Groceries"


@pytest.mark.django_db
def test_all_shopping_lists_are_listed(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    url = reverse("all-shopping-lists")

    create_shopping_list(name="Groceries", user=user)
    create_shopping_list(name="Books", user=user)

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Groceries"
    assert response.data[1]["name"] == "Books"


@pytest.mark.django_db
def test_shopping_item_is_retrieved_by_id(create_shopping_item, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)
    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Eggs"


@pytest.mark.django_db
def test_shopping_list_includes_only_corresponding_items(create_shopping_item, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)
    another_shopping_item = create_shopping_item(list_name="Books", item_name="The seven sisters", user=user)
    url = reverse("shopping-list-detail", args=[shopping_item.shopping_list.id])

    response = client.get(url)

    assert len(response.data["shopping_items"]) == 1
    assert response.data["shopping_items"][0]["name"] == "Eggs"


@pytest.mark.django_db
def test_shopping_list_name_is_changed(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)
    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}

    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_shopping_list_not_changed_because_name_missing(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)
    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"something_else": "blahblah"}

    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_shopping_list_name_is_changed_with_partial_update(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)
    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_partial_update_with_missing_name_has_no_impact(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)
    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"something_else": "blahblah"}

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_shopping_list_is_deleted(create_shopping_list, create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)
    url = reverse("shopping-list-detail", args=[shopping_list.id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(ShoppingList.objects.all()) == 0
