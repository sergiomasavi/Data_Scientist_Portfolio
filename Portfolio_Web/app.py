# Librerías

# Paquetes
from dash_flask_tutorial import init_app

# Variables globales
app = init_app()

@server.route("/dash")
def my_dash_app():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run_server(debug=True, port=5500,host='localhost')
