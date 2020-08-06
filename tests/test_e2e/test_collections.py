import falcon
import pytest


@pytest.mark.parametrize(
    "headers, status",
    (
        ({"Authorization": ""}, falcon.HTTP_200),
        ({"Authorization": "Bearer user-session, Apikey ILoveKittens"}, falcon.HTTP_200,),
    ),
)
def test_collections(api_client, headers, status):
    response = api_client.simulate_get("/collections", headers=headers)

    assert response.status == status
    assert response.json == {"collections": ["collection1", "collection2"]}


@pytest.mark.parametrize(
    "headers, status",
    (
        ({"Authorization": ""}, falcon.HTTP_403),
        ({"Authorization": "Bearer user-session, Apikey ILoveKittens"}, falcon.HTTP_200,),
    ),
)
def test_collections_internal(api_client, headers, status):
    response = api_client.simulate_get("/internal/collections", headers=headers)

    assert response.status == status
    if response.status == falcon.HTTP_200:
        assert response.json == {"collections": ["collection1", "collection2"]}
