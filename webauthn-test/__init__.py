from flask import Flask, render_template

from .db import init_db

def create_app(test_config=None):

    # initialize application
    app = Flask(__name__)
    app.secret_key = 'super secret key'

    # initialize database
    init_db()

    # handle testing config, if it was passed in
    # we call this second because we want to overwite MONGO_URI
    # see: conftest.py:pytest_configure()
    if test_config:
        app.config.update(**test_config)

    # import blueprints
    from .blueprints import main, register, login
    app.register_blueprint(main)
    app.register_blueprint(register)
    app.register_blueprint(login)

    # return the app
    return app