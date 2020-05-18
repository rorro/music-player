from flask import Flask
from home.views import bp

import socket

def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(bp)

    return app

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    app = create_app('settingslocal.py')
    app.run(host=get_ip(), port='5000')
