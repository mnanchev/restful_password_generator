from sqlalchemy import func

from db import db


class SecretModel(db.Model):
    __tablename__ = "secrets"
    creator_id = db.Column(db.Integer, db.ForeignKey("creators.id"))
    create_on = db.Column(db.DateTime, server_default=func.now())
    id = db.Column(db.String(255), primary_key=True)
    secret = db.Column(db.String())
    is_password_protected = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255), nullable=True)
    creator = db.relationship("CreatorModel", back_populates="secrets")
