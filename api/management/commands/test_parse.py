import logging
import os

from django.core.management import BaseCommand

from api.helpers.parser import MtgaLogParser


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('--dry-run', action='store_true', help='List the requests, do not perform the update.')

    def handle(self, *args, **options):

        for path, dirs, files in os.walk("H:\Magic The Gathering Arena\MTGA\MTGA_Data\Logs\Logs"):
            for file in files:
                full_path = os.path.join(path, file)
                logger.info(file)
                parser = MtgaLogParser(full_path)
                parser.fetch_infos()
                logger.info(parser.games)
                logger.info(len(parser.games))
