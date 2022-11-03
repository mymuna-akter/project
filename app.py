from flask import Flask
from flask_restful import Api

from apispec import configure_apispec
from db_connections import configure_connections


def create_app():
    app: Flask = Flask("project")
    api = Api(app)

    configure_connections(app)
    configure_apispec(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
