from sqlalchemy import func

from db import db


class SharedPasswordModel(db.Model):
    creator_id = db.Column(db.Integer, db.ForeignKey("creators.id"))
    creator = db.relationship("UserModel")
    create_on = db.Column(db.DateTime, server_default=func.now())
    id = db.Column(db.Integer, primary_key=True)
    is_password_protected = db.Column(db.Boolean, nullable=True)
    password_value = db.Column(db.String(255), nullable=True)
