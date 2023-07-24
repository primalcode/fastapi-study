from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.heroes import Hero
from app.services import hero_service

client = TestClient(app)


def test_get_heroes():
    with patch.object(hero_service, "get_all_hero", return_value=[Hero(id=1, name="hoge", secret_name="fuga", age=15)]):
        response = client.get("/heroes")
        assert response.status_code == 200
        assert response.json() == [{'age': 15, 'id': 1, 'name': 'hoge', 'secret_name': 'fuga'}]
