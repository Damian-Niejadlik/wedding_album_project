from weasyprint import HTML
from django.template.loader import render_to_string

def generate_html(album):
    html_string = render_to_string('album_export.html', {'album': album, 'photos': album.photos.all()})
    return html_string

def generate_pdf_from_html(html_content):
    pdf = HTML(string=html_content).write_pdf()
    return pdf
