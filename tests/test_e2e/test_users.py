import falcon
import pytest


@pytest.mark.parametrize(
    "headers, status",
    (
        ({"Authorization": ""}, falcon.HTTP_403),
        ({"Authorization": "Bearer user-session"}, falcon.HTTP_403),
        ({"Authorization": "Bearer user-session, Apikey ILoveKittens"}, falcon.HTTP_200,),
    ),
)
def test_users(api_client, headers, status):
    response = api_client.simulate_get("/internal/users/", headers=headers)
    assert response.status == status
