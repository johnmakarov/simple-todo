from tests.core.client import Client
from tests.core.configuration import Configuration
from clients.http.todo import AuthApi, UsersApi
from clients.http.todo.models.api_models import (
    UserCreate,
    BodyAuthJwtLoginApiAuthJwtLoginPost,
)
import pytest
import httpx
from faker import Faker

fake = Faker()


base_url = "http://127.0.0.1:8000"


@pytest.fixture
def anon_api_client():
    return Client(configuration=Configuration(base_url=base_url))


@pytest.fixture
def authenticated_api_client(auth_headers):
    return Client(configuration=Configuration(base_url=base_url, headers=auth_headers))


@pytest.fixture
def auth_service(anon_api_client) -> AuthApi:
    return AuthApi(api_client=anon_api_client)


@pytest.fixture
def authenticated_users_service(authenticated_api_client) -> UsersApi:
    return UsersApi(authenticated_api_client)


@pytest.fixture
def anon_users_service(anon_api_client) -> UsersApi:
    return UsersApi(anon_api_client)


@pytest.fixture
def user():
    return UserCreate(
        email=fake.email(),
        password="1234",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )


@pytest.fixture
def auth_headers(auth_service, user):
    auth_service.post_api_auth_register(user)
    token = httpx.post(
        url=base_url + "/api/auth/jwt/login",
        data={
            "username": user.email,
            "password": user.password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()
    return {"authorization": f"Bearer {token['access_token']}"}
