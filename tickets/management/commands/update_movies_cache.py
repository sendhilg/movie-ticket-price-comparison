from django.core.management.base import BaseCommand

from tickets.services import update_movies_cache


class Command(BaseCommand):
    help = 'Updates the movies cache'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Updating cache............'))

        update_movies_cache()

        self.stdout.write(self.style.SUCCESS('Updating cache successful.'))
