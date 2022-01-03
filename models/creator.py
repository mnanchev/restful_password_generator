from db import db
from models.enums import RoleType


class CreatorModel(db.Model):
    """Creator Model"""

    __tablename__ = "creators"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleType), default=RoleType.SIGNED_CREATOR, nullable=False)
    secrets = db.relationship("SecretModel", back_populates="creator")
