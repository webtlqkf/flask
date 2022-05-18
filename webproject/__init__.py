from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    migrate.init_app(app,db)


    from . import models
    from .views import main_views,post_views,reply_views,auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(post_views.bp)
    app.register_blueprint(reply_views.bp)
    app.register_blueprint(auth_views.bp)
    return app