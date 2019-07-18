from django.apps import AppConfig
from django.conf import settings


class TicketsConfig(AppConfig):
    name = 'tickets'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()               # Start the scheduler to the update the requests cache periodically

        from . import services
        services.update_movies_cache()      # Update the requests cache once on app startup
