from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from structlog import get_logger

from apps.forex.models import ForexQuote
from apps.forex.tasks import fetch_latest_forex_data
from core.utils.decorators import api_key_required
from core.utils.mixins import JSONResponseMixin


class ForexQuoteView(JSONResponseMixin, View):
    @csrf_exempt
    @method_decorator(api_key_required())
    def dispatch(self, *args, **kwargs):
        return super(ForexQuoteView, self).dispatch(*args, **kwargs)

    def get(self, request):
        logger = get_logger(__name__).bind(action='forex_data_fetch')

        try:
            latest: ForexQuote = ForexQuote.objects.latest('created_at')

            data = {
                'from': latest.currency_from,
                'to': latest.currency_to,
                'exchange_rate': str(latest.exchange_rate),
                'ask_price': str(latest.ask_price),
                'bid_price': str(latest.bid_price),
                'created': str(latest.created_at.replace(microsecond=0)),
            }
        except ForexQuote.DoesNotExist:
            data = {}

        logger.info('latest_quote', data=data)

        return self.render_to_json(context=data)

    def post(self, request, *args, **kwargs):
        logger = get_logger(__name__).bind(
            request_data=request.body.strip(), action='forex_data_refresh'
        )

        try:
            fetch_latest_forex_data()
            logger.info('succeeded')
            return self.render_to_json('Forex quotes for BTC/USD successfully updated', status=200)
        except Exception as e:
            logger.error('invalid_request', error=str(e))
            return self.render_to_json(
                status=400,
                context='Error refreshing forex data',
            )
