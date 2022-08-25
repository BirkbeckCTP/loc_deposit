from django import forms

from plugins.loc_deposit import models
from journal import models as jm


class SRNForm(forms.ModelForm):
    class Meta:
        model = models.JournalSRN
        fields = ('journal', 'srn', 'journal_name_filename')

    def __init__(self, *args, **kwargs):
        super(SRNForm, self).__init__(*args, **kwargs)

