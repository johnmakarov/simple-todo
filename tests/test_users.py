from clients.http.todo import UsersApi


def test_get_me(authenticated_users_service: UsersApi, user):
    got = authenticated_users_service.get_api_users_me()
    assert got.email == user.email
