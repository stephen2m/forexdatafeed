import logging
import os
from time import sleep, time

import psycopg2

check_timeout = os.getenv('POSTGRES_CHECK_TIMEOUT', 60)
check_interval = os.getenv('POSTGRES_CHECK_INTERVAL', 10)
interval_unit = 'second' if check_interval == 1 else 'seconds'
config = {
    'dsn': os.getenv('DATABASE_URL'),
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def pg_ready(dsn):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info('Postgres is ready! ✨ 💅')
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            logger.info(
                "Postgres isn't ready: {}\nWaiting for {} {}...".format(
                    str(e), check_interval, interval_unit
                )
            )
            sleep(check_interval)

    logger.error('Could not connect to postgres within {} seconds.'.format(check_timeout))
    return False


pg_ready(**config)
