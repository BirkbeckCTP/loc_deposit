import os

from janeway_ftp import ftp

from utils.deposit import helpers as deposit_helpers
from core import files


def add_article_to_package(request, article, temp_folder):
    article_folder = os.path.join(temp_folder, str(article.pk))
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
            request,
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


def package_issues_for_deposit(issues, initial=False, serve=False):
    # TODO: replace with actual code
    loc_code = '1-950967504_{}'.format(
        'initial_' if initial else '',
    )
    temp_folder, folder_string = deposit_helpers.prepare_temp_folder(
        loc_code=loc_code,
    )
    for issue in issues:
        for article in issue.issue_articles:
            request = deposit_helpers.create_fake_request(issue=issue)
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
