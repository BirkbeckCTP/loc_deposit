from django.core.management.base import BaseCommand
from django.conf import settings
from janeway_ftp import ftp

from plugins.loc_deposit import utils
from journal import models


class Command(BaseCommand):
    """
    Sends an issue archive to Portico
    """

    help = "Sends an issue to the Library of Congress for archiving"

    def add_arguments(self, parser):
        parser.add_argument('journal_code')
        parser.add_argument('issue_ids', nargs='*', default=None)
        parser.add_argument('--initial', action='store_true', default=False)

    def handle(self, *args, **options):
        journal_code = options.get('journal_code')
        issue_ids = options.get('issue_ids')
        initial = options.get('initial')

        try:
            journal = models.Journal.objects.get(
                code=journal_code,
            )
        except models.Journal.DoesNotExist:
            exit('No journal with code {} found.'.format(journal_code))

        if issue_ids:
            issues = models.Issue.objects.filter(
                pk__in=issue_ids,
                journal=journal,
            )
            zip_file, file_name = utils.package_issues_for_deposit(issues, initial=initial)

            ftp.send_file_via_ftp(
                ftp_server=settings.LOC_FTP_SERVER,
                ftp_username=settings.LOC_FTP_USERNAME,
                ftp_password=settings.LOC_FTP_PASSWORD,
                file_path=zip_file,
            )
