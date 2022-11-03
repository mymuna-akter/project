from db_connections import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    address = db.relationship("Address", backref="user", cascade="all, delete-orphan")
    child = db.relationship("Relation", backref="user", cascade="all, delete-orphan")


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zip = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    child_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
