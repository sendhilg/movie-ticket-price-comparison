from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .services import (get_cinema_world_movies,
                       get_cinema_world_movies_details, get_film_world_movies,
                       get_film_world_movies_details, merge_movies_data)


class PriceComparison(TemplateView):
    def get(self, request, **kwargs):
        cinema_world_movies = get_cinema_world_movies()
        cinema_world_movies_details = get_cinema_world_movies_details(cinema_world_movies)
        film_world_movies = get_film_world_movies()
        film_world_movies_details = get_film_world_movies_details(film_world_movies)

        movies_data = merge_movies_data(cinema_world_movies_details, film_world_movies_details)

        template = loader.get_template('tickets/index.html')
        context = {
            'movies_data': movies_data,
        }

        return HttpResponse(template.render(context, request))
