from django.conf.urls import url

from apps.forex.views import ForexQuoteView

urlpatterns = [
    url('quotes$', ForexQuoteView.as_view(), name='forex-quotes'),
]
