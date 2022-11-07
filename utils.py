import os

from janeway_ftp import ftp, helpers as deposit_helpers

from core import files


def add_article_to_package(request, article, temp_folder):
    issue_folder_name = "vol{}-issue{}".format(
        article.primary_issue.volume if article.primary_issue else article.issue.volume,
        article.primary_issue.issue if article.primary_issue else article.issue.issue
    )
    article_folder = os.path.join(temp_folder, issue_folder_name, str(article.pk))
    files.mkdirs(article_folder)
    galleys = article.galley_set.all()

    xml_galley = deposit_helpers.get_best_deposit_xml_galley(article, galleys)
    if xml_galley:
        files.copy_file_to_folder(
            xml_galley.file.self_article_path(),
            xml_galley.file.uuid_filename,
            article_folder,
        )
        for image in xml_galley.images.all():
            files.copy_file_to_folder(
                image.self_article_path(),
                image.original_filename,
                article_folder,
            )
    else:
        deposit_helpers.generate_jats_metadata(
            article,
            article_folder,
        )

    pdf_galley = deposit_helpers.get_best_deposit_pdf_galley(galleys)
    if pdf_galley:
        files.copy_file_to_folder(
            deposit_helpers.file_path(article.pk, pdf_galley.file.uuid_filename),
            pdf_galley.file.uuid_filename,
            article_folder,
        )


def package_issues_for_deposit(journal, issues, user, initial=False, serve=False):
    loc_code = '{}_{}{}'.format(
        journal.journalsrn.srn,
        'initial_' if initial else '',
        journal.journalsrn.journal_name_filename if journal.journalsrn.journal_name_filename else '',

    )
    temp_folder, folder_string = deposit_helpers.prepare_temp_folder(
        loc_code=loc_code,
    )
    for issue in issues:
        request = deposit_helpers.create_fake_request(
            journal=issue.journal,
            user=user,
        )
        for article in issue.issue_articles:
            add_article_to_package(request, article.get('article'), temp_folder)

    deposit_helpers.zip_temp_folder(temp_folder)

    if serve:
        return files.serve_temp_file(
            '{folder}.zip'.format(folder=temp_folder),
            '{filename}.zip'.format(filename=folder_string),
        )

    return [
        '{folder}.zip'.format(folder=temp_folder),
        '{filename}.zip'.format(filename=folder_string)
    ]
