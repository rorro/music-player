from flask import Flask
from home.views import bp

def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(bp)

    return app

if __name__ == '__main__':
    app = create_app('settingslocal.py')
    app.run()
