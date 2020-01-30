from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^csv_test/', views.test_view_csv),
    url(r'^csv_test_2/', views.test_view_csv_2),
    url(r'^csv_test_3/', views.test_streaming_csv_view),
    url(r'^pdf_test/', views.pdf_some_view),
]
