from flask_app import app

# import our controllers so the routes are recognized
from flask_app.controllers import users, recipes

if __name__=='__main__':
    app.run(debug=True)