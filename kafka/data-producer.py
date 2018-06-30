import argparse
import logging
import requests

# Config logger
logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)

API_BASE = 'https://api.gdax.com'


def check_symbol(symbol):
    """
    Helper method check if the symbol exists in coinbase API.
    """
    logger.debug('Checking is symbol available.')
    try:
        response = requests.get(API_BASE + '/')
        product_ids = [product['id'] for product in response.json()]

        if symbol not in product_ids:
            logger.warn("Symbol %s not available. The list of supported symbols is %s", symbol, product_ids)
            exit() 
    except Exception as e:
        logger.warn('Failed to fetch products from gdax.com')



if __name__ == '__main__':
    # Based on type of parameter to process 
    parser = argparse.ArgumentParse()
    parser.add_argument('symbol', help='The symbol data you want to pull.')
    parser.add_argument('topic_name', help='The kafka topic you want to produce to.')
    parser.add_argument('kafka_broker', help='The location of the kafka broker.')

    # Parse arguments from console
    args = parser.parse_args()
    symbol = args.symbol
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker

    # Check if the symbol is available.
    check_symbol(symbol)
    
    # Instantiate a simple Kafka producer
    
