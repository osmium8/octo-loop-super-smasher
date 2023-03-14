from flask import Flask
from . import extensions
from .resources.report import report
from .resources.poll import poll
from .tasks import generate_report

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<user>:<password>@localhost:5432/<database_name>'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    extensions.db.init_app(app)
    with app.app_context():
        extensions.db.create_all()

    app.register_blueprint(report)
    app.register_blueprint(poll)

    return app

app = create_app()  
app.app_context().push()

if __name__ == '__name__':
    app.run()
