from flask import Flask
from home.views import bp

import socket
from os import system
from pathlib import Path

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

def create_db():
    if not Path("database.db").is_file():
        system("sqlite3 database.db < schema.sql")

if __name__ == '__main__':
    create_db()
    app = create_app('settingslocal.py')
    app.run(host=get_ip(), port='5000')
