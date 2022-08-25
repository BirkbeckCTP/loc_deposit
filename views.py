from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from plugins.loc_deposit import forms, models
from security.decorators import editor_user_required


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
                'loc_deposit_manager',
            )
        )

    template = 'loc_deposit/manager.html'
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
                    'loc_deposit_manager',
                )
            )

    template = 'loc_deposit/manage_srn.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
