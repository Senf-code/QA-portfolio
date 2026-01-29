import pytest
import requests


class TestAPI:

    BASE_URL = "https://jsonplaceholder.typicode.com"

    @pytest.fixture(scope="class")
    def session(self):
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json"})
        yield s
        s.close()

    def test_get_all_users_success(self, session):
        response = session.get(f"{self.BASE_URL}/users")
        assert response.status_code == 200

    def test_get_all_users_returns_valid_data(self, session):
        response = session.get(f"{self.BASE_URL}/users")
        users = response.json()

        assert isinstance(users, list)
        assert len(users) > 0

        first_user = users[0]
        assert 'id' in first_user
        assert 'name' in first_user
        assert 'email' in first_user

    def test_get_user_by_valid_id(self, session):
        user_id = 1
        response = session.get(f"{self.BASE_URL}/users/{user_id}")

        assert response.status_code == 200

        user = response.json()
        assert user['id'] == user_id
        assert user['name'] != ""
        assert user['email'] != ""

    @pytest.mark.parametrize("user_id", [1, 3, 5, 10])
    def test_get_users_with_different_valid_ids(self, session, user_id):
        response = session.get(f"{self.BASE_URL}/users/{user_id}")

        assert response.status_code == 200
        user = response.json()
        assert user['id'] == user_id

    def test_get_user_with_nonexistent_id(self, session):
        user_id = 99999
        response = session.get(f"{self.BASE_URL}/users/{user_id}")
        assert response.status_code == 404

    def test_get_user_with_invalid_id_format(self, session):
        invalid_id = "abc"
        response = session.get(f"{self.BASE_URL}/users/{invalid_id}")
        assert response.status_code in [400, 404]

    def test_get_user_with_negative_id(self, session):
        user_id = -1
        response = session.get(f"{self.BASE_URL}/users/{user_id}")
        assert response.status_code == 404

    def test_create_post_with_all_fields(self, session):
        new_post = {
            "title": "Тестовый заголовок",
            "body": "Тестовое содержимое поста",
            "userId": 1
        }

        response = session.post(f"{self.BASE_URL}/posts", json=new_post)

        assert response.status_code == 201

        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        assert 'id' in created_post

    @pytest.mark.parametrize("user_id", [1, 2, 5])
    def test_create_posts_for_different_users(self, session, user_id):
        new_post = {
            "title": f"Пост пользователя {user_id}",
            "body": "Содержимое поста",
            "userId": user_id
        }

        response = session.post(f"{self.BASE_URL}/posts", json=new_post)
        assert response.status_code == 201

        created_post = response.json()
        assert created_post['userId'] == user_id

    def test_get_all_posts(self, session):
        response = session.get(f"{self.BASE_URL}/posts")

        assert response.status_code == 200

        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_get_post_by_id(self, session):
        post_id = 1
        response = session.get(f"{self.BASE_URL}/posts/{post_id}")

        assert response.status_code == 200

        post = response.json()
        assert post['id'] == post_id

    def test_get_posts_by_user_id(self, session):
        user_id = 1
        response = session.get(f"{self.BASE_URL}/posts?userId={user_id}")

        assert response.status_code == 200

        posts = response.json()
        assert len(posts) > 0

        for post in posts:
            assert post['userId'] == user_id

    def test_full_update_post(self, session):
        post_id = 1
        updated_data = {
            "id": post_id,
            "title": "Полностью обновлённый заголовок",
            "body": "Полностью обновлённое содержимое",
            "userId": 1
        }

        response = session.put(f"{self.BASE_URL}/posts/{post_id}", json=updated_data)

        assert response.status_code == 200

        result = response.json()
        assert result['title'] == updated_data['title']
        assert result['body'] == updated_data['body']

    def test_partial_update_post(self, session):
        post_id = 1

        original_response = session.get(f"{self.BASE_URL}/posts/{post_id}")
        original_post = original_response.json()

        update_data = {"title": "Обновлён только заголовок"}

        response = session.patch(f"{self.BASE_URL}/posts/{post_id}", json=update_data)

        assert response.status_code == 200

        updated_post = response.json()
        assert updated_post['title'] == update_data['title']
        assert updated_post['body'] == original_post['body']

    def test_delete_post_success(self, session):
        post_id = 1
        response = session.delete(f"{self.BASE_URL}/posts/{post_id}")
        assert response.status_code == 200

    def test_create_post_without_title(self, session):
        incomplete_post = {
            "body": "Только содержимое без заголовка",
            "userId": 1
        }

        response = session.post(f"{self.BASE_URL}/posts", json=incomplete_post)

        assert response.status_code in [201, 400, 422]

    def test_create_post_without_user_id(self, session):
        invalid_post = {
            "title": "Заголовок",
            "body": "Содержимое"
        }

        response = session.post(f"{self.BASE_URL}/posts", json=invalid_post)
        assert response.status_code in [201, 400, 422]

    def test_create_post_with_invalid_user_id(self, session):
        invalid_post = {
            "title": "Тестовый заголовок",
            "body": "Содержимое",
            "userId": 99999
        }

        response = session.post(f"{self.BASE_URL}/posts", json=invalid_post)

        assert response.status_code in [201, 400, 404]

    def test_create_post_with_empty_body(self, session):
        post_with_empty_body = {
            "title": "Заголовок",
            "body": "",
            "userId": 1
        }

        response = session.post(f"{self.BASE_URL}/posts", json=post_with_empty_body)
        assert response.status_code in [201, 400]

    def test_get_post_with_nonexistent_id(self, session):
        post_id = 99999
        response = session.get(f"{self.BASE_URL}/posts/{post_id}")
        assert response.status_code == 404

    def test_update_nonexistent_post(self, session):
        post_id = 99999
        update_data = {
            "title": "Обновление",
            "body": "Новое содержимое"
        }

        response = session.patch(f"{self.BASE_URL}/posts/{post_id}", json=update_data)
       
        assert response.status_code in [200, 404]

    def test_delete_nonexistent_post(self, session):
        post_id = 99999
        response = session.delete(f"{self.BASE_URL}/posts/{post_id}")

        assert response.status_code in [200, 404]

    def test_update_post_with_invalid_data_type(self, session):
        post_id = 1
        invalid_data = {
            "title": 12345,  # Число вместо строки
            "userId": "invalid"  # Строка вместо числа
        }

        response = session.patch(f"{self.BASE_URL}/posts/{post_id}", json=invalid_data)

        assert response.status_code in [200, 400, 422]

    def test_get_all_comments(self, session):
        response = session.get(f"{self.BASE_URL}/comments")

        assert response.status_code == 200

        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) > 0

    def test_get_comments_for_specific_post(self, session):
        post_id = 1
        response = session.get(f"{self.BASE_URL}/posts/{post_id}/comments")

        assert response.status_code == 200

        comments = response.json()
        assert len(comments) > 0

        for comment in comments:
            assert comment['postId'] == post_id

    def test_get_comment_by_id(self, session):
        comment_id = 1
        response = session.get(f"{self.BASE_URL}/comments/{comment_id}")

        assert response.status_code == 200

        comment = response.json()
        assert comment['id'] == comment_id
        assert 'name' in comment
        assert 'email' in comment
        assert 'body' in comment

    def test_create_comment_for_post(self, session):
        new_comment = {
            "postId": 1,
            "name": "Тестовый комментарий",
            "email": "test@example.com",
            "body": "Это тестовый комментарий"
        }

        response = session.post(f"{self.BASE_URL}/comments", json=new_comment)

        assert response.status_code == 201

        created_comment = response.json()
        assert created_comment['name'] == new_comment['name']
        assert created_comment['email'] == new_comment['email']

    def test_get_comments_for_nonexistent_post(self, session):
        post_id = 99999
        response = session.get(f"{self.BASE_URL}/posts/{post_id}/comments")

        assert response.status_code in [200, 404]

        if response.status_code == 200:
            comments = response.json()
            assert len(comments) == 0

    def test_create_comment_with_invalid_email(self, session):
        invalid_comment = {
            "postId": 1,
            "name": "Комментарий",
            "email": "not-an-email",
            "body": "Содержимое"
        }

        response = session.post(f"{self.BASE_URL}/comments", json=invalid_comment)
        assert response.status_code in [201, 400, 422]

    def test_create_comment_without_email(self, session):
        incomplete_comment = {
            "postId": 1,
            "name": "Комментарий",
            "body": "Содержимое"
        }

        response = session.post(f"{self.BASE_URL}/comments", json=incomplete_comment)
        assert response.status_code in [201, 400, 422]

    def test_api_returns_json_content_type(self, session):
        response = session.get(f"{self.BASE_URL}/users")

        content_type = response.headers.get('Content-Type')
        assert 'application/json' in content_type

    def test_api_response_is_valid_json(self, session):
        response = session.get(f"{self.BASE_URL}/posts")

        try:
            data = response.json()
            assert data is not None
        except ValueError:
            pytest.fail("Ответ не является JSON")

    @pytest.mark.parametrize("endpoint", [
        "/users",
        "/posts",
        "/comments",
        "/albums",
        "/todos"
    ])
    def test_all_main_endpoints_accessible(self, session, endpoint):
        response = session.get(f"{self.BASE_URL}{endpoint}")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])