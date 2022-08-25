from django.db import models


class JournalSRN(models.Model):
    journal = models.OneToOneField(
        'journal.Journal',
    )
    srn = models.CharField(
        max_length=12,
        help_text='Library of Congress SRN.',
        verbose_name='SRN',
    )
    journal_name_filename = models.CharField(
        max_length=255,
        help_text='Slug-field like name of the journal to be added to the '
                  'filename eg. a_demo_journal',
    )

    class Meta:
        verbose_name = 'Journal SRN'
        verbose_name_plural = 'Journal SRNs'

    def __str__(self):
        return self.srn
