import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from .services import update_movies_cache


def start():
    if settings.DEBUG:
        # Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Create scheduler to run in a thread inside the application process
    scheduler = BackgroundScheduler()

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    scheduler.add_job(
        update_movies_cache, "cron", id="update_movies_cache", minute="0,15,45,59", replace_existing=True
    )

    scheduler.start()
