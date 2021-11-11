from flask import Flask
import os
from config import config
from .extensions import moment, login_manager, mail, bootstrap
from .db import Base

def create_app(config_name):
    """
    Permite crear aplicación Flask.
    """
    # Instanciar aplicación Flask
    app = Flask(__name__, template_folder='templates')

    # Secret Key de la aplicación
    app.secret_key = os.urandom(12).hex()

    # Configuración de la aplicación Flask
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.update(config)

    # Añadir extensiones a la aplicación Flask
    moment.init_app(app=app)
    mail.init_app(app=app)
    login_manager.init_app(app=app)
    bootstrap.init_app(app=app)

    # Crear modelo de datos en la bbdd
    db.Base.metadata.create_all(db.engine)

    # Registrar planos de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Devolver app Flask a la aplicación python
    return app
