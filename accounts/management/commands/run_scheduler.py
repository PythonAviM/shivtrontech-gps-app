from django.core.management.base import BaseCommand

from apscheduler.schedulers.blocking import BlockingScheduler

from accounts.scheduler import (
    check_expiry_notifications
)


class Command(BaseCommand):

    help = "Run APScheduler"

    def handle(self, *args, **kwargs):

        scheduler = BlockingScheduler()

        scheduler.add_job(

            check_expiry_notifications,

            'interval',

            minutes=240
        )

        self.stdout.write(
            self.style.SUCCESS(
                '✅ Scheduler Started'
            )
        )

        scheduler.start()
