import falcon
import pytest


@pytest.mark.parametrize(
    "headers, status",
    (
        ({"Authorization": ""}, falcon.HTTP_401),
        ({"Authorization": "Bearer user-session"}, falcon.HTTP_200),
        ({"Authorization": "Bearer user-session,"}, falcon.HTTP_200),
        ({"Authorization": " Bearer user-session"}, falcon.HTTP_200),
        ({"Authorization": "Bearer user-session,Apikey ILoveKittens"}, falcon.HTTP_200,),
        (
            {"Authorization": "Bearer user-session, Apikey ILoveKittens "},
            falcon.HTTP_200,
        ),
        (
            {"Authorization": "Bearer user-session, Apikey ILoveKittens,"},
            falcon.HTTP_200,
        ),
        ({"Authorization": "Bearer user-session, Apikey ILoveKittens"}, falcon.HTTP_200,),
    ),
)
def test_whoami(api_client, headers, status):
    response = api_client.simulate_get("/users/whoami", headers=headers)
    assert response.status == status
