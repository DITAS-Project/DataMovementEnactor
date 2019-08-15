import connexion
import datetime

from flask_sqlalchemy import sqlalchemy, SQLAlchemy

db_name = "iskam.db"

app = connexion.App(__name__, specification_dir='./swagger/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def _get_date():
    return datetime.datetime.now()


class MovementRoutes(db.Model):

    __tablename__ = 'movement_routes'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)
    destination = db.Column(db.String)
    batch = db.Column(db.String)
    transformation = db.Column(db.String)
    type = db.Column(db.String)
    added = db.Column(db.Date, default=_get_date)
    tables = db.Column(db.String)


def create_db():
    db.create_all()


if __name__ == '__main__':
    create_db()