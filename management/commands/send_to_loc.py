from django.core.management.base import BaseCommand
from django.conf import settings
from janeway_ftp import sftp

from plugins.loc_transporter import utils, models as loc_models
from journal import models
from core import models as core_models


class Command(BaseCommand):
    """
    Sends an issue archive to Portico
    """

    help = "Sends an issue to the Library of Congress for archiving"

    def add_arguments(self, parser):
        parser.add_argument('journal_code')
        parser.add_argument('user_id')
        parser.add_argument('--issue_ids', nargs='*', default=None)
        parser.add_argument('--initial', action='store_true', default=False)

    def handle(self, *args, **options):
        journal_code = options.get('journal_code')
        user_id = options.get('user_id')
        issue_ids = options.get('issue_ids')
        initial = options.get('initial')

        try:
            journal = models.Journal.objects.get(
                code=journal_code,
            )

            if not journal.journalsrn:
                exit('{} does not have a SRN, please add one.')

            try:
                user = core_models.Account.objects.get(pk=user_id)
            except core_models.Account.DoesNotExist:
                exit('User with supplied ID not found.')

            if issue_ids:
                issues = models.Issue.objects.filter(
                    pk__in=issue_ids,
                    journal=journal,
                )
                utils.send_issue(
                    journal,
                    issues,
                    user,
                    initial=initial,
                )
            else:
                exit('No issue codes supplied.')
        except models.Journal.DoesNotExist:
            exit('No journal with code {} found.'.format(journal_code))
