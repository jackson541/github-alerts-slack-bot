import os
from flask import Flask
from . import main

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print('tessssssteeeeeee')

    app.register_blueprint(main.bp)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

if __name__ == 'main':
    create_app()
