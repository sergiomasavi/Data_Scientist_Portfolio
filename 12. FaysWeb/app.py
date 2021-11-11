import os
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Permission

# Instanciar/Crear apicación
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# Migración 1
migrate = Migrate(app, db)
# Crear o actualizar roles de usuario
Role.insert_roles()

# Migración 2 (con roles)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,
                Permission=Permission)

@app.cli.command()
def deploy():
    """ Arrancar todas las operaciones de desarrollo. """
    # Migrar la bbdd a la última versión
    upgrade()

    # Crear o actualizar roles de usuario
    Role.insert_roles()


if __name__ == '__main__':
    app.run(debug=True, port=5500)