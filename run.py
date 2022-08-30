from flask_migrate import Migrate
from flaskblog import create_app,db


app = create_app()
migrate = Migrate(app, db)


# app.debug = True

if __name__ == '__main__':
    app.run(debug=True)