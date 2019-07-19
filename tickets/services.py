import itertools as it
import os
from urllib.parse import urljoin

import requests
import requests_cache
from django.conf import settings

requests_cache.install_cache(
    'movies_cache',
    backend='sqlite',
    expire_after=settings.EXPIRE_CACHE_AFTER_SECONDS
)

requests_cache.remove_expired_responses()


def get_service_base_url():
    return settings.SERVICE_BASE_URL


def get_cinema_world_movies_endpoint():
    return settings.CINEMA_WORLD_MOVIES_ENDPOINT


def get_cinema_world_movies_details_endpoint():
    return settings.CINEMA_WORLD_MOVIES_DETAILS_ENDPOINT


def get_film_world_movies_endpoint():
    return settings.FILM_WORLD_MOVIES_ENDPOINT


def get_film_world_movies_details_endpoint():
    return settings.FILM_WORLD_MOVIES_DETAILS_ENDPOINT


def get_http_headers():
    return {
        'content-type': 'application/json',
        'x-access-token': os.environ.get('MOVIES_API_ACCESS_TOKEN')
    }


def requests_with_retry(url, headers, retries=settings.NUMBER_OF_REQUEST_RETRIES):
    response_data = None
    attempt = 1
    while attempt <= retries:
        try:
            response = requests.get(
                url=url,
                headers=headers,
                timeout=(
                    settings.REQUEST_CONNECTION_TIMEOUT_SECONDS,
                    settings.REQUEST_READ_TIMEOUT_SECONDS
                )
            )
        except requests.exceptions.RequestException:
            pass
        else:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                except ValueError:
                    response_data = None
                return response_data
        attempt += 1

    return response_data


def update_movies_cache():
    get_cinema_world_movies_details(get_cinema_world_movies())
    get_film_world_movies_details(get_film_world_movies())


def get_cinema_world_movies():
    url = urljoin(get_service_base_url(), get_cinema_world_movies_endpoint())
    response_data = requests_with_retry(url=url, headers=get_http_headers())
    return response_data


def get_cinema_world_movies_details(cinema_world_movies):
    url = urljoin(get_service_base_url(), get_cinema_world_movies_details_endpoint())

    cinema_world_movies_details = []
    if cinema_world_movies:
        movies = cinema_world_movies.get('Movies')
        for movie in movies:
            response_data = requests_with_retry(
                url=url.format(movie_id=movie.get('ID')), headers=get_http_headers()
            )
            if response_data:
                cinema_world_movies_details.append(
                    {
                        'title': response_data.get('Title'), 'cinemaWorldPrice': response_data.get('Price')
                    }
                )

    return cinema_world_movies_details


def get_film_world_movies():
    url = urljoin(get_service_base_url(), get_film_world_movies_endpoint())
    response_data = requests_with_retry(url=url, headers=get_http_headers())
    return response_data


def get_film_world_movies_details(film_world_movies):
    url = urljoin(get_service_base_url(), get_film_world_movies_details_endpoint())

    film_world_movies_details = []
    if film_world_movies:
        movies = film_world_movies.get('Movies')
        for movie in movies:
            response_data = requests_with_retry(
                url=url.format(movie_id=movie.get('ID')), headers=get_http_headers()
            )
            if response_data:
                film_world_movies_details.append(
                    {
                        'title': response_data.get('Title'), 'filmWorldPrice': response_data.get('Price')
                    }
                )

    return film_world_movies_details


def merge_movies_data(cinema_world_movies_details, film_world_movies_details):
    combined_movies_data = cinema_world_movies_details + film_world_movies_details
    sorted_movies_data = sorted(combined_movies_data, key=lambda x: x['title'])

    merged_movies_data = []
    for _, v in it.groupby(sorted_movies_data, key=lambda x: x['title']):
        v = list(v)
        if len(v) > 1:
            v[0].update(v[1])
            v[0]['filmWorldPrice'] = v[0].get('filmWorldPrice', 'Not Available')
            v[0]['cinemaWorldPrice'] = v[0].get('cinemaWorldPrice', 'Not Available')
            merged_movies_data.append(v[0])
        else:
            v[0]['filmWorldPrice'] = v[0].get('filmWorldPrice', 'Not Available')
            v[0]['cinemaWorldPrice'] = v[0].get('cinemaWorldPrice', 'Not Available')
            merged_movies_data.append(v[0])

    return merged_movies_data
