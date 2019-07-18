from django.urls import reverse


def test_price_comparison(client, monkeypatch):
    monkeypatch.setattr('tickets.services.get_cinema_world_movies', lambda: None)
    monkeypatch.setattr('tickets.services.get_cinema_world_movies_details', lambda x: [])
    monkeypatch.setattr('tickets.services.get_film_world_movies', lambda: None)
    monkeypatch.setattr('tickets.services.get_film_world_movies_details', lambda x: [])
    response = client.get(reverse('compare'))
    assert response.status_code == 200
    data = next((item for item in response.context if 'movies_data' in item.keys()), None)
    if data:
        assert data['movies_data'] == []
