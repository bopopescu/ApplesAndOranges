# generate PDF
import io
import pdfkit
from django.conf import settings
from django.template.loader import render_to_string

default_options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}


def template2pdf(template=None, **kwargs):
    """
    Convert string to pdf field
    :param template:
        django template path
    :param kwargs:
        pass here parameters that will be submitted inside HTML template as is
    :param output:
        if False function would return in-memory file, otherwise it will be stored on disk
        (this will be part of KWARGS)
    :return:
        file if kwargs.output is not set or is false
    """
    str = render_to_string(template, kwargs)
    output = kwargs.get('output', False)
    ret = pdfkit.from_string(str, output, settings.WKHTMLTOPDF_OPTIONS or default_options)
    return (ret, str)
