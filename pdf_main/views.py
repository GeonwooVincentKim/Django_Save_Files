import csv

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import loader, Context
from reportlab.pdfgen import canvas

# Create your views here.


def test_view_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment;' \
        'filename="csv_test_1.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"'])
    return response


def test_view_csv_2(request):
    response = HttpResponse(context_type='text/csv')
    response['Content-Disposition'] = \
        'attachment;'\
        'filename="csv_test_2.csv"'

    csv_data = (
        ('Name', 'Ralph', 'Johnson', 'Chuck'),
        ('Age', '18', '17', '19', )
    )

    t = loader.get_template('my_template_name.txt')
    c = Context({'data': csv_data})
    response.write(t.render(c))
    return response


class Echo(object):
    """An object that implements just the write method of the
    file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing
        in a buffer."""
        return value


def test_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a series of rows.
    # The range is based on the maximum number of rows
    # that most spreadsheet applications can process
    # as a single sheet.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row)
                                      for row in rows), content_type="text/csv")
    response['Content-Disposition'] \
        = 'attachment;' \
          'filename="echo_csv.csv"'
    return response


def pdf_some_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] \
        = 'attachment;' \
          'filename="somefilename.pdf"'

    # Use the response object as "file"
    # to create the PDF object.
    p = canvas.Canvas(response)

    # Draw a picture on the PDF.
    # This is where the creation of the PDF takes place.
    # See the ReportLab documentation for the full list of features.

    # First and Second Parameter of drawString
    # is let you know where you want to save
    # through to coordinates you've already made
    p.drawString(100, 100, "Hello world.")

    # Closing the PDF object ends.
    p.showPage()
    p.save()
    return response
