from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app,db)
    from . import models

    from .views import main_views, age_views, area_views, gender_views, overseas_views 
    app.register_blueprint(main_views.bp)
    app.register_blueprint(age_views.bp)
    app.register_blueprint(area_views.bp)
    app.register_blueprint(gender_views.bp)
    app.register_blueprint(overseas_views.bp)

    return app