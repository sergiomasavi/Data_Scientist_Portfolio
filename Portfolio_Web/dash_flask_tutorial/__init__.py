# Librerías
from flask import Flask
from dash import Dash
from dash import html
from dash import dcc
import os

# Paquetes
from . import routes

"""Initialize Flask app."""
from flask import Flask


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        return app

# Funciones
def init_app():
    """
    Función que inicializa y crea una aplicación dash con servidor en Flask.
    """
    # Inicializar aplicación
    app = Flask(__name__, template_folder='templates', instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from dashboard import create_dashboard
        app = create_dashboard(app)

        return app

    app = Dash(__name__, server=server, url_base_pathname='/dash/')

    # Secret Key de la aplicación
    app.secret_key = os.urandom(12).hex()

    # Create layout
    app.layout = html.Div(id='dash-container')

    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        return app

    return server, app