from flask import Flask, request
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging with file output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('client_access.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def log_client_info(route_name):
    """Function to log comprehensive client information"""
    client_info = {
        'timestamp': datetime.now().isoformat(),
        'route': route_name,
        'ip': request.remote_addr,
        'method': request.method,
        'url': request.url,
        'user_agent': str(request.user_agent),
        'browser': request.user_agent.browser,
        'version': request.user_agent.version,
        'platform': request.user_agent.platform,
        'referrer': request.referrer,
        'host': request.host,
        'headers': dict(request.headers)
    }

    logger.info(f"Client Access: {client_info}")


@app.route('/')
def hello():
    log_client_info('home')
    return "HELLO WORLD!"


@app.route('/hello/<name>')
def hello_name(name):
    log_client_info(f'hello/{name}')
    return f'Hello {name}!'


if __name__ == '__main__':
    app.run(debug=True)