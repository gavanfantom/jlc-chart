import os

from flask import Flask, redirect, url_for

from .util import ListConverter

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'components.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.url_map.converters['list'] = ListConverter

    @app.route('/')
    def index():
        return redirect(url_for('bom.bom'))

    from . import db
    db.init_app(app)

    from . import fetcher
    fetcher.init_app(app)

    from . import components
    app.register_blueprint(components.bp)

    from . import bom
    app.register_blueprint(bom.bp)

    return app

