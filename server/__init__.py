import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'\xaa\x05\xeb\x8fc\x17:\x9c+\x1091\x1cR\xba\xe7',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # setup database
    from . import db
    db.init_app(app)

    from server import recordhandler, stationhandler, settingshandler, vishandler
    app.register_blueprint(recordhandler.bp)
    app.register_blueprint(stationhandler.bp)
    app.register_blueprint(settingshandler.bp)
    app.register_blueprint(vishandler.bp)

    @app.route('/')
    def hello():
        return render_template('base.html')

    return app
