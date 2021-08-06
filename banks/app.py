from banks.views import redisviews
from flask import Flask


from .views import mongoviews, redisviews, errorsviews

def create_app():
    app = Flask(__name__)

    errorsviews.init_app(app)
    mongoviews.init_app(app)
    redisviews.init_app(app)
    return app