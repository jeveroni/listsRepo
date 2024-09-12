from django.core.management.base import BaseCommand, CommandError
from altprem.scraping import mainScrape

class Command(BaseCommand):
    help = 'Scrapes sky sports for '

    def handle(self, *args, **options):
        mainScrape()