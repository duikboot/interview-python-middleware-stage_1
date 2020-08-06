import falcon
import pytest


@pytest.mark.parametrize(
    "headers, status",
    (
        ({"Authorization": ""}, falcon.HTTP_201),
        ({"Authorization": "Apikey ILoveKittens"}, falcon.HTTP_201,),
    ),
)
def test_registration(api_client, headers, status):
    response = api_client.simulate_post(
        "/auth/register",
        json={"email": "a@example.com", "password": "example"},
        headers=headers,
    )
    assert response.status == status
