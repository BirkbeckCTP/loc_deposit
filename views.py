from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import Http404

from plugins.loc_transporter import forms, models, utils
from security.decorators import editor_user_required
from journal import models as journal_models


@editor_user_required
def manager(request):
    srns = models.JournalSRN.objects.all()

    if request.POST and 'delete' in request.POST:
        id_to_delete = request.POST.get('delete')
        object_to_delete = get_object_or_404(
            models.JournalSRN,
            pk=id_to_delete
        )
        object_to_delete.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'SRN Deleted',
        )
        return redirect(
            reverse(
                'loc_transporter_manager',
            )
        )

    template = 'loc_transporter/manager.html'
    context = {
        'srns': srns,
    }

    return render(request, template, context)


@editor_user_required
def manage_srn(request, srn_id=None):
    srn = None
    if srn_id:
        srn = get_object_or_404(
            models.JournalSRN,
            pk=srn_id,
        )

    form = forms.SRNForm(
        instance=srn,
    )

    if request.POST:
        form = forms.SRNForm(
            request.POST,
            instance=srn,
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'SRN Saved',
            )
            return redirect(
                reverse(
                    'loc_transporter_manager',
                )
            )

    template = 'loc_transporter/manage_srn.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@editor_user_required
def view_journal_issues(request, srn_id):
    srn = get_object_or_404(
        models.JournalSRN,
        srn=srn_id,
    )
    journal = srn.journal

    issues = journal_models.Issue.objects.filter(
        journal=journal,
        date__lte=timezone.now(),
    )

    if request.POST:
        try:
            if 'send-to-loc' in request.POST:
                issue_id = request.POST.get('send-to-loc')
                try:
                    issue = issues.get(pk=issue_id)
                    utils.send_issue(
                        journal,
                        [issue],
                        request.user,
                    )
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'Deposit sent to Library of Congress.',
                    )
                except journal_models.Issue.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f'No issue with ID {issue_id} found.',
                    )
            if 'export-download' in request.POST:
                issue_id = request.POST.get('export-download')
                try:
                    issue = issues.get(pk=issue_id)
                    return utils.package_issues_for_deposit(
                        journal,
                        [issue],
                        request.user,
                        serve=True,
                    )
                except journal_models.Issue.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        f'No issue with ID {issue_id} found.',
                    )
        except FileNotFoundError as e:
            messages.add_message(
                request,
                messages.ERROR,
                f'{e}. Contact support or your administrator.',
            )
        return redirect(
            reverse(
                'loc_view_journal_issues',
                kwargs={
                    'srn_id': srn.srn,
                }
            )
        )

    template = 'loc_transporter/issues.html'
    context = {
        'journal': journal,
        'issues': issues,
    }
    return render(
        request,
        template,
        context,
    )