import fitz
from io import BytesIO
from django.template.loader import render_to_string
from django.core.files.temp import NamedTemporaryFile
from weasyprint import HTML


def setup_pdf_worker_thread():
    import django

    django.setup()


def generate_pdf_page_worker(
    key,
    template,
    context,
):
    doc = HTML(string=render_to_string(template, context)).render()
    with BytesIO() as f:
        doc.write_pdf(f)
        f.seek(0)
        return f.read()


def add_page(page_binary, doc):
    with NamedTemporaryFile(suffix=".pdf") as f:
        f.write(page_binary)
        f.seek(0)
        with fitz.open(f.name) as page:
            doc.insert_pdf(page)
    return doc
