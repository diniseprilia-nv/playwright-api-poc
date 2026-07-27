from clients.posts_client import PostsClient
from models.post import POST_REQUIRED_FIELDS
from utils.assertions import assert_json_keys, assert_non_empty_list, assert_status


def test_list_posts_returns_non_empty_array(posts_client: PostsClient) -> None:
    response = posts_client.list_posts()

    assert_status(response, 200)
    posts = assert_non_empty_list(response.json())
    assert_json_keys(posts[0], POST_REQUIRED_FIELDS)


def test_get_post_by_id_returns_expected_fields(posts_client: PostsClient) -> None:
    response = posts_client.get_post(1)

    assert_status(response, 200)
    post = response.json()
    assert_json_keys(post, POST_REQUIRED_FIELDS)
    assert post["id"] == 1
    assert isinstance(post["title"], str) and post["title"]


def test_create_post_echoes_payload(posts_client: PostsClient) -> None:
    payload = {
        "title": "framework smoke post",
        "body": "created by playwright api tests",
        "userId": 1,
    }

    response = posts_client.create_post(payload)

    assert_status(response, (200, 201))
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert "id" in created


def test_get_unknown_post_returns_404(posts_client: PostsClient) -> None:
    response = posts_client.get_post(999_999)

    assert_status(response, 404)
