import os

from flask import Flask

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True) # Creating a flask instance which will tell Flask the name of our app and the location of the config files
    app.config.from_mapping(  # Sets a secret that keeps data safe and where to store the database file
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path) # Making the instance folder in the location flask wants it
    except OSError:
        pass # Instance already exists, so we just move on

    # Index page

    @app.route('/hello')
    def hello():
        return 'Hi Mom'
    

    # Registering database functions
    from . import db
    db.init_app(app)

    # Registering the blueprint for the auth relate views
    from . import auth
    app.register_blueprint(auth.bp)

    # Registering the blueprint for the blog related views
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app