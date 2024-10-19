import pytest

from django.urls import reverse
from rest_framework import status

from app.models import ShoppingList


@pytest.mark.django_db
def test_valid_shopping_list_is_created(create_user, create_authenticated_client):
    user = create_user()
    client = create_authenticated_client(user=user)

    url = reverse("all-shopping-lists")
    data = {"name": "Groceries"}
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.get().name == "Groceries"


@pytest.mark.django_db
def test_client_retrieves_only_shopping_lists_they_are_member_of(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    create_shopping_list(name="Groceries", user=user)

    another_user = create_user(username="another_user")
    create_shopping_list(name="Books", user=another_user)

    url = reverse("all-shopping-lists")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Groceries"


@pytest.mark.django_db
def test_shopping_item_is_retrieved_by_id(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Eggs"


@pytest.mark.django_db
def test_shopping_list_includes_only_corresponding_items(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)
    another_shopping_item = create_shopping_item(list_name="Books", item_name="The seven sisters", user=user)

    url = reverse("shopping-list-detail", args=[shopping_item.shopping_list.id])
    response = client.get(url)

    assert len(response.data["unpurchased_items"]) == 1
    assert response.data["unpurchased_items"][0]["name"] == "Eggs"


@pytest.mark.django_db
def test_shopping_list_name_is_changed(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}
    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_shopping_list_not_changed_because_name_missing(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"something_else": "blahblah"}
    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_shopping_list_name_is_changed_with_partial_update(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}
    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_partial_update_with_missing_name_has_no_impact(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"something_else": "blahblah"}
    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_shopping_list_is_deleted(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(ShoppingList.objects.all()) == 0


@pytest.mark.django_db
def test_update_shopping_list_restricted_if_not_member(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_list = create_shopping_list(name="Groceries", user=another_user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}
    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_partial_update_shopping_list_restricted_if_not_member(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_list = create_shopping_list(name="Groceries", user=another_user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    data = {"name": "Food"}
    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_shopping_list_restricted_if_not_member(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_list = create_shopping_list(name="Groceries", user=another_user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_retrieve_shopping_list(admin_client, create_user, create_shopping_list):
    user = create_user()
    shopping_list = create_shopping_list(name="Groceies", user=user)

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_not_member_of_list_can_not_add_shopping_item(create_user, create_authenticated_client, create_shopping_list):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_list = create_shopping_list(name="Groceries", user=another_user)

    url = reverse("list-add-shopping-item", args=[shopping_list.id])
    data = {"name": "Eggs", "purchased": False}

    response = client.post(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_add_shopping_items(admin_client, create_user, create_shopping_list):
    user = create_user()
    shopping_list = create_shopping_list(name="Groceries", user=user)

    url = reverse("list-add-shopping-item",  kwargs={"pk": shopping_list.id})
    data = {"name": "Eggs", "purchased": False}
    response = admin_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_shopping_item_detail_access_restricted_if_not_member_of_shopping_list(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=another_user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_shopping_item_update_restricted_if_not_member_of_shopping_list(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=another_user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    data = {"name": "Cake", "purchased": True}
    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_shopping_item_partial_update_restricted_if_not_member_of_shopping_list(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=another_user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    data = {"purchased": True}
    response = client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_shopping_item_delete_restricted_if_not_member_of_shopping_list(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user(username="another_user")
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=another_user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_retrieve_single_shopping_item(create_user, create_shopping_item, admin_client):
    user = create_user()
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)

    url = reverse("shopping-item-detail", kwargs={"pk": shopping_item.shopping_list.id, "item_pk": shopping_item.id})
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_shopping_items_is_retrieved_by_shopping_list_member(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)

    url = reverse("list-add-shopping-item",  kwargs={"pk": shopping_item.shopping_list.id})
    response = client.get(url)

    assert len(response.data) == 1
    assert response.data[0]["name"] == shopping_item.name


@pytest.mark.django_db
def test_not_member_can_not_retrieve_shopping_items(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)

    another_user = create_user("another_user")
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=another_user)

    url = reverse("list-add-shopping-item",  kwargs={"pk": shopping_item.shopping_list.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_list_shopping_items_only_the_ones_belonging_to_the_same_shopping_list(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user=user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)
    another_shopping_item = create_shopping_item(list_name="Books", item_name="The seven sisters", user=user)

    url = reverse("list-add-shopping-item", kwargs={"pk": shopping_item.shopping_list.id})
    response = client.get(url)

    assert len(response.data) == 1
    assert response.data[0]["name"] == shopping_item.name


@pytest.mark.django_db
def test_duplicate_item_on_list_bad_request(create_user, create_authenticated_client, create_shopping_item):
    user = create_user()
    client = create_authenticated_client(user)
    shopping_item = create_shopping_item(list_name="Groceries", item_name="Eggs", user=user)

    url = reverse("list-add-shopping-item", args=[shopping_item.shopping_list.id])
    data = {"name": "Eggs", "purchased": False}
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "There's already this item on the list"
