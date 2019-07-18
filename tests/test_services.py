from urllib.parse import urljoin

import pytest
import requests

from tickets.services import (get_cinema_world_movies,
                              get_cinema_world_movies_details,
                              get_cinema_world_movies_details_endpoint,
                              get_cinema_world_movies_endpoint,
                              get_film_world_movies,
                              get_film_world_movies_details,
                              get_film_world_movies_details_endpoint,
                              get_film_world_movies_endpoint,
                              get_service_base_url, merge_movies_data,
                              requests_with_retry)


def test_requests_for_successful_response_from_external_api(requests_mock):
    expected_response_data = {
        "Movies": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "ID": "cw0076759"
            },
            {
                "Title": "Star Wars: Episode V - The Empire Strikes Back",
                "ID": "cw0080684",
            }
        ]
    }
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    requests_mock.get(url=url, status_code=200, json=expected_response_data)
    response_data = requests_with_retry(url=url, headers={})
    assert response_data == expected_response_data


@pytest.mark.parametrize(
    'unsuccessful_status_code', [401, 403, 404, 405, 500]
)
def test_requests_for_unsuccessful_response_from_external_api(requests_mock, unsuccessful_status_code):
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    requests_mock.get(url=url, status_code=unsuccessful_status_code)
    response_data = requests_with_retry(url=url, headers={})
    assert response_data is None


def test_requests_for_invalid_json_response_from_external_api(requests_mock):
    expected_response_data = None
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    requests_mock.get(url=url, status_code=200, json=expected_response_data)
    response_data = requests_with_retry(url=url, headers={})
    assert response_data == expected_response_data


def test_requests_for_request_exception_from_external_api(requests_mock):
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    requests_mock.get(url=url, exc=requests.exceptions.RequestException)
    response_data = requests_with_retry(url=url, headers={})
    assert response_data is None


def test_get_from_cinema_world_movies_api(requests_mock):
    response_data = {
        "Movies": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "ID": "cw0076759"
            },
            {
                "Title": "Star Wars: Episode V - The Empire Strikes Back",
                "ID": "cw0080684",
            }
        ]
    }
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    requests_mock.get(url, status_code=200, json=response_data)
    cinema_world_movies = get_cinema_world_movies()
    assert cinema_world_movies == response_data


def test_get_from_cinema_world_movies_details_api(requests_mock):
    cinema_world_movies_data = {
        "Movies": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "ID": "cw0076759"
            }
        ]
    }
    service_response_data = {
        "Title": "Star Wars: Episode IV - A New Hope",
        "Price": "123.5"
    }
    expected_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5"
        }
    ]

    url = urljoin(get_service_base_url(), get_cinema_world_movies_details_endpoint())
    requests_mock.get(url.format(movie_id='cw0076759'), status_code=200, json=service_response_data)
    cinema_world_movies_details = get_cinema_world_movies_details(cinema_world_movies_data)
    assert cinema_world_movies_details == expected_data


def test_get_from_film_world_movies_api(requests_mock):
    response_data = {
        "Movies": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "ID": "fw0076759"
            },
            {
                "Title": "Star Wars: Episode V - The Empire Strikes Back",
                "ID": "fw0080684",
            }
        ]
    }
    url = urljoin(get_service_base_url(), get_film_world_movies_endpoint())
    requests_mock.get(url, status_code=200, json=response_data)
    film_world_movies = get_film_world_movies()
    assert film_world_movies == response_data


def test_get_from_film_world_movies_details_api(requests_mock):
    film_world_movies_data = {
        "Movies": [
            {
                "Title": "Star Wars: Episode IV - A New Hope",
                "ID": "fw0076759"
            }
        ]
    }
    service_response_data = {
        "Title": "Star Wars: Episode IV - A New Hope",
        "Price": "12.5"
    }
    expected_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "filmWorldPrice": "12.5"
        }
    ]

    url = urljoin(get_service_base_url(), get_film_world_movies_details_endpoint())
    requests_mock.get(url.format(movie_id='fw0076759'), status_code=200, json=service_response_data)
    film_world_movies_details = get_film_world_movies_details(film_world_movies_data)
    assert film_world_movies_details == expected_data


def test_movies_data_is_merged_and_returned_to_client():
    cinema_world_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
        }
    ]
    film_world_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "filmWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "filmWorldPrice": "22.9"
        }
    ]
    data_expected_by_client = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5",
            "filmWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "cinemaWorldPrice": "Not Available",
            "filmWorldPrice": "22.9"
        }
    ]

    merged_movies_data = merge_movies_data(cinema_world_data, film_world_data)
    assert merged_movies_data == data_expected_by_client


def test_movies_data_returned_to_client_when_the_cinema_world_data_is_empty():
    cinema_world_data = []
    film_world_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "filmWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "filmWorldPrice": "22.9"
        }
    ]
    data_expected_by_client = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "Not Available",
            "filmWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "cinemaWorldPrice": "Not Available",
            "filmWorldPrice": "22.9"
        }
    ]

    merged_movies_data = merge_movies_data(cinema_world_data, film_world_data)
    assert merged_movies_data == data_expected_by_client


def test_movies_data_returned_to_client_when_the_film_world_data_is_empty():
    cinema_world_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "cinemaWorldPrice": "22.9"
        }
    ]
    film_world_data = []
    data_expected_by_client = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "12.5",
            "filmWorldPrice": "Not Available"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "cinemaWorldPrice": "22.9",
            "filmWorldPrice": "Not Available"
        }
    ]

    merged_movies_data = merge_movies_data(cinema_world_data, film_world_data)
    assert merged_movies_data == data_expected_by_client


def test_movies_data_returned_to_client_when_there_is_no_movies_data():
    cinema_world_data = []
    film_world_data = []
    data_expected_by_client = []

    merged_movies_data = merge_movies_data(cinema_world_data, film_world_data)
    assert merged_movies_data == data_expected_by_client


def test_movies_data_returned_to_client_does_not_have_duplicates():
    cinema_world_data = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5"
        },
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5"
        }
    ]
    film_world_data = [
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "filmWorldPrice": "12.5"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "filmWorldPrice": "12.5"
        }
    ]
    data_expected_by_client = [
        {
            "title": "Star Wars: Episode IV - A New Hope",
            "cinemaWorldPrice": "123.5",
            "filmWorldPrice": "Not Available"
        },
        {
            "title": "Star Wars: Episode IV - A Renewed Hope",
            "cinemaWorldPrice": "Not Available",
            "filmWorldPrice": "12.5"
        }
    ]

    merged_movies_data = merge_movies_data(cinema_world_data, film_world_data)
    assert merged_movies_data == data_expected_by_client
