from clients.users_client import UsersClient
from models.user import USER_REQUIRED_FIELDS
from utils.assertions import assert_json_keys, assert_non_empty_list, assert_status


def test_list_users_returns_non_empty_array(users_client: UsersClient) -> None:
    response = users_client.list_users()

    assert_status(response, 200)
    users = assert_non_empty_list(response.json())
    assert_json_keys(users[0], USER_REQUIRED_FIELDS)


def test_get_user_by_id_returns_expected_fields(users_client: UsersClient) -> None:
    response = users_client.get_user(1)

    assert_status(response, 200)
    user = response.json()
    assert_json_keys(user, USER_REQUIRED_FIELDS)
    assert user["id"] == 1
    assert isinstance(user["email"], str) and "@" in user["email"]


def test_get_unknown_user_returns_404(users_client: UsersClient) -> None:
    response = users_client.get_user(999_999)

    assert_status(response, 404)
