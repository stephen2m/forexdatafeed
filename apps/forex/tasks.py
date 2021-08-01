import requests
from celery import shared_task
from django.conf import settings
from structlog import get_logger

from apps.forex.models import ForexQuote


@shared_task(name='apps.forex.tasks.update_forex_data', max_retries=3, acks_late=True)
def fetch_latest_forex_data():
    logger = get_logger(__name__).bind(action='forex_data_refresh_task')
    base_url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'
    url = f'{base_url}&from_currency=BTC&to_currency=USD&apikey={settings.ALPHAVANTAGE_API_KEY}'

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()['Realtime Currency Exchange Rate']
        ForexQuote.objects.create(
            currency_from='BTC',
            currency_to='USD',
            exchange_rate=data.get('5. Exchange Rate'),
            bid_price=data.get('8. Bid Price'),
            ask_price=data.get('9. Ask Price'),
        )
        logger.info('request_response', data=data)
    except Exception as e:
        logger.error('request_error', error=str(e))

        raise e
