from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(
  "sqlite:///localhost.sqlite"
)

class User(db.Model):
  uid = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String, unique=True)
  secret_number = db.Column(db.Integer)